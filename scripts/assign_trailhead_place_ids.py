#!/usr/bin/env python3
"""
Script to assign Google Place IDs to trailheads data with nested structure.
"""

import json
import os
import time
import requests
from typing import Dict, List, Optional, Tuple
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('trailhead_place_id_assignment.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class TrailheadPlaceIDAssigner:
    def __init__(self, api_key: str, data_dir: str = "public/data"):
        self.api_key = api_key
        self.data_dir = Path(data_dir)
        self.base_url = "https://maps.googleapis.com/maps/api/place"
        self.session = requests.Session()
        self.rate_limit_delay = 0.1  # 100ms between requests
        self.max_retries = 3

    def search_place(self, name: str, location: str = None, lat: float = None, lng: float = None) -> Optional[Dict]:
        """
        Search for a place using Google Places API.
        """
        # Build search query
        query_parts = [name]
        if location:
            query_parts.append(location)
        
        query = " ".join(query_parts)
        
        # Add location bias if coordinates are available
        location_bias = None
        if lat is not None and lng is not None:
            location_bias = f"point:{lat},{lng}"
        
        params = {
            'query': query,
            'key': self.api_key,
            'fields': 'place_id,formatted_address,name,geometry'
        }
        
        if location_bias:
            params['locationbias'] = location_bias
        
        for attempt in range(self.max_retries):
            try:
                response = self.session.get(f"{self.base_url}/textsearch/json", params=params)
                response.raise_for_status()
                
                data = response.json()
                
                if data.get('status') == 'OK' and data.get('results'):
                    result = data['results'][0]  # Take the first result
                    place_id = result.get('place_id')
                    formatted_address = result.get('formatted_address')
                    
                    if place_id:
                        google_maps_url = f"https://www.google.com/maps/place/?q=place_id:{place_id}"
                        return {
                            'place_id': place_id,
                            'formatted_address': formatted_address,
                            'google_maps_url': google_maps_url
                        }
                
                logger.warning(f"API returned status: {data.get('status')} for query: {query}")
                return None
                
            except requests.exceptions.RequestException as e:
                logger.warning(f"Request failed (attempt {attempt + 1}/{self.max_retries}): {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    logger.error(f"All retry attempts failed for query: {query}")
                    return None
        
        return None

    def process_trailheads_file(self, file_path: Path) -> Tuple[int, int]:
        """
        Process trailheads JSON file with nested structure.
        """
        logger.info(f"Processing file: {file_path}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            logger.error(f"Failed to load {file_path}: {e}")
            return 0, 0
        
        if not isinstance(data, list):
            logger.error(f"Expected list structure in {file_path}")
            return 0, 0
        
        successful_updates = 0
        total_entries = 0
        
        # Process each region
        for region_idx, region in enumerate(data):
            if not isinstance(region, dict) or 'trails' not in region:
                continue
                
            region_name = region.get('region', f'Region {region_idx + 1}')
            trails = region.get('trails', [])
            
            logger.info(f"Processing region: {region_name} with {len(trails)} trails")
            
            # Process each trail in the region
            for trail_idx, trail in enumerate(trails):
                if not isinstance(trail, dict):
                    continue
                    
                total_entries += 1
                
                # Skip if place_id already exists and is not null
                if trail.get('place_id') and trail.get('place_id') != 'null':
                    logger.info(f"Trail {trail_idx+1} in {region_name} already has place_id: {trail.get('place_id')}")
                    continue
                
                # Extract location information
                name = trail.get('name', '')
                location = trail.get('location', '')
                lat = trail.get('lat')
                lng = trail.get('lng')
                place_query = trail.get('place_query', '')
                
                if not name:
                    logger.warning(f"Trail {trail_idx+1} in {region_name} has no name, skipping")
                    continue
                
                # Use place_query if available, otherwise use name + location
                search_query = place_query if place_query else f"{name} {location}".strip()
                
                logger.info(f"Searching for trail: {name} in {region_name}")
                logger.info(f"Search query: {search_query}")
                
                # Search for the place
                place_info = self.search_place(name, location, lat, lng)
                
                if place_info:
                    # Update the trail entry
                    trail['place_id'] = place_info['place_id']
                    trail['google_maps_url'] = place_info['google_maps_url']
                    
                    # Update formatted address if available
                    if place_info.get('formatted_address'):
                        trail['formatted_address'] = place_info['formatted_address']
                    
                    successful_updates += 1
                    logger.info(f"✓ Updated trail {trail_idx+1} in {region_name}: {name} -> {place_info['place_id']}")
                else:
                    logger.warning(f"✗ Failed to find place_id for trail: {name} in {region_name}")
                
                # Rate limiting
                time.sleep(self.rate_limit_delay)
        
        # Save the updated file
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            logger.info(f"Saved updated file: {file_path}")
        except Exception as e:
            logger.error(f"Failed to save {file_path}: {e}")
            return successful_updates, total_entries
        
        return successful_updates, total_entries

def main():
    """Main function to run trailhead place ID assignment."""
    
    # Get API key from environment variable or .env file
    api_key = os.getenv('GOOGLE_PLACES_API_KEY') or os.getenv('GOOGLE_MAPS_API_KEY')
    
    if not api_key:
        # Try to load from .env file
        env_file = Path(__file__).parent / '.env'
        if env_file.exists():
            with open(env_file, 'r') as f:
                for line in f:
                    if line.startswith('GOOGLE_MAPS_API_KEY='):
                        api_key = line.split('=', 1)[1].strip()
                        break
    
    if not api_key:
        print("Google Places API key not found!")
        print("Please set GOOGLE_PLACES_API_KEY or GOOGLE_MAPS_API_KEY environment variable")
        print("Or create a .env file with: GOOGLE_MAPS_API_KEY=your_api_key_here")
        return
    
    # Set up paths
    script_dir = Path(__file__).parent
    data_dir = script_dir.parent / "public" / "data"
    
    if not data_dir.exists():
        print(f"Data directory not found: {data_dir}")
        return
    
    print(f"Using data directory: {data_dir}")
    print(f"API key: {api_key[:10]}...{api_key[-4:] if len(api_key) > 14 else '***'}")
    
    # Create assigner and process trailheads
    assigner = TrailheadPlaceIDAssigner(api_key, str(data_dir))
    
    trailheads_file = data_dir / "trail-heads.json"
    if not trailheads_file.exists():
        print(f"Trailheads file not found: {trailheads_file}")
        return
    
    # Process trailheads file
    successful, total = assigner.process_trailheads_file(trailheads_file)
    
    # Print summary
    print("\n" + "="*50)
    print("TRAILHEAD PLACE ID ASSIGNMENT SUMMARY")
    print("="*50)
    print(f"trail-heads.json: {successful}/{total} successful")
    
    if total > 0:
        success_rate = (successful / total) * 100
        print(f"Success rate: {success_rate:.1f}%")
    
    print("="*50)

if __name__ == "__main__":
    main()
