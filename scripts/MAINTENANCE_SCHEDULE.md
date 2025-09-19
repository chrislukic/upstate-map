# Scenic NY Map - Maintenance Schedule

## Regular Maintenance Tasks

### Weekly Tasks
- **Restaurant Status Check**
  ```bash
  cd scripts
  python check_restaurant_status.py
  ```
  - Checks if restaurants are still open/closed
  - Updates business status and closed flags
  - Only checks entries older than 30 days (use `--force` to check all)

### Monthly Tasks
- **Data Enrichment**
  ```bash
  cd scripts
  python enrich_with_google_maps_improved.py
  ```
  - Enriches all datasets with Google Places data
  - Updates coordinates from Google Places API
  - Prevents duplicate place IDs

### Quarterly Tasks
- **Coordinate Verification**
  ```bash
  cd scripts
  python verify_coordinates_google.py
  ```
  - Compares current coordinates to Google Places locations
  - Generates discrepancy report for manual review
  - Review `scripts/google_coordinate_verification_report.json`

## As-Needed Tasks

### After Adding New Data
- Run data enrichment script to get Google Places data for new entries

### Before Major Releases
- Run coordinate verification to ensure data accuracy
- Review and fix any coordinate discrepancies

### Troubleshooting
- If POIs have overlapping coordinates: `python check_duplicate_poi_coordinates.py`
- If population data seems wrong: `python check_population_data.py`
- If place queries need updating: `python add_place_queries.py`

## Script Categories

### ✅ Active Maintenance Scripts
- `check_restaurant_status.py` - Weekly restaurant status checks
- `enrich_with_google_maps_improved.py` - Monthly data enrichment
- `verify_coordinates_google.py` - Quarterly coordinate verification

### 🛠️ Utility Scripts (Use as needed)
- `check_duplicate_poi_coordinates.py` - Check for overlapping POI coordinates
- `check_population_data.py` - Verify population data accuracy
- `add_place_queries.py` - Add place_query fields for better searches
- `cleanup_place_queries.py` - Simplify existing place_query fields
- `update_place_queries_from_descriptions.py` - Update queries based on descriptions
- `re_enrich_with_updated_queries.py` - Re-enrich with updated queries
- `remove_all_place_ids.py` - Clear place IDs for re-enrichment

### 📚 Legacy Scripts (Keep for reference)
- `geocode_orchards.py` - Original orchard geocoding
- `merge_orchards.py` - Original orchard merging
- `enrich_new_restaurants.py` - Targeted restaurant enrichment

### 🗑️ Deleted Scripts (Superseded)
- `enrich_with_google_maps.py` - Replaced by improved version
- `enrich_with_google_maps_fixed.py` - Replaced by improved version
- `verify_coordinates.py` - Replaced by Google-based verification
- `apply_corrections_from_report.py` - One-time use, completed
- `apply_corrections_safe.py` - One-time use, completed

## Setup Requirements
- Python 3.9+
- Install dependencies: `pip install -r requirements.txt`
- Create `scripts/.env` with: `GOOGLE_MAPS_API_KEY=your_api_key_here`



