# Google Maps Enrichment — Overview

Preferred script: `maintenance/enrich_with_google_maps_enhanced.py`

Enriches datasets with Google Maps place IDs, direct Maps URLs, and authoritative coordinates. Creates timestamped backups automatically.

## Setup

1. **Install dependencies:** see `scripts/README_configuration.md`

2. **Set up your Google Maps API key:**
   
   Create a `.env` file in the `scripts` directory:
   ```bash
   echo "GOOGLE_MAPS_API_KEY=your_api_key_here" > scripts/.env
   ```
   
   Or set the environment variable directly:
   ```bash
   export GOOGLE_MAPS_API_KEY=your_api_key_here
   ```

3. **Get a Google Maps API key:**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select existing one
   - Enable the "Places API" 
   - Create credentials (API key)
   - Restrict the API key to only the Places API for security

## Usage (enhanced)

```bash
cd scripts
python maintenance/enrich_with_google_maps_enhanced.py --dry-run   # safe preview
python maintenance/enrich_with_google_maps_enhanced.py             # apply changes
```

The script will:
- Process datasets (waterfalls, breweries, restaurants, PYO, POIs, cities, etc.)
- Find Google Place IDs; add `place_id` and `google_maps_url`
- Update coordinates from Google (when confident)
- Write backups to `/backups` and show progress/stats

## What it adds

Each location will get two new fields:
- `place_id`: Google Maps place ID (e.g., "ChIJ...")
- `google_maps_url`: Direct link to Google Maps (e.g., "https://www.google.com/maps/place/?q=place_id:ChIJ...")

## Features

- **Backups**: timestamped backups to `/backups`
- **Retry & error recovery**: resilient requests with limited retries
- **Skip existing**: won’t re-process already enriched items
- **Context-aware**: smarter queries (e.g., “waterfall”, “brewery”)
- **Progress & logging**: console + file logs

## After running

The map will automatically show "View on Google Maps" links in all popups when you click on markers. The links open in new tabs and take users directly to the Google Maps page for that location.

## Troubleshooting

- **"API key not set"**: Make sure your `.env` file exists and contains `GOOGLE_MAPS_API_KEY=your_key`
- **"No place found"**: Some locations might not be found in Google Maps - this is normal
- **API quota exceeded**: You may need to wait or upgrade your Google Cloud billing plan

