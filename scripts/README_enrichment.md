# Google Maps Enrichment Script

This script enriches all datasets with Google Maps place IDs and creates direct links to Google Maps for each location.

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

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

## Usage

Run the enrichment script:
```bash
cd scripts
python enrich_with_google_maps.py
```

The script will:
- Process all datasets: waterfalls, breweries, restaurants, cities
- Find Google Maps place IDs for each location
- Add `place_id` and `google_maps_url` fields to each record
- Save the enriched data back to the original files
- Show progress and results for each dataset

## What it adds

Each location will get two new fields:
- `place_id`: Google Maps place ID (e.g., "ChIJ...")
- `google_maps_url`: Direct link to Google Maps (e.g., "https://www.google.com/maps/place/?q=place_id:ChIJ...")

## Features

- **Rate limiting**: Respects Google's API limits with 100ms delays
- **Error handling**: Continues processing even if some locations fail
- **Skip existing**: Won't re-process already enriched locations
- **Context-aware**: Uses location context (e.g., "waterfall", "brewery") for better matching
- **Progress tracking**: Shows detailed progress for each dataset

## After running

The map will automatically show "View on Google Maps" links in all popups when you click on markers. The links open in new tabs and take users directly to the Google Maps page for that location.

## Troubleshooting

- **"API key not set"**: Make sure your `.env` file exists and contains `GOOGLE_MAPS_API_KEY=your_key`
- **"No place found"**: Some locations might not be found in Google Maps - this is normal
- **API quota exceeded**: You may need to wait or upgrade your Google Cloud billing plan

