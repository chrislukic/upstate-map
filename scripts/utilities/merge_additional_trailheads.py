#!/usr/bin/env python3
"""
Merge additional trailhead data (Hudson Valley, Western NY, Tug Hill, Thousand Islands, Southern Tier) into existing trail-heads.json
"""

import json
from pathlib import Path

def merge_additional_trailheads():
    # Load existing trailheads data
    trailheads_file = Path(__file__).parent.parent.parent / 'public' / 'data' / 'trail-heads.json'
    
    with open(trailheads_file, 'r', encoding='utf-8') as f:
        trailheads = json.load(f)
    
    # New trailhead data to merge
    new_trailheads = [
        {
            "name": "Bear Mountain State Park Trailhead (Major Welch Trail)",
            "lat": 41.3128,
            "lng": -74.0058,
            "location": "3006 Seven Lakes Dr, Bear Mountain, NY 10911",
            "region": "Hudson Valley",
            "difficulty_range": "Moderate–Hard",
            "season": "Year-round",
            "description": "Trailhead for the Major Welch Trail, a steep loop to Bear Mountain's summit with sweeping Hudson River views.",
            "full_description": "Bear Mountain is one of the most iconic hikes in the Hudson Valley, with the Major Welch Trail offering a challenging rock-scramble ascent to the summit. The loop is 4 miles round trip and rewards hikers with panoramic views of the Hudson River, Perkins Memorial Tower, and nearby peaks. It's especially popular in fall foliage season. Families often combine this with a visit to the Bear Mountain Zoo or carousel. The trail is open year-round, though icy conditions make winter ascents demanding.",
            "place_id": None,
            "place_query": "Bear Mountain Major Welch trailhead NY"
        },
        {
            "name": "Anthony's Nose Trailhead",
            "lat": 41.3229,
            "lng": -73.9753,
            "location": "US-9D, Cortlandt Manor, NY 10567",
            "region": "Hudson Valley",
            "difficulty_range": "Moderate",
            "season": "Year-round",
            "description": "Trailhead for a short but steep climb to Anthony's Nose, one of the most famous viewpoints over the Hudson River and Bear Mountain Bridge.",
            "full_description": "The Anthony's Nose trail begins from a roadside lot on Route 9D and ascends 1.5 miles to a rocky overlook perched high above the Hudson River. From the summit, hikers enjoy postcard views of the Bear Mountain Bridge, Hudson Highlands, and river valley. Despite its short length, the steep rocky sections give it a moderate rating. It is one of the most popular short hikes in the Hudson Valley, especially for sunrise and sunset.",
            "place_id": None,
            "place_query": "Anthony's Nose trailhead Hudson Valley NY"
        },
        {
            "name": "Minnewaska State Park (Lake Minnewaska Carriage Road Trailhead)",
            "lat": 41.7275,
            "lng": -74.2651,
            "location": "5281 Route 44-55, Kerhonkson, NY 12446",
            "region": "Hudson Valley",
            "difficulty_range": "Easy–Moderate",
            "season": "Year-round",
            "description": "Trailhead for carriage road loops around Lake Minnewaska with dramatic cliffs and Shawangunk views.",
            "full_description": "Minnewaska State Park Preserve is a premier Hudson Valley destination, offering dozens of miles of wide, family-friendly carriage roads. The main trailhead at Lake Minnewaska provides easy access to a 2-mile loop around the cliff-rimmed lake, as well as longer routes to Awosting Falls and Gertrude's Nose. The setting is striking, with white cliffs, dwarf pine barrens, and sweeping views. Open year-round, it's popular for hiking, biking, and cross-country skiing.",
            "place_id": None,
            "place_query": "Lake Minnewaska trailhead Kerhonkson NY"
        },
        {
            "name": "Zoar Valley Multiple Use Area Trailhead",
            "lat": 42.4845,
            "lng": -78.9150,
            "location": "Zoar Valley Rd, Gowanda, NY 14070",
            "region": "Western NY",
            "difficulty_range": "Moderate",
            "season": "Spring–Fall",
            "description": "Trailhead into the wild Zoar Valley gorge, known for towering cliffs, waterfalls, and old-growth forest.",
            "full_description": "The Zoar Valley trailhead gives access to one of the most scenic and ecologically rich areas in Western New York. Trails descend into a deep gorge carved by Cattaraugus Creek, where 400-foot cliffs rise above the river. Visitors can explore waterfalls, giant sycamores, and some of the state's oldest trees. The area is rugged and requires care, but it is beloved by experienced hikers seeking wild beauty. Best visited spring through fall; sections may close in winter for safety.",
            "place_id": None,
            "place_query": "Zoar Valley trailhead Gowanda NY"
        },
        {
            "name": "Allegany State Park (Quaker Area Trailhead)",
            "lat": 42.0626,
            "lng": -78.7601,
            "location": "2373 ASP Route 1, Salamanca, NY 14779",
            "region": "Western NY",
            "difficulty_range": "Easy–Hard",
            "season": "Year-round",
            "description": "Trailhead hub in Allegany State Park's Quaker Area, giving access to miles of forest trails, fire towers, and lake loops.",
            "full_description": "Allegany State Park, the largest state park in New York, offers more than 65,000 acres of forest and trails. The Quaker Area trailheads serve popular hikes like Bear Caves, Mount Tuscarora, and the Quaker Lake loop. Trails range from easy lake walks to strenuous climbs with views across the Allegheny Plateau. The park is open year-round, with hiking in summer and snowshoeing and skiing in winter.",
            "place_id": None,
            "place_query": "Allegany State Park Quaker Area trailhead NY"
        },
        {
            "name": "Southwick Beach State Park Trailhead",
            "lat": 43.7161,
            "lng": -76.1989,
            "location": "8119 Southwick Pl, Henderson, NY 13650",
            "region": "Tug Hill Plateau",
            "difficulty_range": "Easy",
            "season": "Summer–Fall",
            "description": "Trailhead for sandy beach walks and dunes at Southwick Beach, part of a unique freshwater coastal environment.",
            "full_description": "Southwick Beach State Park sits on Lake Ontario's eastern shore, offering access to long sandy beaches and dune trails. The trailhead connects to a network of easy paths through the Lakeview Wildlife Management Area, where visitors can explore rare dune ecosystems and wetlands. It's a family-friendly area best visited in summer and fall. Birdwatchers flock here to see migrating species, while kids enjoy the sandy shoreline and shallow water.",
            "place_id": None,
            "place_query": "Southwick Beach State Park trailhead Henderson NY"
        },
        {
            "name": "Wellesley Island State Park (Minna Anthony Common Nature Center Trailhead)",
            "lat": 44.3332,
            "lng": -75.9850,
            "location": "44927 Cross Island Rd, Wellesley Island, NY 13640",
            "region": "Thousand Islands",
            "difficulty_range": "Easy–Moderate",
            "season": "Spring–Fall",
            "description": "Trailhead at the Minna Anthony Common Nature Center with scenic trails through forest, wetlands, and St. Lawrence River overlooks.",
            "full_description": "This nature center trailhead in Wellesley Island State Park is one of the premier hiking destinations in the Thousand Islands. Trails range from short loops suitable for children to longer routes that explore diverse habitats, including wildflower meadows, wetlands, and rocky river overlooks. Educational exhibits and guided programs make it especially family-friendly. Trails are open spring through fall, with some access in winter for snowshoeing.",
            "place_id": None,
            "place_query": "Wellesley Island Nature Center trailhead NY"
        },
        {
            "name": "Rock City Park Trailhead",
            "lat": 42.0921,
            "lng": -78.4056,
            "location": "505 NY-16, Olean, NY 14760",
            "region": "Southern Tier",
            "difficulty_range": "Easy–Moderate",
            "season": "Spring–Fall",
            "description": "Trailhead to a privately run park with giant rock formations, crevices, and panoramic views over the Southern Tier.",
            "full_description": "Rock City Park near Olean features a trail winding through a remarkable landscape of enormous quartz conglomerate rocks. The formations create narrow passageways and caves that delight children and adventurous hikers. A loop trail explores the boulder field before reaching a scenic overlook with expansive views of the Allegheny Plateau. The park is privately operated, with a small admission fee, and is open seasonally from spring through fall.",
            "place_id": None,
            "place_query": "Rock City Park trailhead Olean NY"
        },
        {
            "name": "Lime Hollow Nature Center Trailhead",
            "lat": 42.5746,
            "lng": -76.2297,
            "location": "338 McLean Rd, Cortland, NY 13045",
            "region": "Southern Tier",
            "difficulty_range": "Easy–Moderate",
            "season": "Year-round",
            "description": "Trailhead for 12 miles of trails through forests, wetlands, and fields at a conservation center in Cortland.",
            "full_description": "The Lime Hollow Nature Center provides year-round hiking opportunities on a 430-acre preserve. Trails explore diverse habitats, including bogs, forests, and meadows. Boardwalks cross wetlands rich in wildlife, and interpretive signage makes it a great destination for families and school groups. The main visitor center has restrooms and maps. Trails are mostly easy, with a few moderate sections, and are open daily throughout the year.",
            "place_id": None,
            "place_query": "Lime Hollow Nature Center trailhead Cortland NY"
        }
    ]
    
    print(f"🗺️ Merging {len(new_trailheads)} additional trailheads into existing data...")
    
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
    merge_additional_trailheads()



