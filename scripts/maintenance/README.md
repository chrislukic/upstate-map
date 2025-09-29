Scenic NY Map — Maintenance Scripts

Purpose
- Periodic data hygiene and enrichment tasks that keep map data accurate.

How to run
1) Environment
- Python 3.9+
- cd scripts
- pip install -r requirements.txt
- Create scripts/.env with GOOGLE_MAPS_API_KEY=...

2) Common commands
- python maintenance/check_restaurant_status.py [--force]
- python maintenance/enrich_with_google_maps_enhanced.py [--dry-run] [--config maintenance/config.json]
- python maintenance/verify_coordinates_google.py

Backups
- All maintenance scripts create timestamped backups in ./backups before writing.
- Example: backups/restaurants.json.backup_YYYYMMDD_HHMMSS

Scripts index
- check_restaurant_status.py: Updates restaurant business status fields; can skip recent checks unless --force.
- enrich_with_google_maps_enhanced.py: Adds place_id, google_maps_url, and may update coordinates for datasets (breweries, restaurants, waterfalls, PYO, trail-heads, our-airbnbs, points_of_interest, cities in map-data.json).
- verify_coordinates_google.py: Compares stored coordinates to Google and writes a JSON report for manual review.
- research-events.py: Research/assist event data generation. See inline docstring/usage.

Configuration
- maintenance/config.json controls rate limits, backup_files, and other behavior.
- Shared config is under scripts/config/*.json via the centralized loader.

Conventions
- All JSON reads/writes are UTF-8 with ensure_ascii=False.
- Validate JSON after large changes; commit with clear messages.

# Maintenance Scripts

This folder contains scripts for regular maintenance tasks that should be run periodically to keep the map data accurate and up-to-date.

## Scripts

### `check_restaurant_status.py`
- **Purpose**: Check restaurant operational status (temporary/permanent closure)
- **Frequency**: Weekly
- **What it does**: Queries Google Places business_status and updates fields on restaurants
- **Usage**: `python maintenance/check_restaurant_status.py`


### `verify_coordinates_google.py`
- **Purpose**: Verify and correct GPS coordinates using Google Places API
- **Frequency**: Quarterly or before major releases
- **What it does**: Compares current coordinates to Google Places locations, writes discrepancy report
- **Usage**: `python maintenance/verify_coordinates_google.py`

## Prerequisites

- Python 3.9+
- Google Maps API key in `scripts/.env`
- Dependencies installed: `pip install -r requirements.txt`


