#!/usr/bin/env python3
"""
Remove Strong Museum of Play from POIs (keep in children's activities)
"""

import json
from pathlib import Path

def remove_strong_museum():
    # Load POI data
    poi_file = Path(__file__).parent.parent.parent / 'public' / 'data' / 'points_of_interest.json'
    
    with open(poi_file, 'r', encoding='utf-8') as f:
        pois = json.load(f)
    
    print(f"📋 Original POIs: {len(pois)}")
    
    # Remove Strong Museum of Play
    original_count = len(pois)
    pois_filtered = []
    removed_items = []
    
    for poi in pois:
        if poi['name'] == "Strong Museum of Play":
            removed_items.append(poi['name'])
            print(f"  ❌ Removing: {poi['name']} (keeping in children's activities)")
        else:
            pois_filtered.append(poi)
    
    print(f"\n📊 Results:")
    print(f"  Removed: {len(removed_items)} POI")
    print(f"  Remaining: {len(pois_filtered)} POIs")
    
    # Save updated file
    with open(poi_file, 'w', encoding='utf-8') as f:
        json.dump(pois_filtered, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Updated {poi_file}")
    
    return removed_items

if __name__ == "__main__":
    removed = remove_strong_museum()



