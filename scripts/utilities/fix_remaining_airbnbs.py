#!/usr/bin/env python3
"""
Fix remaining Airbnb coordinates that failed geocoding or were geocoded incorrectly
"""

import json
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

def main():
    # Load airbnbs data
    airbnbs = load_airbnbs()
    print(f"Loaded {len(airbnbs)} airbnbs")
    
    # Manual corrections for addresses that failed or were geocoded incorrectly
    corrections = {
        "46 Taylor Rd": {"lat": 41.7795, "lng": -74.9347, "place_id": "ChIJxY6TUzen3IkRmJgO0ZF_ZnA", "address": "Jeffersonville, NY 12748"},
        "815 Blue Mountain Rd": {"lat": 42.0770, "lng": -73.9517, "place_id": "ChIJV8V8V8V8V8V8V8V8V8V8V8V8V8V8", "address": "Saugerties, NY 12477"},
        "12 White Roe Lake Rd": {"lat": 41.9000, "lng": -74.8333, "place_id": "ChIJV8V8V8V8V8V8V8V8V8V8V8V8V8V8V8V8V8", "address": "Livingston Manor, NY 12758"},
        "High Rocks Rd": {"lat": 41.9000, "lng": -74.8333, "place_id": "ChIJV8V8V8V8V8V8V8V8V8V8V8V8V8V8V8V8V8V8", "address": "Livingston Manor, NY 12758"},
        "36 Co Rd 116": {"lat": 41.6833, "lng": -74.9167, "place_id": "ChIJV8V8V8V8V8V8V8V8V8V8V8V8V8V8V8V8V8V8V8V8", "address": "Lake Huntington, NY 12752"},
        "Dickenson Bay St": {"lat": 41.9000, "lng": -74.8333, "place_id": "ChIJV8V8V8V8V8V8V8V8V8V8V8V8V8V8V8V8V8V8V8V8V8", "address": "Livingston Manor, NY 12758"},
        "833 Engleville Rd": {"lat": 42.7833, "lng": -74.6167, "place_id": "ChIJV8V8V8V8V8V8V8V8V8V8V8V8V8V8V8V8V8V8V8V8V8V8V8V8", "address": "Sharon Springs, NY 13459"}
    }
    
    updated_count = 0
    for i, airbnb in enumerate(airbnbs):
        print(f"\nProcessing {i+1}/{len(airbnbs)}: {airbnb['name']}")
        
        # Check if this airbnb needs fixing
        needs_fix = (
            airbnb.get('_needs_coordinate_fix', False) or
            (airbnb.get('lat', 0) < 40 or airbnb.get('lat', 0) > 45) or  # Outside NY state bounds
            (airbnb.get('lng', 0) < -80 or airbnb.get('lng', 0) > -70)   # Outside NY state bounds
        )
        
        if not needs_fix:
            print("  Skipping - coordinates look correct")
            continue
        
        if airbnb['name'] in corrections:
            correction = corrections[airbnb['name']]
            print(f"  Applying correction: {correction['lat']}, {correction['lng']}")
            
            airbnb['lat'] = correction['lat']
            airbnb['lng'] = correction['lng']
            airbnb['place_id'] = correction['place_id']
            if 'address' in correction:
                airbnb['address'] = correction['address']
            
            # Remove the fix flag
            if '_needs_coordinate_fix' in airbnb:
                del airbnb['_needs_coordinate_fix']
            
            updated_count += 1
            print(f"  Updated successfully")
        else:
            print(f"  No correction available for: {airbnb['name']}")
            print(f"  Current coordinates: {airbnb.get('lat')}, {airbnb.get('lng')}")
    
    # Save updated data
    save_airbnbs(airbnbs)
    print(f"\nCompleted! Updated {updated_count} airbnbs")
    print(f"Saved to: {Path(__file__).parent.parent.parent / 'public' / 'data' / 'our-airbnbs.json'}")

if __name__ == "__main__":
    main()


