#!/usr/bin/env python3
"""
Extract all place queries from trailheads data
"""

import json
from pathlib import Path

def extract_place_queries():
    # Load trailheads data
    trailheads_file = Path(__file__).parent.parent.parent / 'public' / 'data' / 'trail-heads.json'
    
    with open(trailheads_file, 'r', encoding='utf-8') as f:
        trailheads = json.load(f)
    
    print("🥾 Trailhead Place Queries:")
    print("=" * 50)
    
    total_queries = 0
    
    # Process each region's trails
    for region in trailheads:
        region_name = region.get('region', 'Unknown Region')
        print(f"\n📍 {region_name}:")
        
        if region.get('trails'):
            for trail in region['trails']:
                name = trail.get('name', 'Unknown Trail')
                place_query = trail.get('place_query', 'No place query')
                print(f"  • {name}")
                print(f"    Query: {place_query}")
                total_queries += 1
    
    print(f"\n📊 Total trailheads: {total_queries}")
    print("=" * 50)

if __name__ == "__main__":
    extract_place_queries()



