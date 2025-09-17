#!/usr/bin/env python3
"""
Script to enrich new restaurants with Google Places data.
This script specifically targets restaurants with null coordinates.
"""

import json
import requests
import time
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_google_places_data(name, location, api_key):
    """Get place details from Google Places API"""
    try:
        # First, search for the place
        search_url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
        search_params = {
            'input': f"{name} {location}",
            'inputtype': 'textquery',
            'fields': 'place_id,geometry,name,formatted_address',
            'key': api_key
        }
        
        response = requests.get(search_url, params=search_params)
        data = response.json()
        
        if data.get('status') == 'OK' and data.get('candidates'):
            candidate = data['candidates'][0]
            place_id = candidate.get('place_id')
            geometry = candidate.get('geometry', {})
            location_data = geometry.get('location', {})
            
            if place_id and location_data:
                lat = location_data.get('lat')
                lng = location_data.get('lng')
                google_maps_url = f"https://www.google.com/maps/place/?q=place_id:{place_id}"
                
                return {
                    'place_id': place_id,
                    'lat': lat,
                    'lng': lng,
                    'google_maps_url': google_maps_url
                }
        
        print(f"  ❌ No results found for: {name} in {location}")
        return None
        
    except Exception as e:
        print(f"  ❌ Error searching for {name}: {e}")
        return None

def enrich_restaurants():
    """Enrich restaurants with null coordinates"""
    api_key = os.getenv('GOOGLE_MAPS_API_KEY')
    if not api_key:
        print("❌ Error: GOOGLE_MAPS_API_KEY not found in .env file")
        return
    
    # Load restaurants data
    restaurants_file = '../public/data/restaurants.json'
    try:
        with open(restaurants_file, 'r', encoding='utf-8') as f:
            restaurants = json.load(f)
    except Exception as e:
        print(f"❌ Error loading restaurants: {e}")
        return
    
    # Find restaurants with null coordinates
    null_restaurants = [r for r in restaurants if r.get('lat') is None or r.get('lng') is None]
    
    if not null_restaurants:
        print("✅ No restaurants with null coordinates found!")
        return
    
    print(f"🍽️  Found {len(null_restaurants)} restaurants with null coordinates")
    print("=" * 60)
    
    enriched_count = 0
    
    for i, restaurant in enumerate(null_restaurants, 1):
        name = restaurant.get('name', 'Unknown')
        location = restaurant.get('location', '')
        
        print(f"[{i}/{len(null_restaurants)}] Enriching: {name} ({location})")
        
        # Get Google Places data
        places_data = get_google_places_data(name, location, api_key)
        
        if places_data:
            # Update the restaurant data
            restaurant['place_id'] = places_data['place_id']
            restaurant['lat'] = places_data['lat']
            restaurant['lng'] = places_data['lng']
            restaurant['google_maps_url'] = places_data['google_maps_url']
            
            print(f"  ✅ Found: {places_data['lat']:.6f}, {places_data['lng']:.6f}")
            enriched_count += 1
        else:
            print(f"  ❌ Could not find data for: {name}")
        
        # Rate limiting - be nice to the API
        time.sleep(0.1)
    
    # Save updated data
    try:
        with open(restaurants_file, 'w', encoding='utf-8') as f:
            json.dump(restaurants, f, indent=2, ensure_ascii=False)
        
        print("=" * 60)
        print(f"📊 Enrichment Summary:")
        print(f"  • Total restaurants with null coordinates: {len(null_restaurants)}")
        print(f"  • Successfully enriched: {enriched_count}")
        print(f"  • Failed to enrich: {len(null_restaurants) - enriched_count}")
        print(f"✅ Updated restaurants data saved to: {restaurants_file}")
        
    except Exception as e:
        print(f"❌ Error saving restaurants data: {e}")

if __name__ == "__main__":
    print("🍽️  Restaurant Enrichment Script")
    print("=" * 40)
    enrich_restaurants()