#!/usr/bin/env python3
"""
Fix Village/Town Place ID Issues

This script identifies and fixes cases where Google Places API returned
village place IDs when we actually want town place IDs (or vice versa).

The issue occurs because:
1. NY State has both villages and towns with the same name
2. Google Places API often returns the village first (more specific)
3. But our population data is for the town (larger area)

Usage:
    python fix_village_town_place_ids.py
"""

import json
import os
import requests
import time
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_place_details(place_id, api_key):
    """Get detailed information about a place using its place ID"""
    url = "https://maps.googleapis.com/maps/api/place/details/json"
    params = {
        'place_id': place_id,
        'fields': 'name,formatted_address,geometry,types,address_components',
        'key': api_key
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        if data['status'] == 'OK':
            return data['result']
        else:
            print(f"[ERROR] Place details failed: {data['status']}")
            return None
    except Exception as e:
        print(f"[ERROR] API request failed: {e}")
        return None

def find_place_id(query, api_key, prefer_town=True):
    """Find place ID with preference for town vs village"""
    url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
    params = {
        'input': query,
        'inputtype': 'textquery',
        'fields': 'place_id,name,formatted_address,geometry,types',
        'key': api_key
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        if data['status'] == 'OK' and data['candidates']:
            candidates = data['candidates']
            
            # If we prefer town, look for candidates that are towns
            if prefer_town:
                for candidate in candidates:
                    # Check if this is a town (not a village)
                    place_details = get_place_details(candidate['place_id'], api_key)
                    if place_details:
                        types = place_details.get('types', [])
                        address_components = place_details.get('address_components', [])
                        
                        # Look for town indicators
                        is_town = any('administrative_area_level_2' in types or 
                                    any('locality' in comp.get('types', []) for comp in address_components))
                        is_village = any('sublocality' in types or 
                                       any('sublocality_level_1' in comp.get('types', []) for comp in address_components))
                        
                        if is_town and not is_village:
                            print(f"[TOWN] Found town match: {candidate['name']}")
                            return candidate['place_id']
                
                # If no town found, return the first result
                print(f"[FALLBACK] No town found, using first result: {candidates[0]['name']}")
                return candidates[0]['place_id']
            else:
                # Return first result if we don't have a preference
                return candidates[0]['place_id']
        else:
            print(f"[ERROR] No candidates found for: {query}")
            return None
            
    except Exception as e:
        print(f"[ERROR] API request failed: {e}")
        return None

def analyze_place_id_issues():
    """Analyze current place IDs to identify village/town issues"""
    data_dir = Path(__file__).parent.parent / "public" / "data"
    map_data_path = data_dir / "map-data.json"
    
    print("Analyzing Place ID Issues")
    print("=" * 50)
    
    with open(map_data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    cities = data.get('cities', [])
    api_key = os.getenv('GOOGLE_MAPS_API_KEY')
    
    if not api_key:
        print("[ERROR] GOOGLE_MAPS_API_KEY not found in environment")
        return
    
    print(f"Analyzing {len(cities)} cities...")
    print()
    
    # Known problematic cases
    problematic_cities = []
    
    for city in cities:
        name = city.get('name', '')
        population = city.get('population', 0)
        place_id = city.get('place_id', '')
        description = city.get('description', '')
        
        # Skip if no place ID
        if not place_id:
            continue
        
        # Get place details to check if it's village vs town
        place_details = get_place_details(place_id, api_key)
        if not place_details:
            continue
        
        types = place_details.get('types', [])
        address_components = place_details.get('address_components', [])
        formatted_address = place_details.get('formatted_address', '')
        
        # Determine if current place ID is for village or town
        is_village = ('sublocality' in types or 
                     any('sublocality_level_1' in comp.get('types', []) for comp in address_components))
        is_town = ('administrative_area_level_2' in types or 
                  any('locality' in comp.get('types', []) for comp in address_components))
        
        # Check if there's a mismatch
        description_lower = description.lower()
        wants_town = 'town' in description_lower or population > 5000
        
        if wants_town and is_village:
            problematic_cities.append({
                'name': name,
                'population': population,
                'current_place_id': place_id,
                'current_address': formatted_address,
                'issue': 'Has village place ID but needs town',
                'description': description
            })
        elif not wants_town and is_town:
            problematic_cities.append({
                'name': name,
                'population': population,
                'current_place_id': place_id,
                'current_address': formatted_address,
                'issue': 'Has town place ID but needs village',
                'description': description
            })
        
        time.sleep(0.1)  # Rate limiting
    
    print("Problematic Place IDs Found:")
    print("-" * 60)
    
    if problematic_cities:
        for city in problematic_cities:
            print(f"• {city['name']:20s} - {city['issue']}")
            print(f"  Population: {city['population']:,}")
            print(f"  Current: {city['current_address']}")
            print()
    else:
        print("No obvious village/town mismatches found.")
    
    return problematic_cities

def fix_specific_city(city_name, prefer_town=True):
    """Fix place ID for a specific city"""
    data_dir = Path(__file__).parent.parent / "public" / "data"
    map_data_path = data_dir / "map-data.json"
    
    api_key = os.getenv('GOOGLE_MAPS_API_KEY')
    if not api_key:
        print("[ERROR] GOOGLE_MAPS_API_KEY not found in environment")
        return
    
    with open(map_data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    cities = data.get('cities', [])
    
    for city in cities:
        if city.get('name') == city_name:
            print(f"Fixing place ID for {city_name}...")
            
            # Create search query
            query = f"{city_name}, NY"
            if prefer_town:
                query += " town"
            
            # Find new place ID
            new_place_id = find_place_id(query, api_key, prefer_town)
            
            if new_place_id:
                # Get details for the new place ID
                place_details = get_place_details(new_place_id, api_key)
                if place_details:
                    # Update the city data
                    city['place_id'] = new_place_id
                    city['google_maps_url'] = f"https://www.google.com/maps/place/?q=place_id:{new_place_id}"
                    
                    print(f"[SUCCESS] Updated {city_name}")
                    print(f"  New place ID: {new_place_id}")
                    print(f"  New address: {place_details.get('formatted_address', '')}")
                    
                    # Save the updated data
                    with open(map_data_path, 'w', encoding='utf-8') as f:
                        json.dump(data, f, indent=2, ensure_ascii=False)
                    
                    return True
            
            print(f"[ERROR] Failed to find new place ID for {city_name}")
            return False
    
    print(f"[ERROR] City {city_name} not found")
    return False

if __name__ == "__main__":
    print("Village/Town Place ID Fixer")
    print("=" * 50)
    print()
    
    # First, analyze the issues
    problematic_cities = analyze_place_id_issues()
    
    print()
    print("Manual Fixes Available:")
    print("-" * 60)
    print("To fix a specific city, run:")
    print("  python fix_village_town_place_ids.py --fix Dryden")
    print()
    print("To fix all problematic cities, run:")
    print("  python fix_village_town_place_ids.py --fix-all")
    
    # Check for command line arguments
    import sys
    if len(sys.argv) > 1:
        if sys.argv[1] == '--fix' and len(sys.argv) > 2:
            city_name = sys.argv[2]
            fix_specific_city(city_name, prefer_town=True)
        elif sys.argv[1] == '--fix-all':
            if problematic_cities:
                for city in problematic_cities:
                    if city['issue'].startswith('Has village'):
                        fix_specific_city(city['name'], prefer_town=True)
                    elif city['issue'].startswith('Has town'):
                        fix_specific_city(city['name'], prefer_town=False)
