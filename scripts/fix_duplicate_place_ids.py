#!/usr/bin/env python3
"""
Complete Duplicate Place ID Fix Script

This script:
1. Identifies all duplicate place IDs
2. Cleans them from the data files
3. Re-enriches with the fixed enrichment script
4. Verifies no duplicates remain

Usage:
    python fix_duplicate_place_ids.py
"""

import subprocess
import sys
from pathlib import Path

def run_script(script_name, description):
    """Run a Python script and handle errors"""
    print(f"\n{'='*60}")
    print(f"[RUN] {description}")
    print(f"{'='*60}")
    
    script_path = Path(__file__).parent / script_name
    
    try:
        result = subprocess.run([sys.executable, str(script_path)], 
                              capture_output=True, text=True, cwd=Path(__file__).parent)
        
        if result.returncode == 0:
            print(result.stdout)
            print(f"[OK] {description} completed successfully")
            return True
        else:
            print(f"[ERROR] {description} failed:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"[ERROR] Error running {script_name}: {e}")
        return False

def main():
    """Main process to fix duplicate place IDs"""
    print("[FIX] Complete Duplicate Place ID Fix Process")
    print("=" * 60)
    print("This will:")
    print("1. Identify duplicate place IDs")
    print("2. Clean duplicates from data files")
    print("3. Re-enrich with improved algorithm")
    print("4. Verify no duplicates remain")
    print("=" * 60)
    
    # Step 1: Find duplicates
    if not run_script("find_duplicate_place_ids.py", "Finding duplicate place IDs"):
        print("[ERROR] Failed to identify duplicates. Stopping.")
        return
    
    # Step 2: Clean duplicates
    if not run_script("clean_duplicate_place_ids.py", "Cleaning duplicate place IDs"):
        print("[ERROR] Failed to clean duplicates. Stopping.")
        return
    
    # Step 3: Re-enrich with fixed script
    print(f"\n{'='*60}")
    print("[RUN] Re-enriching with fixed algorithm")
    print(f"{'='*60}")
    print("[WARN] This will make API calls to Google Maps. Continue? (y/n): ", end="")
    
    response = input().strip().lower()
    if response != 'y':
        print("[CANCEL] Process cancelled by user")
        return
    
    if not run_script("enrich_with_google_maps_fixed.py", "Re-enriching with fixed algorithm"):
        print("[ERROR] Failed to re-enrich data. Stopping.")
        return
    
    # Step 4: Verify no duplicates remain
    if not run_script("find_duplicate_place_ids.py", "Verifying no duplicates remain"):
        print("[ERROR] Failed to verify results. Please check manually.")
        return
    
    print(f"\n{'='*60}")
    print("[SUCCESS] Duplicate Place ID Fix Complete!")
    print(f"{'='*60}")
    print("All duplicate place IDs have been resolved.")
    print("The data is now ready for deployment.")

if __name__ == "__main__":
    main()
