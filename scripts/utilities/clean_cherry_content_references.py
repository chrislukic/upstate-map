#!/usr/bin/env python3
"""
Clean content reference artifacts from cherry farms data.
This script removes patterns like :contentReference[oaicite:X]{index=X} from text fields.
"""

import json
import re
from pathlib import Path

def load_json_file(file_path):
    """Load JSON data from file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return None

def save_json_file(file_path, data):
    """Save JSON data to file."""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error saving {file_path}: {e}")
        return False

def clean_content_references(text):
    """Remove content reference artifacts from text."""
    if not isinstance(text, str):
        return text
    
    # Remove :contentReference[oaicite:X]{index=X} patterns
    cleaned = re.sub(r':contentReference\[oaicite:\d+\]\{index=\d+\}', '', text)
    
    # Clean up any double spaces or periods that might be left
    cleaned = re.sub(r'\s+', ' ', cleaned)  # Replace multiple spaces with single space
    cleaned = re.sub(r'\.\s*\.', '.', cleaned)  # Remove double periods
    cleaned = cleaned.strip()
    
    return cleaned

def clean_cherry_farms(data):
    """Clean content references from all cherry farms."""
    if not isinstance(data, list):
        print("Error: Expected list of farms")
        return data
    
    cleaned_count = 0
    
    for farm in data:
        farm_cleaned = False
        
        # Clean text fields that might contain content references
        text_fields = ['notes', 'reservation_required', 'description']
        
        for field in text_fields:
            if field in farm and farm[field]:
                original = farm[field]
                cleaned = clean_content_references(original)
                if original != cleaned:
                    farm[field] = cleaned
                    farm_cleaned = True
                    print(f"  Cleaned {field} for {farm.get('name', 'Unknown')}")
        
        if farm_cleaned:
            cleaned_count += 1
    
    print(f"\nCleaned content references from {cleaned_count} farms")
    return data

def main():
    """Main function."""
    print("Cleaning content references from cherry farms data...")
    
    # Get project root directory
    project_root = Path(__file__).parent.parent.parent
    
    # File path
    cherries_file = project_root / 'public' / 'data' / 'pyo_cherries.json'
    
    # Load current data
    print(f"Loading data from {cherries_file.name}...")
    farms_data = load_json_file(cherries_file)
    
    if not farms_data:
        print("Failed to load cherry farms data")
        return
    
    # Clean the data
    cleaned_data = clean_cherry_farms(farms_data)
    
    # Save updated data
    print(f"\nSaving cleaned data to {cherries_file.name}...")
    if save_json_file(cherries_file, cleaned_data):
        print("✅ Successfully cleaned cherry farms data")
    else:
        print("❌ Failed to save cleaned data")

if __name__ == "__main__":
    main()
