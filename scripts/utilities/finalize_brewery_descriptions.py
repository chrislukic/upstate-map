#!/usr/bin/env python3
"""
Finalize brewery short descriptions to be clean and concise
- Create clean short descriptions (10-20 words) for mouseover
- Keep full descriptions for click
"""

import json
import re
import os
from typing import List, Dict, Any

def load_json_file(filepath: str) -> List[Dict[str, Any]]:
    """Load JSON data from file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"File not found: {filepath}")
        return []
    except json.JSONDecodeError as e:
        print(f"JSON decode error in {filepath}: {e}")
        return []

def save_json_file(filepath: str, data: List[Dict[str, Any]]) -> None:
    """Save JSON data to file"""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def create_final_short_description(brewery: Dict[str, Any]) -> str:
    """Create a final, clean short description (10-20 words) from brewery data"""
    
    name = brewery.get('name', '')
    location = brewery.get('location', '')
    specialty = brewery.get('specialty', '')
    
    # Extract location city
    location_parts = location.split(',')
    city = location_parts[0].strip() if location_parts else ""
    
    # Create clean specialty summary
    if specialty:
        # Remove parenthetical content and clean up
        specialty_clean = re.sub(r'\([^)]*\)', '', specialty)
        specialty_clean = re.sub(r'\s+', ' ', specialty_clean).strip()
        
        # Take first 8-12 words
        words = specialty_clean.split()[:12]
        specialty_text = " ".join(words)
        
        # If it ends with a comma or incomplete word, clean it up
        if specialty_text.endswith(',') or specialty_text.endswith(';'):
            specialty_text = specialty_text[:-1]
        
        # Add location
        if city and len(specialty_text.split()) <= 15:
            return f"{specialty_text} in {city}"
    
    # Fallback: Create simple description based on name and type
    if city:
        if "cider" in name.lower():
            return f"Hard cider and apple products in {city}"
        elif "farm" in name.lower() or "farm" in specialty.lower():
            return f"Farm brewery with local ingredients in {city}"
        elif "pub" in name.lower():
            return f"Brewpub with food and beer in {city}"
        else:
            return f"Craft brewery in {city}"
    
    return "Craft brewery"

def finalize_brewery_descriptions(breweries: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Finalize short descriptions for all breweries"""
    
    finalized_count = 0
    
    for brewery in breweries:
        if 'full_description' in brewery:
            old_short = brewery.get('description', '')
            new_short = create_final_short_description(brewery)
            
            if old_short != new_short:
                brewery['description'] = new_short
                finalized_count += 1
                print(f"[FINALIZED] {brewery.get('name', 'Unknown')}")
                print(f"  New: {new_short}")
                print()
    
    print(f"\n[FINALIZATION SUMMARY]")
    print(f"Total breweries processed: {len(breweries)}")
    print(f"Descriptions finalized: {finalized_count}")
    
    return breweries

def main():
    """Main function to finalize brewery descriptions"""
    
    # File paths
    breweries_file = '../../public/data/breweries.json'
    
    print("Starting brewery description finalization...")
    
    # Load existing breweries
    breweries = load_json_file(breweries_file)
    if not breweries:
        print(f"Could not load breweries from {breweries_file}")
        return
    
    print(f"Loaded {len(breweries)} breweries")
    
    # Finalize descriptions
    finalized_breweries = finalize_brewery_descriptions(breweries)
    
    # Save finalized data
    save_json_file(breweries_file, finalized_breweries)
    print(f"\n[SUCCESS] Finalized brewery data saved to {breweries_file}")

if __name__ == "__main__":
    main()


