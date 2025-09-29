#!/usr/bin/env python3
"""
JSON schemas for configuration validation
"""

# Common schema components
API_SCHEMA = {
    "type": "object",
    "properties": {
        "google_maps": {
            "type": "object",
            "properties": {
                "geocoding_endpoint": {"type": "string", "format": "uri"},
                "timeout": {"type": "number", "minimum": 1, "maximum": 300},
                "rate_limit_delay": {"type": "number", "minimum": 0, "maximum": 10}
            },
            "required": ["geocoding_endpoint", "timeout", "rate_limit_delay"]
        },
        "openai": {
            "type": "object",
            "properties": {
                "default_model": {"type": "string"},
                "timeout": {"type": "number", "minimum": 1, "maximum": 300},
                "max_retries": {"type": "integer", "minimum": 1, "maximum": 10}
            },
            "required": ["default_model", "timeout", "max_retries"]
        }
    }
}

PATHS_SCHEMA = {
    "type": "object",
    "properties": {
        "data_dir": {"type": "string"},
        "backup_dir": {"type": "string"},
        "log_dir": {"type": "string"}
    },
    "required": ["data_dir", "backup_dir", "log_dir"]
}

LOGGING_SCHEMA = {
    "type": "object",
    "properties": {
        "level": {
            "type": "string",
            "enum": ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        },
        "format": {"type": "string"},
        "file_rotation": {
            "type": "object",
            "properties": {
                "max_bytes": {"type": "integer", "minimum": 1024},
                "backup_count": {"type": "integer", "minimum": 1, "maximum": 20}
            },
            "required": ["max_bytes", "backup_count"]
        }
    },
    "required": ["level", "format"]
}

VALIDATION_SCHEMA = {
    "type": "object",
    "properties": {
        "strict_mode": {"type": "boolean"},
        "skip_invalid": {"type": "boolean"},
        "coordinate_bounds": {
            "type": "object",
            "properties": {
                "lat_min": {"type": "number", "minimum": -90, "maximum": 90},
                "lat_max": {"type": "number", "minimum": -90, "maximum": 90},
                "lng_min": {"type": "number", "minimum": -180, "maximum": 180},
                "lng_max": {"type": "number", "minimum": -180, "maximum": 180}
            },
            "required": ["lat_min", "lat_max", "lng_min", "lng_max"]
        },
        "address_validation": {
            "type": "object",
            "properties": {
                "min_length": {"type": "integer", "minimum": 1},
                "required_components": {
                    "type": "array",
                    "items": {"type": "string"}
                }
            }
        },
        "required_fields": {
            "type": "object",
            "additionalProperties": {
                "type": "array",
                "items": {"type": "string"}
            }
        }
    }
}

# Main configuration schemas
COMMON_SCHEMA = {
    "type": "object",
    "properties": {
        "api": API_SCHEMA,
        "paths": PATHS_SCHEMA,
        "logging": LOGGING_SCHEMA,
        "validation": VALIDATION_SCHEMA
    },
    "required": ["api", "paths", "logging"]
}

MAINTENANCE_SCHEMA = {
    "type": "object",
    "properties": {
        "research_events": {
            "type": "object",
            "properties": {
                "months_ahead": {"type": "integer", "minimum": 1, "maximum": 12},
                "sleep_between_regions": {"type": "number", "minimum": 0, "maximum": 10},
                "geocode_delay_base": {"type": "number", "minimum": 0, "maximum": 10},
                "geocode_delay_progressive": {
                    "type": "object",
                    "properties": {
                        "after_5": {"type": "number", "minimum": 0, "maximum": 10},
                        "after_10": {"type": "number", "minimum": 0, "maximum": 10}
                    }
                },
                "max_events_per_region": {"type": "integer", "minimum": 1, "maximum": 1000},
                "max_retries": {"type": "integer", "minimum": 1, "maximum": 10},
                "exponential_backoff": {
                    "type": "object",
                    "properties": {
                        "base_delay": {"type": "number", "minimum": 0.1, "maximum": 60},
                        "max_delay": {"type": "number", "minimum": 1, "maximum": 300}
                    },
                    "required": ["base_delay", "max_delay"]
                },
                "filters": {
                    "type": "object",
                    "properties": {
                        "notable_only": {"type": "boolean"},
                        "family_weight": {"type": "number", "minimum": 0, "maximum": 1},
                        "max_drive_hours_from_nyc": {"type": "number", "minimum": 0, "maximum": 24}
                    }
                },
                "output": {
                    "type": "object",
                    "properties": {
                        "events_file": {"type": "string"},
                        "annuals_file": {"type": "string"},
                        "worklog_file": {"type": "string"}
                    },
                    "required": ["events_file", "annuals_file", "worklog_file"]
                }
            },
            "required": ["months_ahead", "sleep_between_regions", "filters", "output"]
        },
        "data_cleanup": {
            "type": "object",
            "properties": {
                "backup_before_changes": {"type": "boolean"},
                "validate_after_changes": {"type": "boolean"},
                "dry_run_default": {"type": "boolean"}
            }
        },
        "scheduling": {
            "type": "object",
            "properties": {
                "default_timeout": {"type": "integer", "minimum": 60, "maximum": 86400},
                "retry_failed_jobs": {"type": "boolean"},
                "max_concurrent_jobs": {"type": "integer", "minimum": 1, "maximum": 10}
            }
        }
    }
}

UTILITIES_SCHEMA = {
    "type": "object",
    "properties": {
        "geocoding": {
            "type": "object",
            "properties": {
                "rate_limit_delay": {"type": "number", "minimum": 0, "maximum": 10},
                "progressive_delays": {
                    "type": "object",
                    "properties": {
                        "after_5": {"type": "number", "minimum": 0, "maximum": 10},
                        "after_10": {"type": "number", "minimum": 0, "maximum": 10}
                    }
                },
                "max_retries": {"type": "integer", "minimum": 1, "maximum": 10},
                "timeout": {"type": "number", "minimum": 1, "maximum": 300}
            },
            "required": ["rate_limit_delay", "max_retries", "timeout"]
        },
        "place_api": {
            "type": "object",
            "properties": {
                "rate_limit_delay": {"type": "number", "minimum": 0, "maximum": 10},
                "max_retries": {"type": "integer", "minimum": 1, "maximum": 10},
                "timeout": {"type": "number", "minimum": 1, "maximum": 300}
            },
            "required": ["rate_limit_delay", "max_retries", "timeout"]
        },
        "data_processing": {
            "type": "object",
            "properties": {
                "backup_before_changes": {"type": "boolean"},
                "validate_after_changes": {"type": "boolean"},
                "dry_run_default": {"type": "boolean"}
            }
        },
        "file_paths": {
            "type": "object",
            "properties": {
                "data_dir": {"type": "string"},
                "backup_dir": {"type": "string"}
            },
            "required": ["data_dir"]
        },
        "validation": VALIDATION_SCHEMA
    }
}

GEOCODING_SCHEMA = {
    "type": "object",
    "properties": {
        "rate_limiting": {
            "type": "object",
            "properties": {
                "base_delay": {"type": "number", "minimum": 0, "maximum": 10},
                "progressive_delays": {
                    "type": "object",
                    "properties": {
                        "after_5": {"type": "number", "minimum": 0, "maximum": 10},
                        "after_10": {"type": "number", "minimum": 0, "maximum": 10}
                    }
                },
                "jitter_range": {
                    "type": "array",
                    "items": {"type": "number", "minimum": 0.1, "maximum": 2.0},
                    "minItems": 2,
                    "maxItems": 2
                }
            },
            "required": ["base_delay"]
        },
        "retry": {
            "type": "object",
            "properties": {
                "max_attempts": {"type": "integer", "minimum": 1, "maximum": 10},
                "exponential_backoff": {
                    "type": "object",
                    "properties": {
                        "base_delay": {"type": "number", "minimum": 0.1, "maximum": 60},
                        "max_delay": {"type": "number", "minimum": 1, "maximum": 300}
                    },
                    "required": ["base_delay", "max_delay"]
                }
            },
            "required": ["max_attempts"]
        },
        "validation": VALIDATION_SCHEMA
    }
}

# Schema registry
SCHEMAS = {
    "common": COMMON_SCHEMA,
    "maintenance": MAINTENANCE_SCHEMA,
    "utilities": UTILITIES_SCHEMA,
    "geocoding": GEOCODING_SCHEMA
}

def get_schema(config_name: str) -> dict:
    """Get schema for a configuration file"""
    return SCHEMAS.get(config_name, {})

def validate_config(config: dict, config_name: str) -> tuple[bool, list]:
    """
    Validate configuration against its schema
    
    Args:
        config: Configuration dictionary to validate
        config_name: Name of the configuration (common, maintenance, etc.)
    
    Returns:
        Tuple of (is_valid, error_messages)
    """
    try:
        import jsonschema
        from jsonschema import validate, ValidationError
        
        schema = get_schema(config_name)
        if not schema:
            return False, [f"No schema found for configuration '{config_name}'"]
        
        validate(instance=config, schema=schema)
        return True, []
        
    except ImportError:
        return False, ["jsonschema package not installed. Install with: pip install jsonschema"]
    except ValidationError as e:
        return False, [f"Validation error: {e.message} at path: {'.'.join(str(p) for p in e.absolute_path)}"]
    except Exception as e:
        return False, [f"Unexpected validation error: {str(e)}"]




