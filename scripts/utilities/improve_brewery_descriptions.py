#!/usr/bin/env python3
"""
Improve brewery short descriptions to be more concise and meaningful
- Create better short descriptions (10-20 words) for mouseover
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

def create_improved_short_description(brewery: Dict[str, Any]) -> str:
    """Create an improved short description (10-20 words) from brewery data"""
    
    name = brewery.get('name', '')
    location = brewery.get('location', '')
    specialty = brewery.get('specialty', '')
    full_desc = brewery.get('full_description', '')
    
    # Extract location city/region
    location_parts = location.split(',')
    city = location_parts[0].strip() if location_parts else ""
    region = location_parts[1].strip() if len(location_parts) > 1 else ""
    
    # Create specialty summary (first 6-8 words)
    specialty_words = specialty.split()[:8] if specialty else []
    specialty_text = " ".join(specialty_words) if specialty_words else ""
    
    # Try different approaches based on available data
    
    # Approach 1: Use specialty + location
    if specialty_text and city:
        if len(specialty_text.split()) <= 12:
            return f"{specialty_text} in {city}"
    
    # Approach 2: Extract key info from full description
    if full_desc:
        # Look for key phrases
        key_phrases = [
            "farm brewery", "brewpub", "microbrewery", "craft brewery", "cidery", "distillery",
            "Belgian-style", "IPAs", "lagers", "sours", "stouts", "farmhouse ales"
        ]
        
        found_phrases = []
        for phrase in key_phrases:
            if phrase.lower() in full_desc.lower():
                found_phrases.append(phrase)
        
        if found_phrases and city:
            main_phrase = found_phrases[0]
            return f"{main_phrase} in {city}"
    
    # Approach 3: Use name + key descriptor
    if city:
        # Extract key descriptor from specialty or description
        if "farm" in specialty.lower() or "farm" in full_desc.lower():
            return f"Farm brewery in {city}"
        elif "pub" in name.lower() or "pub" in specialty.lower():
            return f"Brewpub in {city}"
        elif "cider" in name.lower() or "cider" in specialty.lower():
            return f"Cidery in {city}"
        else:
            return f"Craft brewery in {city}"
    
    # Fallback: Use first 15 words of specialty or description
    source_text = specialty if specialty else full_desc
    if source_text:
        words = source_text.split()[:15]
        return " ".join(words)
    
    return "Craft brewery"

def improve_brewery_descriptions(breweries: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Improve short descriptions for all breweries"""
    
    improved_count = 0
    
    for brewery in breweries:
        if 'full_description' in brewery:
            old_short = brewery.get('description', '')
            new_short = create_improved_short_description(brewery)
            
            if old_short != new_short:
                brewery['description'] = new_short
                improved_count += 1
                print(f"[IMPROVED] {brewery.get('name', 'Unknown')}")
                print(f"  Old: {old_short}")
                print(f"  New: {new_short}")
                print()
    
    print(f"\n[IMPROVEMENT SUMMARY]")
    print(f"Total breweries processed: {len(breweries)}")
    print(f"Descriptions improved: {improved_count}")
    
    return breweries

def main():
    """Main function to improve brewery descriptions"""
    
    # File paths
    breweries_file = '../../public/data/breweries.json'
    
    print("Starting brewery description improvement...")
    
    # Load existing breweries
    breweries = load_json_file(breweries_file)
    if not breweries:
        print(f"Could not load breweries from {breweries_file}")
        return
    
    print(f"Loaded {len(breweries)} breweries")
    
    # Improve descriptions
    improved_breweries = improve_brewery_descriptions(breweries)
    
    # Save improved data
    save_json_file(breweries_file, improved_breweries)
    print(f"\n[SUCCESS] Improved brewery data saved to {breweries_file}")

if __name__ == "__main__":
    main()


