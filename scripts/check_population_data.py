#!/usr/bin/env python3
"""
Check Population Data Script

This script analyzes the population data in the cities to identify potential
issues with population figures that might be too high or too low.

Usage:
    python check_population_data.py
"""

import json
from pathlib import Path

def check_population_data():
    """Check population data for potential issues"""
    data_dir = Path(__file__).parent.parent / "public" / "data"
    map_data_path = data_dir / "map-data.json"
    
    print("Population Data Analysis")
    print("=" * 50)
    
    with open(map_data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    cities = data.get('cities', [])
    if not cities:
        print("No cities found in map-data.json")
        return
    
    print(f"Analyzing {len(cities)} cities...")
    print()
    
    # Sort cities by population
    cities_by_pop = sorted(cities, key=lambda x: x.get('population', 0), reverse=True)
    
    print("Cities with highest populations (might be town vs village issue):")
    print("-" * 60)
    for i, city in enumerate(cities_by_pop[:10]):
        name = city.get('name', 'Unknown')
        pop = city.get('population', 0)
        scenic_area = city.get('scenicArea', '')
        print(f"{i+1:2d}. {name:20s} - {pop:6,} ({scenic_area})")
    
    print()
    print("Cities with lowest populations:")
    print("-" * 60)
    for i, city in enumerate(cities_by_pop[-10:]):
        name = city.get('name', 'Unknown')
        pop = city.get('population', 0)
        scenic_area = city.get('scenicArea', '')
        print(f"{i+1:2d}. {name:20s} - {pop:6,} ({scenic_area})")
    
    print()
    print("Cities that might have incorrect populations:")
    print("-" * 60)
    
    # Flag potentially incorrect populations
    suspicious_cities = []
    
    for city in cities:
        name = city.get('name', 'Unknown')
        pop = city.get('population', 0)
        scenic_area = city.get('scenicArea', '')
        
        # Flag cities with very high populations for small towns
        if pop > 50000:
            suspicious_cities.append((name, pop, scenic_area, "Very high population"))
        # Flag cities with very low populations
        elif pop < 500:
            suspicious_cities.append((name, pop, scenic_area, "Very low population"))
        # Flag specific known issues
        elif name == "Dryden" and pop > 5000:
            suspicious_cities.append((name, pop, scenic_area, "Should be ~1,887 (village)"))
    
    if suspicious_cities:
        for name, pop, scenic_area, reason in suspicious_cities:
            print(f"• {name:20s} - {pop:6,} ({reason})")
    else:
        print("No obviously suspicious populations found.")
    
    print()
    print("Population distribution:")
    print("-" * 60)
    
    # Count cities by population ranges
    ranges = [
        (0, 1000, "Under 1,000"),
        (1000, 5000, "1,000 - 5,000"),
        (5000, 10000, "5,000 - 10,000"),
        (10000, 25000, "10,000 - 25,000"),
        (25000, 50000, "25,000 - 50,000"),
        (50000, float('inf'), "Over 50,000")
    ]
    
    for min_pop, max_pop, label in ranges:
        count = sum(1 for city in cities if min_pop <= city.get('population', 0) < max_pop)
        print(f"{label:20s}: {count:2d} cities")
    
    print()
    print("Recommendations:")
    print("-" * 60)
    print("1. Check if populations are for villages vs. towns")
    print("2. Verify data source (Census 2020 vs. older data)")
    print("3. Consider using village populations for better accuracy")
    print("4. Update Dryden from 14,000 to ~1,887 (village population)")

if __name__ == "__main__":
    check_population_data()

