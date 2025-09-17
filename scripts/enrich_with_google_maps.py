#!/usr/bin/env python3
"""
Google Maps Place ID Enrichment Script

This script enriches all datasets (waterfalls, breweries, restaurants, cities) 
with Google Maps place IDs and creates Google Maps links for popups.

Usage:
    python enrich_with_google_maps.py

The script will:
1. Read the Google Maps API key from environment variable GOOGLE_MAPS_API_KEY
2. For each location in the datasets, find the Google Maps place ID
3. Add the place_id and google_maps_url fields to each record
4. Save the enriched data back to the original files

Requirements:
    pip install requests python-dotenv
"""

import json
import os
import requests
import time
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class GoogleMapsEnricher:
    def __init__(self):
        self.api_key = os.getenv('GOOGLE_MAPS_API_KEY')
        if not self.api_key:
            raise ValueError("GOOGLE_MAPS_API_KEY environment variable not set")
        
        self.base_url = "https://maps.googleapis.com/maps/api/place"
        self.rate_limit_delay = 0.1  # 100ms between requests to respect rate limits
        
    def find_place_id(self, name, lat, lng, location_context=""):
        """
        Find Google Maps place ID for a location using Places API Text Search
        """
        try:
            # Construct search query
            query = name
            if location_context:
                query += f" {location_context}"
            
            # Use Places Text Search API
            url = f"{self.base_url}/textsearch/json"
            params = {
                'query': query,
                'location': f"{lat},{lng}",
                'radius': 5000,  # 5km radius
                'key': self.api_key
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            if data['status'] == 'OK' and data['results']:
                # Return the first result (most relevant)
                place_id = data['results'][0]['place_id']
                return place_id
            else:
                print(f"  No place found for: {name} ({data.get('status', 'Unknown error')})")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"  API error for {name}: {e}")
            return None
        except Exception as e:
            print(f"  Unexpected error for {name}: {e}")
            return None
    
    def create_google_maps_url(self, place_id):
        """Create Google Maps URL from place ID"""
        return f"https://www.google.com/maps/place/?q=place_id:{place_id}"
    
    def enrich_dataset(self, file_path, location_context=""):
        """
        Enrich a dataset with Google Maps place IDs
        """
        print(f"\nEnriching {file_path}...")
        
        # Read the dataset
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if not isinstance(data, list):
            print(f"  Skipping {file_path} - not a list format")
            return
        
        enriched_count = 0
        total_count = len(data)
        
        for i, item in enumerate(data):
            print(f"  Processing {i+1}/{total_count}: {item.get('name', 'Unknown')}")
            
            # Check if already enriched
            if 'place_id' in item and 'google_maps_url' in item:
                print(f"    Already enriched, skipping")
                continue
            
            # Get coordinates
            lat = item.get('lat')
            lng = item.get('lng')
            
            if lat is None or lng is None:
                print(f"    No coordinates found, skipping")
                continue
            
            # Find place ID
            place_id = self.find_place_id(
                item['name'], 
                lat, 
                lng, 
                location_context
            )
            
            if place_id:
                # Add place ID and Google Maps URL
                item['place_id'] = place_id
                item['google_maps_url'] = self.create_google_maps_url(place_id)
                enriched_count += 1
                print(f"    ✓ Found place ID: {place_id}")
            else:
                print(f"    ✗ No place ID found")
            
            # Rate limiting
            time.sleep(self.rate_limit_delay)
        
        # Save enriched data
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"  ✓ Enriched {enriched_count}/{total_count} items in {file_path}")
    
    def enrich_cities_from_map_data(self, file_path):
        """
        Enrich cities from the main map-data.json file
        """
        print(f"\nEnriching cities from {file_path}...")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        cities = data.get('cities', [])
        if not cities:
            print("  No cities found in map-data.json")
            return
        
        enriched_count = 0
        total_count = len(cities)
        
        for i, city in enumerate(cities):
            print(f"  Processing {i+1}/{total_count}: {city.get('name', 'Unknown')}")
            
            # Check if already enriched
            if 'place_id' in city and 'google_maps_url' in city:
                print(f"    Already enriched, skipping")
                continue
            
            # Get coordinates
            coords = city.get('coordinates')
            if not coords or len(coords) != 2:
                print(f"    No valid coordinates found, skipping")
                continue
            
            lat, lng = coords
            
            # Find place ID
            place_id = self.find_place_id(
                city['name'], 
                lat, 
                lng, 
                city.get('scenicArea', '')
            )
            
            if place_id:
                # Add place ID and Google Maps URL
                city['place_id'] = place_id
                city['google_maps_url'] = self.create_google_maps_url(place_id)
                enriched_count += 1
                print(f"    ✓ Found place ID: {place_id}")
            else:
                print(f"    ✗ No place ID found")
            
            # Rate limiting
            time.sleep(self.rate_limit_delay)
        
        # Save enriched data
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"  ✓ Enriched {enriched_count}/{total_count} cities in {file_path}")
    
    def run(self):
        """
        Run the enrichment process for all datasets
        """
        print("🗺️  Google Maps Place ID Enrichment Script")
        print("=" * 50)
        
        # Define data directory
        data_dir = Path(__file__).parent.parent / "public" / "data"
        
        # List of datasets to enrich
        datasets = [
            ("waterfalls.json", "waterfall"),
            ("breweries.json", "brewery"),
            ("restaurants.json", "restaurant"),
            ("orchards_points.json", "orchard"),
        ]
        
        # Enrich individual datasets
        for filename, context in datasets:
            file_path = data_dir / filename
            if file_path.exists():
                self.enrich_dataset(file_path, context)
            else:
                print(f"  File not found: {file_path}")
        
        # Enrich cities from map-data.json
        map_data_path = data_dir / "map-data.json"
        if map_data_path.exists():
            self.enrich_cities_from_map_data(map_data_path)
        else:
            print(f"  File not found: {map_data_path}")
        
        print("\n✅ Enrichment complete!")
        print("\nNext steps:")
        print("1. Update the map renderer to include Google Maps links in popups")
        print("2. Test the links to ensure they work correctly")

if __name__ == "__main__":
    try:
        enricher = GoogleMapsEnricher()
        enricher.run()
    except ValueError as e:
        print(f"❌ Error: {e}")
        print("\nPlease set your Google Maps API key:")
        print("1. Create a .env file in the scripts directory")
        print("2. Add: GOOGLE_MAPS_API_KEY=your_api_key_here")
        print("3. Or set the environment variable directly")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
