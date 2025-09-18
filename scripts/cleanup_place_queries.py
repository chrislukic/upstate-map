#!/usr/bin/env python3
"""
Cleanup Place Query Fields Script

This script cleans up existing place_query fields to use simpler, more effective
queries for Google Places API searches.

Usage:
    python cleanup_place_queries.py
"""

import json
import os
from pathlib import Path

def cleanup_place_queries_in_dataset(file_path, location_context=""):
    """
    Clean up place_query fields in a dataset
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
        
        # Skip if no place_query exists
        if 'place_query' not in item or not item['place_query']:
            continue
        
        current_query = item['place_query']
        
        # Create a cleaner query
        if "(" in name and ")" in name:
            # Extract location from parentheses
            start = name.find("(") + 1
            end = name.find(")")
            location_in_name = name[start:end]
            new_query = f"{name.split('(')[0].strip()}, {location_in_name}, NY"
        elif location:
            new_query = f"{name}, {location}"
        elif location_context:
            new_query = f"{name}, {location_context}, NY"
        else:
            new_query = f"{name}, NY"
        
        # Only update if the query is different
        if current_query != new_query:
            item['place_query'] = new_query
            modified_count += 1
            
            print(f"  {i+1}/{total_count}: {name}")
            print(f"    Old: '{current_query}'")
            print(f"    New: '{new_query}'")
    
    # Save the modified data
    if modified_count > 0:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"  [OK] Updated {modified_count} place queries in {file_path}")
    else:
        print(f"  [SKIP] No place queries updated in {file_path}")

def cleanup_place_queries_in_cities(file_path):
    """
    Clean up place_query fields in cities - make them simple "CityName, NY"
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
        
        # Skip if no place_query exists
        if 'place_query' not in city or not city['place_query']:
            continue
        
        current_query = city['place_query']
        
        # For cities, always use simple "CityName, NY" format
        new_query = f"{name}, NY"
        
        # Only update if the query is different
        if current_query != new_query:
            city['place_query'] = new_query
            modified_count += 1
            
            print(f"  {i+1}/{total_count}: {name}")
            print(f"    Old: '{current_query}'")
            print(f"    New: '{new_query}'")
    
    # Save the modified data
    if modified_count > 0:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"  [OK] Updated {modified_count} place queries in cities in {file_path}")
    else:
        print(f"  [SKIP] No place queries updated in cities in {file_path}")

def main():
    """
    Main process to clean up place queries in all datasets
    """
    print("Cleanup Place Query Fields Script")
    print("=" * 50)
    print("This will clean up existing place_query fields to use")
    print("simpler, more effective queries for Google Places API.")
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
            cleanup_place_queries_in_dataset(file_path, context)
        else:
            print(f"  File not found: {file_path}")
    
    # Process cities from map-data.json
    map_data_path = data_dir / "map-data.json"
    if map_data_path.exists():
        cleanup_place_queries_in_cities(map_data_path)
    else:
        print(f"  File not found: {map_data_path}")
    
    print(f"\n[OK] Place query cleanup complete!")
    print("\nNext steps:")
    print("1. Review the updated place_query fields")
    print("2. Run the improved enrichment script")

if __name__ == "__main__":
    main()

