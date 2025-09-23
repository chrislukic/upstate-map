#!/usr/bin/env python3
"""
Merge new Finger Lakes and Central NY trailhead data into existing trail-heads.json
"""

import json
from pathlib import Path

def merge_finger_lakes_trailheads():
    # Load existing trailheads data
    trailheads_file = Path(__file__).parent.parent.parent / 'public' / 'data' / 'trail-heads.json'
    
    with open(trailheads_file, 'r', encoding='utf-8') as f:
        trailheads = json.load(f)
    
    # New trailhead data to merge
    new_trailheads = [
        {
            "name": "Buttermilk Falls State Park (Main Entrance)",
            "lat": 42.4177,
            "lng": -76.5234,
            "location": "112 E Buttermilk Falls Rd, Ithaca, NY 14850",
            "region": "Finger Lakes",
            "difficulty_range": "Easy–Moderate",
            "season": "Spring–Fall",
            "description": "Trailhead for the Gorge and Rim Trails, passing a dramatic series of cascades culminating in the 165′ Buttermilk Falls.",
            "full_description": "This popular state park in Ithaca begins right at the parking lot, where Buttermilk Falls tumbles 165 feet into a swimming hole. The Gorge Trail climbs alongside Buttermilk Creek, crossing stone bridges and staircases past a series of smaller cascades, while the Rim Trail offers a quieter return loop through forest. The trails total about 1.5 miles and are suitable for families, though the stairs can be steep. The gorge trails are open seasonally (spring–fall), while the upper park offers picnic areas and additional hiking loops.",
            "place_id": None,
            "place_query": "Buttermilk Falls State Park trailhead Ithaca NY"
        },
        {
            "name": "Fillmore Glen State Park",
            "lat": 42.7379,
            "lng": -76.3965,
            "location": "1686 NY-38, Moravia, NY 13118",
            "region": "Finger Lakes",
            "difficulty_range": "Easy–Moderate",
            "season": "Spring–Fall",
            "description": "Trailhead for gorge paths that follow cascading Glen Creek past multiple waterfalls in a quiet, less-crowded Finger Lakes gorge.",
            "full_description": "Fillmore Glen, near Moravia, is one of the lesser-known but most beautiful Finger Lakes gorge parks. From the main entrance, trails lead into a narrow glen filled with mossy stone, ferns, and five waterfalls. The Gorge Trail is about 2 miles round trip, with stone stairways and footbridges crossing Glen Creek. Highlights include Cowsheds Falls, a picturesque curtain waterfall. Trails are open seasonally (usually May–October), and the park is named after President Millard Fillmore, who was born nearby.",
            "place_id": None,
            "place_query": "Fillmore Glen State Park trailhead Moravia NY"
        },
        {
            "name": "Cascadilla Gorge Trail",
            "lat": 42.4407,
            "lng": -76.4840,
            "location": "College Ave & Court St, Ithaca, NY 14850",
            "region": "Finger Lakes",
            "difficulty_range": "Easy–Moderate",
            "season": "Spring–Fall",
            "description": "Scenic stone stairway trail connecting downtown Ithaca to Cornell University via a gorge with eight waterfalls.",
            "full_description": "This urban gorge trail begins near downtown Ithaca and climbs 0.6 miles to Cornell's campus along Cascadilla Creek. The stone path, maintained with stairways and bridges, passes eight waterfalls ranging from 8 to 80 feet tall. Though short, the trail is steep with over 400 stone steps, making it a fun workout and a dramatic walk to campus. It is open seasonally due to icy conditions in winter and is one of the most popular short gorge hikes in Ithaca.",
            "place_id": None,
            "place_query": "Cascadilla Gorge trailhead Ithaca NY"
        },
        {
            "name": "Clark Reservation State Park",
            "lat": 42.9981,
            "lng": -76.0827,
            "location": "6105 E Seneca Turnpike, Jamesville, NY 13078",
            "region": "Central NY",
            "difficulty_range": "Easy–Moderate",
            "season": "Year-round",
            "description": "Trailhead around a glacial lake surrounded by limestone cliffs, with diverse trails and a scenic overlook.",
            "full_description": "Clark Reservation, just south of Syracuse, features a dramatic glacial plunge basin lake bordered by cliffs and forest. From the main parking area, trails range from easy lake loops to rocky cliffside scrambles. The Long Trail provides a dramatic overlook of the lake and valley, while shorter paths allow for family-friendly walks. Open year-round, it's especially popular for spring wildflowers and fall foliage. Interpretive signage explains the rare geology and ecosystems preserved in the park.",
            "place_id": None,
            "place_query": "Clark Reservation State Park trailhead Jamesville NY"
        },
        {
            "name": "Highland Forest (Skyline Trailhead)",
            "lat": 42.8657,
            "lng": -75.9711,
            "location": "1254 Highland Park Rd, Fabius, NY 13063",
            "region": "Central NY",
            "difficulty_range": "Easy–Hard",
            "season": "Year-round",
            "description": "Large county forest park with over 20 miles of hiking trails through rolling hills, fields, and forest.",
            "full_description": "Highland Forest, known as the 'Adirondacks of Central New York,' offers a vast trail network starting from its Skyline Lodge. Trails range from easy meadow loops to the 8.6-mile Main Trail that circles the park. The terrain is gently rolling, making it accessible for families but also appealing to long-distance hikers. The park is open year-round, with trails used for hiking in warm months and cross-country skiing in winter.",
            "place_id": None,
            "place_query": "Highland Forest trailhead Fabius NY"
        },
        {
            "name": "Clark Reservation State Park (Cliff Trailhead)",
            "lat": 42.9968,
            "lng": -76.0823,
            "location": "6105 E Seneca Turnpike, Jamesville, NY 13078",
            "region": "Central NY",
            "difficulty_range": "Moderate",
            "season": "Year-round",
            "description": "Trailhead to the rocky Cliff Trail offering views over the glacial lake basin.",
            "full_description": "The Cliff Trail is the most challenging path in Clark Reservation, beginning near the park's visitor center. It scrambles along the rim of limestone cliffs with dramatic views down to Glacier Lake. Though short, it is rugged and rocky, offering a taste of wilderness close to Syracuse. Families with adventurous kids often enjoy it as a mini climbing challenge. Open all year but can be icy in winter.",
            "place_id": None,
            "place_query": "Cliff Trailhead Clark Reservation Jamesville NY"
        },
        {
            "name": "Onondaga Lake Park West Shore Trailhead",
            "lat": 43.0986,
            "lng": -76.2214,
            "location": "3957 Long Branch Rd, Liverpool, NY 13090",
            "region": "Central NY",
            "difficulty_range": "Easy",
            "season": "Year-round",
            "description": "Paved, stroller- and bike-friendly trail along the western shore of Onondaga Lake.",
            "full_description": "This popular multi-use path begins at the Long Branch parking area and follows Onondaga Lake's shoreline for several miles. The West Shore Trail is level, paved, and perfect for families with small children or strollers. While not a mountain hike, it is one of Central NY's most popular walking and running trails, offering lake views, wetlands, and birdwatching opportunities. Open all year, with restrooms and picnic areas nearby.",
            "place_id": None,
            "place_query": "Onondaga Lake Park West Shore trailhead Liverpool NY"
        }
    ]
    
    print(f"🏞️ Merging {len(new_trailheads)} new Finger Lakes and Central NY trailheads into existing data...")
    
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
    merge_finger_lakes_trailheads()



