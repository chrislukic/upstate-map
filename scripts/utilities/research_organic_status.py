#!/usr/bin/env python3
"""
Research and update organic status for PYO farms.
This script provides a framework for researching and updating organic certification status.
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

def display_farm_info(farm):
    """Display farm information for research."""
    print(f"\n{'='*60}")
    print(f"Farm: {farm.get('name', 'Unknown')}")
    print(f"Address: {farm.get('address', 'Unknown')}")
    print(f"Website: {farm.get('website', 'No website')}")
    print(f"Current Organic Status: {farm.get('organic', 'Not set')}")
    print(f"Notes: {farm.get('notes', 'No notes')}")
    print(f"{'='*60}")

def research_organic_status():
    """Interactive research session for organic status."""
    # Get project root directory
    project_root = Path(__file__).parent.parent.parent
    
    # File paths
    apples_file = project_root / 'public' / 'data' / 'pyo_apples.json'
    strawberries_file = project_root / 'public' / 'data' / 'pyo_strawberries.json'
    
    print("PYO Farm Organic Status Research Tool")
    print("="*50)
    
    # Load data
    apples_data = load_json_file(apples_file)
    strawberries_data = load_json_file(strawberries_file)
    
    if not apples_data or not strawberries_data:
        print("Error loading data files")
        return
    
    # Combine all farms for research
    all_farms = []
    for farm in apples_data:
        farm['file_type'] = 'apples'
        all_farms.append(farm)
    
    for farm in strawberries_data:
        farm['file_type'] = 'strawberries'
        all_farms.append(farm)
    
    # Filter farms that need research (not already confirmed organic)
    farms_to_research = [farm for farm in all_farms if not farm.get('organic', False)]
    
    print(f"\nFound {len(farms_to_research)} farms to research for organic status")
    print("Instructions:")
    print("1. For each farm, visit their website and research their organic certification")
    print("2. Enter 'y' if the farm is certified organic")
    print("3. Enter 'n' if the farm is not organic")
    print("4. Enter 's' to skip this farm")
    print("5. Enter 'q' to quit")
    
    for i, farm in enumerate(farms_to_research, 1):
        display_farm_info(farm)
        
        while True:
            response = input(f"\n[{i}/{len(farms_to_research)}] Is this farm organic? (y/n/s/q): ").lower().strip()
            
            if response == 'q':
                print("Exiting research session...")
                return
            elif response == 's':
                print("Skipping this farm...")
                break
            elif response == 'y':
                farm['organic'] = True
                print(f"✅ Marked {farm['name']} as organic")
                break
            elif response == 'n':
                farm['organic'] = False
                print(f"❌ Marked {farm['name']} as not organic")
                break
            else:
                print("Please enter 'y', 'n', 's', or 'q'")
    
    # Save updated data
    print("\nSaving updated data...")
    
    # Separate back into original files
    updated_apples = [farm for farm in all_farms if farm['file_type'] == 'apples']
    updated_strawberries = [farm for farm in all_farms if farm['file_type'] == 'strawberries']
    
    # Remove the temporary file_type field
    for farm in updated_apples:
        del farm['file_type']
    for farm in updated_strawberries:
        del farm['file_type']
    
    # Save files
    if save_json_file(apples_file, updated_apples):
        print(f"✅ Updated {apples_file.name}")
    else:
        print(f"❌ Failed to update {apples_file.name}")
    
    if save_json_file(strawberries_file, updated_strawberries):
        print(f"✅ Updated {strawberries_file.name}")
    else:
        print(f"❌ Failed to update {strawberries_file.name}")
    
    print("\nResearch session complete!")

def show_organic_summary():
    """Show summary of current organic status."""
    # Get project root directory
    project_root = Path(__file__).parent.parent.parent
    
    # File paths
    apples_file = project_root / 'public' / 'data' / 'pyo_apples.json'
    strawberries_file = project_root / 'public' / 'data' / 'pyo_strawberries.json'
    
    # Load data
    apples_data = load_json_file(apples_file)
    strawberries_data = load_json_file(strawberries_file)
    
    if not apples_data or not strawberries_data:
        print("Error loading data files")
        return
    
    print("Current Organic Status Summary")
    print("="*40)
    
    # Apple orchards
    organic_apples = [farm for farm in apples_data if farm.get('organic', False)]
    print(f"\nApple Orchards:")
    print(f"  Total: {len(apples_data)}")
    print(f"  Organic: {len(organic_apples)}")
    print(f"  Non-organic: {len(apples_data) - len(organic_apples)}")
    
    if organic_apples:
        print("  Organic farms:")
        for farm in organic_apples:
            print(f"    - {farm['name']}")
    
    # Strawberry farms
    organic_strawberries = [farm for farm in strawberries_data if farm.get('organic', False)]
    print(f"\nStrawberry Farms:")
    print(f"  Total: {len(strawberries_data)}")
    print(f"  Organic: {len(organic_strawberries)}")
    print(f"  Non-organic: {len(strawberries_data) - len(organic_strawberries)}")
    
    if organic_strawberries:
        print("  Organic farms:")
        for farm in organic_strawberries:
            print(f"    - {farm['name']}")

def main():
    """Main function."""
    if len(sys.argv) > 1 and sys.argv[1] == 'summary':
        show_organic_summary()
    else:
        research_organic_status()

if __name__ == "__main__":
    main()
