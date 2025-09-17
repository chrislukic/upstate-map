#!/usr/bin/env python3
"""
Apply coordinate corrections from the verification report, but filter out
obviously incorrect matches (like locations in wrong states).
"""

import json
import os

def is_reasonable_correction(correction):
    """
    Check if a correction is reasonable or if it's likely a wrong location match.
    Returns True if the correction should be applied, False if it should be skipped.
    """
    name = correction['name']
    distance = correction['distance_m']
    current_lat = correction['current'][0]
    current_lng = correction['current'][1]
    google_lat = correction['google'][0]
    google_lng = correction['google'][1]
    
    # Skip corrections that are too far (likely wrong location)
    if distance > 50000:  # More than 50km difference
        print(f"  ⚠️  Skipping {name}: {distance:.0f}m difference (likely wrong location)")
        return False
    
    # Skip corrections that move locations to different states/regions
    # New York state is roughly 40.5-45.0 latitude, -79.8 to -71.8 longitude
    if not (40.0 <= google_lat <= 45.5 and -80.0 <= google_lng <= -71.0):
        print(f"  ⚠️  Skipping {name}: Google coordinates ({google_lat:.3f}, {google_lng:.3f}) are outside NY region")
        return False
    
    # Skip if the correction moves the location too far from the original region
    lat_diff = abs(current_lat - google_lat)
    lng_diff = abs(current_lng - google_lng)
    
    if lat_diff > 2.0 or lng_diff > 2.0:  # More than 2 degrees difference
        print(f"  ⚠️  Skipping {name}: Too far from original location ({lat_diff:.2f}° lat, {lng_diff:.2f}° lng difference)")
        return False
    
    return True

def apply_corrections_safe():
    """Apply corrections from the verification report, filtering out unreasonable ones."""
    
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
    
    print(f"📊 Reviewing {len(discrepancies)} potential coordinate corrections...")
    print("=" * 60)
    
    # Filter out unreasonable corrections
    reasonable_corrections = []
    skipped_count = 0
    
    for correction in discrepancies:
        if is_reasonable_correction(correction):
            reasonable_corrections.append(correction)
        else:
            skipped_count += 1
    
    print(f"\n📋 Summary:")
    print(f"  • Total discrepancies found: {len(discrepancies)}")
    print(f"  • Reasonable corrections: {len(reasonable_corrections)}")
    print(f"  • Skipped (likely wrong): {skipped_count}")
    
    if not reasonable_corrections:
        print("\n🎉 No reasonable corrections to apply!")
        return
    
    print(f"\n🔧 Applying {len(reasonable_corrections)} reasonable corrections...")
    print("=" * 60)
    
    # Apply reasonable corrections
    applied_count = 0
    
    for correction in reasonable_corrections:
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
                applied_count += 1
            else:
                print(f"  ❌ Could not find {name} in {filepath}")
                
        except Exception as e:
            print(f"  ❌ Error updating {name}: {e}")
    
    print(f"\n🎉 Applied {applied_count} coordinate corrections!")
    print(f"   Skipped {skipped_count} corrections that were likely wrong locations.")
    print("   Refresh your browser to see the updated locations on the map.")

if __name__ == "__main__":
    apply_corrections_safe()

