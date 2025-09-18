#!/usr/bin/env python3
"""
Add Place Query Fields Script

This script helps add 'place_query' fields to JSON objects for more precise
Google Places API searches. It analyzes the existing data and suggests
place queries based on the name and location information.

Usage:
    python add_place_queries.py

The script will:
1. Analyze existing names and locations
2. Suggest place queries for better Google Places matching
3. Add 'place_query' fields to the JSON objects
4. Preserve existing place_query fields if they exist
"""

import json
import os
from pathlib import Path

def suggest_place_query(name, location="", location_context=""):
    """
    Suggest a place query based on the name and location
    """
    # If name already contains location info in parentheses, extract it
    if "(" in name and ")" in name:
        # Extract location from parentheses
        start = name.find("(") + 1
        end = name.find(")")
        location_in_name = name[start:end]
        
        # Create query with the location from the name
        base_name = name.split("(")[0].strip()
        return f"{base_name}, {location_in_name}, NY"
    
    # If we have a location field, use it
    if location:
        return f"{name}, {location}"
    
    # If we have location context, use it
    if location_context:
        return f"{name}, {location_context}, NY"
    
    # Default fallback
    return f"{name}, NY"

def add_place_queries_to_dataset(file_path, location_context=""):
    """
    Add place_query fields to a dataset
    """
    print(f"\nProcessing {file_path}...")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    if not isinstance(data, list):
        print(f"  Skipping {file_path} - not a list format")
        return
    
    modified_count = 0
    total_count = len(data)
    
    for i, item in enumerate(data):
        name = item.get('name', 'Unknown')
        location = item.get('location', '')
        
        # Skip if place_query already exists
        if 'place_query' in item and item['place_query']:
            continue
        
        # Suggest a place query
        suggested_query = suggest_place_query(name, location, location_context)
        
        # Add the place_query field
        item['place_query'] = suggested_query
        modified_count += 1
        
        print(f"  {i+1}/{total_count}: {name}")
        print(f"    Added: '{suggested_query}'")
    
    # Save the modified data
    if modified_count > 0:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"  [OK] Added {modified_count} place queries to {file_path}")
    else:
        print(f"  [SKIP] No place queries added to {file_path}")

def add_place_queries_to_cities(file_path):
    """
    Add place_query fields to cities in map-data.json
    """
    print(f"\nProcessing cities in {file_path}...")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    cities = data.get('cities', [])
    if not cities:
        print("  No cities found in map-data.json")
        return
    
    modified_count = 0
    total_count = len(cities)
    
    for i, city in enumerate(cities):
        name = city.get('name', 'Unknown')
        scenic_area = city.get('scenicArea', '')
        
        # Skip if place_query already exists
        if 'place_query' in city and city['place_query']:
            continue
        
        # For cities, keep it simple: just "CityName, NY"
        suggested_query = f"{name}, NY"
        
        # Add the place_query field
        city['place_query'] = suggested_query
        modified_count += 1
        
        print(f"  {i+1}/{total_count}: {name}")
        print(f"    Added: '{suggested_query}'")
    
    # Save the modified data
    if modified_count > 0:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"  [OK] Added {modified_count} place queries to cities in {file_path}")
    else:
        print(f"  [SKIP] No place queries added to cities in {file_path}")

def main():
    """
    Main process to add place queries to all datasets
    """
    print("Add Place Query Fields Script")
    print("=" * 50)
    print("This will add 'place_query' fields to JSON objects for")
    print("more precise Google Places API searches.")
    print("=" * 50)
    
    # Define data directory
    data_dir = Path(__file__).parent.parent / "public" / "data"
    
    # List of datasets to process
    datasets = [
        ("waterfalls.json", "waterfall"),
        ("breweries.json", "brewery"),
        ("restaurants.json", "restaurant"),
        ("orchards_points.json", "orchard"),
    ]
    
    # Process individual datasets
    for filename, context in datasets:
        file_path = data_dir / filename
        if file_path.exists():
            add_place_queries_to_dataset(file_path, context)
        else:
            print(f"  File not found: {file_path}")
    
    # Process cities from map-data.json
    map_data_path = data_dir / "map-data.json"
    if map_data_path.exists():
        add_place_queries_to_cities(map_data_path)
    else:
        print(f"  File not found: {map_data_path}")
    
    print(f"\n[OK] Place query addition complete!")
    print("\nNext steps:")
    print("1. Review the added place_query fields")
    print("2. Modify any place_query fields that need adjustment")
    print("3. Run the improved enrichment script")

if __name__ == "__main__":
    main()
