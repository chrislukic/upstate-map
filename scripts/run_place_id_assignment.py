#!/usr/bin/env python3
"""
Simple wrapper script to run place ID assignment with environment variable support.
"""

import os
import sys
from pathlib import Path

# Add the current directory to Python path
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))

from assign_place_ids import PlaceIDAssigner

def main():
    """Run place ID assignment with environment variable support."""
    
    # Get API key from environment variable or prompt user
    api_key = os.getenv('GOOGLE_PLACES_API_KEY')
    
    if not api_key:
        print("Google Places API key not found in environment variable GOOGLE_PLACES_API_KEY")
        print("Please set it with: export GOOGLE_PLACES_API_KEY='your_api_key_here'")
        print("Or enter it manually:")
        api_key = input("Enter your Google Places API key: ").strip()
        
        if not api_key:
            print("No API key provided. Exiting.")
            return
    
    # Set up paths
    data_dir = script_dir.parent / "public" / "data"
    
    if not data_dir.exists():
        print(f"Data directory not found: {data_dir}")
        return
    
    print(f"Using data directory: {data_dir}")
    print(f"API key: {api_key[:10]}...{api_key[-4:] if len(api_key) > 14 else '***'}")
    
    # Confirm before proceeding
    response = input("\nProceed with place ID assignment? (y/N): ").strip().lower()
    if response != 'y':
        print("Cancelled.")
        return
    
    # Create assigner and process files
    assigner = PlaceIDAssigner(api_key, str(data_dir))
    
    # Process all JSON files
    results = assigner.process_all_files()
    
    # Print summary
    print("\n" + "="*50)
    print("SUMMARY")
    print("="*50)
    
    total_successful = 0
    total_entries = 0
    
    for filename, (successful, total) in results.items():
        print(f"{filename}: {successful}/{total} successful")
        total_successful += successful
        total_entries += total
    
    if total_entries > 0:
        success_rate = total_successful / total_entries * 100
        print(f"\nOverall: {total_successful}/{total_entries} successful")
        print(f"Success rate: {success_rate:.1f}%")
    else:
        print("No entries processed")

if __name__ == "__main__":
    main()
