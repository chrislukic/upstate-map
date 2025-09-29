Configuration — Centralized Settings

Purpose
- Define shared settings for maintenance/utilities: data_dir, backup behavior, API endpoints, and schema validation.

Key files
- common.json: Directories (data_dir, backup_dir, log_dir), logging settings.
- utilities.json: Defaults for utility scripts (data_dir, backup_before_changes, rate limits).
- maintenance.json: Defaults for maintenance scripts (backup_before_changes, pacing).
- geocoding.json: Geocoding-specific settings (timeouts, delays).
- schemas.py: JSON schema definitions for validating config files.
- loader.py: Helper to load/merge configs, set up logging, and validate env.
- validate_config.py: Validates configs against schemas.

Usage
- Loaded automatically by scripts via config.loader.load_script_config().
- Override via per-script config files or command-line --config where supported.

Backups
- Scripts honor backup_before_changes and write to /backups.

Tips
- Keep API keys in scripts/.env; never commit them.
- Run validate_config.py if changing schema or adding new keys.
- Health check: `python scripts/config/health_check.py` for a one‑shot sanity check.

