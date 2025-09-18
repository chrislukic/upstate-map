#!/usr/bin/env python3
"""
Re-enrich Data with Updated Place Queries

This script uses the updated place_query fields (like "Dryden town, NY") to get
the correct coordinates, place IDs, and populations from Google Places API.

Usage:
    python re_enrich_with_updated_queries.py
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
        'fields': 'name,formatted_address,geometry,types,address_components,place_id',
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

def find_place_id(query, api_key):
    """Find place ID using the specific query"""
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
            return data['candidates'][0]['place_id']
        else:
            print(f"[ERROR] No candidates found for: {query}")
            return None
            
    except Exception as e:
        print(f"[ERROR] API request failed: {e}")
        return None

def get_population_from_place_details(place_details):
    """Extract population information from place details if available"""
    # Google Places API doesn't directly provide population data
    # This would need to be supplemented with other data sources
    # For now, we'll keep the existing population data
    return None

def re_enrich_cities():
    """Re-enrich city data using updated place queries"""
    data_dir = Path(__file__).parent.parent / "public" / "data"
    map_data_path = data_dir / "map-data.json"
    
    api_key = os.getenv('GOOGLE_MAPS_API_KEY')
    if not api_key:
        print("[ERROR] GOOGLE_MAPS_API_KEY not found in environment")
        return
    
    print("Re-enriching Cities with Updated Place Queries")
    print("=" * 60)
    
    with open(map_data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    cities = data.get('cities', [])
    if not cities:
        print("No cities found in map-data.json")
        return
    
    print(f"Processing {len(cities)} cities...")
    print()
    
    updated_count = 0
    
    for i, city in enumerate(cities):
        name = city.get('name', '')
        place_query = city.get('place_query', '')
        
        if not place_query:
            print(f"[SKIP] {name}: No place_query found")
            continue
        
        print(f"[{i+1:2d}/{len(cities)}] Processing {name}...")
        print(f"  Query: {place_query}")
        
        # Find new place ID using the specific query
        new_place_id = find_place_id(place_query, api_key)
        
        if new_place_id:
            # Get detailed information
            place_details = get_place_details(new_place_id, api_key)
            
            if place_details:
                # Update the city data
                old_place_id = city.get('place_id', '')
                old_lat = city.get('coordinates', [None, None])[0]
                old_lng = city.get('coordinates', [None, None])[1]
                
                # Extract new coordinates
                geometry = place_details.get('geometry', {})
                location = geometry.get('location', {})
                new_lat = location.get('lat')
                new_lng = location.get('lng')
                
                # Update the data
                city['place_id'] = new_place_id
                city['google_maps_url'] = f"https://www.google.com/maps/place/?q=place_id:{new_place_id}"
                
                if new_lat and new_lng:
                    city['coordinates'] = [new_lat, new_lng]
                
                # Show what changed
                if old_place_id != new_place_id:
                    print(f"  [UPDATED] Place ID: {old_place_id} -> {new_place_id}")
                
                if old_lat and old_lng and new_lat and new_lng:
                    lat_diff = abs(new_lat - old_lat)
                    lng_diff = abs(new_lng - old_lng)
                    if lat_diff > 0.001 or lng_diff > 0.001:  # Significant change
                        print(f"  [UPDATED] Coordinates: ({old_lat:.6f}, {old_lng:.6f}) -> ({new_lat:.6f}, {new_lng:.6f})")
                
                print(f"  [SUCCESS] Updated {name}")
                updated_count += 1
            else:
                print(f"  [ERROR] Could not get place details for {name}")
        else:
            print(f"  [ERROR] Could not find place ID for {name}")
        
        print()
        
        # Rate limiting
        time.sleep(0.1)
    
    if updated_count > 0:
        # Save the updated data
        with open(map_data_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"Successfully updated {updated_count} cities.")
    else:
        print("No cities were updated.")

def main():
    """Main function"""
    print("Re-enrichment with Updated Place Queries")
    print("=" * 60)
    print()
    
    # Check if we have the required environment variable
    api_key = os.getenv('GOOGLE_MAPS_API_KEY')
    if not api_key:
        print("[ERROR] GOOGLE_MAPS_API_KEY not found in environment")
        print("Please make sure you have a .env file in the scripts directory with:")
        print("GOOGLE_MAPS_API_KEY=your_api_key_here")
        return
    
    # Re-enrich the cities
    re_enrich_cities()
    
    print()
    print("Re-enrichment complete!")
    print()
    print("Note: Population data was not updated as Google Places API")
    print("does not provide population information. You may need to")
    print("manually verify and update population figures from other sources.")

if __name__ == "__main__":
    main()

