# Utility Scripts

This folder contains utility scripts for one-time or occasional data processing tasks.

## Scripts

### Data Processing
- `add_place_queries.py` - Add place_query fields to JSON objects
- `cleanup_place_queries.py` - Simplify existing place_query fields
- `re_enrich_with_updated_queries.py` - Re-enrich data with updated queries
- `remove_all_place_ids.py` - Remove all place IDs for fresh enrichment

### Data Enrichment
- `enrich_with_google_maps_improved.py` - Main enrichment script using Google Places API
- `enrich_brewery_place_ids.py` - Enrich brewery data with Google Places IDs
- `enrich_cherry_place_ids.py` - Enrich cherry farm data with Google Places IDs
- `enrich_peach_place_ids.py` - Enrich peach farm data with Google Places IDs
- `enrich_strawberry_place_ids.py` - Enrich strawberry farm data with Google Places IDs

### Data Quality Checks
- `check_duplicate_poi_coordinates.py` - Check for overlapping POI coordinates
- `check_population_data.py` - Verify population data accuracy

### Data Sources
- `geocode_orchards.py` - Geocode orchard locations
- `merge_orchards.py` - Merge orchard data
- `copy_and_serve.py` - Copy data and serve locally

## Usage

Most scripts can be run directly:
```bash
cd scripts
python utilities/script_name.py
```

Some scripts require environment variables (like `GOOGLE_MAPS_API_KEY`) to be set.


