#!/usr/bin/env python3
"""
Restaurant status maintenance script

- Checks Google Places business_status for each restaurant
- Updates fields:
    - business_status: 'OPERATIONAL' | 'CLOSED_TEMPORARILY' | 'CLOSED_PERMANENTLY'
    - closed_flag: null | 'temporary' | 'permanent'
    - status_last_checked: ISO8601 timestamp of last check
- Only checks entries not checked in the last 30 days (unless --force)
- Uses place_id when available; otherwise attempts a Find Place search

Usage:
  python check_restaurant_status.py [--force]

Requires:
  - scripts/.env with GOOGLE_MAPS_API_KEY
  - requests, python-dotenv
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime, timedelta, timezone

import requests
from dotenv import load_dotenv

GOOGLE_FIND_PLACE_URL = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
GOOGLE_PLACE_DETAILS_URL = "https://maps.googleapis.com/maps/api/place/details/json"

RESTAURANTS_PATH = os.path.join(os.path.dirname(__file__), "..", "public", "data", "restaurants.json")

CHECK_INTERVAL_DAYS = 30
RATE_LIMIT_DELAY_SEC = 0.12  # gentle pacing


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check restaurant status via Google Places")
    parser.add_argument("--force", action="store_true", help="Force re-check all restaurants regardless of last check date")
    return parser.parse_args()


def load_api_key() -> str:
    load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))
    api_key = os.getenv("GOOGLE_MAPS_API_KEY")
    if not api_key:
        print("❌ Error: GOOGLE_MAPS_API_KEY not found in scripts/.env or environment", file=sys.stderr)
        sys.exit(1)
    return api_key


def read_json(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path: str, data) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def iso_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def needs_check(item: dict, force: bool) -> bool:
    if force:
        return True
    last = item.get("status_last_checked")
    if not last:
        return True
    try:
        last_dt = datetime.fromisoformat(last)
    except Exception:
        return True
    return (datetime.now(timezone.utc) - last_dt) >= timedelta(days=CHECK_INTERVAL_DAYS)


def map_business_status_to_flag(status: str):
    if status == "CLOSED_TEMPORARILY":
        return "temporary"
    if status == "CLOSED_PERMANENTLY":
        return "permanent"
    return None


def ensure_place_id(api_key: str, restaurant: dict) -> str | None:
    place_id = restaurant.get("place_id")
    if place_id:
        return place_id

    # Build input text from name + optional location
    name = restaurant.get("name", "")
    location = restaurant.get("location") or ""
    input_text = f"{name} {location}".strip()
    if not input_text:
        return None

    params = {
        "input": input_text,
        "inputtype": "textquery",
        "fields": "place_id",
        "key": api_key,
    }
    try:
        r = requests.get(GOOGLE_FIND_PLACE_URL, params=params, timeout=20)
        r.raise_for_status()
        data = r.json()
        if data.get("status") == "OK" and data.get("candidates"):
            return data["candidates"][0].get("place_id")
    except Exception:
        return None
    return None


def fetch_business_status(api_key: str, place_id: str) -> str | None:
    params = {
        "place_id": place_id,
        "fields": "business_status",
        "key": api_key,
    }
    try:
        r = requests.get(GOOGLE_PLACE_DETAILS_URL, params=params, timeout=20)
        r.raise_for_status()
        data = r.json()
        if data.get("status") == "OK":
            result = data.get("result", {})
            return result.get("business_status")
    except Exception:
        return None
    return None


def main() -> None:
    args = parse_args()
    api_key = load_api_key()

    try:
        restaurants = read_json(RESTAURANTS_PATH)
        if not isinstance(restaurants, list):
            print("❌ restaurants.json is not a list", file=sys.stderr)
            sys.exit(1)
    except Exception as e:
        print(f"❌ Failed to read restaurants.json: {e}", file=sys.stderr)
        sys.exit(1)

    to_check = [r for r in restaurants if needs_check(r, args.force)]
    print(f"🍽️  Checking {len(to_check)} of {len(restaurants)} restaurants (force={args.force})")

    checked = 0
    updated = 0

    for r in to_check:
        name = r.get("name", "<unnamed>")
        place_id = ensure_place_id(api_key, r)
        if not place_id:
            print(f"  ⚠️  Skipping (no place_id found): {name}")
            # still update last checked to avoid hammering if truly unresolvable? choose not to.
            r["status_last_checked"] = iso_now()
            checked += 1
            continue

        status = fetch_business_status(api_key, place_id)
        if status is None:
            print(f"  ⚠️  No status for: {name}")
            r["status_last_checked"] = iso_now()
            checked += 1
            time.sleep(RATE_LIMIT_DELAY_SEC)
            continue

        # Map to closed_flag
        closed_flag = map_business_status_to_flag(status)

        # Persist
        before_status = r.get("business_status")
        before_flag = r.get("closed_flag")

        r["place_id"] = place_id
        r["business_status"] = status
        r["closed_flag"] = closed_flag
        r["status_last_checked"] = iso_now()

        if status != before_status or closed_flag != before_flag:
            updated += 1

        state_msg = status if status else "UNKNOWN"
        print(f"  ✅ {name}: {state_msg}")

        checked += 1
        time.sleep(RATE_LIMIT_DELAY_SEC)

    # Save
    try:
        write_json(RESTAURANTS_PATH, restaurants)
        print("\n📄 Saved updates to:", os.path.relpath(RESTAURANTS_PATH, start=os.path.dirname(__file__)))
        print(f"📊 Checked: {checked} | Updated: {updated}")
    except Exception as e:
        print(f"❌ Failed to save restaurants.json: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

