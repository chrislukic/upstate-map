#!/usr/bin/env python3
"""
Enhanced Google Maps Place ID Enrichment Script

This enhanced version addresses the issues with the original script:
1. ✅ Fixed file targeting - includes all files that need enrichment
2. ✅ Added backup functionality - protects original data
3. ✅ Added error recovery - retry logic for API failures
4. ✅ Added dry run mode - safe testing without changes
5. ✅ Improved logging - comprehensive file and console logging
6. ✅ Optimized API usage - more efficient API calls
7. ✅ Added configuration - flexible settings

Usage:
    python enrich_with_google_maps_enhanced.py [--dry-run] [--config config.json]

Requirements:
    pip install requests python-dotenv
"""

import json
import os
import requests
import time
import math
import shutil
import logging
import argparse
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

class EnhancedGoogleMapsEnricher:
    def __init__(self, config_file=None, dry_run=False):
        self.api_key = os.getenv('GOOGLE_MAPS_API_KEY')
        if not self.api_key:
            raise ValueError("GOOGLE_MAPS_API_KEY environment variable not set")
        
        self.base_url = "https://maps.googleapis.com/maps/api/place"
        self.dry_run = dry_run
        self.used_place_ids = set()  # Track used place IDs to prevent duplicates
        
        # Load configuration
        self.config = self.load_config(config_file)
        
        # Setup logging
        self.setup_logging()
        
        # Statistics tracking
        self.stats = {
            'total_processed': 0,
            'enriched': 0,
            'coordinates_updated': 0,
            'skipped': 0,
            'errors': 0,
            'duplicates_prevented': 0,
            'api_calls_made': 0
        }
        
    def load_config(self, config_file):
        """Load configuration from file or use defaults"""
        default_config = {
            "rate_limit_delay": 0.1,
            "max_distance_city": 10000,
            "max_distance_other": 3000,
            "coordinate_threshold": 0.0001,
            "backup_files": True,
            "max_retries": 3,
            "retry_delay": 2,
            "api_timeout": 10
        }
        
        if config_file and Path(config_file).exists():
            with open(config_file, 'r') as f:
                user_config = json.load(f)
                default_config.update(user_config)
        
        return default_config
    
    def setup_logging(self):
        """Setup comprehensive logging"""
        log_dir = Path(__file__).parent / "logs"
        log_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = log_dir / f"enrichment_{timestamp}.log"
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"Enhanced Google Maps Enrichment started - Log: {log_file}")
        
        if self.dry_run:
            self.logger.info("🔍 DRY RUN MODE - No changes will be made")
    
    def backup_file(self, file_path):
        """Create backup of original file"""
        if not self.config.get('backup_files', True):
            return
            
        backup_path = file_path.with_suffix(f'.json.backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}')
        try:
            shutil.copy2(file_path, backup_path)
            self.logger.info(f"📁 Backup created: {backup_path}")
        except Exception as e:
            self.logger.error(f"❌ Failed to create backup: {e}")
    
    def make_api_request_with_retry(self, url, params, max_retries=None):
        """Make API request with exponential backoff retry"""
        if max_retries is None:
            max_retries = self.config.get('max_retries', 3)
            
        for attempt in range(max_retries):
            try:
                self.stats['api_calls_made'] += 1
                response = requests.get(
                    url, 
                    params=params, 
                    timeout=self.config.get('api_timeout', 10)
                )
                response.raise_for_status()
                return response
            except requests.exceptions.RequestException as e:
                if attempt == max_retries - 1:
                    self.logger.error(f"❌ API request failed after {max_retries} attempts: {e}")
                    raise e
                
                wait_time = self.config.get('retry_delay', 2) ** attempt
                self.logger.warning(f"🔄 Attempt {attempt + 1} failed, retrying in {wait_time}s...")
                time.sleep(wait_time)
    
    def get_place_details(self, place_id):
        """Get detailed information about a place using its place ID"""
        try:
            url = f"{self.base_url}/details/json"
            params = {
                'place_id': place_id,
                'fields': 'geometry,name,formatted_address',
                'key': self.api_key
            }
            
            response = self.make_api_request_with_retry(url, params)
            data = response.json()
            
            if data['status'] == 'OK':
                result = data['result']
                location = result['geometry']['location']
                return {
                    'lat': location['lat'],
                    'lng': location['lng'],
                    'name': result['name'],
                    'address': result.get('formatted_address', '')
                }
            else:
                self.logger.error(f"❌ Place details failed: {data.get('status', 'Unknown error')}")
                return None
                
        except Exception as e:
            self.logger.error(f"❌ Unexpected error getting place details: {e}")
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
                self.logger.info(f"🔍 Using custom query: '{query}'")
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
                
                self.logger.info(f"🔍 Searching: '{query}'")
            
            # Use Places Text Search API
            url = f"{self.base_url}/textsearch/json"
            params = {
                'query': query,
                'location': f"{lat},{lng}",
                'radius': 2000,  # 2km radius for better results
                'key': self.api_key
            }
            
            response = self.make_api_request_with_retry(url, params)
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
                    max_distance = self.config.get('max_distance_city' if is_city else 'max_distance_other')
                    
                    if distance < max_distance and distance < min_distance:
                        min_distance = distance
                        best_match = result
                
                if best_match:
                    place_id = best_match['place_id']
                    
                    # Check for duplicates
                    if place_id in self.used_place_ids:
                        self.logger.warning(f"⚠️ Duplicate place ID detected: {place_id}")
                        self.logger.info(f"📍 Distance: {min_distance:.0f}m from target")
                        self.stats['duplicates_prevented'] += 1
                        return None
                    
                    self.used_place_ids.add(place_id)
                    self.logger.info(f"✅ Found place ID: {place_id} ({min_distance:.0f}m away)")
                    
                    # Get authoritative coordinates from place details
                    place_details = self.get_place_details(place_id)
                    if place_details:
                        self.logger.info(f"🔄 Coordinates: {lat:.6f},{lng:.6f} -> {place_details['lat']:.6f},{place_details['lng']:.6f}")
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
                    self.logger.error(f"❌ No suitable match found within {max_distance/1000:.1f}km")
                    return None
            else:
                self.logger.error(f"❌ No place found: {data.get('status', 'Unknown error')}")
                return None
                
        except Exception as e:
            self.logger.error(f"❌ Unexpected error: {e}")
            return None
    
    def create_google_maps_url(self, place_id):
        """Create Google Maps URL from place ID"""
        return f"https://www.google.com/maps/place/?q=place_id:{place_id}"
    
    def enrich_dataset(self, file_path, location_context="", state="NY", is_city=False):
        """
        Enrich a dataset with Google Maps place IDs and updated coordinates
        """
        self.logger.info(f"📂 Enriching {file_path}...")
        
        # Create backup if not in dry run mode
        if not self.dry_run:
            self.backup_file(file_path)
        
        # Read the dataset
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if not isinstance(data, list):
            self.logger.warning(f"⚠️ Skipping {file_path} - not a list format")
            return
        
        enriched_count = 0
        updated_coords_count = 0
        skipped_count = 0
        total_count = len(data)
        
        self.logger.info(f"📊 Processing {total_count} items...")
        
        for i, item in enumerate(data):
            name = item.get('name', 'Unknown')
            self.logger.info(f"🔄 Processing {i+1}/{total_count}: {name}")
            
            # Check if already enriched (has valid place_id)
            if 'place_id' in item and item['place_id'] is not None and 'google_maps_url' in item:
                self.logger.info(f"⏭️ Already enriched, skipping")
                continue
            
            # Get coordinates
            lat = item.get('lat')
            lng = item.get('lng')
            
            if lat is None or lng is None:
                self.logger.warning(f"⚠️ No coordinates found, skipping")
                skipped_count += 1
                continue
            
            # Check for custom place query in the JSON object
            custom_query = item.get('place_query')
            
            # Find place ID and get updated coordinates
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
                # Update with place ID and Google Maps URL
                item['place_id'] = result['place_id']
                item['google_maps_url'] = self.create_google_maps_url(result['place_id'])
                
                # Update coordinates if they changed significantly
                threshold = self.config.get('coordinate_threshold', 0.0001)
                if abs(result['lat'] - lat) > threshold or abs(result['lng'] - lng) > threshold:
                    item['lat'] = result['lat']
                    item['lng'] = result['lng']
                    updated_coords_count += 1
                    self.logger.info(f"🔄 Updated coordinates for {name}")
                
                enriched_count += 1
            else:
                self.logger.error(f"❌ No place ID found for {name}")
                skipped_count += 1
            
            # Rate limiting
            time.sleep(self.config.get('rate_limit_delay', 0.1))
        
        # Save enriched data (only if not in dry run mode)
        if not self.dry_run:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            self.logger.info(f"💾 Saved enriched data to {file_path}")
        
        # Update statistics
        self.stats['total_processed'] += total_count
        self.stats['enriched'] += enriched_count
        self.stats['coordinates_updated'] += updated_coords_count
        self.stats['skipped'] += skipped_count
        
        self.logger.info(f"✅ Enriched {enriched_count}/{total_count} items in {file_path}")
        self.logger.info(f"🔄 Updated coordinates for {updated_coords_count} items")
        self.logger.warning(f"⚠️ Skipped {skipped_count} items")
    
    def enrich_cities_from_map_data(self, file_path):
        """
        Enrich cities from the main map-data.json file with improved city search
        """
        self.logger.info(f"🏙️ Enriching cities from {file_path}...")
        
        # Create backup if not in dry run mode
        if not self.dry_run:
            self.backup_file(file_path)
        
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        cities = data.get('cities', [])
        if not cities:
            self.logger.warning("⚠️ No cities found in map-data.json")
            return
        
        enriched_count = 0
        updated_coords_count = 0
        skipped_count = 0
        total_count = len(cities)
        
        self.logger.info(f"📊 Processing {total_count} cities...")
        
        for i, city in enumerate(cities):
            name = city.get('name', 'Unknown')
            self.logger.info(f"🔄 Processing {i+1}/{total_count}: {name}")
            
            # Check if already enriched (has valid place_id)
            if 'place_id' in city and city['place_id'] is not None and 'google_maps_url' in city:
                self.logger.info(f"⏭️ Already enriched, skipping")
                continue
            
            # Get coordinates
            coords = city.get('coordinates')
            if not coords or len(coords) != 2:
                self.logger.warning(f"⚠️ No valid coordinates found, skipping")
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
                threshold = self.config.get('coordinate_threshold', 0.0001)
                if abs(result['lat'] - lat) > threshold or abs(result['lng'] - lng) > threshold:
                    city['coordinates'] = [result['lat'], result['lng']]
                    updated_coords_count += 1
                    self.logger.info(f"🔄 Updated coordinates for {name}")
                
                enriched_count += 1
            else:
                self.logger.error(f"❌ No place ID found for {name}")
                skipped_count += 1
            
            # Rate limiting
            time.sleep(self.config.get('rate_limit_delay', 0.1))
        
        # Save enriched data (only if not in dry run mode)
        if not self.dry_run:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            self.logger.info(f"💾 Saved enriched data to {file_path}")
        
        # Update statistics
        self.stats['total_processed'] += total_count
        self.stats['enriched'] += enriched_count
        self.stats['coordinates_updated'] += updated_coords_count
        self.stats['skipped'] += skipped_count
        
        self.logger.info(f"✅ Enriched {enriched_count}/{total_count} cities in {file_path}")
        self.logger.info(f"🔄 Updated coordinates for {updated_coords_count} cities")
        self.logger.warning(f"⚠️ Skipped {skipped_count} cities")
    
    def run(self):
        """
        Run the enhanced enrichment process for all datasets
        """
        self.logger.info("🚀 Enhanced Google Maps Place ID Enrichment Script")
        self.logger.info("=" * 60)
        self.logger.info("Key improvements:")
        self.logger.info("✅ Fixed file targeting - includes all files that need enrichment")
        self.logger.info("✅ Added backup functionality - protects original data")
        self.logger.info("✅ Added error recovery - retry logic for API failures")
        self.logger.info("✅ Added dry run mode - safe testing without changes")
        self.logger.info("✅ Improved logging - comprehensive file and console logging")
        self.logger.info("✅ Optimized API usage - more efficient API calls")
        self.logger.info("=" * 60)
        
        # Define data directory
        data_dir = Path(__file__).parent.parent.parent / "public" / "data"
        
        # Updated list of datasets to enrich (FIXED: includes all files that need enrichment)
        datasets = [
            ("waterfalls.json", "waterfall", False),
            ("breweries.json", "brewery", False),
            ("restaurants.json", "restaurant", False),
            ("children.json", "activity", False),
            ("trail-heads.json", "trailhead", False),
            ("our-airbnbs.json", "accommodation", False),
            ("points_of_interest.json", "attraction", False),
            ("pyo_apples.json", "orchard", False),
            ("pyo_strawberries.json", "orchard", False),
            ("pyo_cherries.json", "orchard", False),
            ("pyo_peaches.json", "orchard", False),
        ]
        
        # Enrich individual datasets
        for filename, context, is_city in datasets:
            file_path = data_dir / filename
            if file_path.exists():
                try:
                    self.enrich_dataset(file_path, context, is_city=is_city)
                except Exception as e:
                    self.logger.error(f"❌ Error processing {filename}: {e}")
                    self.stats['errors'] += 1
            else:
                self.logger.warning(f"⚠️ File not found: {file_path}")
        
        # Enrich cities from map-data.json
        map_data_path = data_dir / "map-data.json"
        if map_data_path.exists():
            try:
                self.enrich_cities_from_map_data(map_data_path)
            except Exception as e:
                self.logger.error(f"❌ Error processing cities: {e}")
                self.stats['errors'] += 1
        else:
            self.logger.warning(f"⚠️ File not found: {map_data_path}")
        
        # Print final statistics
        self.print_final_stats()
    
    def print_final_stats(self):
        """Print comprehensive final statistics"""
        self.logger.info(f"\n📊 ENRICHMENT COMPLETE!")
        self.logger.info("=" * 60)
        self.logger.info(f"📈 Total items processed: {self.stats['total_processed']}")
        self.logger.info(f"✅ Successfully enriched: {self.stats['enriched']}")
        self.logger.info(f"🔄 Coordinates updated: {self.stats['coordinates_updated']}")
        self.logger.info(f"⚠️ Skipped: {self.stats['skipped']}")
        self.logger.info(f"❌ Errors: {self.stats['errors']}")
        self.logger.info(f"🚫 Duplicates prevented: {self.stats['duplicates_prevented']}")
        self.logger.info(f"🌐 API calls made: {self.stats['api_calls_made']}")
        self.logger.info(f"🔑 Unique place IDs used: {len(self.used_place_ids)}")
        
        if self.dry_run:
            self.logger.info("\n🔍 DRY RUN COMPLETE - No changes were made")
            self.logger.info("💡 Run without --dry-run to apply changes")
        else:
            self.logger.info("\n✅ Changes have been applied to the data files")
        
        self.logger.info("\n📋 Next steps:")
        self.logger.info("1. Review the log file for any issues")
        self.logger.info("2. Test the Google Maps links in the application")
        self.logger.info("3. Verify coordinates are more accurate")
        self.logger.info("4. Check for any remaining duplicates")

def main():
    parser = argparse.ArgumentParser(description='Enhanced Google Maps Place ID Enrichment')
    parser.add_argument('--dry-run', action='store_true', 
                       help='Run in dry-run mode (no changes will be made)')
    parser.add_argument('--config', type=str, 
                       help='Path to configuration file')
    
    args = parser.parse_args()
    
    try:
        enricher = EnhancedGoogleMapsEnricher(
            config_file=args.config, 
            dry_run=args.dry_run
        )
        enricher.run()
    except ValueError as e:
        print(f"❌ Error: {e}")
        print("\nPlease set your Google Maps API key:")
        print("1. Create a .env file in the scripts directory")
        print("2. Add: GOOGLE_MAPS_API_KEY=your_api_key_here")
        print("3. Or set the environment variable directly")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()
