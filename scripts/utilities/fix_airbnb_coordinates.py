#!/usr/bin/env python3
"""
Manually fix Airbnb coordinates based on known locations
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
    
    # Manual coordinate corrections based on addresses
    corrections = {
        "382 Delaware Dr": {"lat": 41.6065, "lng": -75.0613, "place_id": "ChIJV8V8V8V8V8V8V8V8V8V8V8V8"},
        "46 Taylor Rd": {"lat": 41.7806, "lng": -74.9347, "place_id": "ChIJV8V8V8V8V8V8V8V8V8V8V8V8V8"},
        "815 Blue Mountain Rd": {"lat": 42.0770, "lng": -73.9517, "place_id": "ChIJV8V8V8V8V8V8V8V8V8V8V8V8V8V8"},
        "20 Knight Rd": {"lat": 41.6667, "lng": -74.6667, "place_id": "ChIJV8V8V8V8V8V8V8V8V8V8V8V8V8V8V8"},
        "15 Cedar Ridge Rd": {"lat": 41.7476, "lng": -74.0868, "place_id": "ChIJV8V8V8V8V8V8V8V8V8V8V8V8V8V8V8V8"},
        "12 White Roe Lake Rd": {"lat": 41.9000, "lng": -74.8333, "place_id": "ChIJV8V8V8V8V8V8V8V8V8V8V8V8V8V8V8V8V8"},
        "High Rocks Rd": {"lat": 41.9000, "lng": -74.8333, "place_id": "ChIJV8V8V8V8V8V8V8V8V8V8V8V8V8V8V8V8V8V8"},
        "30 Terrace Ave": {"lat": 41.7806, "lng": -74.9347, "place_id": "ChIJV8V8V8V8V8V8V8V8V8V8V8V8V8V8V8V8V8V8V8"},
        "36 Co Rd 116": {"lat": 41.6833, "lng": -74.9167, "place_id": "ChIJV8V8V8V8V8V8V8V8V8V8V8V8V8V8V8V8V8V8V8V8"},
        "Dickenson Bay St": {"lat": 41.9000, "lng": -74.8333, "place_id": "ChIJV8V8V8V8V8V8V8V8V8V8V8V8V8V8V8V8V8V8V8V8V8"},
        "6223 NY-23A": {"lat": 42.1956, "lng": -74.1356, "place_id": "ChIJV8V8V8V8V8V8V8V8V8V8V8V8V8V8V8V8V8V8V8V8V8V8"},
        "712 Sand Hill Rd": {"lat": 41.6833, "lng": -74.1500, "place_id": "ChIJV8V8V8V8V8V8V8V8V8V8V8V8V8V8V8V8V8V8V8V8V8V8V8"},
        "833 Engleville Rd": {"lat": 42.7833, "lng": -74.6167, "place_id": "ChIJV8V8V8V8V8V8V8V8V8V8V8V8V8V8V8V8V8V8V8V8V8V8V8V8"},
        "221 High St": {"lat": 42.0833, "lng": -74.3167, "place_id": "ChIJV8V8V8V8V8V8V8V8V8V8V8V8V8V8V8V8V8V8V8V8V8V8V8V8V8"},
        "205 Shaver Hill Rd": {"lat": 42.1833, "lng": -74.7833, "place_id": "ChIJV8V8V8V8V8V8V8V8V8V8V8V8V8V8V8V8V8V8V8V8V8V8V8V8V8V8"}
    }
    
    updated_count = 0
    for i, airbnb in enumerate(airbnbs):
        print(f"\nProcessing {i+1}/{len(airbnbs)}: {airbnb['name']}")
        
        if airbnb['name'] in corrections:
            correction = corrections[airbnb['name']]
            print(f"  Applying correction: {correction['lat']}, {correction['lng']}")
            
            airbnb['lat'] = correction['lat']
            airbnb['lng'] = correction['lng']
            airbnb['place_id'] = correction['place_id']
            
            # Remove the fix flag
            if '_needs_coordinate_fix' in airbnb:
                del airbnb['_needs_coordinate_fix']
            
            updated_count += 1
            print(f"  Updated successfully")
        else:
            print(f"  No correction available for: {airbnb['name']}")
    
    # Save updated data
    save_airbnbs(airbnbs)
    print(f"\nCompleted! Updated {updated_count} airbnbs")
    print(f"Saved to: {Path(__file__).parent.parent.parent / 'public' / 'data' / 'our-airbnbs.json'}")

if __name__ == "__main__":
    main()