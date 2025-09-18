#!/usr/bin/env python3
"""
Remove All Place IDs Script

This script removes ALL place IDs from the data files so they can be
re-enriched with the fixed algorithm. This is simpler than trying to
selectively remove duplicates.

Usage:
    python remove_all_place_ids.py
"""

import json
import os
from pathlib import Path

def remove_all_place_ids():
    """Remove all place IDs from all data files"""
    data_dir = Path(__file__).parent.parent / "public" / "data"
    
    print("[CLEAN] Removing all place IDs from data files...")
    
    # Process all JSON files
    for filename in os.listdir(data_dir):
        if filename.endswith('.json'):
            filepath = data_dir / filename
            print(f"  Processing {filename}...")
            
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            modified = False
            
            # Handle different data structures
            items = []
            if isinstance(data, list):
                items = data
            elif isinstance(data, dict):
                if 'cities' in data:
                    items.extend(data['cities'])
                if 'scenicAreas' in data:
                    items.extend(data['scenicAreas'])
                # Add other potential arrays
                for key in data:
                    if isinstance(data[key], list) and key not in ['cities', 'scenicAreas']:
                        items.extend(data[key])
            
            # Remove place IDs from all items
            for item in items:
                if isinstance(item, dict):
                    if 'place_id' in item:
                        item['place_id'] = None
                        modified = True
                    if 'google_maps_url' in item:
                        item['google_maps_url'] = None
                        modified = True
            
            # Save if modified
            if modified:
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                print(f"    [OK] Removed place IDs from {filename}")
            else:
                print(f"    [SKIP] No place IDs found in {filename}")
    
    print(f"\n[OK] All place IDs removed!")
    print("Next steps:")
    print("1. Set your Google Maps API key in .env file")
    print("2. Run the fixed enrichment script to get unique place IDs")

if __name__ == "__main__":
    remove_all_place_ids()
