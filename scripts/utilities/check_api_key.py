#!/usr/bin/env python3
"""
Check Google Maps API key status
"""

import os
import requests
from pathlib import Path
from dotenv import load_dotenv

def main():
    # Load environment variables
    env_path = Path(__file__).parent.parent.parent / '.env'
    print(f"Loading .env from: {env_path}")
    load_dotenv(env_path)
    
    api_key = os.getenv('GOOGLE_MAPS_API_KEY')
    if not api_key:
        print("Error: GOOGLE_MAPS_API_KEY environment variable not set")
        return
    
    print(f"API key loaded: {api_key[:10]}...")
    
    # Test with a simple geocoding request
    test_address = "New York, NY"
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        'address': test_address,
        'key': api_key
    }
    
    print(f"Testing geocoding API with: {test_address}")
    try:
        response = requests.get(url, params=params)
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

if __name__ == "__main__":
    main()


