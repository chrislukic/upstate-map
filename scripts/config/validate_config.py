#!/usr/bin/env python3
"""
Configuration validation utility
Validates all configuration files against their JSON schemas
"""

import sys
import json
from pathlib import Path
from typing import Dict, Any, List, Tuple

# Add the config directory to the path
sys.path.append(str(Path(__file__).parent))

from schemas import validate_config, get_schema, SCHEMAS
from loader import load_config, CONFIG_DIR

def validate_all_configs() -> Tuple[bool, List[str]]:
    """
    Validate all configuration files
    
    Returns:
        Tuple of (all_valid, error_messages)
    """
    all_valid = True
    all_errors = []
    
    print("🔍 Validating configuration files...")
    print("=" * 50)
    
    for config_name in SCHEMAS.keys():
        config_file = CONFIG_DIR / f"{config_name}.json"
        
        print(f"\n📋 Validating {config_name}.json...")
        
        if not config_file.exists():
            error_msg = f"Configuration file not found: {config_file}"
            print(f"  ❌ {error_msg}")
            all_errors.append(error_msg)
            all_valid = False
            continue
        
        try:
            # Load configuration
            config = load_config(config_name, validate_schema=False)
            
            # Validate against schema
            is_valid, errors = validate_config(config, config_name)
            
            if is_valid:
                print(f"  ✅ Valid")
            else:
                print(f"  ❌ Validation failed:")
                for error in errors:
                    print(f"    - {error}")
                    all_errors.append(f"{config_name}.json: {error}")
                all_valid = False
                
        except Exception as e:
            error_msg = f"Error loading {config_name}.json: {e}"
            print(f"  ❌ {error_msg}")
            all_errors.append(error_msg)
            all_valid = False
    
    return all_valid, all_errors

def validate_single_config(config_name: str) -> Tuple[bool, List[str]]:
    """
    Validate a single configuration file
    
    Args:
        config_name: Name of the configuration to validate
    
    Returns:
        Tuple of (is_valid, error_messages)
    """
    if config_name not in SCHEMAS:
        return False, [f"Unknown configuration: {config_name}. Available: {', '.join(SCHEMAS.keys())}"]
    
    config_file = CONFIG_DIR / f"{config_name}.json"
    
    if not config_file.exists():
        return False, [f"Configuration file not found: {config_file}"]
    
    try:
        config = load_config(config_name, validate_schema=False)
        return validate_config(config, config_name)
    except Exception as e:
        return False, [f"Error loading {config_name}.json: {e}"]

def check_required_dependencies() -> bool:
    """
    Check if required dependencies are available
    
    Returns:
        True if all dependencies are available
    """
    print("🔧 Checking dependencies...")
    
    try:
        import jsonschema
        print("  ✅ jsonschema package available")
        return True
    except ImportError:
        print("  ❌ jsonschema package not found")
        print("  💡 Install with: pip install jsonschema")
        return False

def main():
    """Main validation function"""
    print("🔍 Configuration Validation Tool")
    print("=" * 50)
    
    # Check dependencies
    if not check_required_dependencies():
        return 1
    
    # Parse command line arguments
    if len(sys.argv) > 1:
        config_name = sys.argv[1]
        print(f"\n📋 Validating single configuration: {config_name}")
        is_valid, errors = validate_single_config(config_name)
        
        if is_valid:
            print(f"✅ {config_name}.json is valid")
            return 0
        else:
            print(f"❌ {config_name}.json validation failed:")
            for error in errors:
                print(f"  - {error}")
            return 1
    else:
        # Validate all configurations
        all_valid, all_errors = validate_all_configs()
        
        print("\n" + "=" * 50)
        if all_valid:
            print("🎉 All configuration files are valid!")
            return 0
        else:
            print("❌ Configuration validation failed:")
            for error in all_errors:
                print(f"  - {error}")
            return 1

if __name__ == "__main__":
    sys.exit(main())




