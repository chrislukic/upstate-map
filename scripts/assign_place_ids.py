#!/usr/bin/env python3
"""
Script to assign accurate place IDs to JSON data files using Google Places API.

This script will:
1. Read JSON files from the data directory
2. Use Google Places API to find place IDs for each location
3. Update the JSON files with accurate place IDs and Google Maps URLs
4. Handle rate limiting and API quotas
5. Provide detailed logging of the process

Requirements:
- Google Places API key
- requests library
- json library
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
        logging.FileHandler('place_id_assignment.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class PlaceIDAssigner:
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
        
        Args:
            name: Name of the place
            location: Address or location string
            lat: Latitude (optional)
            lng: Longitude (optional)
            
        Returns:
            Dict with place_id, formatted_address, and google_maps_url, or None if not found
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
                response = self.session.get(
                    f"{self.base_url}/textsearch/json",
                    params=params,
                    timeout=10
                )
                response.raise_for_status()
                
                data = response.json()
                
                if data.get('status') == 'OK' and data.get('results'):
                    result = data['results'][0]  # Take the first result
                    place_id = result.get('place_id')
                    formatted_address = result.get('formatted_address')
                    
                    if place_id:
                        return {
                            'place_id': place_id,
                            'formatted_address': formatted_address,
                            'google_maps_url': f"https://www.google.com/maps/place/?q=place_id:{place_id}",
                            'name': result.get('name', name)
                        }
                
                elif data.get('status') == 'ZERO_RESULTS':
                    logger.warning(f"No results found for: {query}")
                    return None
                    
                elif data.get('status') == 'OVER_QUERY_LIMIT':
                    logger.error("API quota exceeded")
                    return None
                    
                else:
                    logger.warning(f"API returned status: {data.get('status')} for query: {query}")
                    return None
                    
            except requests.exceptions.RequestException as e:
                logger.error(f"Request failed (attempt {attempt + 1}): {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    return None
        
        return None
    
    def process_json_file(self, file_path: Path) -> Tuple[int, int]:
        """
        Process a single JSON file to assign place IDs.
        
        Returns:
            Tuple of (successful_updates, total_entries)
        """
        logger.info(f"Processing file: {file_path}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            logger.error(f"Failed to read {file_path}: {e}")
            return 0, 0
        
        if not isinstance(data, list):
            logger.warning(f"File {file_path} does not contain a list, skipping")
            return 0, 0
        
        successful_updates = 0
        total_entries = len(data)
        
        for i, entry in enumerate(data):
            if not isinstance(entry, dict):
                continue
                
            # Skip if place_id already exists and is not null
            if entry.get('place_id') and entry.get('place_id') != 'null':
                logger.info(f"Entry {i+1} already has place_id: {entry.get('place_id')}")
                continue
            
            # Extract location information
            name = entry.get('name', '')
            location = entry.get('location') or entry.get('address', '')
            lat = entry.get('lat')
            lng = entry.get('lng')
            
            if not name:
                logger.warning(f"Entry {i+1} has no name, skipping")
                continue
            
            logger.info(f"Searching for place: {name} in {location}")
            
            # Search for the place
            place_info = self.search_place(name, location, lat, lng)
            
            if place_info:
                # Update the entry
                entry['place_id'] = place_info['place_id']
                entry['google_maps_url'] = place_info['google_maps_url']
                
                # Update formatted address if available
                if place_info.get('formatted_address'):
                    entry['formatted_address'] = place_info['formatted_address']
                
                successful_updates += 1
                logger.info(f"✓ Updated entry {i+1}: {name} -> {place_info['place_id']}")
            else:
                logger.warning(f"✗ Failed to find place_id for: {name}")
            
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
    
    def process_all_files(self, file_patterns: List[str] = None) -> Dict[str, Tuple[int, int]]:
        """
        Process all JSON files in the data directory.
        
        Args:
            file_patterns: List of file patterns to process (e.g., ['*.json'])
            
        Returns:
            Dict mapping filename to (successful_updates, total_entries)
        """
        if file_patterns is None:
            file_patterns = ['*.json']
        
        results = {}
        
        for pattern in file_patterns:
            for file_path in self.data_dir.glob(pattern):
                if file_path.is_file():
                    logger.info(f"Processing {file_path.name}")
                    successful, total = self.process_json_file(file_path)
                    results[file_path.name] = (successful, total)
                    logger.info(f"Completed {file_path.name}: {successful}/{total} successful")
        
        return results

def main():
    """Main function to run the place ID assignment script."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Assign place IDs to JSON data files')
    parser.add_argument('--api-key', required=True, help='Google Places API key')
    parser.add_argument('--data-dir', default='public/data', help='Directory containing JSON files')
    parser.add_argument('--files', nargs='*', help='Specific files to process (default: all JSON files)')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be done without making changes')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.data_dir):
        logger.error(f"Data directory does not exist: {args.data_dir}")
        return
    
    assigner = PlaceIDAssigner(args.api_key, args.data_dir)
    
    if args.dry_run:
        logger.info("DRY RUN MODE - No changes will be made")
        # TODO: Implement dry run functionality
        return
    
    # Process files
    if args.files:
        # Process specific files
        for filename in args.files:
            file_path = Path(args.data_dir) / filename
            if file_path.exists():
                successful, total = assigner.process_json_file(file_path)
                logger.info(f"Processed {filename}: {successful}/{total} successful")
            else:
                logger.error(f"File not found: {file_path}")
    else:
        # Process all JSON files
        results = assigner.process_all_files()
        
        # Print summary
        logger.info("\n" + "="*50)
        logger.info("SUMMARY")
        logger.info("="*50)
        
        total_successful = 0
        total_entries = 0
        
        for filename, (successful, total) in results.items():
            logger.info(f"{filename}: {successful}/{total} successful")
            total_successful += successful
            total_entries += total
        
        logger.info(f"\nOverall: {total_successful}/{total_entries} successful")
        logger.info(f"Success rate: {total_successful/total_entries*100:.1f}%" if total_entries > 0 else "No entries processed")

if __name__ == "__main__":
    main()
