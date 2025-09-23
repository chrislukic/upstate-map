#!/usr/bin/env python3
"""
Add website links to children's activities
"""

import json
from pathlib import Path

def add_website_links():
    # Load children's activities
    children_file = Path(__file__).parent.parent.parent / 'public' / 'data' / 'children.json'
    
    with open(children_file, 'r', encoding='utf-8') as f:
        children = json.load(f)
    
    print(f"📋 Processing {len(children)} children's activities...")
    
    # Website mappings for children's activities
    website_mappings = {
        "Forsyth Nature Center": "https://www.kingston-ny.gov/forsyth-nature-center",
        "The Strong National Museum of Play": "https://www.museumofplay.org/",
        "Rosamond Gifford Zoo": "https://www.rosamondgiffordzoo.org/",
        "Buffalo Zoo": "https://buffalozoo.org/",
        "Seneca Park Zoo": "https://senecaparkzoo.org/",
        "The Wild Center": "https://www.wildcenter.org/",
        "The Wild Animal Park": "https://www.wildanimalpark.com/",
        "Fort Rickey Discovery Zoo": "https://www.fortrickey.com/",
        "Old McDonald's Farm": "https://www.oldmcdonaldsfarm.com/",
        "Adirondack Animal Land": "https://www.adirondackanimalland.com/",
        "Hidden Valley Animal Adventure": "https://www.hiddenvalleyadventure.com/",
        "Explore & More Children's Museum": "https://exploreandmore.org/",
        "Sciencenter": "https://www.sciencenter.org/",
        "Children's Museum at Saratoga": "https://www.cmssny.org/",
        "Discovery Center of the Southern Tier": "https://www.discoverycenter.org/",
        "Legoland New York Resort": "https://www.legoland.com/new-york/",
        "Santa's Workshop": "https://www.northpoleny.com/",
        "Enchanted Forest Water Safari": "https://www.watersafari.com/",
        "Six Flags Great Escape & Hurricane Harbor": "https://www.sixflags.com/greatescape",
        "Seabreeze Amusement Park": "https://seabreeze.com/",
        "Six Flags Darien Lake": "https://www.sixflags.com/darienlake",
        "Niagara Falls State Park": "https://www.niagarafallsstatepark.com/",
        "Watkins Glen State Park": "https://parks.ny.gov/parks/142",
        "Letchworth State Park": "https://parks.ny.gov/parks/79",
        "Boldt Castle (Heart Island)": "https://www.boldtcastle.com/",
        "The Farmers' Museum": "https://www.farmersmuseum.org/",
        "Mid-Hudson Children's Museum (MHCM)": "https://www.mhcm.org/",
        "Animal Adventure Park": "https://www.theanimaladventurepark.com/"
    }
    
    updated_count = 0
    
    for child in children:
        name = child['name']
        if name in website_mappings and not child.get('website'):
            child['website'] = website_mappings[name]
            print(f"  ✅ Added website for: {name}")
            updated_count += 1
        elif name in website_mappings and child.get('website'):
            print(f"  ⏭️  Already has website: {name}")
        else:
            print(f"  ❓ No website mapping found for: {name}")
    
    # Save updated data
    with open(children_file, 'w', encoding='utf-8') as f:
        json.dump(children, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Added {updated_count} website links")
    print(f"💾 Saved to: {children_file}")

if __name__ == "__main__":
    add_website_links()



