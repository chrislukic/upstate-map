#!/usr/bin/env python3
"""
Update peach farm GPS coordinates using Google Place IDs
"""

import json
import requests
import time
import sys
from pathlib import Path

# Add the scripts directory to the path so we can import from config
sys.path.append(str(Path(__file__).parent.parent))

# Import shared configuration loader
from config.loader import load_script_config, setup_logging, validate_environment, get_api_key

def get_place_details(place_id, api_key, config):
    """Get detailed place information including coordinates"""
    try:
        # Get timeout from configuration
        timeout = config.get("place_api", {}).get("timeout", 20)
        
        url = "https://maps.googleapis.com/maps/api/place/details/json"
        params = {
            'place_id': place_id,
            'fields': 'geometry,formatted_address,name',
            'key': api_key
        }
        
        response = requests.get(url, params=params, timeout=timeout)
        data = response.json()
        
        if data['status'] == 'OK' and 'result' in data:
            result = data['result']
            geometry = result.get('geometry', {})
            location = geometry.get('location', {})
            
            return {
                'lat': location.get('lat'),
                'lng': location.get('lng'),
                'formatted_address': result.get('formatted_address', ''),
                'name': result.get('name', '')
            }
        else:
            print(f"  ❌ No details found for place_id: {place_id}")
            return None
            
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return None

def main():
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
        return 1
    
    # Get file paths from configuration
    data_dir = Path(config.get("file_paths", {}).get("data_dir", "../../public/data"))
    peaches_file = data_dir / "pyo_peaches.json"
    
    if not peaches_file.exists():
        logger.error(f"File not found: {peaches_file}")
        return 1
    
    with open(peaches_file, 'r', encoding='utf-8') as f:
        peaches = json.load(f)
    
    print(f"🍑 Updating GPS coordinates for {len(peaches)} peach farms...")
    
    updated_count = 0
    for i, peach in enumerate(peaches, 1):
        print(f"\n[{i}/{len(peaches)}] {peach['name']}")
        
        # Skip if no place_id
        if not peach.get('place_id'):
            print(f"  ⏭️  No place_id available")
            continue
        
        place_id = peach['place_id']
        print(f"  🔍 Getting details for place_id: {place_id}")
        
        result = get_place_details(place_id, api_key, config)
        if result and result['lat'] and result['lng']:
            old_lat = peach.get('lat')
            old_lng = peach.get('lng')
            
            peach['lat'] = result['lat']
            peach['lng'] = result['lng']
            
            print(f"  ✅ Updated coordinates:")
            print(f"     Old: {old_lat}, {old_lng}")
            print(f"     New: {result['lat']}, {result['lng']}")
            print(f"  📍 Address: {result['formatted_address']}")
            updated_count += 1
        else:
            print(f"  ❌ Could not get coordinates")
        
        # Rate limiting
        time.sleep(0.1)
    
    # Save updated data
    with open(peaches_file, 'w', encoding='utf-8') as f:
        json.dump(peaches, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Updated coordinates for {updated_count} peach farms")
    print(f"💾 Saved to: {peaches_file}")

if __name__ == "__main__":
    main()
