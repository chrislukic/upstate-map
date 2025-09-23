#!/usr/bin/env python3
"""
Merge new trailhead data into existing trail-heads.json
"""

import json
from pathlib import Path

def merge_trailheads():
    # Load existing trailheads data
    trailheads_file = Path(__file__).parent.parent.parent / 'public' / 'data' / 'trail-heads.json'
    
    with open(trailheads_file, 'r', encoding='utf-8') as f:
        trailheads = json.load(f)
    
    # New trailhead data to merge
    new_trailheads = [
        {
            "name": "Rooster Comb Trailhead",
            "lat": 44.1885,
            "lng": -73.7693,
            "location": "NY-73, Keene Valley, NY 12943",
            "region": "Adirondacks",
            "difficulty_range": "Moderate",
            "season": "Year-round",
            "description": "A central Keene Valley trailhead leading to the Rooster Comb summit, Snow Mountain, and as a gateway into the Great Range.",
            "full_description": "This official parking lot on Route 73 in Keene Valley provides direct access to the Rooster Comb trail, a moderate 4.8-mile round trip climb that rewards hikers with sweeping views of Giant Mountain, the Great Range, and Keene Valley itself. The trail also connects to Snow Mountain for additional vistas, and further links into the Great Range trail system. It's a less intimidating but still rewarding alternative to the High Peaks climbs, making it a very popular hike year-round.",
            "place_id": None,
            "place_query": "Rooster Comb Trailhead Keene Valley NY"
        },
        {
            "name": "Chapel Pond Trailhead (Giant Mountain via Ridge Trail)",
            "lat": 44.1338,
            "lng": -73.7432,
            "location": "Chapel Pond, NY-73, Keene, NY 12942",
            "region": "Adirondacks",
            "difficulty_range": "Hard",
            "season": "Year-round",
            "description": "Steep trailhead climbing Giant Mountain, one of the most scenic High Peaks, with exposed ridges and open views.",
            "full_description": "Located across from Chapel Pond, this trailhead starts the Ridge Trail up Giant Mountain (4,627′). It's one of the most direct High Peak routes, gaining over 3,000′ in just 3 miles. The climb is strenuous but offers frequent open ledges with panoramic views of the Adirondack High Peaks and Champlain Valley. The trailhead is also a starting point for Nubble and Rocky Peak Ridge, making it a hub for challenging but spectacular day hikes.",
            "place_id": None,
            "place_query": "Chapel Pond Giant Mountain Ridge Trailhead Keene NY"
        },
        {
            "name": "St. Huberts Trailhead (AMR Lot)",
            "lat": 44.0931,
            "lng": -73.7650,
            "location": "Rt 73, Ausable Club, Keene Valley, NY 12943",
            "region": "Adirondacks",
            "difficulty_range": "Moderate–Hard",
            "season": "Year-round (limited access rules)",
            "description": "The AMR/Ausable Club parking area giving access to trails to popular peaks like Noonmark, Dial, Nippletop, and the Great Range.",
            "full_description": "This heavily used trailhead provides access through the Adirondack Mountain Reserve to dozens of routes, including the Noonmark Mountain hike, the scenic Lake Road approach to Colvin, Blake, Dial, Nippletop, and trails into the Great Range. A permit system and access restrictions apply, but it remains one of the most important trailheads in the Adirondacks. The Noonmark hike (4.2 miles round trip) is especially popular with families seeking a manageable but scenic summit.",
            "place_id": None,
            "place_query": "St Huberts Trailhead Ausable Club Keene Valley NY"
        },
        {
            "name": "Saranac Lake 6er Trailhead (Baker Mountain)",
            "lat": 44.3131,
            "lng": -74.1286,
            "location": "Forest Hill Ave, Saranac Lake, NY 12983",
            "region": "Adirondacks",
            "difficulty_range": "Easy–Moderate",
            "season": "Year-round",
            "description": "Trailhead for Baker Mountain, the shortest of the Saranac Lake 6ers, popular for families and first-time climbers.",
            "full_description": "Located just outside downtown Saranac Lake, the Baker Mountain trailhead provides quick access to a 1.8-mile round trip climb. Despite its modest size, Baker's rocky summit offers great views of McKenzie Mountain and the village of Saranac Lake. It's a cornerstone of the Saranac Lake 6er challenge and ideal for families or those new to Adirondack hiking. Open year-round, Baker is especially popular for short sunrise or sunset hikes.",
            "place_id": None,
            "place_query": "Baker Mountain trailhead Saranac Lake NY"
        },
        {
            "name": "Goodnow Mountain Trailhead",
            "lat": 43.9733,
            "lng": -74.1353,
            "location": "Route 28N, Newcomb, NY 12852",
            "region": "Adirondacks",
            "difficulty_range": "Easy–Moderate",
            "season": "Year-round",
            "description": "A well-maintained trail near Newcomb leading to a fire tower with sweeping High Peaks views.",
            "full_description": "This family-friendly trailhead starts a 1.9-mile climb up Goodnow Mountain, located near the SUNY ESF Visitor Interpretive Center in Newcomb. The summit fire tower provides a full panorama of the central Adirondacks, including the High Peaks to the north. The trail, managed by SUNY, is well-graded and suitable for kids, making it one of the best introductory fire tower hikes in the region.",
            "place_id": None,
            "place_query": "Goodnow Mountain trailhead Newcomb NY"
        },
        {
            "name": "Owls Head Mountain Trailhead (Long Lake)",
            "lat": 43.9718,
            "lng": -74.4215,
            "location": "Endion Rd, Long Lake, NY 12847",
            "region": "Adirondacks",
            "difficulty_range": "Moderate",
            "season": "Year-round",
            "description": "Trailhead near Long Lake leading to a 3.2-mile hike up to a fire tower with views of the High Peaks and the Adirondack interior.",
            "full_description": "Owls Head Mountain is a classic 3,150′ fire tower peak in Hamilton County. The 3.2-mile trail climbs gradually through forest before steepening near the summit. The restored fire tower provides 360° views over Long Lake, the High Peaks, and the Central Adirondacks. The trailhead has a small parking area and is used year-round, though best from spring to fall. It's one of the most rewarding moderate hikes in the Long Lake area.",
            "place_id": None,
            "place_query": "Owls Head Mountain trailhead Long Lake NY"
        },
        {
            "name": "Pharaoh Lake Wilderness Trailhead",
            "lat": 43.7406,
            "lng": -73.6233,
            "location": "Pharaoh Rd, Brant Lake, NY 12815",
            "region": "Adirondacks",
            "difficulty_range": "Easy–Moderate",
            "season": "Year-round",
            "description": "Trailhead into the Pharaoh Lake Wilderness, one of the largest roadless tracts in the Adirondacks, featuring a scenic lake and network of trails.",
            "full_description": "This official DEC parking area at the end of Pharaoh Road provides access into the Pharaoh Lake Wilderness, a 46,000-acre backcountry area east of Schroon Lake. A gentle 3-mile trail leads to Pharaoh Lake, one of the Adirondacks' largest wilderness lakes, with campsites, lean-tos, and mountain backdrops. From here, trails radiate out to summits like Pharaoh Mountain and Treadway Mountain. It's a quieter but beloved alternative to the High Peaks, offering solitude, swimming, and accessible wilderness for hikers and backpackers.",
            "place_id": None,
            "place_query": "Pharaoh Lake Wilderness trailhead Brant Lake NY"
        }
    ]
    
    print(f"🥾 Merging {len(new_trailheads)} new trailheads into existing data...")
    
    # Find the Adirondacks region and add new trailheads
    adirondacks_region = None
    for region in trailheads:
        if region.get('region') == 'Adirondacks':
            adirondacks_region = region
            break
    
    if adirondacks_region:
        # Add new trailheads to existing Adirondacks region
        existing_trails = adirondacks_region.get('trails', [])
        existing_names = {trail['name'] for trail in existing_trails}
        
        added_count = 0
        for new_trail in new_trailheads:
            if new_trail['name'] not in existing_names:
                existing_trails.append(new_trail)
                print(f"  ✅ Added: {new_trail['name']}")
                added_count += 1
            else:
                print(f"  ⏭️  Already exists: {new_trail['name']}")
        
        adirondacks_region['trails'] = existing_trails
        print(f"\n📊 Added {added_count} new trailheads to Adirondacks region")
    else:
        print("❌ Adirondacks region not found in existing data")
        return
    
    # Save updated data
    with open(trailheads_file, 'w', encoding='utf-8') as f:
        json.dump(trailheads, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Saved to: {trailheads_file}")

if __name__ == "__main__":
    merge_trailheads()



