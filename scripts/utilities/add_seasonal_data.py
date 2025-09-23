#!/usr/bin/env python3
"""
Add seasonal data to PYO crops
"""

import json
from pathlib import Path

def add_seasonal_data():
    # Define seasonal data for each crop type
    seasonal_data = {
        'pyo_apples.json': {
            'season': 'Fall',
            'season_months': [9, 10, 11],  # September, October, November
            'season_description': 'Apple picking season typically runs from September through November'
        },
        'pyo_strawberries.json': {
            'season': 'Spring/Summer',
            'season_months': [5, 6, 7],  # May, June, July
            'season_description': 'Strawberry picking season typically runs from May through July'
        },
        'pyo_cherries.json': {
            'season': 'Summer',
            'season_months': [6, 7],  # June, July
            'season_description': 'Cherry picking season typically runs from June through July'
        },
        'pyo_peaches.json': {
            'season': 'Summer',
            'season_months': [7, 8, 9],  # July, August, September
            'season_description': 'Peach picking season typically runs from July through September'
        }
    }
    
    for filename, season_info in seasonal_data.items():
        file_path = Path(__file__).parent.parent.parent / 'public' / 'data' / filename
        
        if not file_path.exists():
            print(f"❌ File not found: {filename}")
            continue
            
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"📅 Adding seasonal data to {filename}...")
        
        updated_count = 0
        for item in data:
            if 'season' not in item:
                item['season'] = season_info['season']
                item['season_months'] = season_info['season_months']
                item['season_description'] = season_info['season_description']
                updated_count += 1
        
        # Save updated data
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"  ✅ Updated {updated_count} items in {filename}")
    
    print(f"\n📊 Seasonal data added to all PYO files")

if __name__ == "__main__":
    add_seasonal_data()



