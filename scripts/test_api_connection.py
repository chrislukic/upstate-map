#!/usr/bin/env python3
"""
Test script to verify Google Places API connection and get a sample place ID.
"""

import os
import requests
import json

def test_api_connection(api_key: str):
    """Test the Google Places API connection with a simple query."""
    
    # Test with a well-known location
    test_query = "Central Park, New York, NY"
    
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {
        'query': test_query,
        'key': api_key,
        'fields': 'place_id,formatted_address,name'
    }
    
    try:
        print(f"Testing API connection with query: '{test_query}'")
        print("Making request...")
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        print(f"Response status: {data.get('status')}")
        
        if data.get('status') == 'OK' and data.get('results'):
            result = data['results'][0]
            print(f"✓ API connection successful!")
            print(f"  Place ID: {result.get('place_id')}")
            print(f"  Name: {result.get('name')}")
            print(f"  Address: {result.get('formatted_address')}")
            return True
        else:
            print(f"✗ API returned status: {data.get('status')}")
            if 'error_message' in data:
                print(f"  Error: {data['error_message']}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"✗ Request failed: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False

def main():
    """Main function to test API connection."""
    
    # Get API key
    api_key = os.getenv('GOOGLE_PLACES_API_KEY')
    
    if not api_key:
        print("Google Places API key not found in environment variable GOOGLE_PLACES_API_KEY")
        print("Please set it with: export GOOGLE_PLACES_API_KEY='your_api_key_here'")
        print("Or enter it manually:")
        api_key = input("Enter your Google Places API key: ").strip()
        
        if not api_key:
            print("No API key provided. Exiting.")
            return
    
    print(f"API key: {api_key[:10]}...{api_key[-4:] if len(api_key) > 14 else '***'}")
    print()
    
    # Test connection
    success = test_api_connection(api_key)
    
    if success:
        print("\n✓ API connection test passed! You can now run the place ID assignment script.")
    else:
        print("\n✗ API connection test failed. Please check your API key and try again.")
        print("\nTroubleshooting:")
        print("1. Verify your API key is correct")
        print("2. Ensure Places API is enabled in Google Cloud Console")
        print("3. Check if you have remaining quota")
        print("4. Verify billing is set up if you've exceeded free tier")

if __name__ == "__main__":
    main()
