Backups — Automated Snapshots

Purpose
- Central location for timestamped backups of JSON files before scripts modify them.

Format
- <original_filename>.backup_YYYYMMDD_HHMMSS

Created by
- maintenance/enrich_with_google_maps_enhanced.py
- utilities/geocode_events.py
- scripts based on templates/utility_script_template.py

Retention
- Manual cleanup policy (git tracks this directory). Consider pruning periodically or adding a retention script.
- Large backups can bloat diffs; prefer reviewing and squashing when appropriate.

