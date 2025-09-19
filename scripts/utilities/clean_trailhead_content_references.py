#!/usr/bin/env python3
"""
Clean up content reference artifacts from trailheads data
"""

import json
import re
from pathlib import Path

def clean_content_references():
    # Load trailheads data
    trailheads_file = Path(__file__).parent.parent.parent / 'public' / 'data' / 'trail-heads.json'
    
    with open(trailheads_file, 'r', encoding='utf-8') as f:
        trailheads = json.load(f)
    
    print(f"🧹 Cleaning content references from {len(trailheads)} trailhead regions...")
    
    cleaned_count = 0
    
    # Clean each region's trails
    for region in trailheads:
        if region.get('trails'):
            for trail in region['trails']:
                # Clean description field
                if 'description' in trail and trail['description']:
                    original = trail['description']
                    trail['description'] = re.sub(r':contentReference\[oaicite:\d+\]\{index=\d+\}', '', original)
                    if original != trail['description']:
                        cleaned_count += 1
                
                # Clean full_description field
                if 'full_description' in trail and trail['full_description']:
                    original = trail['full_description']
                    trail['full_description'] = re.sub(r':contentReference\[oaicite:\d+\]\{index=\d+\}', '', original)
                    if original != trail['full_description']:
                        cleaned_count += 1
    
    # Save cleaned data
    with open(trailheads_file, 'w', encoding='utf-8') as f:
        json.dump(trailheads, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Cleaned {cleaned_count} content references")
    print(f"💾 Saved to: {trailheads_file}")

if __name__ == "__main__":
    clean_content_references()
