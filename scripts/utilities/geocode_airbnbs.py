#!/usr/bin/env python3
"""
Geocode Airbnb addresses using Google Places API
"""

import json
import os
import time
import requests
from pathlib import Path
from dotenv import load_dotenv

def load_airbnbs():
    """Load the airbnbs data from JSON file"""
    data_file = Path(__file__).parent.parent.parent / 'public' / 'data' / 'our-airbnbs.json'
    with open(data_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_airbnbs(airbnbs):
    """Save the updated airbnbs data to JSON file"""
    data_file = Path(__file__).parent.parent.parent / 'public' / 'data' / 'our-airbnbs.json'
    with open(data_file, 'w', encoding='utf-8') as f:
        json.dump(airbnbs, f, indent=2, ensure_ascii=False)

def geocode_address(api_key, name, address):
    """Geocode a single address using Google Geocoding API"""
    try:
        # Combine name and address for better geocoding
        full_address = f"{name}, {address}"
        print(f"Geocoding: {full_address}")
        
        # Use Google Geocoding API
        url = "https://maps.googleapis.com/maps/api/geocode/json"
        params = {
            'address': full_address,
            'key': api_key
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        if data['status'] == 'OK' and data['results']:
            result = data['results'][0]
            location = result['geometry']['location']
            place_id = result.get('place_id')
            
            print(f"  Found: {location['lat']}, {location['lng']}")
            print(f"  Place ID: {place_id}")
            
            return {
                'lat': location['lat'],
                'lng': location['lng'],
                'place_id': place_id,
                'geocoded_address': result['formatted_address']
            }
        else:
            print(f"  No results found for: {full_address} (Status: {data['status']})")
            return None
            
    except Exception as e:
        print(f"  Error geocoding {full_address}: {e}")
        return None

def main():
    # Load environment variables
    env_path = Path(__file__).parent.parent.parent / '.env'
    print(f"Loading .env from: {env_path}")
    load_dotenv(env_path)
    
    api_key = os.getenv('GOOGLE_MAPS_API_KEY')
    if not api_key:
        print("Error: GOOGLE_MAPS_API_KEY environment variable not set")
        return
    
    print(f"API key loaded: {api_key[:10]}...")
    
    # Load airbnbs data
    airbnbs = load_airbnbs()
    print(f"Loaded {len(airbnbs)} airbnbs")
    
    # Geocode each airbnb
    updated_count = 0
    for i, airbnb in enumerate(airbnbs):
        print(f"\nProcessing {i+1}/{len(airbnbs)}: {airbnb['name']}")
        
        # Skip if already has correct coordinates and place_id
        if (airbnb.get('place_id') and 
            not airbnb.get('_needs_coordinate_fix', False) and
            airbnb.get('lat') and airbnb.get('lng')):
            print("  Skipping - already geocoded")
            continue
        
        # Geocode the address
        result = geocode_address(api_key, airbnb['name'], airbnb['address'])
        
        if result:
            # Update the airbnb data
            airbnb['lat'] = result['lat']
            airbnb['lng'] = result['lng']
            airbnb['place_id'] = result['place_id']
            airbnb['geocoded_address'] = result['geocoded_address']
            
            # Remove the fix flag
            if '_needs_coordinate_fix' in airbnb:
                del airbnb['_needs_coordinate_fix']
            
            updated_count += 1
            print(f"  Updated successfully")
        else:
            print(f"  Failed to geocode")
        
        # Rate limiting - Google Geocoding API has limits
        time.sleep(0.1)  # 100ms delay between requests
    
    # Save updated data
    save_airbnbs(airbnbs)
    print(f"\nCompleted! Updated {updated_count} airbnbs")
    print(f"Saved to: {Path(__file__).parent.parent.parent / 'public' / 'data' / 'our-airbnbs.json'}")

if __name__ == "__main__":
    main()