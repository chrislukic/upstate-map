#!/usr/bin/env python3
"""
Enrich cherry farms with proper Google Place IDs using Google Maps API.
This script will update place_id, google_maps_url, and place_query fields.
"""

import json
import time
import requests
from pathlib import Path
from dotenv import load_dotenv
import os

def load_env_file():
    """Load environment variables from .env file."""
    project_root = Path(__file__).parent.parent.parent
    env_file = project_root / '.env'
    
    if env_file.exists():
        load_dotenv(env_file)
        print(f"Loaded environment from {env_file}")
    else:
        print(f"Warning: .env file not found at {env_file}")
    
    api_key = os.getenv('GOOGLE_MAPS_API_KEY')
    if not api_key:
        print("Error: GOOGLE_MAPS_API_KEY not found in environment variables")
        return None
    
    return api_key

def load_json_file(file_path):
    """Load JSON data from file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return None

def save_json_file(file_path, data):
    """Save JSON data to file."""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error saving {file_path}: {e}")
        return False

def search_place_by_name_and_location(api_key, name, address, lat, lng):
    """Search for a place using name, address, and coordinates."""
    base_url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
    
    # Create a more specific search query
    query = f"{name}, {address}"
    
    params = {
        'input': query,
        'inputtype': 'textquery',
        'fields': 'place_id,name,formatted_address,geometry,types',
        'locationbias': f'point:{lat},{lng}',
        'key': api_key
    }
    
    try:
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if data.get('status') == 'OK' and data.get('candidates'):
            candidate = data['candidates'][0]
            return {
                'place_id': candidate.get('place_id'),
                'name': candidate.get('name'),
                'formatted_address': candidate.get('formatted_address'),
                'geometry': candidate.get('geometry')
            }
        else:
            print(f"  [WARNING] No results for {name}: {data.get('status', 'Unknown error')}")
            return None
            
    except Exception as e:
        print(f"  [ERROR] API request failed for {name}: {e}")
        return None

def enrich_cherry_farms(api_key, farms_data):
    """Enrich cherry farms with proper place IDs."""
    enriched_count = 0
    skipped_count = 0
    
    print(f"Processing {len(farms_data)} cherry farms...")
    
    for i, farm in enumerate(farms_data, 1):
        name = farm.get('name', '')
        address = farm.get('address', '')
        lat = farm.get('lat')
        lng = farm.get('lng')
        
        print(f"\n[{i}/{len(farms_data)}] Processing: {name}")
        
        if not all([name, address, lat, lng]):
            print(f"  [SKIP] Missing required data (name, address, lat, lng)")
            skipped_count += 1
            continue
        
        # Search for the place
        result = search_place_by_name_and_location(api_key, name, address, lat, lng)
        
        if result:
            # Update the farm data
            farm['place_id'] = result['place_id']
            farm['google_maps_url'] = f"https://www.google.com/maps/place/?q=place_id:{result['place_id']}"
            farm['place_query'] = f"{name}, cherries, NY"
            
            print(f"  [SUCCESS] Updated place_id: {result['place_id']}")
            print(f"  [INFO] Found as: {result.get('name', 'Unknown')}")
            print(f"  [INFO] Address: {result.get('formatted_address', 'Unknown')}")
            
            enriched_count += 1
        else:
            print(f"  [FAILED] Could not find place for {name}")
            skipped_count += 1
        
        # Rate limiting - be nice to the API
        time.sleep(0.1)
    
    print(f"\n=== Enrichment Summary ===")
    print(f"Total farms: {len(farms_data)}")
    print(f"Successfully enriched: {enriched_count}")
    print(f"Skipped/Failed: {skipped_count}")
    
    return farms_data

def main():
    """Main function."""
    print("Cherry Farms Place ID Enrichment")
    print("=" * 40)
    
    # Load API key
    api_key = load_env_file()
    if not api_key:
        return
    
    # Get project root directory
    project_root = Path(__file__).parent.parent.parent
    
    # File path
    cherries_file = project_root / 'public' / 'data' / 'pyo_cherries.json'
    
    # Load current data
    print(f"Loading data from {cherries_file.name}...")
    farms_data = load_json_file(cherries_file)
    
    if not farms_data:
        print("Failed to load cherry farms data")
        return
    
    # Enrich the data
    enriched_data = enrich_cherry_farms(api_key, farms_data)
    
    # Save updated data
    print(f"\nSaving updated data to {cherries_file.name}...")
    if save_json_file(cherries_file, enriched_data):
        print("✅ Successfully saved updated cherry farms data")
    else:
        print("❌ Failed to save updated data")

if __name__ == "__main__":
    main()
