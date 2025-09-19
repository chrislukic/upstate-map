#!/usr/bin/env python3
"""
Update cherry farms with accurate GPS coordinates using Google Places API.
This script will update lat/lng coordinates using the place_id from Google Places.
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

def get_place_details(api_key, place_id):
    """Get detailed information about a place using its place_id."""
    base_url = "https://maps.googleapis.com/maps/api/place/details/json"
    
    params = {
        'place_id': place_id,
        'fields': 'place_id,name,formatted_address,geometry,types',
        'key': api_key
    }
    
    try:
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if data.get('status') == 'OK' and data.get('result'):
            result = data['result']
            geometry = result.get('geometry', {})
            location = geometry.get('location', {})
            
            return {
                'place_id': result.get('place_id'),
                'name': result.get('name'),
                'formatted_address': result.get('formatted_address'),
                'lat': location.get('lat'),
                'lng': location.get('lng'),
                'types': result.get('types', [])
            }
        else:
            print(f"  [WARNING] No details found for place_id {place_id}: {data.get('status', 'Unknown error')}")
            return None
            
    except Exception as e:
        print(f"  [ERROR] API request failed for place_id {place_id}: {e}")
        return None

def update_cherry_coordinates(api_key, farms_data):
    """Update cherry farms with accurate GPS coordinates."""
    updated_count = 0
    skipped_count = 0
    
    print(f"Processing {len(farms_data)} cherry farms...")
    
    for i, farm in enumerate(farms_data, 1):
        name = farm.get('name', '')
        place_id = farm.get('place_id', '')
        current_lat = farm.get('lat')
        current_lng = farm.get('lng')
        
        print(f"\n[{i}/{len(farms_data)}] Processing: {name}")
        print(f"  Current coordinates: {current_lat}, {current_lng}")
        
        if not place_id:
            print(f"  [SKIP] No place_id found")
            skipped_count += 1
            continue
        
        # Get place details from Google Places API
        result = get_place_details(api_key, place_id)
        
        if result and result.get('lat') and result.get('lng'):
            new_lat = result['lat']
            new_lng = result['lng']
            
            # Update the farm data
            farm['lat'] = new_lat
            farm['lng'] = new_lng
            
            print(f"  [SUCCESS] Updated coordinates: {new_lat}, {new_lng}")
            print(f"  [INFO] Verified name: {result.get('name', 'Unknown')}")
            print(f"  [INFO] Verified address: {result.get('formatted_address', 'Unknown')}")
            
            # Show coordinate difference if significant
            if current_lat and current_lng:
                lat_diff = abs(new_lat - current_lat)
                lng_diff = abs(new_lng - current_lng)
                if lat_diff > 0.001 or lng_diff > 0.001:  # More than ~100m difference
                    print(f"  [NOTICE] Significant coordinate change detected:")
                    print(f"    Old: {current_lat}, {current_lng}")
                    print(f"    New: {new_lat}, {new_lng}")
                    print(f"    Difference: {lat_diff:.6f}, {lng_diff:.6f}")
            
            updated_count += 1
        else:
            print(f"  [FAILED] Could not get coordinates for {name}")
            skipped_count += 1
        
        # Rate limiting - be nice to the API
        time.sleep(0.1)
    
    print(f"\n=== Coordinate Update Summary ===")
    print(f"Total farms: {len(farms_data)}")
    print(f"Successfully updated: {updated_count}")
    print(f"Skipped/Failed: {skipped_count}")
    
    return farms_data

def main():
    """Main function."""
    print("Cherry Farms GPS Coordinate Update")
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
    
    # Update coordinates
    updated_data = update_cherry_coordinates(api_key, farms_data)
    
    # Save updated data
    print(f"\nSaving updated data to {cherries_file.name}...")
    if save_json_file(cherries_file, updated_data):
        print("✅ Successfully saved updated cherry farms data with accurate coordinates")
    else:
        print("❌ Failed to save updated data")

if __name__ == "__main__":
    main()
