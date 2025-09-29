#!/usr/bin/env python3
"""
Configuration Health Check Utility
Performs comprehensive health checks on the configuration system
"""

import sys
import os
import requests
from pathlib import Path
from typing import Dict, List, Tuple, Any

# Add the config directory to the path
sys.path.append(str(Path(__file__).parent))

from loader import load_script_config, get_api_key, validate_environment, CONFIG_DIR
from schemas import validate_config, SCHEMAS

class ConfigHealthChecker:
    """Health checker for configuration system"""
    
    def __init__(self):
        self.issues = []
        self.warnings = []
        self.successes = []
    
    def add_issue(self, message: str):
        """Add a critical issue"""
        self.issues.append(message)
    
    def add_warning(self, message: str):
        """Add a warning"""
        self.warnings.append(message)
    
    def add_success(self, message: str):
        """Add a success message"""
        self.successes.append(message)
    
    def check_configuration_files(self) -> bool:
        """Check that all configuration files exist and are valid"""
        print("🔍 Checking configuration files...")
        
        all_valid = True
        
        for config_name in SCHEMAS.keys():
            config_file = CONFIG_DIR / f"{config_name}.json"
            
            if not config_file.exists():
                self.add_issue(f"Configuration file missing: {config_file}")
                all_valid = False
                continue
            
            try:
                # Load and validate configuration
                config = load_script_config(config_name)
                is_valid, errors = validate_config(config, config_name)
                
                if is_valid:
                    self.add_success(f"✅ {config_name}.json is valid")
                else:
                    self.add_issue(f"❌ {config_name}.json validation failed:")
                    for error in errors:
                        self.add_issue(f"  - {error}")
                    all_valid = False
                    
            except Exception as e:
                self.add_issue(f"❌ Error loading {config_name}.json: {e}")
                all_valid = False
        
        return all_valid
    
    def check_environment_variables(self) -> bool:
        """Check required environment variables"""
        print("🔍 Checking environment variables...")
        
        required_vars = ['GOOGLE_MAPS_API_KEY']
        optional_vars = ['OPENAI_API_KEY']
        
        all_present = True
        
        for var in required_vars:
            if not os.getenv(var):
                self.add_issue(f"Required environment variable not set: {var}")
                all_present = False
            else:
                self.add_success(f"✅ {var} is set")
        
        for var in optional_vars:
            if not os.getenv(var):
                self.add_warning(f"Optional environment variable not set: {var}")
            else:
                self.add_success(f"✅ {var} is set")
        
        return all_present
    
    def check_api_keys(self) -> bool:
        """Check API key validity"""
        print("🔍 Checking API keys...")
        
        all_valid = True
        
        # Check Google Maps API key
        google_key = get_api_key('google_maps')
        if google_key:
            if self.test_google_maps_api(google_key):
                self.add_success("✅ Google Maps API key is valid")
            else:
                self.add_issue("❌ Google Maps API key is invalid or quota exceeded")
                all_valid = False
        else:
            self.add_issue("❌ Google Maps API key not found")
            all_valid = False
        
        # Check OpenAI API key
        openai_key = get_api_key('openai')
        if openai_key:
            if self.test_openai_api(openai_key):
                self.add_success("✅ OpenAI API key is valid")
            else:
                self.add_warning("⚠️ OpenAI API key validation failed (may still work)")
        else:
            self.add_warning("⚠️ OpenAI API key not found")
        
        return all_valid
    
    def test_google_maps_api(self, api_key: str) -> bool:
        """Test Google Maps API key with a simple request"""
        try:
            url = "https://maps.googleapis.com/maps/api/geocode/json"
            params = {
                'address': 'New York, NY',
                'key': api_key
            }
            
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            
            return data.get('status') == 'OK'
        except Exception:
            return False
    
    def test_openai_api(self, api_key: str) -> bool:
        """Test OpenAI API key (basic validation)"""
        try:
            # Simple validation - check if key format looks correct
            return api_key.startswith('sk-') and len(api_key) > 20
        except Exception:
            return False
    
    def check_directory_structure(self) -> bool:
        """Check that required directories exist"""
        print("🔍 Checking directory structure...")
        
        all_exist = True
        
        # Check common directories
        directories_to_check = [
            "public/data",
            "scripts/logs",
            "scripts/backups"
        ]
        
        for dir_path in directories_to_check:
            full_path = Path(__file__).parent.parent.parent / dir_path
            if full_path.exists():
                self.add_success(f"✅ Directory exists: {dir_path}")
            else:
                self.add_warning(f"⚠️ Directory missing: {dir_path}")
                # Try to create it
                try:
                    full_path.mkdir(parents=True, exist_ok=True)
                    self.add_success(f"✅ Created directory: {dir_path}")
                except Exception as e:
                    self.add_issue(f"❌ Cannot create directory {dir_path}: {e}")
                    all_exist = False
        
        return all_exist
    
    def check_path_resolution(self) -> bool:
        """Test path resolution functionality"""
        print("🔍 Testing path resolution...")
        
        try:
            # Test path resolution from different locations
            test_config = load_script_config('utilities', __file__)
            
            # Check that paths are resolved
            data_dir = test_config.get("file_paths", {}).get("data_dir")
            if data_dir and Path(data_dir).is_absolute():
                self.add_success("✅ Path resolution working correctly")
                return True
            else:
                self.add_issue("❌ Path resolution not working correctly")
                return False
                
        except Exception as e:
            self.add_issue(f"❌ Path resolution test failed: {e}")
            return False
    
    def run_all_checks(self) -> bool:
        """Run all health checks"""
        print("🏥 Configuration Health Check")
        print("=" * 50)
        
        checks = [
            self.check_configuration_files,
            self.check_environment_variables,
            self.check_api_keys,
            self.check_directory_structure,
            self.check_path_resolution
        ]
        
        all_passed = True
        for check in checks:
            try:
                if not check():
                    all_passed = False
            except Exception as e:
                self.add_issue(f"Health check failed: {e}")
                all_passed = False
            print()  # Add spacing between checks
        
        return all_passed
    
    def print_summary(self):
        """Print health check summary"""
        print("=" * 50)
        print("📊 Health Check Summary")
        print("=" * 50)
        
        if self.successes:
            print(f"✅ Successes ({len(self.successes)}):")
            for success in self.successes:
                print(f"  {success}")
            print()
        
        if self.warnings:
            print(f"⚠️ Warnings ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"  {warning}")
            print()
        
        if self.issues:
            print(f"❌ Issues ({len(self.issues)}):")
            for issue in self.issues:
                print(f"  {issue}")
            print()
        
        total_checks = len(self.successes) + len(self.warnings) + len(self.issues)
        if total_checks > 0:
            success_rate = len(self.successes) / total_checks * 100
            print(f"📈 Success Rate: {success_rate:.1f}%")
        
        if not self.issues:
            print("🎉 All critical checks passed! Configuration system is healthy.")
        else:
            print("⚠️ Some issues found. Please address the critical issues above.")

def main():
    """Main health check function"""
    checker = ConfigHealthChecker()
    
    all_passed = checker.run_all_checks()
    checker.print_summary()
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
