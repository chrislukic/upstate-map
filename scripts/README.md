Scenic NY Map — Data Maintenance Guide

Overview
This folder contains scripts to enrich, validate, and maintain the datasets used by the Scenic NY Map. This guide explains what each script does, how often to run it, and prerequisites.

Setup
- Python 3.9+
- Install dependencies:
  - Windows/macOS/Linux:
    - cd scripts
    - pip install -r requirements.txt
- API Keys:
  - Create scripts/.env with:
    - GOOGLE_MAPS_API_KEY=your_api_key_here

Key Datasets
- ../public/data/waterfalls.json
- ../public/data/breweries.json
- ../public/data/restaurants.json
- ../public/data/orchards_points.json
- ../public/data/map-data.json (cities)

Maintenance Tasks & Cadence

1) Restaurant open/closed status (operational hygiene)
- Script: check_restaurant_status.py
- What it does: Queries Google Places business_status and updates fields on restaurants:
  - business_status: OPERATIONAL | CLOSED_TEMPORARILY | CLOSED_PERMANENTLY
  - closed_flag: null | temporary | permanent
  - status_last_checked: ISO timestamp
- Map impact: Restaurants marked closed (temporary or permanent) are not rendered on the map.
- When to run:
  - Weekly is recommended (the script only re-checks entries older than 30 days by default)
  - On demand after bulk data changes: add --force to re-check all
- Commands:
  - cd scripts
  - python check_restaurant_status.py
  - python check_restaurant_status.py --force

2) Places enrichment (place_id, google_maps_url, coordinates)
- Script: enrich_with_google_maps.py (general) and enrich_new_restaurants.py (targeted)
- What it does:
  - enrich_with_google_maps.py: iterates waterfalls, breweries, restaurants, orchards_points, and cities to populate place_id and google_maps_url (and coordinates when missing)
  - enrich_new_restaurants.py: only processes restaurants with null lat/lng/place_id/google_maps_url
- When to run:
  - After adding new entries (restaurants/orchards/cities) or when you notice missing Google links
  - Monthly as a catch‑up, if desired
- Commands:
  - cd scripts
  - python enrich_new_restaurants.py
  - python enrich_with_google_maps.py

3) Coordinate verification (spot check & safe corrections)
- Scripts: verify_coordinates_google.py, apply_corrections_safe.py
- What they do:
  - verify_coordinates_google.py: compares current coordinates to Google Places locations, writes a discrepancy report
  - apply_corrections_safe.py: applies coordinate updates with distance/geographic safeguards
- When to run:
  - Quarterly, or after large data imports/edits
  - Before major releases to reduce location drift
- Commands:
  - cd scripts
  - python verify_coordinates_google.py
  - Review scripts/google_coordinate_verification_report.json
  - python apply_corrections_safe.py

4) Orchard-specific utilities (legacy)
- Scripts: geocode_orchards.py, merge_orchards.py
- Generally not needed once orchards_points.json is enriched, but kept for provenance and re-runs.

Operational Notes
- Cache busting: The frontend appends a timestamp to fetches; still hard refresh the browser (disable cache in devtools) to ensure updated JSON loads.
- Rate limits: Scripts include light pacing; for large runs, consider spacing or running off-hours.
- Encoding: All writers use UTF‑8 and ensure_ascii=False to preserve characters on Windows.
- Safety:
  - Prefer apply_corrections_safe.py over any older generated scripts if auto‑correcting coordinates.
  - Verify large diffs before committing.

Suggested Schedule (example)
- Weekly: check_restaurant_status.py
- After adding new restaurants: enrich_new_restaurants.py
- Monthly or after bulk edits: enrich_with_google_maps.py
- Quarterly or pre‑release: verify_coordinates_google.py, then apply_corrections_safe.py (if needed)

Troubleshooting
- JSON parse error on data files: Look for unescaped quotes in strings; fix and re-run.
- No Google links after enrichment: Confirm scripts/.env has a valid GOOGLE_MAPS_API_KEY and re-run enrichment; hard-refresh the site with cache disabled.
- Status script does not change items: Items checked < 30 days ago are skipped unless you pass --force.

Contributing & Extensions
- This README will evolve; new maintenance tasks can be added here.
- Future ideas: auto-backups before writes, dry‑run flags, CSV import/export.



