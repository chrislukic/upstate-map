#!/usr/bin/env python3
"""
Merge final batch of trailhead data (additional Southern Tier, Thousand Islands, Tug Hill, North Country) into existing trail-heads.json
"""

import json
from pathlib import Path

def merge_final_trailheads():
    # Load existing trailheads data
    trailheads_file = Path(__file__).parent.parent.parent / 'public' / 'data' / 'trail-heads.json'
    
    with open(trailheads_file, 'r', encoding='utf-8') as f:
        trailheads = json.load(f)
    
    # New trailhead data to merge
    new_trailheads = [
        {
            "name": "Lime Hollow Nature Center Trailhead",
            "lat": 42.5746,
            "lng": -76.2297,
            "location": "338 McLean Rd, Cortland, NY 13045",
            "region": "Southern Tier",
            "difficulty_range": "Easy–Moderate",
            "season": "Year-round",
            "description": "Trailhead for 12 miles of forest, meadow, and wetland trails on a 430-acre conservation center in Cortland.",
            "full_description": "The Lime Hollow Nature Center offers family-friendly hiking across a diverse preserve in the Southern Tier. From this main trailhead, visitors can follow loops through wetlands on boardwalks, along glacial eskers, and into meadows rich with wildlife. The trails are mostly easy, with a few moderate sections, and are accessible year-round. Interpretive signage, an education center, and frequent programs make it popular for families and school trips.",
            "place_id": None,
            "place_query": "Lime Hollow Nature Center trailhead Cortland NY"
        },
        {
            "name": "Jones Hill / Labrador Hollow Trailhead",
            "lat": 42.7521,
            "lng": -76.0118,
            "location": "Labrador Hollow Unique Area, Tully, NY 13159",
            "region": "Southern Tier",
            "difficulty_range": "Moderate",
            "season": "Year-round",
            "description": "Trailhead into Labrador Hollow, leading to Jones Hill and an overlook of the glacial valley below.",
            "full_description": "This DEC-managed trailhead gives access to Labrador Hollow Unique Area, a glacial valley with wetlands, boardwalks, and scenic overlooks. The main climb up Jones Hill gains 800 feet in about 1.5 miles, ending at Hang Glider Launch, a dramatic cliff-top view across the valley. Families often combine the hike with a walk to nearby Tinker Falls, one of the most picturesque waterfalls in Central NY. Trails are open year-round, though steep sections can be icy in winter.",
            "place_id": None,
            "place_query": "Jones Hill Labrador Hollow trailhead Tully NY"
        },
        {
            "name": "Wellesley Island State Park (Minna Anthony Common Nature Center Trailhead)",
            "lat": 44.3332,
            "lng": -75.9850,
            "location": "44927 Cross Island Rd, Wellesley Island, NY 13640",
            "region": "Thousand Islands",
            "difficulty_range": "Easy–Moderate",
            "season": "Spring–Fall",
            "description": "Nature center trailhead with family-friendly loops exploring forests, wetlands, and St. Lawrence River overlooks.",
            "full_description": "The Minna Anthony Common Nature Center is the premier hiking hub in the Thousand Islands. Trails range from short half-mile loops to longer circuits exploring the park's forests, meadows, and shoreline. Kids enjoy spotting bald eagles and great blue herons, while interpretive programs and a butterfly house make it especially family-oriented. Open from spring through fall, with some winter use for snowshoeing.",
            "place_id": None,
            "place_query": "Wellesley Island Nature Center trailhead NY"
        },
        {
            "name": "Grass Point State Park Trailhead",
            "lat": 44.3202,
            "lng": -75.9923,
            "location": "42247 Grassy Point Rd, Alexandria Bay, NY 13607",
            "region": "Thousand Islands",
            "difficulty_range": "Easy",
            "season": "Spring–Fall",
            "description": "Small trail system along the St. Lawrence River with views of passing ships and access to shoreline picnic areas.",
            "full_description": "Grass Point State Park provides gentle walking trails along the St. Lawrence River, perfect for young children and families. The trailhead connects to short paths through forest and along the riverbank, with excellent opportunities to view ships navigating the channel. Open spring through fall, the park also features a sandy beach and picnic areas, making it a relaxed stop for light hiking and riverside play.",
            "place_id": None,
            "place_query": "Grass Point State Park trailhead Alexandria Bay NY"
        },
        {
            "name": "Whetstone Gulf State Park Trailhead",
            "lat": 43.7351,
            "lng": -75.4137,
            "location": "6065 W Road, Lowville, NY 13367",
            "region": "Tug Hill Plateau",
            "difficulty_range": "Moderate",
            "season": "Spring–Fall",
            "description": "Trailhead for rim and gorge trails circling a dramatic 3-mile canyon carved into the Tug Hill Plateau.",
            "full_description": "Whetstone Gulf State Park features one of the most scenic gorges in upstate New York, a 3-mile canyon cut into the Tug Hill Plateau. From the main trailhead, hikers can take rim trails along the canyon edge with constant overlooks, or descend into the gorge itself. Trails are about 5 miles round trip and moderately challenging. Open spring through fall, it's a hidden gem known for solitude, rugged scenery, and fall colors.",
            "place_id": None,
            "place_query": "Whetstone Gulf State Park trailhead Lowville NY"
        },
        {
            "name": "Black River Trailhead",
            "lat": 43.9856,
            "lng": -75.9097,
            "location": "Waterworks Park, Watertown, NY 13601",
            "region": "North Country",
            "difficulty_range": "Easy",
            "season": "Year-round",
            "description": "Trailhead for a paved, family-friendly riverside path along the Black River in Watertown.",
            "full_description": "The Black River Trail offers a 4.5-mile paved multi-use path starting from Waterworks Park in Watertown. It follows the Black River through forested sections and along the riverbank, with benches and interpretive signs along the way. While not a wilderness hike, it is highly popular with walkers, joggers, and families seeking an accessible outdoor experience in the North Country. Open year-round, the trail is especially beautiful in autumn and is frequented by birdwatchers.",
            "place_id": None,
            "place_query": "Black River Trailhead Watertown NY"
        },
        {
            "name": "Point au Roche State Park Trailhead",
            "lat": 44.7574,
            "lng": -73.3956,
            "location": "19 Camp Red Cloud Rd, Plattsburgh, NY 12901",
            "region": "North Country",
            "difficulty_range": "Easy–Moderate",
            "season": "Year-round",
            "description": "Trailhead for a network of shoreline and forest trails on Lake Champlain north of Plattsburgh.",
            "full_description": "Point au Roche State Park offers more than 12 miles of trails starting from its visitor center trailhead. Paths lead through forest, wetlands, and along the Lake Champlain shoreline, with excellent opportunities for birdwatching and scenic views across the lake to Vermont's Green Mountains. Trails are mostly flat and family-friendly, open year-round, and popular for hiking, running, and cross-country skiing in winter.",
            "place_id": None,
            "place_query": "Point au Roche State Park trailhead Plattsburgh NY"
        }
    ]
    
    print(f"🗺️ Merging final batch of {len(new_trailheads)} trailheads into existing data...")
    
    # Group trailheads by region
    regions_to_add = {}
    for trail in new_trailheads:
        region = trail['region']
        if region not in regions_to_add:
            regions_to_add[region] = []
        regions_to_add[region].append(trail)
    
    total_added = 0
    
    # Process each region
    for region_name, region_trails in regions_to_add.items():
        print(f"\n📍 Processing {region_name} region...")
        
        # Find existing region or create new one
        existing_region = None
        for region in trailheads:
            if region.get('region') == region_name:
                existing_region = region
                break
        
        if existing_region:
            # Add to existing region
            existing_trails = existing_region.get('trails', [])
            existing_names = {trail['name'] for trail in existing_trails}
            
            added_count = 0
            for new_trail in region_trails:
                if new_trail['name'] not in existing_names:
                    existing_trails.append(new_trail)
                    print(f"  ✅ Added: {new_trail['name']}")
                    added_count += 1
                else:
                    print(f"  ⏭️  Already exists: {new_trail['name']}")
            
            existing_region['trails'] = existing_trails
            total_added += added_count
            print(f"  📊 Added {added_count} new trailheads to {region_name} region")
        else:
            # Create new region
            new_region = {
                "region": region_name,
                "trails": region_trails
            }
            trailheads.append(new_region)
            print(f"  ✅ Created new {region_name} region with {len(region_trails)} trailheads")
            total_added += len(region_trails)
    
    print(f"\n📊 Total added: {total_added} new trailheads")
    
    # Save updated data
    with open(trailheads_file, 'w', encoding='utf-8') as f:
        json.dump(trailheads, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Saved to: {trailheads_file}")

if __name__ == "__main__":
    merge_final_trailheads()



