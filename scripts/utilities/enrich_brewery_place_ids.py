#!/usr/bin/env python3
"""
Enrich brewery data with Google Maps Place IDs
- Only processes breweries that don't have place_id or have null place_id
- Uses brewery name and location for place queries
- Adds place_id, google_maps_url, and place_query fields
"""

import json
import os
import sys
import time
import requests
from typing import List, Dict, Any, Optional
from pathlib import Path

# Add the scripts directory to the path so we can import from config
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Import shared configuration loader
from config.loader import load_script_config, setup_logging, validate_environment, get_api_key

def load_json_file(filepath) -> List[Dict[str, Any]]:
    """Load JSON data from file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"File not found: {filepath}")
        return []
    except json.JSONDecodeError as e:
        print(f"JSON decode error in {filepath}: {e}")
        return []

def save_json_file(filepath, data: List[Dict[str, Any]]) -> None:
    """Save JSON data to file"""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def get_google_place_id(query: str, api_key: str, config: Dict) -> Optional[Dict[str, str]]:
    """Get place ID from Google Places API"""
    try:
        # Get configuration values
        place_api_config = config.get("place_api", {})
        timeout = place_api_config.get("timeout", 20)
        
        # Use Text Search API for better brewery matching
        url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
        params = {
            'query': query,
            'key': api_key,
            'type': 'establishment'
        }
        
        response = requests.get(url, params=params, timeout=timeout)
        response.raise_for_status()
        data = response.json()
        
        if data['status'] == 'OK' and data['results']:
            result = data['results'][0]  # Take first result
            place_id = result['place_id']
            
            # Build Google Maps URL
            google_maps_url = f"https://www.google.com/maps/place/?q=place_id:{place_id}"
            
            return {
                'place_id': place_id,
                'google_maps_url': google_maps_url,
                'place_query': query
            }
        else:
            print(f"[WARNING] No results for query: {query}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] API request failed for {query}: {e}")
        return None
    except Exception as e:
        print(f"[ERROR] Unexpected error for {query}: {e}")
        return None

def enrich_brewery_place_ids(breweries: List[Dict[str, Any]], api_key: str, config: Dict) -> List[Dict[str, Any]]:
    """Enrich breweries with place IDs"""
    
    enriched_count = 0
    skipped_count = 0
    error_count = 0
    
    for brewery in breweries:
        # Skip if already has place_id
        if brewery.get('place_id') and brewery['place_id'] is not None:
            skipped_count += 1
            continue
        
        # Create search query
        name = brewery.get('name', '')
        location = brewery.get('location', '')
        
        if not name:
            print(f"[SKIP] No name for brewery: {brewery}")
            error_count += 1
            continue
        
        # Build query: "Brewery Name, Location, NY"
        if location:
            query = f"{name}, {location}, NY"
        else:
            query = f"{name}, NY"
        
        print(f"[PROCESSING] {name} -> {query}")
        
        # Get place ID
        result = get_google_place_id(query, api_key, config)
        
        if result:
            brewery.update(result)
            enriched_count += 1
            print(f"[SUCCESS] {name} -> {result['place_id']}")
        else:
            error_count += 1
            print(f"[FAILED] {name}")
        
        # Rate limiting - be nice to Google's API
        time.sleep(0.1)  # 100ms delay between requests
    
    print(f"\n[ENRICHMENT SUMMARY]")
    print(f"Total breweries: {len(breweries)}")
    print(f"Already had place_id: {skipped_count}")
    print(f"Successfully enriched: {enriched_count}")
    print(f"Failed to enrich: {error_count}")
    
    return breweries

def main():
    """Main function to enrich brewery place IDs"""
    
    # Load configuration using centralized system
    config = load_script_config('utilities', __file__)
    
    # Setup logging
    logger = setup_logging(config, Path(__file__).stem)
    
    # Validate environment
    if not validate_environment(['GOOGLE_MAPS_API_KEY']):
        logger.error("Missing required environment variables")
        return 1
    
    # Get API key using centralized system
    api_key = get_api_key('google_maps')
    if not api_key:
        logger.error("Google Maps API key not found!")
        return 1
    
    logger.info(f"API key loaded: {'Yes' if api_key else 'No'}")
    
    # Get file paths from configuration
    data_dir = Path(config.get("file_paths", {}).get("data_dir", "../../public/data"))
    breweries_file = data_dir / "breweries.json"
    
    print("Starting brewery place ID enrichment...")
    
    # Load existing breweries
    breweries = load_json_file(breweries_file)
    if not breweries:
        print(f"Could not load breweries from {breweries_file}")
        return
    
    print(f"Loaded {len(breweries)} breweries")
    
    # Check how many need enrichment
    missing_place_ids = [b for b in breweries if not b.get('place_id') or b.get('place_id') is None]
    print(f"Breweries missing place IDs: {len(missing_place_ids)}")
    
    if not missing_place_ids:
        print("All breweries already have place IDs!")
        return
    
    # Enrich breweries
    enriched_breweries = enrich_brewery_place_ids(breweries, api_key, config)
    
    # Save enriched data
    save_json_file(breweries_file, enriched_breweries)
    print(f"\n[SUCCESS] Enriched brewery data saved to {breweries_file}")

if __name__ == "__main__":
    main()
