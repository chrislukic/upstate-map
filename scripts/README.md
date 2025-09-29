Scenic NY Map — Data Maintenance Guide

Overview
This folder contains organized scripts to enrich, validate, and maintain the datasets used by the Scenic NY Map. This guide explains what each script does, how often to run it, and prerequisites.

## Folder Structure

### 📁 `maintenance/` - Active Maintenance Scripts
Regular maintenance tasks that should be run periodically.

### 📁 `utilities/` - Utility Scripts  
One-time or occasional utility scripts for data processing.

### 📁 `legacy/` - Legacy Scripts
Superseded scripts kept for reference.

### 📁 `data/` - Data Files
Generated data files and reports.

Setup
- Python 3.9+
- Configuration & dependencies: see `scripts/README_configuration.md`
- API key: create `scripts/.env` with `GOOGLE_MAPS_API_KEY=your_api_key_here`

Key datasets (examples)
- ../public/data/map-data.json (scenic areas, cities, tile layer)
- ../public/data/waterfalls.json
- ../public/data/breweries.json
- ../public/data/restaurants.json
- ../public/data/points_of_interest.json
- ../public/data/children.json
- ../public/data/trail-heads.json
- ../public/data/our-airbnbs.json
- ../public/data/pyo_apples.json, pyo_strawberries.json, pyo_cherries.json, pyo_peaches.json
- ../public/data/regions.json (GeoJSON)
- ../public/data/events.json (optional)

Maintenance Tasks & Cadence

1) Restaurant open/closed status (operational hygiene)
- Script: maintenance/check_restaurant_status.py
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
  - python maintenance/check_restaurant_status.py
  - python maintenance/check_restaurant_status.py --force

2) Places enrichment (place_id, google_maps_url, coordinates)
- Preferred script: `maintenance/enrich_with_google_maps_enhanced.py`
- Legacy (still available): `utilities/enrich_with_google_maps_improved.py`
- What it does:
  - Enriches datasets (waterfalls, breweries, restaurants, PYO, cities, POIs, etc.) with Google Places data
  - Updates coordinates from Google Places (source of truth)
  - Prevents duplicates and validates matches; creates backups in `/backups`
- When to run:
  - After adding new entries or when missing Google links
  - Periodically (e.g., monthly) to catch up
- Commands:
  - cd scripts
  - python maintenance/enrich_with_google_maps_enhanced.py

3) Coordinate verification (spot check)
- Script: maintenance/verify_coordinates_google.py
- What it does:
  - Compares current coordinates to Google Places locations using existing place IDs
  - Writes a discrepancy report for manual review
  - Does NOT automatically apply corrections (manual review required)
- When to run:
  - Quarterly, or after large data imports/edits
  - Before major releases to reduce location drift
- Commands:
  - cd scripts
  - python maintenance/verify_coordinates_google.py
  - Review scripts/data/google_coordinate_verification_report.json

4) Orchard-specific utilities (legacy)
- Scripts: utilities/geocode_orchards.py, utilities/merge_orchards.py
- Generally not needed once orchards_points.json is enriched, but kept for provenance and re-runs.

Operational Notes
- Cache busting: The frontend appends a timestamp to fetches; still hard refresh the browser (disable cache in devtools) to ensure updated JSON loads.
- Rate limits: Scripts include light pacing; for large runs, consider spacing or running off-hours.
- Encoding: All writers use UTF‑8 and ensure_ascii=False to preserve characters on Windows.
- Safety:
  - Always review coordinate verification reports before making changes.
  - Verify large diffs before committing.

Suggested Schedule (example)
- Weekly: maintenance/check_restaurant_status.py
- After adding new data: maintenance/enrich_with_google_maps_improved.py
- Monthly or after bulk edits: maintenance/enrich_with_google_maps_improved.py
- Quarterly or pre‑release: maintenance/verify_coordinates_google.py (review report manually)

Troubleshooting
- JSON parse error on data files: Look for unescaped quotes in strings; fix and re-run.
- No Google links after enrichment: Confirm scripts/.env has a valid GOOGLE_MAPS_API_KEY and re-run enrichment; hard-refresh the site with cache disabled.
- Status script does not change items: Items checked < 30 days ago are skipped unless you pass --force.

Contributing & Extensions
- This README will evolve; new maintenance tasks can be added here.
- Future ideas: auto-backups before writes, dry‑run flags, CSV import/export.



