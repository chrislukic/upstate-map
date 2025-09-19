# Maintenance Scripts

This folder contains scripts for regular maintenance tasks that should be run periodically to keep the map data accurate and up-to-date.

## Scripts

### `check_restaurant_status.py`
- **Purpose**: Check restaurant operational status (temporary/permanent closure)
- **Frequency**: Weekly
- **What it does**: Queries Google Places business_status and updates fields on restaurants
- **Usage**: `python maintenance/check_restaurant_status.py`

### `enrich_with_google_maps_improved.py`
- **Purpose**: Main enrichment script using Google Places API
- **Frequency**: After adding new data, monthly catch-up
- **What it does**: Enriches all datasets with Google Places data, updates coordinates, prevents duplicates
- **Usage**: `python maintenance/enrich_with_google_maps_improved.py`

### `verify_coordinates_google.py`
- **Purpose**: Verify and correct GPS coordinates using Google Places API
- **Frequency**: Quarterly or before major releases
- **What it does**: Compares current coordinates to Google Places locations, writes discrepancy report
- **Usage**: `python maintenance/verify_coordinates_google.py`

## Prerequisites

- Python 3.9+
- Google Maps API key in `scripts/.env`
- Dependencies installed: `pip install -r requirements.txt`


