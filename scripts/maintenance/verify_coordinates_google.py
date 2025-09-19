#!/usr/bin/env python3
"""
Script to verify GPS coordinates in the scenic NY map datasets
using Google Places API with existing place IDs.
"""

import json
import requests
import time
import os
from typing import Dict, List, Tuple, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
GOOGLE_PLACES_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')
GOOGLE_PLACES_BASE_URL = "https://maps.googleapis.com/maps/api/place/details/json"
REQUEST_DELAY = 0.1  # Shorter delay since we're using place IDs (more reliable)

def load_json_file(filepath: str) -> Dict:
    """Load JSON data from file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {filepath}: {e}")
        return {}

def get_place_details(place_id: str) -> Optional[Tuple[float, float]]:
    """
    Get place details from Google Places API using place ID.
    Returns (lat, lng) tuple or None if not found.
    """
    if not GOOGLE_PLACES_API_KEY:
        print("❌ Google Maps API key not found in environment variables")
        return None
    
    try:
        params = {
            'place_id': place_id,
            'fields': 'geometry,name,formatted_address',
            'key': GOOGLE_PLACES_API_KEY
        }
        
        response = requests.get(GOOGLE_PLACES_BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        if data.get('status') == 'OK' and 'result' in data:
            result = data['result']
            geometry = result.get('geometry', {})
            location = geometry.get('location', {})
            
            if 'lat' in location and 'lng' in location:
                lat = float(location['lat'])
                lng = float(location['lng'])
                return (lat, lng)
        
        print(f"⚠️  API returned status: {data.get('status', 'UNKNOWN')}")
        return None
        
    except Exception as e:
        print(f"Error getting place details for {place_id}: {e}")
        return None

def calculate_distance(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    """
    Calculate distance between two points using Haversine formula.
    Returns distance in meters.
    """
    import math
    
    R = 6371000  # Earth's radius in meters
    
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    delta_lat = math.radians(lat2 - lat1)
    delta_lng = math.radians(lng2 - lng1)
    
    a = (math.sin(delta_lat / 2) ** 2 + 
         math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lng / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    return R * c

def verify_waterfalls():
    """Verify waterfall coordinates using Google Places API."""
    print("=== Verifying Waterfalls ===")
    data = load_json_file('../public/data/waterfalls.json')
    
    discrepancies = []
    verified_count = 0
    
    for i, waterfall in enumerate(data):
        name = waterfall.get('name', f'Waterfall {i}')
        place_id = waterfall.get('place_id')
        current_lat = waterfall.get('lat')
        current_lng = waterfall.get('lng')
        
        if current_lat is None or current_lng is None:
            print(f"⚠️  {name}: Missing coordinates")
            continue
        
        if not place_id:
            print(f"❓ {name}: No place ID available")
            continue
        
        # Get coordinates from Google Places API
        google_coords = get_place_details(place_id)
        
        if google_coords:
            google_lat, google_lng = google_coords
            distance = calculate_distance(current_lat, current_lng, google_lat, google_lng)
            verified_count += 1
            
            if distance > 100:  # More than 100m difference
                discrepancies.append({
                    'name': name,
                    'type': 'waterfall',
                    'place_id': place_id,
                    'current': (current_lat, current_lng),
                    'google': (google_lat, google_lng),
                    'distance_m': distance
                })
                print(f"❌ {name}: {distance:.0f}m difference")
            else:
                print(f"✅ {name}: {distance:.0f}m difference (OK)")
        else:
            print(f"❓ {name}: Could not verify with Google Places API")
        
        time.sleep(REQUEST_DELAY)
    
    print(f"Verified {verified_count}/{len(data)} waterfalls")
    return discrepancies

def verify_breweries():
    """Verify brewery coordinates using Google Places API."""
    print("\n=== Verifying Breweries ===")
    data = load_json_file('../public/data/breweries.json')
    
    discrepancies = []
    verified_count = 0
    
    for i, brewery in enumerate(data):
        name = brewery.get('name', f'Brewery {i}')
        place_id = brewery.get('place_id')
        current_lat = brewery.get('lat')
        current_lng = brewery.get('lng')
        
        if current_lat is None or current_lng is None:
            print(f"⚠️  {name}: Missing coordinates")
            continue
        
        if not place_id:
            print(f"❓ {name}: No place ID available")
            continue
        
        # Get coordinates from Google Places API
        google_coords = get_place_details(place_id)
        
        if google_coords:
            google_lat, google_lng = google_coords
            distance = calculate_distance(current_lat, current_lng, google_lat, google_lng)
            verified_count += 1
            
            if distance > 100:  # More than 100m difference
                discrepancies.append({
                    'name': name,
                    'type': 'brewery',
                    'place_id': place_id,
                    'current': (current_lat, current_lng),
                    'google': (google_lat, google_lng),
                    'distance_m': distance
                })
                print(f"❌ {name}: {distance:.0f}m difference")
            else:
                print(f"✅ {name}: {distance:.0f}m difference (OK)")
        else:
            print(f"❓ {name}: Could not verify with Google Places API")
        
        time.sleep(REQUEST_DELAY)
    
    print(f"Verified {verified_count}/{len(data)} breweries")
    return discrepancies

def verify_restaurants():
    """Verify restaurant coordinates using Google Places API."""
    print("\n=== Verifying Restaurants ===")
    data = load_json_file('../public/data/restaurants.json')
    
    discrepancies = []
    verified_count = 0
    
    for i, restaurant in enumerate(data):
        name = restaurant.get('name', f'Restaurant {i}')
        place_id = restaurant.get('place_id')
        current_lat = restaurant.get('lat')
        current_lng = restaurant.get('lng')
        
        if current_lat is None or current_lng is None:
            print(f"⚠️  {name}: Missing coordinates")
            continue
        
        if not place_id:
            print(f"❓ {name}: No place ID available")
            continue
        
        # Get coordinates from Google Places API
        google_coords = get_place_details(place_id)
        
        if google_coords:
            google_lat, google_lng = google_coords
            distance = calculate_distance(current_lat, current_lng, google_lat, google_lng)
            verified_count += 1
            
            if distance > 100:  # More than 100m difference
                discrepancies.append({
                    'name': name,
                    'type': 'restaurant',
                    'place_id': place_id,
                    'current': (current_lat, current_lng),
                    'google': (google_lat, google_lng),
                    'distance_m': distance
                })
                print(f"❌ {name}: {distance:.0f}m difference")
            else:
                print(f"✅ {name}: {distance:.0f}m difference (OK)")
        else:
            print(f"❓ {name}: Could not verify with Google Places API")
        
        time.sleep(REQUEST_DELAY)
    
    print(f"Verified {verified_count}/{len(data)} restaurants")
    return discrepancies

def verify_orchards():
    """Verify orchard coordinates using Google Places API."""
    print("\n=== Verifying Orchards ===")
    data = load_json_file('../public/data/orchards_points.json')
    
    discrepancies = []
    verified_count = 0
    
    for i, orchard in enumerate(data):
        name = orchard.get('name', f'Orchard {i}')
        place_id = orchard.get('place_id')
        current_lat = orchard.get('lat')
        current_lng = orchard.get('lng')
        
        if current_lat is None or current_lng is None:
            print(f"⚠️  {name}: Missing coordinates")
            continue
        
        if not place_id:
            print(f"❓ {name}: No place ID available")
            continue
        
        # Get coordinates from Google Places API
        google_coords = get_place_details(place_id)
        
        if google_coords:
            google_lat, google_lng = google_coords
            distance = calculate_distance(current_lat, current_lng, google_lat, google_lng)
            verified_count += 1
            
            if distance > 100:  # More than 100m difference
                discrepancies.append({
                    'name': name,
                    'type': 'orchard',
                    'place_id': place_id,
                    'current': (current_lat, current_lng),
                    'google': (google_lat, google_lng),
                    'distance_m': distance
                })
                print(f"❌ {name}: {distance:.0f}m difference")
            else:
                print(f"✅ {name}: {distance:.0f}m difference (OK)")
        else:
            print(f"❓ {name}: Could not verify with Google Places API")
        
        time.sleep(REQUEST_DELAY)
    
    print(f"Verified {verified_count}/{len(data)} orchards")
    return discrepancies

def verify_cities():
    """Verify city coordinates using Google Places API."""
    print("\n=== Verifying Cities ===")
    data = load_json_file('../public/data/map-data.json')
    cities = data.get('cities', [])
    
    discrepancies = []
    verified_count = 0
    
    for i, city in enumerate(cities):
        name = city.get('name', f'City {i}')
        place_id = city.get('place_id')
        current_lat = city.get('lat')
        current_lng = city.get('lng')
        
        if current_lat is None or current_lng is None:
            print(f"⚠️  {name}: Missing coordinates")
            continue
        
        if not place_id:
            print(f"❓ {name}: No place ID available")
            continue
        
        # Get coordinates from Google Places API
        google_coords = get_place_details(place_id)
        
        if google_coords:
            google_lat, google_lng = google_coords
            distance = calculate_distance(current_lat, current_lng, google_lat, google_lng)
            verified_count += 1
            
            if distance > 1000:  # More than 1km difference (cities can be large)
                discrepancies.append({
                    'name': name,
                    'type': 'city',
                    'place_id': place_id,
                    'current': (current_lat, current_lng),
                    'google': (google_lat, google_lng),
                    'distance_m': distance
                })
                print(f"❌ {name}: {distance:.0f}m difference")
            else:
                print(f"✅ {name}: {distance:.0f}m difference (OK)")
        else:
            print(f"❓ {name}: Could not verify with Google Places API")
        
        time.sleep(REQUEST_DELAY)
    
    print(f"Verified {verified_count}/{len(cities)} cities")
    return discrepancies

def generate_correction_script(discrepancies: List[Dict]):
    """Generate a Python script to automatically correct the coordinates."""
    if not discrepancies:
        print("\n🎉 All coordinates verified successfully!")
        return
    
    print(f"\n📊 SUMMARY: Found {len(discrepancies)} coordinate discrepancies")
    print("=" * 60)
    
    # Group by type
    by_type = {}
    for disc in discrepancies:
        disc_type = disc['type']
        if disc_type not in by_type:
            by_type[disc_type] = []
        by_type[disc_type].append(disc)
    
    for disc_type, items in by_type.items():
        print(f"\n{disc_type.upper()}S:")
        for item in sorted(items, key=lambda x: x['distance_m'], reverse=True):
            print(f"  • {item['name']}: {item['distance_m']:.0f}m difference")
            print(f"    Current: {item['current'][0]:.6f}, {item['current'][1]:.6f}")
            print(f"    Google: {item['google'][0]:.6f}, {item['google'][1]:.6f}")
    
    # Generate correction script
    correction_script = """#!/usr/bin/env python3
'''
Auto-generated script to correct GPS coordinates based on Google Places API verification.
Run this script to automatically update the coordinates in your JSON files.
'''

import json

def update_coordinates():
    corrections = [
"""
    
    for disc in discrepancies:
        # Escape single quotes in names
        escaped_name = disc['name'].replace("'", "\\'")
        correction_script += f"""        {{
            'type': '{disc['type']}',
            'name': '{escaped_name}',
            'place_id': '{disc['place_id']}',
            'old_lat': {disc['current'][0]},
            'old_lng': {disc['current'][1]},
            'new_lat': {disc['google'][0]},
            'new_lng': {disc['google'][1]},
            'distance_m': {disc['distance_m']:.0f}
        }},
"""
    
    correction_script += """    ]
    
    # Apply corrections
    for correction in corrections:
        print(f"Updating {correction['name']} ({correction['type']})...")
        
        if correction['type'] == 'waterfall':
            filepath = '../public/data/waterfalls.json'
        elif correction['type'] == 'brewery':
            filepath = '../public/data/breweries.json'
        elif correction['type'] == 'restaurant':
            filepath = '../public/data/restaurants.json'
        elif correction['type'] == 'orchard':
            filepath = '../public/data/orchards_points.json'
        elif correction['type'] == 'city':
            filepath = '../public/data/map-data.json'
        else:
            continue
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if correction['type'] == 'city':
                # Cities are in a nested structure
                cities = data.get('cities', [])
                for city in cities:
                    if city.get('name') == correction['name']:
                        city['lat'] = correction['new_lat']
                        city['lng'] = correction['new_lng']
                        print(f"  Updated {correction['name']}: {correction['old_lat']:.6f},{correction['old_lng']:.6f} -> {correction['new_lat']:.6f},{correction['new_lng']:.6f}")
                        break
            else:
                # Other types are direct arrays
                for item in data:
                    if item.get('name') == correction['name']:
                        item['lat'] = correction['new_lat']
                        item['lng'] = correction['new_lng']
                        print(f"  Updated {correction['name']}: {correction['old_lat']:.6f},{correction['old_lng']:.6f} -> {correction['new_lat']:.6f},{correction['new_lng']:.6f}")
                        break
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            print(f"  Error updating {correction['name']}: {e}")
    
    print(f"\\n✅ Applied {len(corrections)} coordinate corrections")

if __name__ == "__main__":
    update_coordinates()
"""
    
    # Save correction script
    with open('apply_coordinate_corrections.py', 'w', encoding='utf-8') as f:
        f.write(correction_script)
    
    print(f"\n🔧 Generated correction script: apply_coordinate_corrections.py")
    print("   Run this script to automatically apply all coordinate corrections")
    
    # Save detailed report
    report_file = 'google_coordinate_verification_report.json'
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(discrepancies, f, indent=2, ensure_ascii=False)
    print(f"📄 Detailed report saved to: {report_file}")

def main():
    """Main function to run coordinate verification."""
    print("🗺️  Scenic NY Map - Google Places Coordinate Verification")
    print("=" * 60)
    print("Cross-referencing coordinates with Google Places API using place IDs")
    print("This should be much more accurate than name-based geocoding...")
    print()
    
    if not GOOGLE_PLACES_API_KEY:
        print("❌ Error: GOOGLE_MAPS_API_KEY not found in environment variables")
        print("   Please make sure your .env file contains: GOOGLE_MAPS_API_KEY=your_api_key_here")
        return
    
    all_discrepancies = []
    
    # Verify each dataset
    all_discrepancies.extend(verify_waterfalls())
    all_discrepancies.extend(verify_breweries())
    all_discrepancies.extend(verify_restaurants())
    all_discrepancies.extend(verify_orchards())
    all_discrepancies.extend(verify_cities())
    
    # Generate correction script and report
    generate_correction_script(all_discrepancies)

if __name__ == "__main__":
    main()
