Utilities — Script Index

Purpose
- One-off and helper scripts for data processing, geocoding, and tooling.

How to run
- cd scripts
- pip install -r requirements.txt
- Set GOOGLE_MAPS_API_KEY in scripts/.env when required

Backups
- On write, utilities back up originals to /backups with timestamped filenames.

Notable utilities
- geocode_events.py: Geocodes events in public/data/events.json using Google Maps; writes backups and updates file in place.
- add-coordinates-scenic-area.py: Adds coordinates for scenic areas (see script docstring).
- enrich_with_google_maps_improved.py (legacy name kept in utilities for convenience): Alternative enrichment helper.

Config
- Uses centralized config loader (scripts/config/*). See utilities.json for defaults like data_dir and backup behavior.

Conventions
- UTF-8 I/O, ensure_ascii=False, timestamps appended to backups.


