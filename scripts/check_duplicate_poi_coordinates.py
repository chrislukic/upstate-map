#!/usr/bin/env python3
"""
Check for POIs with duplicate or very close coordinates

This script identifies POIs that have identical or very close coordinates
which would cause overlapping icons on the map.

Usage:
    python check_duplicate_poi_coordinates.py
"""

import json
from pathlib import Path
from collections import defaultdict

def check_duplicate_coordinates():
    """Check for POIs with duplicate or very close coordinates"""
    data_dir = Path(__file__).parent.parent / "public" / "data"
    poi_path = data_dir / "points_of_interest.json"
    
    print("Checking for POIs with duplicate or close coordinates")
    print("=" * 60)
    
    with open(poi_path, 'r', encoding='utf-8') as f:
        pois = json.load(f)
    
    if not pois:
        print("No POIs found in points_of_interest.json")
        return
    
    # Group POIs by coordinates
    coordinate_groups = defaultdict(list)
    
    for poi in pois:
        lat = poi.get('lat')
        lng = poi.get('lng')
        if lat is not None and lng is not None:
            # Round to 4 decimal places (about 11 meters precision)
            key = (round(lat, 4), round(lng, 4))
            coordinate_groups[key].append(poi)
    
    print(f"Analyzing {len(pois)} POIs...")
    print()
    
    # Find groups with multiple POIs
    duplicates = {coord: pois for coord, pois in coordinate_groups.items() if len(pois) > 1}
    
    if duplicates:
        print("POIs with identical coordinates (rounded to 4 decimal places):")
        print("-" * 60)
        
        for coord, poi_list in duplicates.items():
            lat, lng = coord
            print(f"Coordinates: {lat}, {lng}")
            for poi in poi_list:
                name = poi.get('name', 'Unknown')
                category = poi.get('category', 'Unknown')
                location = poi.get('location', 'Unknown')
                print(f"  • {name} ({category}) - {location}")
            print()
    else:
        print("No POIs found with identical coordinates.")
    
    # Check for very close coordinates (within ~100 meters)
    print("Checking for POIs within ~100 meters of each other...")
    print("-" * 60)
    
    close_pairs = []
    poi_list = list(pois)
    
    for i, poi1 in enumerate(poi_list):
        for j, poi2 in enumerate(poi_list[i+1:], i+1):
            lat1, lng1 = poi1.get('lat'), poi1.get('lng')
            lat2, lng2 = poi2.get('lat'), poi2.get('lng')
            
            if all(x is not None for x in [lat1, lng1, lat2, lng2]):
                # Calculate approximate distance in meters
                # Using simple approximation: 1 degree ≈ 111,000 meters
                lat_diff = abs(lat1 - lat2) * 111000
                lng_diff = abs(lng1 - lng2) * 111000 * 0.7  # Adjust for longitude
                distance = (lat_diff**2 + lng_diff**2)**0.5
                
                if distance < 100:  # Within 100 meters
                    close_pairs.append({
                        'distance': distance,
                        'poi1': poi1,
                        'poi2': poi2
                    })
    
    if close_pairs:
        # Sort by distance
        close_pairs.sort(key=lambda x: x['distance'])
        
        for pair in close_pairs:
            distance = pair['distance']
            poi1 = pair['poi1']
            poi2 = pair['poi2']
            
            print(f"Distance: {distance:.0f}m")
            print(f"  • {poi1.get('name')} ({poi1.get('category')}) - {poi1.get('location')}")
            print(f"  • {poi2.get('name')} ({poi2.get('category')}) - {poi2.get('location')}")
            print()
    else:
        print("No POIs found within 100 meters of each other.")
    
    print()
    print("Summary:")
    print(f"Total POIs: {len(pois)}")
    print(f"Unique coordinate locations: {len(coordinate_groups)}")
    print(f"Duplicate coordinates: {len(duplicates)}")
    print(f"Close pairs (<100m): {len(close_pairs)}")

if __name__ == "__main__":
    check_duplicate_coordinates()

