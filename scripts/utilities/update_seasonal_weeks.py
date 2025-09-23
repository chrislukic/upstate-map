#!/usr/bin/env python3
"""
Update PYO JSON files with precise week-based seasonal data.
Based on the notes in the JSON files, assigns accurate week numbers for each crop type.
"""

import json
import os
from pathlib import Path

def get_week_number(month, day):
    """Convert month/day to week number (1-52)"""
    # Simple approximation: each month has ~4.3 weeks
    # Week 1 = Jan 1-7, Week 52 = Dec 25-31
    month_weeks = {
        1: list(range(1, 5)),      # Jan: weeks 1-4
        2: list(range(5, 9)),      # Feb: weeks 5-8  
        3: list(range(9, 13)),     # Mar: weeks 9-12
        4: list(range(13, 17)),    # Apr: weeks 13-16
        5: list(range(17, 22)),    # May: weeks 17-21
        6: list(range(22, 26)),    # Jun: weeks 22-25
        7: list(range(26, 30)),    # Jul: weeks 26-29
        8: list(range(30, 35)),    # Aug: weeks 30-34
        9: list(range(35, 39)),    # Sep: weeks 35-38
        10: list(range(39, 43)),   # Oct: weeks 39-42
        11: list(range(43, 47)),   # Nov: weeks 43-46
        12: list(range(47, 53))    # Dec: weeks 47-52
    }
    return month_weeks.get(month, [])

def get_seasonal_weeks(crop_type):
    """Get seasonal weeks based on crop type and notes analysis"""
    
    if crop_type == "apples":
        # Based on notes: "Sept–Oct", "Labor Day weekend through Oct", "mid-August", "late August–Oct"
        # Labor Day is typically first Monday of September (week 35-36)
        # Most apples start late August/early September through October
        return list(range(34, 43))  # Weeks 34-42 (late Aug through Oct)
    
    elif crop_type == "strawberries":
        # Based on notes: "early June", "late May–June", "mid-June"
        # Strawberries typically start late May through mid-July
        return list(range(21, 28))  # Weeks 21-27 (late May through early July)
    
    elif crop_type == "cherries":
        # Based on notes: "late June through mid-July", "early July", "mid-July"
        # Cherries are typically late June through mid-July
        return list(range(25, 30))  # Weeks 25-29 (late June through mid-July)
    
    elif crop_type == "peaches":
        # Based on notes: "mid-August", "July–August", "late July through August", "early September"
        # Peaches typically start mid-July through early September
        return list(range(29, 37))  # Weeks 29-36 (mid-July through early September)
    
    else:
        return []

def update_pyo_file(file_path, crop_type):
    """Update a PYO JSON file with week-based seasonal data"""
    
    print(f"📅 Updating {crop_type} seasonal data...")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        seasonal_weeks = get_seasonal_weeks(crop_type)
        
        updated_count = 0
        for item in data:
            if 'season_months' in item:
                # Replace season_months with season_weeks
                item['season_weeks'] = seasonal_weeks
                del item['season_months']
                updated_count += 1
        
        # Write back to file
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"  ✅ Updated {updated_count} items in {file_path.name}")
        return updated_count
        
    except Exception as e:
        print(f"  ❌ Error updating {file_path.name}: {e}")
        return 0

def main():
    """Main function to update all PYO files"""
    
    # Get the script directory and project root
    script_dir = Path(__file__).parent
    project_root = script_dir.parent.parent
    data_dir = project_root / 'public' / 'data'
    
    # PYO files to update
    pyo_files = [
        ('pyo_apples.json', 'apples'),
        ('pyo_strawberries.json', 'strawberries'), 
        ('pyo_cherries.json', 'cherries'),
        ('pyo_peaches.json', 'peaches')
    ]
    
    total_updated = 0
    
    for filename, crop_type in pyo_files:
        file_path = data_dir / filename
        if file_path.exists():
            updated = update_pyo_file(file_path, crop_type)
            total_updated += updated
        else:
            print(f"  ⚠️  File not found: {filename}")
    
    print(f"\n🎯 Week-based seasonal data updated for {total_updated} total items")
    print("\n📊 Seasonal Week Ranges:")
    print("  🍎 Apples: Weeks 34-42 (late Aug - Oct)")
    print("  🍓 Strawberries: Weeks 21-27 (late May - early July)")  
    print("  🍒 Cherries: Weeks 25-29 (late June - mid July)")
    print("  🍑 Peaches: Weeks 29-36 (mid July - early Sep)")

if __name__ == "__main__":
    main()



