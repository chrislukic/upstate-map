#!/usr/bin/env python3
"""
Improved Google Maps Place ID Enrichment Script

This script addresses the issues with the previous enrichment:
1. Updates coordinates from Google Places API (source of truth)
2. Uses better search queries for cities ("City Name, NY")
3. Validates and corrects coordinates based on place ID results

Usage:
    python enrich_with_google_maps_improved.py

Requirements:
    pip install requests python-dotenv
"""

import json
import os
import requests
import time
import math
from pathlib import Path
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class ImprovedGoogleMapsEnricher:
    def __init__(self):
        self.api_key = os.getenv('GOOGLE_MAPS_API_KEY')
        if not self.api_key:
            raise ValueError("GOOGLE_MAPS_API_KEY environment variable not set")
        
        self.base_url = "https://maps.googleapis.com/maps/api/place"
        self.rate_limit_delay = 0.1  # 100ms between requests
        self.used_place_ids = set()  # Track used place IDs to prevent duplicates
        # Cache/verification policy
        self.cache_path = Path(__file__).parent / ".places_cache.json"
        self.cache_ttl_days = 30
        self.verify_ttl_days = 180
        self.distance_threshold_meters = 30
        self.cache = self._load_cache()

    def _load_cache(self):
        try:
            if self.cache_path.exists():
                with open(self.cache_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception:
            pass
        return {}

    def _save_cache(self):
        try:
            with open(self.cache_path, 'w', encoding='utf-8') as f:
                json.dump(self.cache, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"    [WARN] Failed to save cache: {e}")

    def _iso_now(self):
        return datetime.now(timezone.utc).isoformat()

    def _parse_iso(self, s):
        try:
            return datetime.fromisoformat(s.replace('Z', '+00:00'))
        except Exception:
            return None
        
    def get_place_details(self, place_id):
        """Get detailed information about a place using its place ID"""
        try:
            # Cache check
            cache_entry = self.cache.get(place_id)
            if cache_entry:
                fetched_at = self._parse_iso(cache_entry.get('fetched_at', ''))
                if fetched_at and datetime.now(timezone.utc) - fetched_at < timedelta(days=self.cache_ttl_days):
                    return {
                        'lat': cache_entry['lat'],
                        'lng': cache_entry['lng'],
                        'name': cache_entry.get('name', ''),
                        'address': cache_entry.get('formatted_address', '')
                    }

            url = f"{self.base_url}/details/json"
            params = {
                'place_id': place_id,
                'fields': 'geometry,name,formatted_address',
                'key': self.api_key
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            if data['status'] == 'OK':
                result = data['result']
                location = result['geometry']['location']
                details = {
                    'lat': location['lat'],
                    'lng': location['lng'],
                    'name': result['name'],
                    'address': result.get('formatted_address', '')
                }
                # Update cache
                self.cache[place_id] = {
                    'lat': details['lat'],
                    'lng': details['lng'],
                    'name': details['name'],
                    'formatted_address': details['address'],
                    'fetched_at': self._iso_now()
                }
                self._save_cache()
                return details
            else:
                print(f"    [ERROR] Place details failed: {data.get('status', 'Unknown error')}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"    [ERROR] API error getting place details: {e}")
            return None
        except Exception as e:
            print(f"    [ERROR] Unexpected error getting place details: {e}")
            return None
    
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
    
    def find_place_id(self, name, lat, lng, location_context="", state="NY", country="USA", is_city=False, custom_query=None):
        """
        Find Google Maps place ID with improved accuracy
        """
        try:
            # Use custom query if provided, otherwise construct one
            if custom_query:
                query = custom_query
                print(f"    Using custom query: '{query}'")
            else:
                # Create more specific search query
                if is_city:
                    # For cities, use "City Name, NY" format
                    query = f"{name}, {state}"
                else:
                    # For other locations, include context
                    query = f"{name}"
                    if location_context:
                        query += f" {location_context}"
                    query += f", {state}, {country}"
                
                print(f"    Searching: '{query}'")
            
            # Use Places Text Search API
            url = f"{self.base_url}/textsearch/json"
            params = {
                'query': query,
                'location': f"{lat},{lng}",
                'radius': 2000,  # 2km radius for better results
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
                    
                    # For cities, be more lenient with distance (up to 10km)
                    # For other locations, be stricter (up to 3km)
                    max_distance = 10000 if is_city else 3000
                    
                    if distance < max_distance and distance < min_distance:
                        min_distance = distance
                        best_match = result
                
                if best_match:
                    place_id = best_match['place_id']
                    
                    # Check for duplicates
                    if place_id in self.used_place_ids:
                        print(f"    [WARN] Duplicate place ID detected: {place_id}")
                        print(f"    Distance: {min_distance:.0f}m from target")
                        return None
                    
                    self.used_place_ids.add(place_id)
                    print(f"    [OK] Found place ID: {place_id} ({min_distance:.0f}m away)")
                    
                    # Get authoritative coordinates from place details
                    place_details = self.get_place_details(place_id)
                    if place_details:
                        print(f"    [UPDATE] Coordinates: {lat:.6f},{lng:.6f} -> {place_details['lat']:.6f},{place_details['lng']:.6f}")
                        return {
                            'place_id': place_id,
                            'lat': place_details['lat'],
                            'lng': place_details['lng'],
                            'name': place_details['name'],
                            'address': place_details['address']
                        }
                    else:
                        return {
                            'place_id': place_id,
                            'lat': lat,  # Keep original if details fail
                            'lng': lng,
                            'name': name,
                            'address': ''
                        }
                else:
                    print(f"    [ERROR] No suitable match found within {max_distance/1000:.1f}km")
                    return None
            else:
                print(f"    [ERROR] No place found: {data.get('status', 'Unknown error')}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"    [ERROR] API error: {e}")
            return None
        except Exception as e:
            print(f"    [ERROR] Unexpected error: {e}")
            return None
    
    def create_google_maps_url(self, place_id):
        """Create Google Maps URL from place ID"""
        return f"https://www.google.com/maps/place/?q=place_id:{place_id}"
    
    def enrich_dataset(self, file_path, location_context="", state="NY", is_city=False):
        """
        Enrich a dataset with Google Maps place IDs and updated coordinates
        """
        print(f"\nEnriching {file_path}...")
        
        # Read the dataset
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if not isinstance(data, list):
            print(f"  Skipping {file_path} - not a list format")
            return
        
        enriched_count = 0
        updated_coords_count = 0
        skipped_count = 0
        total_count = len(data)
        
        for i, item in enumerate(data):
            name = item.get('name', 'Unknown')
            print(f"  Processing {i+1}/{total_count}: {name}")
            
            place_id = item.get('place_id')
            if place_id:
                # TTL check for verification
                verified_at = item.get('google_verified_at')
                verified_recent = False
                if verified_at:
                    dt = self._parse_iso(verified_at)
                    if dt and datetime.now(timezone.utc) - dt < timedelta(days=self.verify_ttl_days):
                        verified_recent = True

                lat = item.get('lat')
                lng = item.get('lng')
                if verified_recent and lat is not None and lng is not None:
                    print("    ✔ Verified recently, skipping")
                    skipped_count += 1
                else:
                    details = self.get_place_details(place_id)
                    if details:
                        do_update_coords = False
                        if lat is None or lng is None:
                            do_update_coords = True
                        else:
                            drift = self.calculate_distance(lat, lng, details['lat'], details['lng'])
                            if drift > self.distance_threshold_meters:
                                do_update_coords = True
                                print(f"    [DRIFT] {drift:.1f}m > {self.distance_threshold_meters}m -> updating coords")
                        if do_update_coords:
                            item['lat'] = details['lat']
                            item['lng'] = details['lng']
                            updated_coords_count += 1
                            print(f"    [UPDATE] Coordinates set to {details['lat']:.6f},{details['lng']:.6f}")
                        item['google_verified_lat'] = details['lat']
                        item['google_verified_lng'] = details['lng']
                        if details.get('address'):
                            item['formatted_address'] = details['address']
                        item['google_verified_at'] = self._iso_now()
                        item['google_place_source'] = 'places_details_v1'
                        enriched_count += 1
                    else:
                        print("    [WARN] Failed to fetch details for existing place_id")
                        skipped_count += 1
                time.sleep(self.rate_limit_delay)
                continue

            # No place_id -> attempt to find one (existing behavior)
            lat = item.get('lat')
            lng = item.get('lng')
            if lat is None or lng is None:
                print(f"    No coordinates found, skipping")
                skipped_count += 1
                continue
            custom_query = item.get('place_query')
            result = self.find_place_id(
                name,
                lat,
                lng,
                location_context,
                state,
                is_city=is_city,
                custom_query=custom_query
            )
            if result:
                item['place_id'] = result['place_id']
                item['google_maps_url'] = self.create_google_maps_url(result['place_id'])
                if abs(result['lat'] - lat) > 0.0001 or abs(result['lng'] - lng) > 0.0001:
                    item['lat'] = result['lat']
                    item['lng'] = result['lng']
                    updated_coords_count += 1
                    print(f"    [UPDATE] Updated coordinates for {name}")
                item['google_verified_lat'] = item['lat']
                item['google_verified_lng'] = item['lng']
                item['google_verified_at'] = self._iso_now()
                item['google_place_source'] = 'places_details_v1'
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
        print(f"  [UPDATE] Updated coordinates for {updated_coords_count} items")
        print(f"  [WARN] Skipped {skipped_count} items")
    
    def enrich_cities_from_map_data(self, file_path):
        """
        Enrich cities from the main map-data.json file with improved city search
        """
        print(f"\nEnriching cities from {file_path}...")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        cities = data.get('cities', [])
        if not cities:
            print("  No cities found in map-data.json")
            return
        
        enriched_count = 0
        updated_coords_count = 0
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
            
            # Check for custom place query in the city object
            custom_query = city.get('place_query')
            
            # Find place ID with city-specific search
            result = self.find_place_id(
                name, 
                lat, 
                lng, 
                "",  # No additional context for cities
                "NY",
                is_city=True,  # Use city-specific search
                custom_query=custom_query
            )
            
            if result:
                # Update with place ID and Google Maps URL
                city['place_id'] = result['place_id']
                city['google_maps_url'] = self.create_google_maps_url(result['place_id'])
                
                # Update coordinates if they changed significantly
                if abs(result['lat'] - lat) > 0.0001 or abs(result['lng'] - lng) > 0.0001:
                    city['coordinates'] = [result['lat'], result['lng']]
                    updated_coords_count += 1
                    print(f"    [UPDATE] Updated coordinates for {name}")
                
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
        print(f"  [UPDATE] Updated coordinates for {updated_coords_count} cities")
        print(f"  [WARN] Skipped {skipped_count} cities")
    
    def run(self):
        """
        Run the improved enrichment process for all datasets
        """
        print("Improved Google Maps Place ID Enrichment Script")
        print("=" * 60)
        print("Key improvements:")
        print("- Updates coordinates from Google Places API (source of truth)")
        print("- Better city search queries ('City Name, NY')")
        print("- Coordinate validation and correction")
        print("- Duplicate place ID prevention")
        print("- More lenient distance matching for cities")
        print("=" * 60)
        
        # Define data directory
        data_dir = Path(__file__).parent.parent / "public" / "data"
        
        # List of datasets to enrich
        datasets = [
            ("waterfalls.json", "waterfall", False),
            ("breweries.json", "brewery", False),
            ("restaurants.json", "restaurant", False),
            # Consolidated PYO farms dataset
            ("pyo-fruit-farms.json", "farm", False),
            # Enabled additional datasets
            ("points_of_interest.json", "poi", False),
            ("children.json", "children", False),
            # Note: our-airbnbs.json intentionally excluded per request
        ]
        
        # Enrich individual datasets
        for filename, context, is_city in datasets:
            file_path = data_dir / filename
            if file_path.exists():
                self.enrich_dataset(file_path, context, is_city=is_city)
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
        print("3. Verify coordinates are more accurate")

if __name__ == "__main__":
    try:
        enricher = ImprovedGoogleMapsEnricher()
        enricher.run()
    except ValueError as e:
        print(f"[ERROR] Error: {e}")
        print("\nPlease set your Google Maps API key:")
        print("1. Create a .env file in the scripts directory")
        print("2. Add: GOOGLE_MAPS_API_KEY=your_api_key_here")
        print("3. Or set the environment variable directly")
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
