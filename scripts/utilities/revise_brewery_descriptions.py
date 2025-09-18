#!/usr/bin/env python3
"""
Revise brewery full descriptions to be more balanced and concise
- Remove advertising language and hyperbole
- Make descriptions more factual and balanced
- Reduce wordiness while preserving key information
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

def revise_description(description: str) -> str:
    """Revise a description to be more balanced and concise"""
    if not description:
        return description
    
    text = description.strip()
    
    # Remove advertising language and hyperbole
    advertising_phrases = [
        r'\b(legendary|iconic|world-class|exceptional|renowned|famous|stunning|breathtaking|spectacular|amazing|incredible|outstanding|premier|leading|top-tier|must-visit|destination-worthy|quintessential|perfect|ideal|unforgettable|memorable)\b',
        r'\b(truly|absolutely|completely|totally|entirely|perfectly|beautifully|wonderfully|magnificently|gorgeously)\b',
        r'\b(one of the best|among the best|one of the most|some of the best)\b',
        r'\b(not just|more than just|beyond just)\b',
        r'\b(experience|journey|adventure|escape|retreat|oasis|gem|treasure|hidden gem)\b',
        r'\b(immerse|transport|captivate|delight|thrill|amaze|impress|wow)\b'
    ]
    
    for pattern in advertising_phrases:
        text = re.sub(pattern, '', text, flags=re.IGNORECASE)
    
    # Remove excessive descriptive words
    excessive_words = [
        r'\b(beautiful|gorgeous|stunning|picturesque|charming|delightful|lovely|wonderful|fantastic|excellent|superb|outstanding|remarkable|extraordinary|incredible|amazing|spectacular|magnificent|breathtaking|striking|impressive|elegant|refined|sophisticated|rustic|quaint|cozy|intimate|spacious|expansive|dramatic|serene|peaceful|tranquil|vibrant|lively|energetic|dynamic|unique|distinctive|special|exclusive|premium|high-end|luxury|upscale|gourmet|artisanal|handcrafted|carefully crafted|meticulously crafted|expertly crafted|masterfully crafted)\b'
    ]
    
    for pattern in excessive_words:
        text = re.sub(pattern, '', text, flags=re.IGNORECASE)
    
    # Remove redundant phrases
    redundant_phrases = [
        r'\b(offers a|provides a|features a|boasts a|includes a|has a|contains a)\b',
        r'\b(visitors can|guests can|patrons can|customers can|you can|one can)\b',
        r'\b(where you can|where visitors can|where guests can|where patrons can)\b',
        r'\b(all while|while also|while taking|while enjoying|while savoring|while relaxing)\b',
        r'\b(set on|located on|situated on|perched on|nestled on|tucked on)\b',
        r'\b(in the heart of|at the heart of|in the center of|at the center of)\b',
        r'\b(just a|only a|merely a|simply a)\b',
        r'\b(short walk|quick walk|easy walk|convenient walk)\b',
        r'\b(panoramic views|sweeping views|stunning views|beautiful views|scenic views|breathtaking views)\b',
        r'\b(overlooking|with views of|featuring views of|offering views of)\b'
    ]
    
    for pattern in redundant_phrases:
        text = re.sub(pattern, '', text, flags=re.IGNORECASE)
    
    # Simplify complex sentences
    # Replace "not only... but also" constructions
    text = re.sub(r'not only ([^,]+), but also ([^,]+)', r'\1 and \2', text, flags=re.IGNORECASE)
    
    # Replace "both... and" with simpler constructions
    text = re.sub(r'both ([^,]+) and ([^,]+)', r'\1 and \2', text, flags=re.IGNORECASE)
    
    # Remove unnecessary qualifiers
    qualifiers = [
        r'\b(quite|rather|very|extremely|highly|particularly|especially|notably|significantly|considerably|substantially|remarkably|exceptionally|incredibly|amazingly|surprisingly|unexpectedly)\b'
    ]
    
    for pattern in qualifiers:
        text = re.sub(pattern, '', text, flags=re.IGNORECASE)
    
    # Clean up multiple spaces and punctuation
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\s*,\s*', ', ', text)
    text = re.sub(r'\s*\.\s*', '. ', text)
    text = re.sub(r'\s*;\s*', '; ', text)
    text = re.sub(r'\s*:\s*', ': ', text)
    
    # Remove trailing commas and periods
    text = re.sub(r'[,;\.]+$', '', text)
    
    # Ensure proper sentence structure
    if text and not text.endswith('.'):
        text += '.'
    
    # Remove any remaining artifacts
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def revise_brewery_descriptions(breweries: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Revise full descriptions for all breweries"""
    
    revised_count = 0
    
    for brewery in breweries:
        if 'full_description' in brewery and brewery['full_description']:
            old_desc = brewery['full_description']
            new_desc = revise_description(old_desc)
            
            if old_desc != new_desc:
                brewery['full_description'] = new_desc
                revised_count += 1
                print(f"[REVISED] {brewery.get('name', 'Unknown')}")
                print(f"  Old: {old_desc[:100]}...")
                print(f"  New: {new_desc[:100]}...")
                print()
    
    print(f"\n[REVISION SUMMARY]")
    print(f"Total breweries processed: {len(breweries)}")
    print(f"Descriptions revised: {revised_count}")
    
    return breweries

def main():
    """Main function to revise brewery descriptions"""
    
    # File paths
    breweries_file = '../../public/data/breweries.json'
    
    print("Starting brewery description revision...")
    
    # Load existing breweries
    breweries = load_json_file(breweries_file)
    if not breweries:
        print(f"Could not load breweries from {breweries_file}")
        return
    
    print(f"Loaded {len(breweries)} breweries")
    
    # Revise descriptions
    revised_breweries = revise_brewery_descriptions(breweries)
    
    # Save revised data
    save_json_file(breweries_file, revised_breweries)
    print(f"\n[SUCCESS] Revised brewery data saved to {breweries_file}")

if __name__ == "__main__":
    main()


