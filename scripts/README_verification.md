# Coordinate Verification — Overview

Cross‑checks coordinates in datasets and reports discrepancies for review. Uses Google Places (when place_id exists) and/or Nominatim where applicable.

## What it does

- Loads all location data from your JSON files (waterfalls, breweries, restaurants, orchards, cities)
- For each location, queries OpenStreetMap Nominatim API to get alternative coordinates
- Calculates the distance between your current coordinates and Nominatim's coordinates
- Reports locations with significant discrepancies (>1km for most features, >5km for cities)
- Generates a detailed JSON report of all discrepancies

## Installation

- See `scripts/README_configuration.md` for environment setup
- Dependencies: `pip install -r requirements_verify.txt`

## Usage

Run from the `scripts` directory:

```bash
cd scripts
python maintenance/verify_coordinates_google.py
```

## Output

The script will:
- Print real-time verification results per dataset
- Flag items with large discrepancies (thresholds vary by feature)
- Save a detailed JSON report to `scripts/data/google_coordinate_verification_report.json`

## Example Output

```
🗺️  Scenic NY Map - Coordinate Verification
==================================================
Cross-referencing coordinates with OpenStreetMap Nominatim API
This may take several minutes due to API rate limiting...

=== Verifying Waterfalls ===
✅ Kaaterskill Falls: 45m difference (OK)
❌ Rainbow Falls: 1250m difference
✅ Taughannock Falls: 23m difference (OK)

=== Verifying Breweries ===
✅ Catskill Brewery: 12m difference (OK)
❌ Some Other Brewery: 2100m difference

📊 SUMMARY: Found 2 potential discrepancies
============================================================

WATERFALLS:
  • Rainbow Falls: 1250m difference
    Current: 44.123456, -73.654321
    Nominatim: 44.134567, -73.643210

BREWERIES:
  • Some Other Brewery: 2100m difference
    Current: 42.123456, -74.654321
    Nominatim: 42.134567, -74.643210

📄 Detailed report saved to: coordinate_verification_report.json
```

## Rate limiting

- Light pacing is applied to respect external services; total time depends on dataset size.

## Interpreting Results

- **Small discrepancies (<1km)**: Usually acceptable - different geocoding services may have slight variations
- **Large discrepancies (>1km)**: Worth investigating - may indicate incorrect coordinates
- **Unable to verify**: The location name might not be found in OpenStreetMap, or the name might be ambiguous

## Next Steps

After running the verification:
1. Review the discrepancies in the generated report
2. For locations with large discrepancies, manually verify the correct coordinates
3. Update the JSON files with corrected coordinates
4. Re-run the verification to confirm fixes

## Notes

- This script uses OpenStreetMap's Nominatim API, which is free but has usage policies
- The script is designed to be respectful with rate limiting
- Results may vary as OpenStreetMap data is community-maintained
- Always verify critical discrepancies manually before making changes

