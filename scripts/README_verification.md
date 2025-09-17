# Coordinate Verification Script

This script cross-checks the GPS coordinates in your scenic NY map datasets against OpenStreetMap's Nominatim API to identify potential location discrepancies.

## What it does

- Loads all location data from your JSON files (waterfalls, breweries, restaurants, orchards, cities)
- For each location, queries OpenStreetMap Nominatim API to get alternative coordinates
- Calculates the distance between your current coordinates and Nominatim's coordinates
- Reports locations with significant discrepancies (>1km for most features, >5km for cities)
- Generates a detailed JSON report of all discrepancies

## Installation

1. Install the required Python package:
```bash
pip install -r requirements_verify.txt
```

## Usage

Run the verification script from the `scripts` directory:

```bash
cd scripts
python verify_coordinates.py
```

## Output

The script will:
- Print real-time verification results for each location
- Show ✅ for locations with small discrepancies (<1km)
- Show ❌ for locations with large discrepancies (>1km)
- Show ❓ for locations that couldn't be verified
- Generate a summary report at the end
- Save a detailed JSON report to `coordinate_verification_report.json`

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

## Rate Limiting

The script includes a 1-second delay between API requests to be respectful to the OpenStreetMap Nominatim service. This means the script will take several minutes to complete, but it ensures reliable results.

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

