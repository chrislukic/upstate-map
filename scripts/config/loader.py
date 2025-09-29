#!/usr/bin/env python3
"""
Shared configuration loader for all utility scripts
"""

import json
import os
import logging
from pathlib import Path
from typing import Dict, Any, Optional, Tuple

# Get the config directory
CONFIG_DIR = Path(__file__).parent

def load_config(config_name: str, default: Optional[Dict[str, Any]] = None, validate_schema: bool = True) -> Dict[str, Any]:
    """
    Load a configuration file with fallback to defaults
    
    Args:
        config_name: Name of config file (without .json extension)
        default: Default configuration if file doesn't exist
        validate_schema: Whether to validate against JSON schema
    
    Returns:
        Configuration dictionary
    """
    logger = logging.getLogger(__name__)
    config_path = CONFIG_DIR / f"{config_name}.json"
    
    if config_path.exists():
        try:
            with config_path.open("r", encoding="utf-8") as f:
                config = json.load(f)
            
            # Validate schema if requested
            if validate_schema:
                try:
                    from .schemas import validate_config
                    is_valid, errors = validate_config(config, config_name)
                    if not is_valid:
                        logger.warning(f"Configuration validation failed for {config_name}.json:")
                        for error in errors:
                            logger.warning(f"  - {error}")
                        logger.warning("Using configuration anyway, but please fix validation errors.")
                except ImportError:
                    logger.debug("Schema validation skipped: jsonschema not available")
                except Exception as e:
                    logger.warning(f"Schema validation error: {e}")
            
            return config
            
        except json.JSONDecodeError as e:
            logger.warning(f"Invalid {config_name}.json: {e}, using defaults")
    
    return default or {}

def load_common_config() -> Dict[str, Any]:
    """Load common configuration shared across all scripts"""
    return load_config("common", {
        "api": {
            "google_maps": {
                "geocoding_endpoint": "https://maps.googleapis.com/maps/api/geocode/json",
                "timeout": 20,
                "rate_limit_delay": 0.15
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
    })

def load_script_config(script_type: str, script_path: str = None, config_name: str = None) -> Dict[str, Any]:
    """
    Load configuration for a specific script type
    
    Args:
        script_type: Type of script (geocoding, maintenance, enrichment, etc.)
        script_path: Path to the script calling this function (for path resolution)
        config_name: Specific config name (defaults to script_type)
    
    Returns:
        Merged configuration (common + script-specific) with resolved paths
    """
    if config_name is None:
        config_name = script_type
    
    # Load common config first
    common = load_common_config()
    
    # Load script-specific config
    script_config = load_config(config_name, {})
    
    # Merge configurations (script-specific overrides common)
    def deep_merge(base: Dict, override: Dict) -> Dict:
        result = base.copy()
        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = deep_merge(result[key], value)
            else:
                result[key] = value
        return result
    
    merged_config = deep_merge(common, script_config)
    
    # Resolve paths in the merged configuration
    return resolve_paths(merged_config, script_path)

def get_api_key(service: str) -> Optional[str]:
    """
    Get API key for a service from environment variables
    
    Args:
        service: Service name (google_maps, openai, etc.)
    
    Returns:
        API key or None if not found
    """
    key_mapping = {
        "google_maps": "GOOGLE_MAPS_API_KEY",
        "openai": "OPENAI_API_KEY"
    }
    
    env_var = key_mapping.get(service)
    if not env_var:
        return None
    
    return os.getenv(env_var)

def setup_logging(config: Dict[str, Any], script_name: str) -> logging.Logger:
    """
    Setup logging based on configuration
    
    Args:
        config: Configuration dictionary
        script_name: Name of the script for logger
    
    Returns:
        Configured logger
    """
    log_config = config.get("logging", {})
    
    # Create logs directory if it doesn't exist
    log_dir = Path(log_config.get("log_dir", "./logs"))
    log_dir.mkdir(exist_ok=True)
    
    # Setup logging
    logging.basicConfig(
        level=getattr(logging, log_config.get("level", "INFO")),
        format=log_config.get("format", "%(asctime)s - %(name)s - %(levelname)s - %(message)s"),
        handlers=[
            logging.FileHandler(log_dir / f"{script_name}.log"),
            logging.StreamHandler()
        ]
    )
    
    return logging.getLogger(script_name)

def resolve_paths(config: Dict[str, Any], script_path: str = None) -> Dict[str, Any]:
    """
    Resolve relative paths in configuration to absolute paths
    
    Args:
        config: Configuration dictionary
        script_path: Path to the script calling this function (for relative path resolution)
    
    Returns:
        Configuration with resolved paths
    """
    resolved_config = config.copy()
    
    # Determine base directory for path resolution
    if script_path:
        base_dir = Path(script_path).parent
    else:
        base_dir = Path.cwd()
    
    # Resolve paths in various sections
    path_sections = ["paths", "file_paths"]
    
    for section in path_sections:
        if section in resolved_config:
            for key, path in resolved_config[section].items():
                if isinstance(path, str) and not Path(path).is_absolute():
                    # Resolve relative to base directory
                    resolved_path = (base_dir / path).resolve()
                    resolved_config[section][key] = str(resolved_path)
    
    return resolved_config

def validate_environment(required_keys: list, optional_keys: list = None) -> bool:
    """
    Validate that required environment variables are set
    
    Args:
        required_keys: List of required environment variable names
        optional_keys: List of optional environment variable names
    
    Returns:
        True if all required keys are present
    """
    logger = logging.getLogger(__name__)
    missing = []
    
    for key in required_keys:
        if not os.getenv(key):
            missing.append(key)
    
    if missing:
        logger.error(f"Missing required environment variables: {', '.join(missing)}")
        return False
    
    if optional_keys:
        for key in optional_keys:
            if not os.getenv(key):
                logger.warning(f"Optional environment variable not set: {key}")
    
    return True

