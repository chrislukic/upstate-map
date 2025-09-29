#!/usr/bin/env python3
"""
Check Google Maps API key status
"""

import os
import sys
import requests
from pathlib import Path

# Add the scripts directory to the path so we can import from config
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Import shared configuration loader
from config.loader import load_script_config, setup_logging, validate_environment, get_api_key

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
    
    print(f"API key loaded: {api_key[:10]}...")
    
    # Test with a simple geocoding request
    test_address = "New York, NY"
    geocoding_endpoint = config.get("api", {}).get("google_maps", {}).get("geocoding_endpoint", 
                                                                          "https://maps.googleapis.com/maps/api/geocode/json")
    timeout = config.get("geocoding", {}).get("timeout", 20)
    
    params = {
        'address': test_address,
        'key': api_key
    }
    
    print(f"Testing geocoding API with: {test_address}")
    try:
        response = requests.get(geocoding_endpoint, params=params, timeout=timeout)
        response.raise_for_status()
        data = response.json()
        
        print(f"Status: {data['status']}")
        if data['status'] == 'OK':
            print("✅ Geocoding API is working!")
            result = data['results'][0]
            print(f"Test result: {result['formatted_address']}")
            print(f"Location: {result['geometry']['location']}")
        else:
            print(f"❌ Geocoding API error: {data['status']}")
            if 'error_message' in data:
                print(f"Error message: {data['error_message']}")
                
    except Exception as e:
        print(f"❌ Request failed: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    main()


