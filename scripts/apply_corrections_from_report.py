#!/usr/bin/env python3
"""
Apply coordinate corrections directly from the verification report JSON file.
This avoids the need to regenerate the correction script and saves API costs.
"""

import json
import os

def apply_corrections_from_report():
    """Apply corrections from the verification report JSON file."""
    
    # Load the verification report
    report_file = 'google_coordinate_verification_report.json'
    if not os.path.exists(report_file):
        print(f"❌ Report file not found: {report_file}")
        return
    
    try:
        with open(report_file, 'r', encoding='utf-8') as f:
            discrepancies = json.load(f)
    except Exception as e:
        print(f"❌ Error loading report: {e}")
        return
    
    if not discrepancies:
        print("🎉 No corrections needed!")
        return
    
    print(f"📊 Applying {len(discrepancies)} coordinate corrections...")
    print("=" * 60)
    
    # Apply corrections
    for correction in discrepancies:
        name = correction['name']
        correction_type = correction['type']
        old_lat = correction['current'][0]
        old_lng = correction['current'][1]
        new_lat = correction['google'][0]
        new_lng = correction['google'][1]
        distance = correction['distance_m']
        
        print(f"Updating {name} ({correction_type})...")
        
        # Determine file path
        if correction_type == 'waterfall':
            filepath = '../public/data/waterfalls.json'
        elif correction_type == 'brewery':
            filepath = '../public/data/breweries.json'
        elif correction_type == 'restaurant':
            filepath = '../public/data/restaurants.json'
        elif correction_type == 'orchard':
            filepath = '../public/data/orchards_points.json'
        elif correction_type == 'city':
            filepath = '../public/data/map-data.json'
        else:
            print(f"  ⚠️  Unknown type: {correction_type}")
            continue
        
        try:
            # Load the data file
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            updated = False
            
            if correction_type == 'city':
                # Cities are in a nested structure
                cities = data.get('cities', [])
                for city in cities:
                    if city.get('name') == name:
                        city['lat'] = new_lat
                        city['lng'] = new_lng
                        updated = True
                        break
            else:
                # Other types are direct arrays
                for item in data:
                    if item.get('name') == name:
                        item['lat'] = new_lat
                        item['lng'] = new_lng
                        updated = True
                        break
            
            if updated:
                # Save the updated data
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                
                print(f"  ✅ Updated {name}: {old_lat:.6f},{old_lng:.6f} -> {new_lat:.6f},{new_lng:.6f} ({distance:.0f}m correction)")
            else:
                print(f"  ❌ Could not find {name} in {filepath}")
                
        except Exception as e:
            print(f"  ❌ Error updating {name}: {e}")
    
    print(f"\n🎉 Applied {len(discrepancies)} coordinate corrections!")
    print("   Refresh your browser to see the updated locations on the map.")

if __name__ == "__main__":
    apply_corrections_from_report()

