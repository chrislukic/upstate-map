#!/usr/bin/env python3
"""
Geocode events from events.json using Google Maps Geocoding API
Adds lat/lng coordinates to each event for map display
"""

import json
import os
import sys
import time
from typing import Dict, List, Optional, Tuple
from pathlib import Path

# Add the scripts directory to the path so we can import from config
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Import shared configuration loader
from config.loader import load_script_config, setup_logging, validate_environment, get_api_key

# Configuration will be loaded in main()

def geocode_address(address: str, api_key: str, config: Dict) -> Optional[Tuple[float, float]]:
    """
    Geocode an address using Google Maps Geocoding API
    
    Args:
        address: The address to geocode
        api_key: Google Maps API key
        config: Configuration dictionary
        
    Returns:
        Tuple of (latitude, longitude) or None if geocoding failed
    """
    import requests
    
    # Get configuration values
    geocoding_config = config.get("geocoding", {})
    timeout = geocoding_config.get("timeout", 20)
    geocoding_endpoint = config.get("api", {}).get("google_maps", {}).get("geocoding_endpoint", 
                                                                          "https://maps.googleapis.com/maps/api/geocode/json")
    
    params = {
        'address': address,
        'key': api_key,
        'region': 'us'
    }
    
    try:
        print(f"Geocoding: {address}")
        response = requests.get(geocoding_endpoint, params=params, timeout=timeout)
        response.raise_for_status()
        data = response.json()
        
        if data.get('status') == 'OK' and data.get('results'):
            result = data['results'][0]
            location = result['geometry']['location']
            lat = float(location['lat'])
            lng = float(location['lng'])
            formatted_address = result.get('formatted_address', 'Unknown')
            print(f"  → Found: {formatted_address}")
            print(f"  → Coordinates: {lat}, {lng}")
            return (lat, lng)
        else:
            print(f"  → Geocoding failed: {data.get('status', 'Unknown error')}")
            if 'error_message' in data:
                print(f"  → Error: {data['error_message']}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"  → Request error: {e}")
        return None
    except Exception as e:
        print(f"  → Unexpected error: {e}")
        return None

def geocode_events(events_data: Dict, api_key: str, config: Dict) -> Dict:
    """
    Geocode all events in the events data using Google Maps Geocoding API
    
    Args:
        events_data: The events JSON data
        api_key: Google Maps API key
        config: Configuration dictionary
        
    Returns:
        Updated events data with coordinates added
    """
    updated_events = events_data.copy()
    updated_events['events'] = []
    
    # Get rate limiting configuration
    geocoding_config = config.get("geocoding", {})
    base_delay = geocoding_config.get("rate_limit_delay", 0.15)
    progressive_delays = geocoding_config.get("progressive_delays", {})
    
    for i, event in enumerate(events_data['events']):
        print(f"\nProcessing event {i+1}/{len(events_data['events'])}: {event['name']}")
        
        # Create a copy of the event
        updated_event = event.copy()
        
        # Geocode the address
        coords = geocode_address(event['address'], api_key, config)
        
        if coords:
            updated_event['lat'] = coords[0]
            updated_event['lng'] = coords[1]
            updated_event['geocoded'] = True
            print(f"  ✅ Successfully geocoded")
        else:
            updated_event['geocoded'] = False
            print(f"  ❌ Failed to geocode")
        
        updated_events['events'].append(updated_event)
        
        # Progressive rate limiting based on configuration
        delay = base_delay
        if i >= 10 and "after_10" in progressive_delays:
            delay = progressive_delays["after_10"]
        elif i >= 5 and "after_5" in progressive_delays:
            delay = progressive_delays["after_5"]
        
        time.sleep(delay)
    
    return updated_events

def main():
    """Main function to geocode events using Google Maps Geocoding API"""
    print("🎪 Event Geocoding Script (Google Maps)")
    print("=" * 50)

    # Load configuration using centralized system
    config = load_script_config('utilities', __file__)
    
    # Setup logging
    logger = setup_logging(config, Path(__file__).stem)
    
    # Validate environment
    if not validate_environment(['GOOGLE_MAPS_API_KEY']):
        logger.error("Missing required environment variables")
        return 1
    
    # Get API key using centralized system
    api_key = get_api_key('google_maps')
    if not api_key:
        logger.error("Google Maps API key not found!")
        print("Please set GOOGLE_MAPS_API_KEY environment variable.")
        return 1
    print(f"✅ API key loaded (ends with: ...{api_key[-4:]})")
    
    # Get file paths from configuration
    data_dir = Path(config.get("file_paths", {}).get("data_dir", "../../public/data"))
    events_file = data_dir / "events.json"
    
    if not events_file.exists():
        logger.error(f"Events file not found at {events_file}")
        return 1
    
    try:
        with open(events_file, 'r', encoding='utf-8') as f:
            events_data = json.load(f)
        logger.info(f"Loaded {len(events_data['events'])} events from {events_file}")
    except Exception as e:
        logger.error(f"Error loading events file: {e}")
        return 1
    
    # Check if events are already geocoded
    already_geocoded = all('lat' in event and 'lng' in event for event in events_data['events'])
    if already_geocoded:
        logger.info("Events appear to already be geocoded. Re-geocoding anyway...")
    
    # Geocode events
    logger.info("Starting geocoding process...")
    updated_events = geocode_events(events_data, api_key, config)
    
    # Count successful geocodings
    successful = sum(1 for event in updated_events['events'] if event.get('geocoded', False))
    total = len(updated_events['events'])
    
    print(f"\n📊 Geocoding Results:")
    print(f"  ✅ Successful: {successful}/{total}")
    print(f"  ❌ Failed: {total - successful}/{total}")
    
    # Save updated events
    try:
        # Create backup if configured (store in central ./backups directory)
        if config.get("data_processing", {}).get("backup_before_changes", True):
            from datetime import datetime
            repo_root = Path(__file__).resolve().parents[2]
            backups_dir = repo_root / 'backups'
            backups_dir.mkdir(parents=True, exist_ok=True)
            ts = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_file = backups_dir / f"{events_file.name}.backup_{ts}"
            with open(backup_file, 'w', encoding='utf-8') as f:
                json.dump(events_data, f, indent=2, ensure_ascii=False)
            logger.info(f"Created backup: {backup_file}")
        
        # Save updated file
        with open(events_file, 'w', encoding='utf-8') as f:
            json.dump(updated_events, f, indent=2, ensure_ascii=False)
        logger.info(f"Updated events file: {events_file}")
        
    except Exception as e:
        logger.error(f"Error saving updated events: {e}")
        return 1
    
    logger.info("Geocoding complete!")
    return 0

if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)
