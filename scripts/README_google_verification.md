# Google Places Coordinate Verification Script

This script cross-checks the GPS coordinates in your scenic NY map datasets against Google Places API using your existing place IDs. This is much more accurate than name-based geocoding since it uses the exact place IDs that were already enriched in your data.

## What it does

- Loads all location data from your JSON files (waterfalls, breweries, restaurants, orchards, cities)
- For each location with a place ID, queries Google Places API to get the exact coordinates
- Calculates the distance between your current coordinates and Google's coordinates
- Reports locations with significant discrepancies (>100m for most features, >1km for cities)
- Generates an automatic correction script to fix all discrepancies

## Installation

1. Install the required Python packages:
```bash
pip install -r requirements_verify.txt
```

2. Make sure your `.env` file contains your Google Maps API key:
```
GOOGLE_MAPS_API_KEY=your_api_key_here
```

## Usage

Run the verification script from the `scripts` directory:

```bash
cd scripts
python verify_coordinates_google.py
```

## Output

The script will:
- Print real-time verification results for each location
- Show ✅ for locations with small discrepancies (<100m)
- Show ❌ for locations with large discrepancies (>100m)
- Show ❓ for locations without place IDs
- Generate a summary report at the end
- Create an automatic correction script: `apply_coordinate_corrections.py`
- Save a detailed JSON report to `google_coordinate_verification_report.json`

## Example Output

```
🗺️  Scenic NY Map - Google Places Coordinate Verification
============================================================
Cross-referencing coordinates with Google Places API using place IDs
This should be much more accurate than name-based geocoding...

=== Verifying Waterfalls ===
✅ Kaaterskill Falls: 12m difference (OK)
❌ Rainbow Falls: 250m difference
✅ Taughannock Falls: 8m difference (OK)
Verified 45/47 waterfalls

=== Verifying Breweries ===
✅ Catskill Brewery: 5m difference (OK)
❌ Some Other Brewery: 150m difference
Verified 12/12 breweries

📊 SUMMARY: Found 3 coordinate discrepancies
============================================================

WATERFALLS:
  • Rainbow Falls: 250m difference
    Current: 44.123456, -73.654321
    Google: 44.134567, -73.643210

BREWERIES:
  • Some Other Brewery: 150m difference
    Current: 42.123456, -74.654321
    Google: 42.134567, -74.643210

🔧 Generated correction script: apply_coordinate_corrections.py
   Run this script to automatically apply all coordinate corrections
📄 Detailed report saved to: google_coordinate_verification_report.json
```

## Applying Corrections

After running the verification, you can automatically apply all corrections:

```bash
python apply_coordinate_corrections.py
```

This will:
- Update all JSON files with the corrected coordinates from Google Places API
- Show you exactly what changes were made
- Preserve all other data in your files

## Advantages over Nominatim

- **More accurate**: Uses exact place IDs instead of name-based geocoding
- **Faster**: Shorter delays since place ID lookups are more reliable
- **Better coverage**: Google Places has more comprehensive business/location data
- **Consistent**: Same data source used for both enrichment and verification

## Rate Limiting

The script includes a 0.1-second delay between API requests. Since we're using place IDs (which are very reliable), this is much faster than the Nominatim version.

## Interpreting Results

- **Small discrepancies (<100m)**: Usually acceptable - different coordinate systems or slight variations
- **Large discrepancies (>100m)**: Worth correcting - may indicate incorrect coordinates
- **No place ID**: These locations weren't enriched with Google Maps data

## Next Steps

1. Run the verification script
2. Review the discrepancies in the generated report
3. Run the correction script to automatically fix all issues
4. Re-run the verification to confirm all corrections were applied

## Notes

- This script requires the same Google Maps API key used for enrichment
- The correction script is automatically generated based on the verification results
- All corrections are applied automatically - no manual editing required
- The script preserves all other data in your JSON files

