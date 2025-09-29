# Configuration System Documentation

This document provides comprehensive documentation for the centralized configuration system used by all scripts in the `/scripts` directory.

## Overview

The configuration system provides:
- **Centralized Configuration**: All scripts use shared configuration files
- **Schema Validation**: JSON schemas ensure configuration validity
- **Path Resolution**: Automatic resolution of relative paths to absolute paths
- **Environment Management**: Centralized API key and environment variable handling
- **Logging**: Standardized logging across all scripts
- **Health Monitoring**: Tools to check configuration system health

## Configuration Files

### Core Configuration Files

| File | Purpose | Description |
|------|---------|-------------|
| `scripts/config/common.json` | Common settings | Shared configuration for all scripts |
| `scripts/config/maintenance.json` | Maintenance scripts | Configuration for maintenance and research scripts |
| `scripts/config/utilities.json` | Utility scripts | Configuration for data processing utilities |
| `scripts/config/geocoding.json` | Geocoding settings | Specialized configuration for geocoding operations |

### Configuration Structure

#### Common Configuration (`common.json`)
```json
{
  "api": {
    "google_maps": {
      "geocoding_endpoint": "https://maps.googleapis.com/maps/api/geocode/json",
      "timeout": 20,
      "rate_limit_delay": 0.15
    },
    "openai": {
      "default_model": "gpt-4o-mini",
      "timeout": 30,
      "max_retries": 3
    }
  },
  "paths": {
    "data_dir": "../../public/data",
    "backup_dir": "./backups",
    "log_dir": "./logs"
  },
  "logging": {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  }
}
```

#### Utilities Configuration (`utilities.json`)
```json
{
  "geocoding": {
    "rate_limit_delay": 0.15,
    "progressive_delays": {
      "after_5": 0.3,
      "after_10": 0.5
    },
    "max_retries": 3,
    "timeout": 20
  },
  "place_api": {
    "rate_limit_delay": 0.15,
    "max_retries": 3,
    "timeout": 20
  },
  "data_processing": {
    "backup_before_changes": true,
    "validate_after_changes": true,
    "dry_run_default": false
  }
}
```

## Using the Configuration System

### Basic Usage

```python
#!/usr/bin/env python3
import sys
from pathlib import Path

# Add the scripts directory to the path
sys.path.append(str(Path(__file__).parent.parent))

# Import configuration loader
from config.loader import load_script_config, setup_logging, validate_environment, get_api_key

def main():
    # Load configuration with path resolution
    config = load_script_config('utilities', __file__)
    
    # Setup logging
    logger = setup_logging(config, Path(__file__).stem)
    
    # Validate environment
    if not validate_environment(['GOOGLE_MAPS_API_KEY']):
        logger.error("Missing required environment variables")
        return 1
    
    # Get API key
    api_key = get_api_key('google_maps')
    if not api_key:
        logger.error("API key not found!")
        return 1
    
    # Use configuration values
    data_dir = Path(config.get("file_paths", {}).get("data_dir", "../../public/data"))
    timeout = config.get("geocoding", {}).get("timeout", 20)
    
    logger.info("Script started")
    # ... your script logic here ...
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
```

### Configuration Loading Functions

#### `load_script_config(script_type, script_path=None, config_name=None)`
Loads and merges configuration for a specific script type.

**Parameters:**
- `script_type`: Type of script ('utilities', 'maintenance', etc.)
- `script_path`: Path to the calling script (for path resolution)
- `config_name`: Specific config name (defaults to script_type)

**Returns:** Merged configuration dictionary with resolved paths

#### `setup_logging(config, script_name)`
Sets up standardized logging for a script.

**Parameters:**
- `config`: Configuration dictionary
- `script_name`: Name for the logger

**Returns:** Configured logger instance

#### `validate_environment(required_keys, optional_keys=None)`
Validates that required environment variables are set.

**Parameters:**
- `required_keys`: List of required environment variable names
- `optional_keys`: List of optional environment variable names

**Returns:** True if all required keys are present

#### `get_api_key(service)`
Gets API key for a service from environment variables.

**Parameters:**
- `service`: Service name ('google_maps', 'openai', etc.)

**Returns:** API key string or None if not found

## Path Resolution

The configuration system automatically resolves relative paths to absolute paths based on the calling script's location.

### Example
```python
# Configuration file contains:
{
  "file_paths": {
    "data_dir": "../../public/data"
  }
}

# When loaded from scripts/utilities/my_script.py:
config = load_script_config('utilities', __file__)
data_dir = config["file_paths"]["data_dir"]
# data_dir is now: "/absolute/path/to/project/public/data"
```

## Environment Variables

### Required Environment Variables
- `GOOGLE_MAPS_API_KEY`: Google Maps API key for geocoding and place services

### Optional Environment Variables
- `OPENAI_API_KEY`: OpenAI API key for AI-powered features
- `OPENAI_MODEL`: OpenAI model to use (defaults to gpt-4o-mini)

### Setting Environment Variables

#### Option 1: .env File (Recommended)
Create a `.env` file in the project root:
```bash
GOOGLE_MAPS_API_KEY=your_google_maps_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
```

#### Option 2: Environment Variables
```bash
export GOOGLE_MAPS_API_KEY="your_google_maps_api_key_here"
export OPENAI_API_KEY="your_openai_api_key_here"
```

## Script Templates

### Utility Script Template
Use `scripts/templates/utility_script_template.py` as a starting point for new utility scripts.

### Maintenance Script Template
Use `scripts/templates/maintenance_script_template.py` as a starting point for new maintenance scripts.

## Validation and Health Checks

### Configuration Validation
```bash
# Validate all configuration files
python scripts/config/validate_config.py

# Validate specific configuration
python scripts/config/validate_config.py utilities
```

### Health Check
```bash
# Run comprehensive health check
python scripts/config/health_check.py
```

The health check verifies:
- Configuration file existence and validity
- Environment variable presence
- API key validity
- Directory structure
- Path resolution functionality

## Best Practices

### 1. Always Use Path Resolution
```python
# ✅ Good: Use path resolution
config = load_script_config('utilities', __file__)
data_dir = Path(config.get("file_paths", {}).get("data_dir"))

# ❌ Bad: Hardcoded paths
data_dir = Path("../../public/data")
```

### 2. Validate Environment Early
```python
# ✅ Good: Validate environment at start
if not validate_environment(['GOOGLE_MAPS_API_KEY']):
    logger.error("Missing required environment variables")
    return 1

# ❌ Bad: Check environment variables manually
api_key = os.getenv('GOOGLE_MAPS_API_KEY')
if not api_key:
    print("Error: API key not found")
    return 1
```

### 3. Use Centralized Logging
```python
# ✅ Good: Use centralized logging
logger = setup_logging(config, Path(__file__).stem)
logger.info("Script started")

# ❌ Bad: Manual logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
```

### 4. Handle Configuration Gracefully
```python
# ✅ Good: Use configuration with defaults
timeout = config.get("geocoding", {}).get("timeout", 20)
backup_enabled = config.get("data_processing", {}).get("backup_before_changes", True)

# ❌ Bad: Assume configuration exists
timeout = config["geocoding"]["timeout"]
```

## Troubleshooting

### Common Issues

#### 1. Configuration File Not Found
**Error:** `Configuration file not found: scripts/config/utilities.json`

**Solution:** Ensure the configuration file exists in the correct location.

#### 2. Path Resolution Issues
**Error:** Relative paths not resolving correctly

**Solution:** Always pass `__file__` as the second parameter to `load_script_config()`.

#### 3. Environment Variable Not Set
**Error:** `Missing required environment variables: GOOGLE_MAPS_API_KEY`

**Solution:** Set the required environment variables in your `.env` file or environment.

#### 4. API Key Invalid
**Error:** `Google Maps API key is invalid or quota exceeded`

**Solution:** Check your API key and ensure it has the required permissions and quota.

### Debug Mode

Enable debug logging to see detailed configuration loading information:

```python
import logging
logging.getLogger().setLevel(logging.DEBUG)
```

## Migration Guide

### Migrating Existing Scripts

1. **Update Imports**
   ```python
   # Add these imports
   import sys
   from pathlib import Path
   sys.path.append(str(Path(__file__).parent.parent))
   from config.loader import load_script_config, setup_logging, validate_environment, get_api_key
   ```

2. **Replace Configuration Loading**
   ```python
   # Old way
   config = load_config('utilities')
   
   # New way
   config = load_script_config('utilities', __file__)
   ```

3. **Replace Manual Logging Setup**
   ```python
   # Old way
   logging.basicConfig(level=logging.INFO)
   logger = logging.getLogger(__name__)
   
   # New way
   logger = setup_logging(config, Path(__file__).stem)
   ```

4. **Replace Environment Validation**
   ```python
   # Old way
   api_key = os.getenv('GOOGLE_MAPS_API_KEY')
   if not api_key:
       print("Error: API key not found")
       return 1
   
   # New way
   if not validate_environment(['GOOGLE_MAPS_API_KEY']):
       logger.error("Missing required environment variables")
       return 1
   api_key = get_api_key('google_maps')
   ```

5. **Update Path Usage**
   ```python
   # Old way
   data_dir = Path("../../public/data")
   
   # New way
   data_dir = Path(config.get("file_paths", {}).get("data_dir", "../../public/data"))
   ```

## API Reference

### Configuration Loader (`config/loader.py`)

#### Functions
- `load_config(config_name, default=None, validate_schema=True)`
- `load_common_config()`
- `load_script_config(script_type, script_path=None, config_name=None)`
- `get_api_key(service)`
- `setup_logging(config, script_name)`
- `validate_environment(required_keys, optional_keys=None)`
- `resolve_paths(config, script_path=None)`

### Schema Validation (`config/schemas.py`)

#### Functions
- `get_schema(config_name)`
- `validate_config(config, config_name)`

#### Schemas
- `COMMON_SCHEMA`
- `MAINTENANCE_SCHEMA`
- `UTILITIES_SCHEMA`
- `GEOCODING_SCHEMA`

### Health Check (`config/health_check.py`)

#### Classes
- `ConfigHealthChecker`

#### Methods
- `check_configuration_files()`
- `check_environment_variables()`
- `check_api_keys()`
- `check_directory_structure()`
- `check_path_resolution()`
- `run_all_checks()`

## Contributing

When adding new configuration options:

1. **Update the appropriate schema** in `scripts/config/schemas.py`
2. **Add default values** in the configuration loader
3. **Update documentation** in this file
4. **Add validation tests** if needed
5. **Update health checks** if the new option affects system health

## Support

For issues with the configuration system:

1. Run the health check: `python scripts/config/health_check.py`
2. Validate configurations: `python scripts/config/validate_config.py`
3. Check the logs for detailed error messages
4. Review this documentation for common solutions




