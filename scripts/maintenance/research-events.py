#!/usr/bin/env python3
"""
Weekly Upstate NY Events Crawler (family-forward, notable-only)

- Deep-research via OpenAI Responses API with the web search tool
- Scans each configured region for the next 3 months
- Deduplicates across runs
- Maintains an annual-recurrence index for faster future updates
- Persists a worklog to skip repeated effort
- Geocodes events to lat/lng using Google Maps Geocoding API

Run weekly via cron or GitHub Actions.
"""

import os
import sys
import json
import time
import hashlib
import datetime as dt
import random
import logging
import argparse
from pathlib import Path
from typing import List, Dict, Any, Optional

from dotenv import load_dotenv
import requests
from jsonschema import validate, ValidationError
from dateutil.relativedelta import relativedelta

# Add the scripts directory to the path so we can import from config
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Import shared configuration loader
from config.loader import load_script_config, setup_logging, validate_environment, get_api_key

# --- OpenAI Responses API (2025) ---
# Docs: platform.openai.com/docs/api-reference/responses (see citations)
from openai import OpenAI
from openai.types.responses import Response  # for typing

# ------------------------------
# Config & constants
# ------------------------------

# Load configuration using shared config system with path resolution
CONFIG = load_script_config('maintenance', __file__)

# Setup logging using centralized system
logger = setup_logging(CONFIG, Path(__file__).stem)

# Get data directory from configuration with proper path resolution
data_dir = Path(CONFIG.get("paths", {}).get("data_dir", "./data"))
data_dir.mkdir(exist_ok=True)

# File paths using resolved configuration
EVENTS_OUT = data_dir / CONFIG["research_events"]["output"]["events_file"]
ANNUALS_FILE = data_dir / CONFIG["research_events"]["output"]["annuals_file"]
WORKLOG_FILE = data_dir / CONFIG["research_events"]["output"]["worklog_file"]

# Event validation schema
EVENT_SCHEMA = {
    "type": "object",
    "required": ["name", "start_date", "end_date", "location_name", "address", 
                 "description", "short_description", "website", "family_friendly", "sources"],
    "properties": {
        "name": {"type": "string", "minLength": 1},
        "start_date": {"type": "string", "pattern": r"^\d{4}-\d{2}-\d{2}$"},
        "end_date": {"type": "string", "pattern": r"^\d{4}-\d{2}-\d{2}$"},
        "location_name": {"type": "string", "minLength": 1},
        "address": {"type": "string", "minLength": 1},
        "description": {"type": "string", "minLength": 10},
        "short_description": {"type": "string", "minLength": 5},
        "website": {"type": "string", "format": "uri"},
        "family_friendly": {"type": "boolean"},
        "sources": {
            "type": "array",
            "items": {"type": "string", "format": "uri"},
            "minItems": 1
        },
        "lat": {"type": "number", "minimum": -90, "maximum": 90},
        "lng": {"type": "number", "minimum": -180, "maximum": 180}
    },
    "additionalProperties": True
}

# Treat “upstate” pragmatically for trip planning. Tune as you like.
REGIONS = [
    {
        "region": "Catskills",
        "hints": [
            "Catskills", "Greene County NY", "Ulster County NY", "Delaware County NY",
            "Phoenicia", "Woodstock NY", "Hunter", "Tannersville", "Bethel", "Callicoon", "Delhi"
        ],
        "bias_cities": ["Kingston NY", "Woodstock NY", "Hunter NY", "Bethel NY", "Callicoon NY"],
        "drive_hours_from_nyc_max": 3.5
    },
    {
        "region": "Hudson Valley",
        "hints": ["Hudson Valley", "Dutchess County", "Columbia County", "Orange County NY", "Beacon", "Hudson NY"],
        "bias_cities": ["Beacon NY", "Hudson NY", "New Paltz NY", "Newburgh NY", "Poughkeepsie NY"],
        "drive_hours_from_nyc_max": 3.5
    },
    {
        "region": "Capital Region",
        "hints": ["Albany", "Saratoga Springs", "Troy NY", "Schenectady"],
        "bias_cities": ["Saratoga Springs NY", "Albany NY"],
        "drive_hours_from_nyc_max": 3.5
    },
    {
        "region": "Berkshires (MA side / fringe)",
        "hints": ["Berkshires", "Great Barrington", "Lenox", "Stockbridge"],
        "bias_cities": ["Great Barrington MA", "Lenox MA"],
        "drive_hours_from_nyc_max": 3.5
    }
    # Add/trim regions to taste. Finger Lakes/Adirondacks can exceed 3.5h from NYC—omit or gate them.
]

# Filter knobs from config
NOTABLE_ONLY = CONFIG["research_events"]["filters"]["notable_only"]
FAMILY_WEIGHT = CONFIG["research_events"]["filters"]["family_weight"]

# Geocoding
GEOCODE_ENDPOINT = "https://maps.googleapis.com/maps/api/geocode/json"

# Model to use (text+web). Mini is cheaper; swap to gpt-4o/gpt-5 if you want higher recall.
OPENAI_MODEL = os.environ.get("OPENAI_MODEL", CONFIG["api"]["openai"]["default_model"])

# ------------------------------
# Rate Limiting Utilities
# ------------------------------

def exponential_backoff(attempt: int, base_delay: float = 1.0, max_delay: float = 60.0) -> float:
    """Calculate exponential backoff delay with jitter"""
    delay = min(base_delay * (2 ** attempt), max_delay)
    jitter = random.uniform(0.1, 0.3) * delay
    return delay + jitter

def rate_limited_sleep(delay: float, reason: str = ""):
    """Sleep with informative message"""
    if reason:
        logger.info(f"Rate limiting: {reason} - sleeping {delay:.1f}s")
    time.sleep(delay)

def validate_event(event: Dict[str, Any]) -> bool:
    """Validate an event against the schema"""
    try:
        validate(event, EVENT_SCHEMA)
        return True
    except ValidationError as e:
        logger.warning(f"Invalid event data: {e.message}")
        logger.debug(f"Event: {event}")
        return False
    except Exception as e:
        logger.error(f"Unexpected validation error: {e}")
        return False

def validate_events(events: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Validate a list of events and return only valid ones"""
    valid_events = []
    for event in events:
        if validate_event(event):
            valid_events.append(event)
        else:
            logger.warning(f"Skipping invalid event: {event.get('name', 'Unknown')}")
    return valid_events

# ------------------------------
# Utilities
# ------------------------------

def load_json(path: Path, default):
    if path.exists():
        with path.open("r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError as e:
                logger.warning(f"Invalid JSON in {path}: {e}")
                return default
            except Exception as e:
                logger.error(f"Error reading {path}: {e}")
                return default
    return default

def save_json(path: Path, obj):
    tmp = path.with_suffix(".tmp.json")
    try:
        with tmp.open("w", encoding="utf-8") as f:
            json.dump(obj, f, ensure_ascii=False, indent=2)
        tmp.replace(path)
    except Exception as e:
        logger.error(f"Error saving {path}: {e}")
        if tmp.exists():
            tmp.unlink()  # Clean up temp file
        raise

def month_span_from_today(n_months: int = None) -> List[Dict[str, str]]:
    """Generate month spans from today using dateutil for cleaner date arithmetic"""
    if n_months is None:
        n_months = CONFIG["research_events"]["months_ahead"]
    
    today = dt.date.today()
    months = []
    
    for i in range(n_months):
        # Calculate start of month
        start = today + relativedelta(months=i)
        start = start.replace(day=1)
        
        # Calculate end of month
        end = start + relativedelta(months=1) - dt.timedelta(days=1)
        
        months.append({
            "start": start.isoformat(), 
            "end": end.isoformat()
        })
    
    return months

def stable_event_key(e: Dict[str, Any]) -> str:
    """A dedupe key—normalize name+location+approx date window."""
    base = f"{e.get('name','').strip().lower()}|{e.get('location_name','').strip().lower()}|{e.get('start_date','')}|{e.get('end_date','')}"
    return hashlib.sha1(base.encode("utf-8")).hexdigest()

def looks_annual(e: Dict[str, Any]) -> bool:
    """Heuristics the model will also reinforce: 'annual', 'festival', 'returns', recurring month, venue traditions."""
    txt = " ".join([
        e.get("name", ""), e.get("description", ""), e.get("short_description", "")
    ]).lower()
    flags = any(k in txt for k in ["annual", "anniversary", "returns", "every year", "fall festival", "oktoberfest", "harvest festival"])
    # Guardrails: multi-day + named venue + specific weekend hints
    duration = (dt.date.fromisoformat(e["end_date"]) - dt.date.fromisoformat(e["start_date"])).days if e.get("start_date") and e.get("end_date") else 0
    return flags or duration >= 1

def geocode_address(address: str, api_key: str) -> Optional[Dict[str, float]]:
    if not address:
        return None
    
    try:
        params = {"address": address, "key": api_key}
        timeout = CONFIG["api"]["google_maps"]["timeout"]
        r = requests.get(GEOCODE_ENDPOINT, params=params, timeout=timeout)
        
        if r.status_code != 200:
            logger.warning(f"Geocoding HTTP error {r.status_code} for address: {address}")
            return None
            
        data = r.json()
        
        if data.get("status") == "REQUEST_DENIED":
            logger.error(f"Geocoding denied for address: {address} - Check API key")
            return None
        elif data.get("status") == "ZERO_RESULTS":
            logger.warning(f"No results found for address: {address}")
            return None
        elif data.get("status") != "OK" or not data.get("results"):
            logger.warning(f"Geocoding failed with status '{data.get('status')}' for address: {address}")
            return None
            
        loc = data["results"][0]["geometry"]["location"]
        return {"lat": loc["lat"], "lng": loc["lng"]}
        
    except requests.exceptions.Timeout:
        logger.warning(f"Geocoding timeout for address: {address}")
        return None
    except requests.exceptions.RequestException as e:
        logger.error(f"Geocoding request error for address {address}: {e}")
        return None
    except (KeyError, IndexError) as e:
        logger.error(f"Unexpected geocoding response format for address {address}: {e}")
        return None

# ------------------------------
# OpenAI “deep research” call
# ------------------------------

def openai_client() -> OpenAI:
    """Create OpenAI client using centralized API key loading"""
    api_key = get_api_key('openai')
    if not api_key:
        raise ValueError("OpenAI API key not found")
    return OpenAI(api_key=api_key)

SEARCH_TOOL = {"type": "web_search_preview"}  # per docs; enables web search inside Responses API

def research_events_for_window(
    client: OpenAI,
    region: Dict[str, Any],
    window: Dict[str, str],
    annual_index: Dict[str, Any],
    worklog: Dict[str, Any],
    max_retries: int = None,
) -> List[Dict[str, Any]]:
    """
    Ask the model (with web search tool) to return notable, family-friendly events
    in a strict JSON schema, de-duplicated and with source URLs.
    """
    if max_retries is None:
        max_retries = CONFIG["api"]["openai"]["max_retries"]
    
    region_name = region["region"]
    start, end = window["start"], window["end"]

    # Seed with annuals known for the region & month range to encourage refresh
    annual_hints = [a for a in annual_index.get(region_name, [])]
    annual_hint_names = [a.get("name") for a in annual_hints]

    system = (
        "You are a precise research agent. Return ONLY a JSON array of events. "
        "Quality bar: notable events likely worth a 1–3.5 hour drive from NYC; "
        "family-friendly favored; avoid trivial small-store promos. "
        "No NYC events; focus upstate/Hudson Valley/Berkshires fringe. "
        "Include official links when possible."
    )

    # The schema the model must respect
    schema = {
        "type": "json_schema",
        "json_schema": {
            "name": "events_schema",
            "schema": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": ["name", "start_date", "end_date", "location_name", "address",
                                 "description", "short_description", "website", "family_friendly", "sources"],
                    "properties": {
                        "name": {"type": "string"},
                        "start_date": {"type": "string", "pattern": r"^\d{4}-\d{2}-\d{2}$"},
                        "end_date": {"type": "string", "pattern": r"^\d{4}-\d{2}-\d{2}$"},
                        "location_name": {"type": "string"},
                        "address": {"type": "string"},
                        "description": {"type": "string"},
                        "short_description": {"type": "string"},
                        "website": {"type": "string"},
                        "family_friendly": {"type": "boolean"},
                        "sources": {
                            "type": "array",
                            "items": {"type": "string"}
                        }
                    }
                }
            },
            "strict": True
        }
    }

    # Strong instruction with constraints & prior-knowledge leverage
    user_prompt = f"""
Return notable events for the '{region_name}' region between {start} and {end}.

Rules:
- Exclude New York City proper.
- Prioritize family-friendly events; include some non-kid-specific only if broadly notable.
- Prefer official websites or reputable CVB pages.
- Avoid duplicates and low-signal listings (tiny bar nights, single-store tastings).
- If an event seems annual, include "annual" clues in description.
- If any of these annuals are relevant this window, refresh them first: {annual_hint_names}.

Context hints for recall and geography:
- Region hints: {region['hints']}
- Anchor towns: {region['bias_cities']}
- Max driving time from NYC: {region['drive_hours_from_nyc_max']} hours.

Output must be ONLY valid JSON (no commentary), matching the provided schema exactly.
    """.strip()

    # Call with web search tool + structured output with retry logic
    for attempt in range(max_retries):
        try:
            resp: Response = client.responses.create(
                model=OPENAI_MODEL,
                tools=[SEARCH_TOOL],
                # "input" is supported in Responses API; we also request tool + JSON schema
                input=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": user_prompt}
                ],
                response_format=schema,
                temperature=0.2,  # keep it precise
            )
            break  # Success, exit retry loop
        except Exception as e:
            if attempt < max_retries - 1:
                delay = exponential_backoff(attempt, base_delay=2.0)
                rate_limited_sleep(delay, f"OpenAI API error (attempt {attempt + 1}/{max_retries}): {e}")
                continue
            else:
                logger.error(f"OpenAI API failed after {max_retries} attempts: {e}")
                return []

    # The SDK exposes .output_text for text; for JSON schema, use .output or .parsed
    # Newer SDKs provide .output[0].content[0]....; guard for variations:
    raw_text = getattr(resp, "output_text", None)
    if not raw_text:
        # Try to assemble from content blocks if output_text not present
        try:
            blocks = []
            for item in resp.output:
                for c in getattr(item, "content", []):
                    if c.type == "output_text":
                        blocks.append(c.text)
                    elif c.type == "json":
                        blocks.append(c.json)
            raw_text = blocks[-1] if blocks else "[]"
        except Exception:
            raw_text = "[]"

    try:
        events = json.loads(raw_text)
        # Attach a minimal source set if missing (defensive)
        for e in events:
            e.setdefault("sources", [])
        return events
    except json.JSONDecodeError as e:
        logger.error(f"JSON parse error in OpenAI response: {e}")
        logger.debug(f"Raw response: {raw_text[:200]}...")
        return []
    except Exception as e:
        logger.error(f"Unexpected error parsing OpenAI response: {e}")
        return []

# ------------------------------
# Main workflow
# ------------------------------

def merge_and_dedupe(existing: List[Dict[str, Any]], new: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    seen = {stable_event_key(e) for e in existing}
    out = list(existing)
    for e in new:
        k = stable_event_key(e)
        if k not in seen:
            out.append(e)
            seen.add(k)
    return out

def update_annuals(annuals: Dict[str, Any], region_name: str, events: List[Dict[str, Any]]) -> None:
    bucket = annuals.setdefault(region_name, [])
    # Use name+location slug for identity
    def slug(e):
        return (e["name"].strip().lower(), e.get("location_name","").strip().lower())

    existing = {slug(a): a for a in bucket}
    for e in events:
        if looks_annual(e):
            key = slug(e)
            record = existing.get(key, {
                "name": e["name"],
                "location_name": e.get("location_name", ""),
                "address": e.get("address", ""),
                "typical_months": list(set([e["start_date"][5:7], e["end_date"][5:7]])),
                "last_seen": e.get("end_date"),
                "last_sources": e.get("sources", [])[:5],
                "canonical_urls": [e.get("website")] if e.get("website") else []
            })
            # enrich/refresh
            record["last_seen"] = max(record.get("last_seen","0000-00-00"), e.get("end_date","0000-00-00"))
            record["last_sources"] = list({*(record.get("last_sources", []) or []), *(e.get("sources", []) or [])})[:8]
            if e.get("website"):
                urls = set(record.get("canonical_urls", []))
                urls.add(e["website"])
                record["canonical_urls"] = list(urls)[:5]
            existing[key] = record

    # reassign
    annuals[region_name] = sorted(existing.values(), key=lambda r: (r["name"].lower(), r["location_name"].lower()))

def record_work(worklog: Dict[str, Any], region_name: str, window: Dict[str, str], count: int):
    key = f"{region_name}:{window['start']}:{window['end']}"
    worklog.setdefault("runs", {})
    worklog["runs"][key] = {
        "region": region_name,
        "start": window["start"],
        "end": window["end"],
        "found": count,
        "ts": dt.datetime.utcnow().isoformat(timespec="seconds") + "Z"
    }

def geocode_events(events: List[Dict[str, Any]], gmaps_key: str) -> None:
    for i, e in enumerate(events):
        if "lat" in e and "lng" in e:
            continue
        addr = e.get("address") or e.get("location_name")
        coords = geocode_address(addr, gmaps_key)
        if coords:
            e["lat"] = coords["lat"]
            e["lng"] = coords["lng"]
        
        # Progressive rate limiting - longer delays as we process more
        base_delay = CONFIG["api"]["google_maps"]["rate_limit_delay"]
        if i > 10:
            base_delay = 0.5  # Fallback value
        elif i > 5:
            base_delay = 0.3  # Fallback value
        
        # Add jitter to avoid thundering herd
        jitter = random.uniform(0.8, 1.2)
        time.sleep(base_delay * jitter)

def validate_environment():
    """Validate required environment variables"""
    required_vars = {
        "OPENAI_API_KEY": "OpenAI API key for event research",
    }
    
    optional_vars = {
        "GOOGLE_MAPS_API_KEY": "Google Maps API key for geocoding",
        "OPENAI_MODEL": "OpenAI model to use (defaults to gpt-4o-mini)"
    }
    
    missing_required = []
    for var, description in required_vars.items():
        if not os.getenv(var):
            missing_required.append(f"{var} ({description})")
    
    if missing_required:
        logger.error("Missing required environment variables:")
        for var in missing_required:
            logger.error(f"  - {var}")
        logger.error("Please set these in your .env file or environment")
        return False
    
    # Check optional variables
    for var, description in optional_vars.items():
        if not os.getenv(var):
            logger.warning(f"Optional environment variable not set: {var} ({description})")
    
    # Validate API key formats (basic checks)
    openai_key = os.getenv("OPENAI_API_KEY")
    if openai_key and not openai_key.startswith("sk-"):
        logger.warning("OPENAI_API_KEY doesn't appear to be a valid OpenAI API key format")
    
    gmaps_key = os.getenv("GOOGLE_MAPS_API_KEY")
    if gmaps_key and not gmaps_key.startswith("AIza"):
        logger.warning("GOOGLE_MAPS_API_KEY doesn't appear to be a valid Google Maps API key format")
    
    logger.info("Environment validation passed")
    return True

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="Research upstate NY events using OpenAI API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python research-events.py                    # Normal run
  python research-events.py --dry-run          # Test without saving
  python research-events.py --force            # Force re-research all regions
  python research-events.py --verbose          # Enable debug logging
        """
    )
    
    parser.add_argument(
        "--dry-run", 
        action="store_true",
        help="Run without saving results (for testing)"
    )
    
    parser.add_argument(
        "--force", 
        action="store_true",
        help="Force re-research all regions (ignore worklog)"
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true", 
        help="Enable verbose/debug logging"
    )
    
    parser.add_argument(
        "--months", "-m",
        type=int,
        default=None,
        help="Number of months ahead to research (overrides config)"
    )
    
    parser.add_argument(
        "--region",
        type=str,
        choices=[r["region"] for r in REGIONS],
        help="Research only a specific region"
    )
    
    return parser.parse_args()

def main():
    args = parse_arguments()
    
    # Adjust logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.debug("Debug logging enabled")
    
    # Validate environment using centralized system
    required_env_vars = ['OPENAI_API_KEY']
    optional_env_vars = ['GOOGLE_MAPS_API_KEY', 'OPENAI_MODEL']
    
    if not validate_environment(required_env_vars, optional_env_vars):
        logger.error("Environment validation failed")
        sys.exit(1)
    
    # Override config with command line arguments
    if args.months:
        CONFIG["research_events"]["months_ahead"] = args.months
        logger.info(f"Overriding months_ahead to {args.months}")
    
    if args.dry_run:
        logger.info("DRY RUN MODE - No files will be saved")
    
    if args.force:
        logger.info("FORCE MODE - Will re-research all regions")
    
    if args.region:
        logger.info(f"Researching only region: {args.region}")
        # Filter regions
        global REGIONS
        REGIONS = [r for r in REGIONS if r["region"] == args.region]

    client = openai_client()
    annuals = load_json(ANNUALS_FILE, {})
    worklog = load_json(WORKLOG_FILE, {})
    existing_events = load_json(EVENTS_OUT, [])

    windows = month_span_from_today()
    logger.info(f"Starting research for {len(REGIONS)} regions across {len(windows)} time windows")

    all_new: List[Dict[str, Any]] = []

    for region in REGIONS:
        logger.info(f"Processing region: {region['region']}")
        for w in windows:
            # Skip if we already researched this region/window recently (unless --force)
            run_key = f"{region['region']}:{w['start']}:{w['end']}"
            if not args.force and worklog.get("runs", {}).get(run_key):
                # Already done; skip rework
                logger.debug(f"Skipping {run_key} - already processed")
                continue

            # Research
            logger.info(f"Researching {region['region']} for {w['start']} to {w['end']}")
            events = research_events_for_window(client, region, w, annuals, worklog)
            
            # Validate events
            events = validate_events(events)
            logger.info(f"After validation: {len(events)} valid events")

            # Apply a final local filter for "notable only" if desired
            filtered = []
            for e in events:
                # family-friendly flag is a boolean per schema
                if NOTABLE_ONLY:
                    # Heuristic: require a legit website and multi-sourced citations or an official CVB
                    url_ok = e.get("website", "").startswith(("http://", "https://"))
                    srcs = e.get("sources", [])
                    is_official = any(("gov" in (s or "") or "chamber" in (s or "") or "tourism" in (s or "") or "visit" in (s or "")) for s in srcs)
                    if not url_ok:
                        continue
                    if len(srcs) == 0 and not is_official:
                        continue
                # NYC guard (belt & suspenders)
                if "new york, ny" in e.get("address", "").lower():
                    continue
                filtered.append(e)

            # Update annual index
            update_annuals(annuals, region["region"], filtered)

            # Collect
            all_new.extend(filtered)
            logger.info(f"Found {len(filtered)} events for {region['region']} ({w['start']} to {w['end']})")

            # Worklog
            record_work(worklog, region["region"], w, len(filtered))

            # Polite pacing with jitter
            jitter = random.uniform(0.8, 1.5)
            sleep_delay = CONFIG["research_events"]["sleep_between_regions"] * jitter
            rate_limited_sleep(sleep_delay, f"Between regions ({region['region']})")

    # Merge + dedupe with existing
    merged = merge_and_dedupe(existing_events, all_new)

    # Geocode
    gmaps_key = get_api_key('google_maps')
    if gmaps_key:
        logger.info(f"Geocoding {len(merged)} events...")
        geocode_events(merged, gmaps_key)
        logger.info("Geocoding completed")

    # Save artifacts (unless dry run)
    if not args.dry_run:
        save_json(EVENTS_OUT, merged)
        save_json(ANNUALS_FILE, annuals)
        save_json(WORKLOG_FILE, worklog)
        logger.info(f"Wrote: {EVENTS_OUT}, {ANNUALS_FILE}, {WORKLOG_FILE}")
    else:
        logger.info("DRY RUN - Files not saved")

    logger.info(f"Added {len(all_new)} new events; total now {len(merged)}.")
    logger.info(f"Annual index regions: {', '.join(annuals.keys())}")


if __name__ == "__main__":
    main()
