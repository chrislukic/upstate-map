# Place ID Assignment Script

This script automatically assigns accurate Google Place IDs to JSON data files using the Google Places API.

## Features

- **Accurate Place ID Assignment**: Uses Google Places API to find the correct place ID for each location
- **Rate Limiting**: Respects API quotas with built-in delays
- **Error Handling**: Robust error handling with retries and exponential backoff
- **Detailed Logging**: Comprehensive logging of the assignment process
- **Batch Processing**: Can process all JSON files or specific files
- **Dry Run Mode**: Preview changes before applying them

## Setup

### 1. Install Dependencies

See `scripts/README_configuration.md` for environment setup, then:

```bash
pip install -r requirements_place_ids.txt
```

### 2. Get Google Places API Key

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the "Places API" and "Geocoding API"
4. Create credentials (API Key)
5. Restrict the API key to your domain/IP for security

### 3. Set Environment Variable

Preferred: create `scripts/.env` with:

```
GOOGLE_MAPS_API_KEY=your_api_key_here
```

Or export in your shell (same key name used across scripts):

```bash
export GOOGLE_MAPS_API_KEY="your_api_key_here"
```

## Usage

### Basic Usage

```bash
# Process all JSON files in public/data/
python assign_place_ids.py --api-key YOUR_API_KEY

# Process specific files
python assign_place_ids.py --api-key YOUR_API_KEY --files children.json trail-heads.json

# Dry run (preview changes without applying)
python assign_place_ids.py --api-key YOUR_API_KEY --dry-run

# Use different data directory
python assign_place_ids.py --api-key YOUR_API_KEY --data-dir /path/to/data

### Convenience wrapper

From `scripts/` you can also run:

```bash
python run_place_id_assignment.py --dry-run    # preview
python run_place_id_assignment.py              # apply
```
```

### Advanced Usage

```bash
# Process with custom rate limiting
python assign_place_ids.py --api-key YOUR_API_KEY --rate-limit 0.2

# Process only files matching pattern
python assign_place_ids.py --api-key YOUR_API_KEY --pattern "pyo_*.json"
```

## How It Works

1. **Reads JSON files** from the specified directory
2. **For each entry** without a place_id:
   - Extracts name, location, and coordinates
   - Searches Google Places API using the name and location
   - Uses coordinates as location bias for better accuracy
   - Assigns the found place_id and generates google_maps_url
3. **Updates the JSON file** with the new place_id and google_maps_url
4. **Creates backups** in `/backups` before writes
5. **Logs the process** (console + log file)

## API Quotas and Costs (indicative)

- **Free Tier**: per Google Places pricing (subject to change)
- **Rate Limiting**: Built-in ~100ms delay between requests
- **Estimated Cost**: minimal for current dataset; use `--dry-run` to scope

## File Processing Order

The script processes files in this order:
1. `children.json` - Children's activities
2. `trail-heads.json` - Hiking trailheads  
3. `our-airbnbs.json` - Airbnb listings
4. `points_of_interest.json` - Cultural attractions
5. All other JSON files

## Output

The script provides:
- **Console output**: Real-time progress and results
- **Log file**: `place_id_assignment.log` with detailed information
- **Backups**: original files saved under `/backups`
- **Updated JSON files**: With accurate place_ids and google_maps_urls

## Example Output

```
2024-01-15 10:30:15 - INFO - Processing file: public/data/children.json
2024-01-15 10:30:15 - INFO - Searching for place: Forsyth Nature Center in 125 Lucas Ave, Kingston, NY 12401
2024-01-15 10:30:16 - INFO - ✓ Updated entry 1: Forsyth Nature Center -> ChIJAYk4eQ0T2IkRL8Ea14UKjVs
2024-01-15 10:30:16 - INFO - Searching for place: The Strong National Museum of Play in 1 Manhattan Square Dr, Rochester, NY 14607
2024-01-15 10:30:17 - INFO - ✓ Updated entry 2: The Strong National Museum of Play -> ChIJ8V4sPge11okRpmQC_nR4DQo
...
2024-01-15 10:35:20 - INFO - ==================================================
2024-01-15 10:35:20 - INFO - SUMMARY
2024-01-15 10:35:20 - INFO - ==================================================
2024-01-15 10:35:20 - INFO - children.json: 25/25 successful
2024-01-15 10:35:20 - INFO - trail-heads.json: 60/60 successful
2024-01-15 10:35:20 - INFO - our-airbnbs.json: 15/15 successful
2024-01-15 10:35:20 - INFO - points_of_interest.json: 32/32 successful
2024-01-15 10:35:20 - INFO - Overall: 132/132 successful
2024-01-15 10:35:20 - INFO - Success rate: 100.0%
```

## Troubleshooting

### Common Issues

1. **API Quota Exceeded**
   - Wait 24 hours for quota reset
   - Consider upgrading to paid tier
   - Use `--dry-run` to estimate costs

2. **No Results Found**
   - Check if the place name is accurate
   - Verify the location information
   - Some places may not be in Google's database

3. **Rate Limiting**
   - Increase the `--rate-limit` parameter
   - The script has built-in delays to respect API limits

4. **Permission Errors**
   - Ensure the script has write access to the data directory
   - Check file permissions

### Debug Mode

Enable debug logging:

```python
import logging
logging.getLogger().setLevel(logging.DEBUG)
```

## Security Notes

- **Never commit API keys** to version control
- **Use environment variables** for API keys in production
- **Restrict API keys** to specific domains/IPs
- **Monitor usage** in Google Cloud Console

## Cost Estimation

For the current dataset:
- **children.json**: ~25 entries
- **trail-heads.json**: ~60 entries  
- **our-airbnbs.json**: ~15 entries
- **points_of_interest.json**: ~32 entries
- **Total**: ~132 API calls
- **Cost**: ~$0.02 (within free tier)

## Support

For issues or questions:
1. Check the log file for detailed error messages
2. Verify API key permissions and quotas
3. Test with a small subset of files first
4. Use `--dry-run` to preview changes
