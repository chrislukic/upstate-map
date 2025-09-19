#!/usr/bin/env python3
"""
Remove duplicate entries from children.json that are already in POIs
"""

import json
from pathlib import Path

def remove_duplicates():
    # Load children's activities
    children_file = Path(__file__).parent.parent.parent / 'public' / 'data' / 'children.json'
    
    with open(children_file, 'r', encoding='utf-8') as f:
        children = json.load(f)
    
    print(f"📋 Original children's activities: {len(children)}")
    
    # List of duplicates to remove (keep in POIs instead)
    duplicates_to_remove = [
        "Howe Caverns",
        "Niagara Falls State Park", 
        "Corning Museum of Glass",
        "The Wild Center"
    ]
    
    # Remove duplicates
    original_count = len(children)
    children_filtered = []
    removed_items = []
    
    for child in children:
        if child['name'] in duplicates_to_remove:
            removed_items.append(child['name'])
            print(f"  ❌ Removing: {child['name']} (keeping in POIs)")
        else:
            children_filtered.append(child)
    
    print(f"\n📊 Results:")
    print(f"  Removed: {len(removed_items)} duplicates")
    print(f"  Remaining: {len(children_filtered)} children's activities")
    
    # Save updated file
    with open(children_file, 'w', encoding='utf-8') as f:
        json.dump(children_filtered, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Updated {children_file}")
    
    return removed_items

if __name__ == "__main__":
    removed = remove_duplicates()
