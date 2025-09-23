#!/usr/bin/env python3
"""
Find duplicates between POIs and Children's Activities
"""

import json
from pathlib import Path
from difflib import SequenceMatcher

def similarity(a, b):
    """Calculate similarity between two strings"""
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def find_duplicates():
    # Load both datasets
    poi_file = Path(__file__).parent.parent.parent / 'public' / 'data' / 'points_of_interest.json'
    children_file = Path(__file__).parent.parent.parent / 'public' / 'data' / 'children.json'
    
    with open(poi_file, 'r', encoding='utf-8') as f:
        pois = json.load(f)
    
    with open(children_file, 'r', encoding='utf-8') as f:
        children = json.load(f)
    
    print("🔍 Searching for duplicates between POIs and Children's Activities...")
    print(f"POIs: {len(pois)} items")
    print(f"Children's Activities: {len(children)} items")
    print()
    
    duplicates = []
    
    # Check for exact matches first
    poi_names = {poi['name'].lower(): poi for poi in pois}
    children_names = {child['name'].lower(): child for child in children}
    
    exact_matches = set(poi_names.keys()) & set(children_names.keys())
    
    if exact_matches:
        print("🎯 EXACT MATCHES:")
        for name in exact_matches:
            poi = poi_names[name]
            child = children_names[name]
            print(f"  • {name.title()}")
            print(f"    POI Category: {poi.get('category', 'N/A')}")
            print(f"    POI Description: {poi.get('description', 'N/A')[:100]}...")
            print(f"    Children Description: {child.get('description', 'N/A')[:100]}...")
            print()
            duplicates.append({
                'name': name.title(),
                'type': 'exact',
                'poi': poi,
                'child': child
            })
    
    # Check for similar matches (high similarity score)
    print("🔍 SIMILAR MATCHES (potential duplicates):")
    similar_found = False
    
    for poi in pois:
        for child in children:
            sim = similarity(poi['name'], child['name'])
            if sim > 0.8 and poi['name'].lower() != child['name'].lower():
                print(f"  • {poi['name']} ↔ {child['name']} (similarity: {sim:.2f})")
                print(f"    POI Category: {poi.get('category', 'N/A')}")
                print(f"    POI Description: {poi.get('description', 'N/A')[:100]}...")
                print(f"    Children Description: {child.get('description', 'N/A')[:100]}...")
                print()
                similar_found = True
                duplicates.append({
                    'name': f"{poi['name']} ↔ {child['name']}",
                    'type': 'similar',
                    'similarity': sim,
                    'poi': poi,
                    'child': child
                })
    
    if not similar_found:
        print("  No similar matches found.")
    
    print(f"\n📊 SUMMARY:")
    print(f"  Exact matches: {len([d for d in duplicates if d['type'] == 'exact'])}")
    print(f"  Similar matches: {len([d for d in duplicates if d['type'] == 'similar'])}")
    print(f"  Total potential duplicates: {len(duplicates)}")
    
    return duplicates

if __name__ == "__main__":
    duplicates = find_duplicates()



