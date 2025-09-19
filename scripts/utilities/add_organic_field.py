#!/usr/bin/env python3
"""
Add organic field to PYO farms data files.
This script adds an 'organic' field to each farm entry in the JSON files.
"""

import json
import sys
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

def determine_organic_status(farm):
    """Determine if a farm is organic based on existing notes."""
    name = farm.get('name', '').lower()
    notes = farm.get('notes', '').lower()
    
    # Check for explicit organic mentions
    if 'organic' in notes:
        return True
    
    # Known organic farms (based on research)
    known_organic = [
        'fishkill farms'
    ]
    
    if name in known_organic:
        return True
    
    # Default to false for now - can be updated after research
    return False

def add_organic_field_to_farms(data):
    """Add organic field to all farms in the data."""
    if not isinstance(data, list):
        print("Error: Expected list of farms")
        return data
    
    for farm in data:
        if 'organic' not in farm:
            farm['organic'] = determine_organic_status(farm)
            print(f"Added organic field to {farm.get('name', 'Unknown')}: {farm['organic']}")
    
    return data

def main():
    """Main function to process both PYO files."""
    # Get project root directory
    project_root = Path(__file__).parent.parent.parent
    
    # File paths
    apples_file = project_root / 'public' / 'data' / 'pyo_apples.json'
    strawberries_file = project_root / 'public' / 'data' / 'pyo_strawberries.json'
    
    print("Adding organic field to PYO farms...")
    
    # Process apples file
    print(f"\nProcessing {apples_file.name}...")
    apples_data = load_json_file(apples_file)
    if apples_data:
        apples_data = add_organic_field_to_farms(apples_data)
        if save_json_file(apples_file, apples_data):
            print(f"✅ Successfully updated {apples_file.name}")
        else:
            print(f"❌ Failed to save {apples_file.name}")
    
    # Process strawberries file
    print(f"\nProcessing {strawberries_file.name}...")
    strawberries_data = load_json_file(strawberries_file)
    if strawberries_data:
        strawberries_data = add_organic_field_to_farms(strawberries_data)
        if save_json_file(strawberries_file, strawberries_data):
            print(f"✅ Successfully updated {strawberries_file.name}")
        else:
            print(f"❌ Failed to save {strawberries_file.name}")
    
    print("\nOrganic field addition complete!")

if __name__ == "__main__":
    main()
