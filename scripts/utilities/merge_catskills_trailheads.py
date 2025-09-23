#!/usr/bin/env python3
"""
Merge new Catskills trailhead data into existing trail-heads.json
"""

import json
from pathlib import Path

def merge_catskills_trailheads():
    # Load existing trailheads data
    trailheads_file = Path(__file__).parent.parent.parent / 'public' / 'data' / 'trail-heads.json'
    
    with open(trailheads_file, 'r', encoding='utf-8') as f:
        trailheads = json.load(f)
    
    # New Catskills trailhead data to merge
    new_trailheads = [
        {
            "name": "Hunter Mountain Trailhead (Becker Hollow)",
            "lat": 42.1818,
            "lng": -74.1969,
            "location": "Becker Hollow Rd, Hunter, NY 12442",
            "region": "Catskills",
            "difficulty_range": "Hard",
            "season": "Year-round",
            "description": "Steepest official route to Hunter Mountain, the Catskills' second highest peak, culminating at a fire tower with sweeping 360° views.",
            "full_description": "The Becker Hollow trailhead leads to a demanding 4.7-mile round trip climb up Hunter Mountain, gaining over 2,200 feet in less than 2.5 miles. It is considered the steepest official trail in the Catskills. The reward at the summit is a restored fire tower offering unmatched 360° panoramas across the Catskills and even to the Adirondacks on clear days. This trailhead is popular with peakbaggers and those completing the Catskill 3500 Club list, especially in winter when snowshoeing is required.",
            "place_id": None,
            "place_query": "Hunter Mountain Becker Hollow trailhead NY"
        },
        {
            "name": "Windham High Peak Trailhead (Elm Ridge)",
            "lat": 42.3087,
            "lng": -74.2202,
            "location": "NY-23, East Windham, NY 12496",
            "region": "Catskills",
            "difficulty_range": "Moderate",
            "season": "Year-round",
            "description": "Access point for a moderate hike to Windham High Peak, one of the Catskills' 35 highest, with excellent views toward the Hudson Valley.",
            "full_description": "Located near the Elm Ridge parking area on Route 23, this trailhead provides a 6.6-mile round trip hike up Windham High Peak (3,524′). The climb is gradual and suitable for families with older kids. The summit offers panoramic views east toward the Hudson Valley and west toward the Devil's Path range. As one of the easier Catskill High Peaks, it is a popular choice for hikers seeking a manageable but rewarding summit experience, accessible in all seasons.",
            "place_id": None,
            "place_query": "Windham High Peak trailhead NY"
        },
        {
            "name": "Wittenberg Mountain Trailhead (Woodland Valley)",
            "lat": 42.0215,
            "lng": -74.3575,
            "location": "Woodland Valley Campground, Phoenicia, NY 12464",
            "region": "Catskills",
            "difficulty_range": "Hard",
            "season": "Spring–Fall (campground road closes in winter)",
            "description": "Trailhead in Woodland Valley giving access to Wittenberg and Cornell Mountains, with one of the Catskills' most celebrated vistas.",
            "full_description": "This DEC-managed trailhead begins from the Woodland Valley Campground area. The red-blazed Wittenberg-Cornell-Slide Trail climbs 3.9 miles to Wittenberg Mountain, one of the most iconic summits in the Catskills. The open ledge at Wittenberg offers breathtaking views over Ashokan Reservoir and the southern Catskills, considered among the best vistas in the range. Continuing on, experienced hikers can add Cornell or Slide to form a rugged traverse. Parking fills quickly on summer weekends, and access may be limited when the campground gate is closed in winter.",
            "place_id": None,
            "place_query": "Wittenberg Mountain Woodland Valley trailhead NY"
        },
        {
            "name": "North-South Lake Campground Trailheads",
            "lat": 42.2007,
            "lng": -74.0519,
            "location": "874 North Lake Rd, Haines Falls, NY 12436",
            "region": "Catskills",
            "difficulty_range": "Easy–Moderate",
            "season": "Spring–Fall",
            "description": "Multiple trailheads around North-South Lake giving access to family-friendly loops and the Escarpment Trail's dramatic clifftop views.",
            "full_description": "North-South Lake Campground is the Catskills' largest state campground, and its network of official trailheads provides access to the Escarpment Trail and several historic ledges. Popular destinations include Artist's Rock, Sunset Rock, and the former site of the Catskill Mountain House. Most hikes here are 2–4 miles and easy to moderate, making them highly family-friendly. The overlooks provide dramatic views over the Hudson Valley, and the trails are dotted with historical markers highlighting the Hudson River School of painting. The trails are open spring through fall when the campground is in operation.",
            "place_id": None,
            "place_query": "North South Lake Escarpment trailhead Haines Falls NY"
        },
        {
            "name": "Blackhead Range Trailhead (Big Hollow Rd)",
            "lat": 42.2909,
            "lng": -74.1112,
            "location": "Big Hollow Rd, Maplecrest, NY 12454",
            "region": "Catskills",
            "difficulty_range": "Moderate–Hard",
            "season": "Year-round",
            "description": "Trailhead for the Blackhead Range, accessing Blackhead, Black Dome, and Thomas Cole Mountains via steep climbs and rugged terrain.",
            "full_description": "This DEC trailhead at the end of Big Hollow Road is the gateway to the Blackhead Range, including Blackhead (3,940′), Black Dome, and Thomas Cole Mountains. The hikes here are steep and rugged, with ascents of over 2,000 feet, but the summits reward hikers with excellent views of the northern Catskills. This area is less crowded than Slide or Hunter but is a must for Catskill 3500 Club aspirants. Trails are accessible year-round, though winter conditions can be harsh.",
            "place_id": None,
            "place_query": "Blackhead Range trailhead Big Hollow Rd NY"
        },
        {
            "name": "Balsam Lake Mountain Trailhead",
            "lat": 42.0802,
            "lng": -74.5855,
            "location": "Beaverkill Rd, Hardenburgh, NY 12465",
            "region": "Catskills",
            "difficulty_range": "Moderate",
            "season": "Year-round",
            "description": "Remote trailhead leading to Balsam Lake Mountain, the site of the Catskills' first fire tower, with broad summit views.",
            "full_description": "The Balsam Lake Mountain trailhead, located near the Beaverkill valley, provides a 3.6-mile round trip hike to the 3,720′ summit. The restored fire tower at the top offers sweeping 360° views of the western Catskills. It's considered one of the easier Catskill 3500 peaks, making it popular for families and history buffs alike. Accessible in all seasons, though the road may be challenging in winter.",
            "place_id": None,
            "place_query": "Balsam Lake Mountain trailhead Hardenburgh NY"
        }
    ]
    
    print(f"🏔️ Merging {len(new_trailheads)} new Catskills trailheads into existing data...")
    
    # Find the Catskills region and add new trailheads
    catskills_region = None
    for region in trailheads:
        if region.get('region') == 'Catskills':
            catskills_region = region
            break
    
    if catskills_region:
        # Add new trailheads to existing Catskills region
        existing_trails = catskills_region.get('trails', [])
        existing_names = {trail['name'] for trail in existing_trails}
        
        added_count = 0
        for new_trail in new_trailheads:
            if new_trail['name'] not in existing_names:
                existing_trails.append(new_trail)
                print(f"  ✅ Added: {new_trail['name']}")
                added_count += 1
            else:
                print(f"  ⏭️  Already exists: {new_trail['name']}")
        
        catskills_region['trails'] = existing_trails
        print(f"\n📊 Added {added_count} new trailheads to Catskills region")
    else:
        print("❌ Catskills region not found in existing data")
        return
    
    # Save updated data
    with open(trailheads_file, 'w', encoding='utf-8') as f:
        json.dump(trailheads, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Saved to: {trailheads_file}")

if __name__ == "__main__":
    merge_catskills_trailheads()



