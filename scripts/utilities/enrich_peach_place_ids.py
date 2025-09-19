#!/usr/bin/env python3
"""
Enrich peach farms with Google Place IDs
"""

import json
import requests
import time
from pathlib import Path
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv(Path(__file__).parent.parent.parent / '.env')

def get_place_id(query, api_key):
    """Get place ID from Google Places API"""
    try:
        url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
        params = {
            'input': query,
            'inputtype': 'textquery',
            'fields': 'place_id,formatted_address,geometry',
            'key': api_key
        }
        
        response = requests.get(url, params=params)
        data = response.json()
        
        if data['status'] == 'OK' and data['candidates']:
            candidate = data['candidates'][0]
            return {
                'place_id': candidate['place_id'],
                'formatted_address': candidate.get('formatted_address', ''),
                'geometry': candidate.get('geometry', {})
            }
        else:
            print(f"  ❌ No results for: {query}")
            return None
            
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return None

def main():
    # Load peach data
    peaches_file = Path(__file__).parent.parent.parent / 'public' / 'data' / 'pyo_peaches.json'
    
    if not peaches_file.exists():
        print(f"❌ File not found: {peaches_file}")
        return
    
    with open(peaches_file, 'r', encoding='utf-8') as f:
        peaches = json.load(f)
    
    api_key = os.getenv('GOOGLE_MAPS_API_KEY')
    if not api_key:
        print("❌ GOOGLE_MAPS_API_KEY not found in environment")
        return
    
    print(f"🍑 Enriching {len(peaches)} peach farms with Google Place IDs...")
    
    updated_count = 0
    for i, peach in enumerate(peaches, 1):
        print(f"\n[{i}/{len(peaches)}] {peach['name']}")
        
        # Skip if already has place_id
        if peach.get('place_id'):
            print(f"  ⏭️  Already has place_id: {peach['place_id']}")
            continue
        
        # Use place_query if available, otherwise construct from name and address
        query = peach.get('place_query', f"{peach['name']} {peach.get('address', '')}")
        
        print(f"  🔍 Searching for: {query}")
        
        result = get_place_id(query, api_key)
        if result:
            peach['place_id'] = result['place_id']
            peach['google_maps_url'] = f"https://maps.google.com/?place_id={result['place_id']}"
            peach['place_query'] = query
            
            print(f"  ✅ Found: {result['place_id']}")
            print(f"  📍 Address: {result['formatted_address']}")
            updated_count += 1
        else:
            print(f"  ❌ No place ID found")
        
        # Rate limiting
        time.sleep(0.1)
    
    # Save updated data
    with open(peaches_file, 'w', encoding='utf-8') as f:
        json.dump(peaches, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Updated {updated_count} peach farms with Place IDs")
    print(f"💾 Saved to: {peaches_file}")

if __name__ == "__main__":
    main()
