#!/usr/bin/env python3
"""
Fixed Google Maps Place ID Enrichment Script

This script enriches all datasets with Google Maps place IDs, addressing the issues
that caused duplicate place IDs in the original script.

Key improvements:
1. Reduced search radius (1km instead of 5km)
2. Coordinate validation to ensure returned place ID matches input location
3. More specific search queries with state/country context
4. Fallback logic for better matching
5. Duplicate detection and prevention

Usage:
    python enrich_with_google_maps_fixed.py

Requirements:
    pip install requests python-dotenv
"""

import json
import os
import requests
import time
import math
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class FixedGoogleMapsEnricher:
    def __init__(self):
        self.api_key = os.getenv('GOOGLE_MAPS_API_KEY')
        if not self.api_key:
            raise ValueError("GOOGLE_MAPS_API_KEY environment variable not set")
        
        self.base_url = "https://maps.googleapis.com/maps/api/place"
        self.rate_limit_delay = 0.1  # 100ms between requests
        self.used_place_ids = set()  # Track used place IDs to prevent duplicates
        
    def calculate_distance(self, lat1, lng1, lat2, lng2):
        """Calculate distance between two coordinates in meters"""
        R = 6371000  # Earth's radius in meters
        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        delta_lat = math.radians(lat2 - lat1)
        delta_lng = math.radians(lng2 - lng1)
        
        a = (math.sin(delta_lat/2) * math.sin(delta_lat/2) + 
             math.cos(lat1_rad) * math.cos(lat2_rad) * 
             math.sin(delta_lng/2) * math.sin(delta_lng/2))
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        
        return R * c
    
    def find_place_id(self, name, lat, lng, location_context="", state="NY", country="USA"):
        """
        Find Google Maps place ID with improved accuracy and validation
        """
        try:
            # Create more specific search query
            query = f"{name}, {state}, {country}"
            if location_context:
                query = f"{name} {location_context}, {state}, {country}"
            
            print(f"    Searching: '{query}'")
            
            # Use Places Text Search API with smaller radius
            url = f"{self.base_url}/textsearch/json"
            params = {
                'query': query,
                'location': f"{lat},{lng}",
                'radius': 1000,  # Reduced to 1km for more precise results
                'key': self.api_key
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            if data['status'] == 'OK' and data['results']:
                # Find the best match by validating coordinates
                best_match = None
                min_distance = float('inf')
                
                for result in data['results']:
                    result_lat = result['geometry']['location']['lat']
                    result_lng = result['geometry']['location']['lng']
                    
                    # Calculate distance from our target coordinates
                    distance = self.calculate_distance(lat, lng, result_lat, result_lng)
                    
                    # Prefer results within 2km and closer to our target
                    if distance < 2000 and distance < min_distance:
                        min_distance = distance
                        best_match = result
                
                if best_match:
                    place_id = best_match['place_id']
                    
                    # Check for duplicates
                    if place_id in self.used_place_ids:
                        print(f"    [WARN] Duplicate place ID detected: {place_id}")
                        print(f"    Distance: {min_distance:.0f}m from target")
                        return None
                    
                    # Validate the match is reasonable
                    if min_distance > 1000:  # More than 1km away
                        print(f"    [WARN] Match too far: {min_distance:.0f}m from target")
                        return None
                    
                    self.used_place_ids.add(place_id)
                    print(f"    [OK] Found place ID: {place_id} ({min_distance:.0f}m away)")
                    return place_id
                else:
                    print(f"    [ERROR] No suitable match found within 2km")
                    return None
            else:
                print(f"    [ERROR] No place found: {data.get('status', 'Unknown error')}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"    API error: {e}")
            return None
        except Exception as e:
            print(f"    Unexpected error: {e}")
            return None
    
    def create_google_maps_url(self, place_id):
        """Create Google Maps URL from place ID"""
        return f"https://www.google.com/maps/place/?q=place_id:{place_id}"
    
    def enrich_dataset(self, file_path, location_context="", state="NY"):
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
        skipped_count = 0
        total_count = len(data)
        
        for i, item in enumerate(data):
            name = item.get('name', 'Unknown')
            print(f"  Processing {i+1}/{total_count}: {name}")
            
            # Check if already enriched (has valid place_id)
            if 'place_id' in item and item['place_id'] is not None and 'google_maps_url' in item:
                print(f"    Already enriched, skipping")
                continue
            
            # Get coordinates
            lat = item.get('lat')
            lng = item.get('lng')
            
            if lat is None or lng is None:
                print(f"    No coordinates found, skipping")
                skipped_count += 1
                continue
            
            # Find place ID
            place_id = self.find_place_id(
                name, 
                lat, 
                lng, 
                location_context,
                state
            )
            
            if place_id:
                # Add place ID and Google Maps URL
                item['place_id'] = place_id
                item['google_maps_url'] = self.create_google_maps_url(place_id)
                enriched_count += 1
            else:
                print(f"    [ERROR] No place ID found")
                skipped_count += 1
            
            # Rate limiting
            time.sleep(self.rate_limit_delay)
        
        # Save enriched data
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"  [OK] Enriched {enriched_count}/{total_count} items in {file_path}")
        print(f"  [WARN] Skipped {skipped_count} items")
    
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
        skipped_count = 0
        total_count = len(cities)
        
        for i, city in enumerate(cities):
            name = city.get('name', 'Unknown')
            print(f"  Processing {i+1}/{total_count}: {name}")
            
            # Check if already enriched (has valid place_id)
            if 'place_id' in city and city['place_id'] is not None and 'google_maps_url' in city:
                print(f"    Already enriched, skipping")
                continue
            
            # Get coordinates
            coords = city.get('coordinates')
            if not coords or len(coords) != 2:
                print(f"    No valid coordinates found, skipping")
                skipped_count += 1
                continue
            
            lat, lng = coords
            
            # Find place ID with scenic area context
            scenic_area = city.get('scenicArea', '')
            place_id = self.find_place_id(
                name, 
                lat, 
                lng, 
                scenic_area,
                "NY"
            )
            
            if place_id:
                # Add place ID and Google Maps URL
                city['place_id'] = place_id
                city['google_maps_url'] = self.create_google_maps_url(place_id)
                enriched_count += 1
            else:
                print(f"    [ERROR] No place ID found")
                skipped_count += 1
            
            # Rate limiting
            time.sleep(self.rate_limit_delay)
        
        # Save enriched data
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"  [OK] Enriched {enriched_count}/{total_count} cities in {file_path}")
        print(f"  [WARN] Skipped {skipped_count} cities")
    
    def run(self):
        """
        Run the enrichment process for all datasets
        """
        print("Fixed Google Maps Place ID Enrichment Script")
        print("=" * 60)
        print("Key improvements:")
        print("- Reduced search radius (1km vs 5km)")
        print("- Coordinate validation and distance checking")
        print("- Duplicate place ID prevention")
        print("- More specific search queries")
        print("=" * 60)
        
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
        
        print(f"\n[OK] Enrichment complete!")
        print(f"[INFO] Used {len(self.used_place_ids)} unique place IDs")
        print("\nNext steps:")
        print("1. Run the duplicate checker to verify no duplicates remain")
        print("2. Test the Google Maps links in the application")
        print("3. Update any remaining locations manually if needed")

if __name__ == "__main__":
    try:
        enricher = FixedGoogleMapsEnricher()
        enricher.run()
    except ValueError as e:
        print(f"[ERROR] Error: {e}")
        print("\nPlease set your Google Maps API key:")
        print("1. Create a .env file in the scripts directory")
        print("2. Add: GOOGLE_MAPS_API_KEY=your_api_key_here")
        print("3. Or set the environment variable directly")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
