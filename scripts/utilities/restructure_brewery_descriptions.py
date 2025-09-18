#!/usr/bin/env python3
"""
Restructure brewery descriptions into short and full versions
- Create short_description (10-20 words) for mouseover
- Keep existing description as full_description for click
- Preserve all other data
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

def create_short_description(description: str, specialty: str = "", visitor_experience: str = "") -> str:
    """Create a short description (10-20 words) from existing data"""
    if not description:
        return ""
    
    # Try to extract the first meaningful sentence or phrase
    # Remove common opening phrases and get to the core
    text = description.strip()
    
    # Remove common opening phrases
    opening_phrases = [
        "Nestled in", "Located in", "Set on", "Situated on", "Tucked in", "Perched on",
        "Set in", "Built on", "Housed in", "Found in", "Positioned in", "Placed in"
    ]
    
    for phrase in opening_phrases:
        if text.lower().startswith(phrase.lower()):
            # Find the next sentence
            sentences = text.split('.')
            if len(sentences) > 1:
                text = sentences[1].strip()
            break
    
    # If we have specialty info, try to incorporate it
    if specialty and len(specialty.split()) <= 15:
        specialty_words = specialty.split()[:8]  # Take first 8 words
        specialty_text = " ".join(specialty_words)
        
        # Try to find a location or key detail from description
        words = text.split()
        if len(words) > 10:
            # Take first 8-12 words that aren't common filler words
            filler_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
            meaningful_words = [w for w in words[:15] if w.lower() not in filler_words]
            if len(meaningful_words) >= 6:
                location_text = " ".join(meaningful_words[:8])
                return f"{specialty_text} in {location_text}"
    
    # Fallback: take first 12-15 words
    words = text.split()
    if len(words) <= 20:
        return text
    else:
        # Take first 12-15 words, trying to end at a natural break
        for i in range(12, min(18, len(words))):
            if words[i].endswith(',') or words[i].endswith('.') or words[i].endswith(';'):
                return " ".join(words[:i+1])
        return " ".join(words[:15])

def restructure_brewery_descriptions(breweries: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Restructure brewery data to have short and full descriptions"""
    
    restructured_count = 0
    
    for brewery in breweries:
        if 'description' in brewery and brewery['description']:
            # Create short description
            short_desc = create_short_description(
                brewery['description'],
                brewery.get('specialty', ''),
                brewery.get('visitor_experience', '')
            )
            
            # Move existing description to full_description
            brewery['full_description'] = brewery['description']
            brewery['description'] = short_desc
            
            restructured_count += 1
            print(f"[RESTRUCTURED] {brewery.get('name', 'Unknown')}")
            print(f"  Short: {short_desc}")
            print(f"  Full: {brewery['full_description'][:100]}...")
            print()
    
    print(f"\n[RESTRUCTURE SUMMARY]")
    print(f"Total breweries processed: {len(breweries)}")
    print(f"Breweries restructured: {restructured_count}")
    
    return breweries

def main():
    """Main function to restructure brewery descriptions"""
    
    # File paths
    breweries_file = '../../public/data/breweries.json'
    
    print("Starting brewery description restructuring...")
    
    # Load existing breweries
    breweries = load_json_file(breweries_file)
    if not breweries:
        print(f"Could not load breweries from {breweries_file}")
        return
    
    print(f"Loaded {len(breweries)} breweries")
    
    # Restructure descriptions
    restructured_breweries = restructure_brewery_descriptions(breweries)
    
    # Save restructured data
    save_json_file(breweries_file, restructured_breweries)
    print(f"\n[SUCCESS] Restructured brewery data saved to {breweries_file}")

if __name__ == "__main__":
    main()


