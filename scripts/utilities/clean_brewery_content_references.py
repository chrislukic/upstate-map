#!/usr/bin/env python3
"""
Clean content reference artifacts from brewery descriptions
- Removes :contentReference[oaicite:X]{index=X} patterns
- Cleans up any other AI-generated artifacts
"""

import json
import re
from pathlib import Path
from typing import List, Dict, Any

def load_json_file(filepath) -> List[Dict[str, Any]]:
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

def save_json_file(filepath, data: List[Dict[str, Any]]) -> None:
    """Save JSON data to file"""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def clean_content_references(text: str) -> str:
    """Remove content reference artifacts from text"""
    if not text:
        return text
    
    # Remove :contentReference[oaicite:X]{index=X} patterns
    text = re.sub(r':contentReference\[oaicite:\d+\]\{index=\d+\}', '', text)
    
    # Remove any remaining artifacts that might look like citations
    text = re.sub(r'\[oaicite:\d+\]', '', text)
    text = re.sub(r'\{index=\d+\}', '', text)
    
    # Clean up any double spaces or trailing punctuation
    text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces with single space
    text = re.sub(r'\s*\.\s*$', '.', text)  # Clean up trailing periods
    text = re.sub(r'\s*,\s*$', '', text)  # Remove trailing commas
    
    return text.strip()

def clean_brewery_descriptions(breweries: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Clean content references from all brewery text fields"""
    
    cleaned_count = 0
    
    for brewery in breweries:
        original_brewery = brewery.copy()
        
        # Clean description field
        if 'description' in brewery and brewery['description']:
            brewery['description'] = clean_content_references(brewery['description'])
        
        # Clean full_description field
        if 'full_description' in brewery and brewery['full_description']:
            brewery['full_description'] = clean_content_references(brewery['full_description'])
        
        # Clean short_description field if it exists
        if 'short_description' in brewery and brewery['short_description']:
            brewery['short_description'] = clean_content_references(brewery['short_description'])
        
        # Clean specialty field
        if 'specialty' in brewery and brewery['specialty']:
            brewery['specialty'] = clean_content_references(brewery['specialty'])
        
        # Clean visitor_experience field
        if 'visitor_experience' in brewery and brewery['visitor_experience']:
            brewery['visitor_experience'] = clean_content_references(brewery['visitor_experience'])
        
        # Check if any changes were made
        if brewery != original_brewery:
            cleaned_count += 1
            print(f"[CLEANED] {brewery.get('name', 'Unknown')}")
    
    print(f"\n[CLEANING SUMMARY]")
    print(f"Total breweries processed: {len(breweries)}")
    print(f"Breweries cleaned: {cleaned_count}")
    
    return breweries

def main():
    """Main function to clean brewery content references"""
    
    # File paths
    script_dir = Path(__file__).parent
    project_root = script_dir.parent.parent
    breweries_file = project_root / 'public' / 'data' / 'breweries.json'
    
    print("Starting brewery content reference cleanup...")
    
    # Load existing breweries
    breweries = load_json_file(breweries_file)
    if not breweries:
        print(f"Could not load breweries from {breweries_file}")
        return
    
    print(f"Loaded {len(breweries)} breweries")
    
    # Clean content references
    cleaned_breweries = clean_brewery_descriptions(breweries)
    
    # Save cleaned data
    save_json_file(breweries_file, cleaned_breweries)
    print(f"\n[SUCCESS] Cleaned brewery data saved to {breweries_file}")

if __name__ == "__main__":
    main()
