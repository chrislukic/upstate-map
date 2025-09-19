#!/usr/bin/env python3
"""
Fix Overlapping POI Coordinates

This script fixes POIs that have identical coordinates by adding small offsets
to separate them visually on the map while keeping them close to their actual locations.

Usage:
    python fix_overlapping_poi_coordinates.py
"""

import json
from pathlib import Path

def fix_overlapping_coordinates():
    """Fix POIs with identical coordinates by adding small offsets"""
    data_dir = Path(__file__).parent.parent / "public" / "data"
    poi_path = data_dir / "points_of_interest.json"
    
    print("Fixing Overlapping POI Coordinates")
    print("=" * 50)
    
    with open(poi_path, 'r', encoding='utf-8') as f:
        pois = json.load(f)
    
    if not pois:
        print("No POIs found in points_of_interest.json")
        return
    
    # Define the overlapping groups and their offsets
    coordinate_fixes = {
        # Rochester, NY - Strong Museum and George Eastman Museum
        (43.1528, -77.6028): [
            {"name": "Strong Museum of Play", "offset": (0.0005, 0.0005)},  # NE
            {"name": "George Eastman Museum", "offset": (-0.0005, -0.0005)}  # SW
        ],
        
        # Storm King Area - Art Center and State Park
        (41.4206, -74.0611): [
            {"name": "Storm King Art Center", "offset": (0.0003, 0.0003)},  # NE
            {"name": "Storm King State Park", "offset": (-0.0003, -0.0003)}  # SW
        ],
        
        # Cooperstown, NY - Baseball Hall of Fame and Fenimore Art Museum
        (42.7006, -74.9242): [
            {"name": "Cooperstown Baseball Hall of Fame", "offset": (0.0004, 0.0004)},  # NE
            {"name": "Fenimore Art Museum", "offset": (-0.0004, -0.0004)}  # SW
        ],
        
        # Hyde Park, NY - FDR Library and Vanderbilt Mansion
        (41.7667, -73.9333): [
            {"name": "Franklin D. Roosevelt Presidential Library and Museum", "offset": (0.0006, 0.0006)},  # NE
            {"name": "Vanderbilt Mansion National Historic Site", "offset": (-0.0006, -0.0006)}  # SW
        ]
    }
    
    print(f"Processing {len(pois)} POIs...")
    print()
    
    fixes_applied = 0
    
    for poi in pois:
        name = poi.get('name', '')
        lat = poi.get('lat')
        lng = poi.get('lng')
        
        if lat is None or lng is None:
            continue
        
        # Round to 4 decimal places to match our coordinate groups
        rounded_coord = (round(lat, 4), round(lng, 4))
        
        if rounded_coord in coordinate_fixes:
            # Find the specific POI in the fix list
            for fix in coordinate_fixes[rounded_coord]:
                if fix["name"] == name:
                    # Apply the offset
                    lat_offset, lng_offset = fix["offset"]
                    new_lat = lat + lat_offset
                    new_lng = lng + lng_offset
                    
                    print(f"Fixing {name}:")
                    print(f"  Old: {lat:.6f}, {lng:.6f}")
                    print(f"  New: {new_lat:.6f}, {new_lng:.6f}")
                    print(f"  Offset: {lat_offset:.6f}, {lng_offset:.6f}")
                    print()
                    
                    # Update the coordinates
                    poi['lat'] = new_lat
                    poi['lng'] = new_lng
                    fixes_applied += 1
                    break
    
    if fixes_applied > 0:
        # Save the updated data
        with open(poi_path, 'w', encoding='utf-8') as f:
            json.dump(pois, f, indent=2, ensure_ascii=False)
        
        print(f"Applied {fixes_applied} coordinate fixes.")
        print("Updated points_of_interest.json with separated coordinates.")
    else:
        print("No overlapping coordinates found to fix.")
    
    print()
    print("Coordinate offsets applied:")
    print("- Each offset is approximately 50-100 meters")
    print("- POIs are now visually separated but remain close to actual locations")
    print("- NE offset: slightly northeast of original position")
    print("- SW offset: slightly southwest of original position")

if __name__ == "__main__":
    fix_overlapping_coordinates()

