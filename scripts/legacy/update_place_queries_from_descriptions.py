#!/usr/bin/env python3
"""
Update Place Queries Based on Descriptions

This script analyzes the descriptions in map-data.json and updates the place_query
fields to be more specific based on whether the description mentions "city", "town", 
"village", etc.

Examples:
- "Rural town with rolling hills" -> "Dryden town, NY"
- "Historic Mohawk Valley city" -> "Utica city, NY"
- "Olympic village" -> "Lake Placid village, NY"

Usage:
    python update_place_queries_from_descriptions.py
"""

import json
import re
from pathlib import Path

def analyze_description_for_type(description):
    """Analyze description to determine if it's a city, town, or village"""
    if not description:
        return None
    
    description_lower = description.lower()
    
    # Look for specific keywords
    if 'city' in description_lower:
        return 'city'
    elif 'town' in description_lower:
        return 'town'
    elif 'village' in description_lower:
        return 'village'
    elif 'hamlet' in description_lower:
        return 'hamlet'
    elif 'borough' in description_lower:
        return 'borough'
    
    return None

def update_place_queries():
    """Update place_query fields based on descriptions"""
    data_dir = Path(__file__).parent.parent / "public" / "data"
    map_data_path = data_dir / "map-data.json"
    
    print("Updating Place Queries Based on Descriptions")
    print("=" * 60)
    
    with open(map_data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    cities = data.get('cities', [])
    if not cities:
        print("No cities found in map-data.json")
        return
    
    print(f"Analyzing {len(cities)} cities...")
    print()
    
    updates_made = 0
    
    for city in cities:
        name = city.get('name', '')
        description = city.get('description', '')
        current_query = city.get('place_query', '')
        
        # Analyze the description
        place_type = analyze_description_for_type(description)
        
        if place_type:
            # Create new query
            new_query = f"{name} {place_type}, NY"
            
            # Only update if different from current
            if current_query != new_query:
                print(f"Updating {name}:")
                print(f"  Description: {description[:80]}...")
                print(f"  Detected type: {place_type}")
                print(f"  Old query: {current_query}")
                print(f"  New query: {new_query}")
                print()
                
                city['place_query'] = new_query
                updates_made += 1
        else:
            # No specific type found in description
            if current_query and current_query != f"{name}, NY":
                print(f"No type detected for {name}, keeping current: {current_query}")
    
    if updates_made > 0:
        # Save the updated data
        with open(map_data_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"Updated {updates_made} place queries.")
    else:
        print("No updates needed.")
    
    print()
    print("Summary of place types found:")
    print("-" * 40)
    
    # Count place types
    type_counts = {}
    for city in cities:
        place_type = analyze_description_for_type(city.get('description', ''))
        if place_type:
            type_counts[place_type] = type_counts.get(place_type, 0) + 1
    
    for place_type, count in sorted(type_counts.items()):
        print(f"{place_type.capitalize():10s}: {count:2d} cities")

if __name__ == "__main__":
    update_place_queries()

