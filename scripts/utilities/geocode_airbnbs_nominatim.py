#!/usr/bin/env python3
"""
Geocode Airbnb addresses using Nominatim (OpenStreetMap) - free service
"""

import json
import time
import requests
from pathlib import Path

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

def geocode_with_nominatim(name, address):
    """Geocode using Nominatim (OpenStreetMap)"""
    try:
        # Combine name and address for better geocoding
        full_address = f"{name}, {address}, New York, USA"
        print(f"Geocoding: {full_address}")
        
        # Use Nominatim API
        url = "https://nominatim.openstreetmap.org/search"
        params = {
            'q': full_address,
            'format': 'json',
            'limit': 1,
            'countrycodes': 'us',
            'state': 'NY'
        }
        
        headers = {
            'User-Agent': 'ScenicNYMap/1.0 (contact@example.com)'  # Required by Nominatim
        }
        
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        if data and len(data) > 0:
            result = data[0]
            lat = float(result['lat'])
            lng = float(result['lon'])
            
            print(f"  Found: {lat}, {lng}")
            print(f"  Display name: {result.get('display_name', 'N/A')}")
            
            return {
                'lat': lat,
                'lng': lng,
                'place_id': result.get('place_id'),
                'geocoded_address': result.get('display_name', full_address)
            }
        else:
            print(f"  No results found for: {full_address}")
            return None
            
    except Exception as e:
        print(f"  Error geocoding {full_address}: {e}")
        return None

def main():
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
        
        # Skip if address is None or empty
        if not airbnb.get('address') or airbnb['address'] == 'None':
            print("  Skipping - no address")
            continue
        
        # Geocode the address
        result = geocode_with_nominatim(airbnb['name'], airbnb['address'])
        
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
        
        # Rate limiting - Nominatim requires 1 second between requests
        time.sleep(1.1)
    
    # Save updated data
    save_airbnbs(airbnbs)
    print(f"\nCompleted! Updated {updated_count} airbnbs")
    print(f"Saved to: {Path(__file__).parent.parent.parent / 'public' / 'data' / 'our-airbnbs.json'}")

if __name__ == "__main__":
    main()


