#!/usr/bin/env python3
"""
Script to verify GPS coordinates in the scenic NY map datasets
using OpenStreetMap Nominatim API as a cross-reference source.
"""

import json
import requests
import time
import os
from typing import Dict, List, Tuple, Optional

# Configuration
NOMINATIM_BASE_URL = "https://nominatim.openstreetmap.org/search"
REQUEST_DELAY = 1.0  # Delay between requests to be respectful to the API

def load_json_file(filepath: str) -> Dict:
    """Load JSON data from file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {filepath}: {e}")
        return {}

def geocode_with_nominatim(name: str, location: str = None) -> Optional[Tuple[float, float]]:
    """
    Geocode a location using OpenStreetMap Nominatim API.
    Returns (lat, lng) tuple or None if not found.
    """
    try:
        # Construct search query
        query_parts = [name]
        if location:
            query_parts.append(location)
        query = ", ".join(query_parts)
        
        params = {
            'q': query,
            'format': 'json',
            'limit': 1,
            'countrycodes': 'us',  # Focus on US results
            'addressdetails': 1
        }
        
        headers = {
            'User-Agent': 'ScenicNYMap-Verification/1.0'
        }
        
        response = requests.get(NOMINATIM_BASE_URL, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        if data and len(data) > 0:
            result = data[0]
            lat = float(result['lat'])
            lng = float(result['lon'])
            return (lat, lng)
        
        return None
        
    except Exception as e:
        print(f"Error geocoding '{name}': {e}")
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
    """Verify waterfall coordinates."""
    print("=== Verifying Waterfalls ===")
    data = load_json_file('../public/data/waterfalls.json')
    
    discrepancies = []
    
    for i, waterfall in enumerate(data):
        name = waterfall.get('name', f'Waterfall {i}')
        current_lat = waterfall.get('lat')
        current_lng = waterfall.get('lng')
        
        if current_lat is None or current_lng is None:
            print(f"⚠️  {name}: Missing coordinates")
            continue
        
        # Try to geocode the waterfall
        nominatim_coords = geocode_with_nominatim(name, "New York")
        
        if nominatim_coords:
            nom_lat, nom_lng = nominatim_coords
            distance = calculate_distance(current_lat, current_lng, nom_lat, nom_lng)
            
            if distance > 1000:  # More than 1km difference
                discrepancies.append({
                    'name': name,
                    'type': 'waterfall',
                    'current': (current_lat, current_lng),
                    'nominatim': (nom_lat, nom_lng),
                    'distance_m': distance
                })
                print(f"❌ {name}: {distance:.0f}m difference")
            else:
                print(f"✅ {name}: {distance:.0f}m difference (OK)")
        else:
            print(f"❓ {name}: Could not verify with Nominatim")
        
        time.sleep(REQUEST_DELAY)
    
    return discrepancies

def verify_breweries():
    """Verify brewery coordinates."""
    print("\n=== Verifying Breweries ===")
    data = load_json_file('../public/data/breweries.json')
    
    discrepancies = []
    
    for i, brewery in enumerate(data):
        name = brewery.get('name', f'Brewery {i}')
        location = brewery.get('location', '')
        current_lat = brewery.get('lat')
        current_lng = brewery.get('lng')
        
        if current_lat is None or current_lng is None:
            print(f"⚠️  {name}: Missing coordinates")
            continue
        
        # Try to geocode the brewery
        nominatim_coords = geocode_with_nominatim(name, location)
        
        if nominatim_coords:
            nom_lat, nom_lng = nominatim_coords
            distance = calculate_distance(current_lat, current_lng, nom_lat, nom_lng)
            
            if distance > 1000:  # More than 1km difference
                discrepancies.append({
                    'name': name,
                    'type': 'brewery',
                    'current': (current_lat, current_lng),
                    'nominatim': (nom_lat, nom_lng),
                    'distance_m': distance
                })
                print(f"❌ {name}: {distance:.0f}m difference")
            else:
                print(f"✅ {name}: {distance:.0f}m difference (OK)")
        else:
            print(f"❓ {name}: Could not verify with Nominatim")
        
        time.sleep(REQUEST_DELAY)
    
    return discrepancies

def verify_restaurants():
    """Verify restaurant coordinates."""
    print("\n=== Verifying Restaurants ===")
    data = load_json_file('../public/data/restaurants.json')
    
    discrepancies = []
    
    for i, restaurant in enumerate(data):
        name = restaurant.get('name', f'Restaurant {i}')
        location = restaurant.get('location', '')
        current_lat = restaurant.get('lat')
        current_lng = restaurant.get('lng')
        
        if current_lat is None or current_lng is None:
            print(f"⚠️  {name}: Missing coordinates")
            continue
        
        # Try to geocode the restaurant
        nominatim_coords = geocode_with_nominatim(name, location)
        
        if nominatim_coords:
            nom_lat, nom_lng = nominatim_coords
            distance = calculate_distance(current_lat, current_lng, nom_lat, nom_lng)
            
            if distance > 1000:  # More than 1km difference
                discrepancies.append({
                    'name': name,
                    'type': 'restaurant',
                    'current': (current_lat, current_lng),
                    'nominatim': (nom_lat, nom_lng),
                    'distance_m': distance
                })
                print(f"❌ {name}: {distance:.0f}m difference")
            else:
                print(f"✅ {name}: {distance:.0f}m difference (OK)")
        else:
            print(f"❓ {name}: Could not verify with Nominatim")
        
        time.sleep(REQUEST_DELAY)
    
    return discrepancies

def verify_orchards():
    """Verify orchard coordinates."""
    print("\n=== Verifying Orchards ===")
    data = load_json_file('../public/data/orchards_points.json')
    
    discrepancies = []
    
    for i, orchard in enumerate(data):
        name = orchard.get('name', f'Orchard {i}')
        address = orchard.get('address', '')
        current_lat = orchard.get('lat')
        current_lng = orchard.get('lng')
        
        if current_lat is None or current_lng is None:
            print(f"⚠️  {name}: Missing coordinates")
            continue
        
        # Try to geocode the orchard
        nominatim_coords = geocode_with_nominatim(name, address)
        
        if nominatim_coords:
            nom_lat, nom_lng = nominatim_coords
            distance = calculate_distance(current_lat, current_lng, nom_lat, nom_lng)
            
            if distance > 1000:  # More than 1km difference
                discrepancies.append({
                    'name': name,
                    'type': 'orchard',
                    'current': (current_lat, current_lng),
                    'nominatim': (nom_lat, nom_lng),
                    'distance_m': distance
                })
                print(f"❌ {name}: {distance:.0f}m difference")
            else:
                print(f"✅ {name}: {distance:.0f}m difference (OK)")
        else:
            print(f"❓ {name}: Could not verify with Nominatim")
        
        time.sleep(REQUEST_DELAY)
    
    return discrepancies

def verify_cities():
    """Verify city coordinates."""
    print("\n=== Verifying Cities ===")
    data = load_json_file('../public/data/map-data.json')
    cities = data.get('cities', [])
    
    discrepancies = []
    
    for i, city in enumerate(cities):
        name = city.get('name', f'City {i}')
        current_lat = city.get('lat')
        current_lng = city.get('lng')
        
        if current_lat is None or current_lng is None:
            print(f"⚠️  {name}: Missing coordinates")
            continue
        
        # Try to geocode the city
        nominatim_coords = geocode_with_nominatim(name, "New York")
        
        if nominatim_coords:
            nom_lat, nom_lng = nominatim_coords
            distance = calculate_distance(current_lat, current_lng, nom_lat, nom_lng)
            
            if distance > 5000:  # More than 5km difference (cities can be large)
                discrepancies.append({
                    'name': name,
                    'type': 'city',
                    'current': (current_lat, current_lng),
                    'nominatim': (nom_lat, nom_lng),
                    'distance_m': distance
                })
                print(f"❌ {name}: {distance:.0f}m difference")
            else:
                print(f"✅ {name}: {distance:.0f}m difference (OK)")
        else:
            print(f"❓ {name}: Could not verify with Nominatim")
        
        time.sleep(REQUEST_DELAY)
    
    return discrepancies

def generate_report(discrepancies: List[Dict]):
    """Generate a summary report of discrepancies."""
    if not discrepancies:
        print("\n🎉 All coordinates verified successfully!")
        return
    
    print(f"\n📊 SUMMARY: Found {len(discrepancies)} potential discrepancies")
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
            print(f"    Nominatim: {item['nominatim'][0]:.6f}, {item['nominatim'][1]:.6f}")
    
    # Save detailed report
    report_file = 'coordinate_verification_report.json'
    with open(report_file, 'w') as f:
        json.dump(discrepancies, f, indent=2)
    print(f"\n📄 Detailed report saved to: {report_file}")

def main():
    """Main function to run coordinate verification."""
    print("🗺️  Scenic NY Map - Coordinate Verification")
    print("=" * 50)
    print("Cross-referencing coordinates with OpenStreetMap Nominatim API")
    print("This may take several minutes due to API rate limiting...")
    print()
    
    all_discrepancies = []
    
    # Verify each dataset
    all_discrepancies.extend(verify_waterfalls())
    all_discrepancies.extend(verify_breweries())
    all_discrepancies.extend(verify_restaurants())
    all_discrepancies.extend(verify_orchards())
    all_discrepancies.extend(verify_cities())
    
    # Generate summary report
    generate_report(all_discrepancies)

if __name__ == "__main__":
    main()

