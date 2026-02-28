"""
Configuration management system for playwright-enhance.

Supports configuration from multiple sources with priority:
1. Runtime options (highest priority)
2. Environment variables
3. Config file
4. Defaults (lowest priority)
"""

import os
import json
from typing import Any, Dict, Optional
from pathlib import Path


DEFAULT_CONFIG = {
    # Smart Waiting
    'smart_waiting': {
        'enabled': False,
        'initial_timeout': 5000,  # ms
        'max_timeout': 10000,  # ms
        'min_timeout': 1000,  # ms
    },
    
    # Multi-Locator
    'multi_locator': {
        'enabled': False,
        'semantic_enabled': True,
        'visual_enabled': True,
        'visual_confidence_threshold': 0.85,
        'fuzzy_match_threshold': 0.75,
    },
    
    # Concurrent Engine
    'concurrent_engine': {
        'enabled': False,
        'max_concurrent_ops': 10,
        'auto_flush': True,
        'flush_interval': 100,  # ms
    },
    
    # Cache System
    'cache_system': {
        'enabled': False,
        'l1_ttl': 5000,  # ms - element locator cache
        'l2_ttl': 10000,  # ms - page state cache
        'l3_max_size': 100 * 1024 * 1024,  # bytes - resource cache (100MB)
        'lru_enabled': True,
    },
    
    # AI API
    'ai_api': {
        'enabled': False,
        'natural_language_enabled': True,
        'batch_enabled': True,
    },
    
    # Performance Monitor
    'perf_monitor': {
        'enabled': False,
        'detailed_timing': True,
        'output_format': 'json',  # json, text, or none
        'output_file': None,  # None for console output
    },
}


class Config:
    """Configuration manager with multi-source support."""
    
    def __init__(self, config_file: Optional[str] = None, **runtime_options):
        """
        Initialize configuration manager.
        
        Args:
            config_file: Path to JSON config file (optional)
            **runtime_options: Runtime configuration overrides
        """
        self._config = self._load_config(config_file, runtime_options)
    
    def _load_config(self, config_file: Optional[str], runtime_options: Dict) -> Dict:
        """Load configuration from all sources with proper priority."""
        # Start with defaults
        config = DEFAULT_CONFIG.copy()
        
        # Load from config file if provided
        if config_file:
            file_config = self._load_from_file(config_file)
            config = self._deep_merge(config, file_config)
        
        # Load from environment variables
        env_config = self._load_from_env()
        config = self._deep_merge(config, env_config)
        
        # Apply runtime options (highest priority)
        config = self._deep_merge(config, runtime_options)
        
        return config
    
    def _load_from_file(self, config_file: str) -> Dict:
        """Load configuration from JSON file."""
        try:
            path = Path(config_file)
            if path.exists():
                with open(path, 'r') as f:
                    return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Warning: Failed to load config file {config_file}: {e}")
        return {}
    
    def _load_from_env(self) -> Dict:
        """Load configuration from environment variables."""
        config = {}
        
        # Support env vars like: PLAYWRIGHT_ENHANCE_SMART_WAITING__ENABLED=true
        # Use double underscore __ as separator between section and field
        prefix = 'PLAYWRIGHT_ENHANCE_'
        
        for key, value in os.environ.items():
            if key.startswith(prefix):
                # Parse key: PLAYWRIGHT_ENHANCE_SMART_WAITING__ENABLED -> smart_waiting.enabled
                remaining = key[len(prefix):].lower()
                
                # Split by double underscore first
                if '__' in remaining:
                    parts = remaining.split('__')
                else:
                    # Fallback: try to match known section patterns
                    # This handles legacy format like SMART_WAITING_ENABLED
                    known_sections = list(DEFAULT_CONFIG.keys())
                    matched = False
                    for section in known_sections:
                        # Convert section name to expected env format (e.g., smart_waiting -> SMART_WAITING)
                        section_upper = section.upper()
                        if remaining.upper().startswith(section_upper):
                            rest = remaining[len(section):]
                            if rest.startswith('_'):
                                rest = rest[1:]  # Remove leading underscore
                            parts = [section, rest] if rest else [section]
                            matched = True
                            break
                    
                    if not matched:
                        # Complete fallback
                        parts = remaining.split('_', 1)  # Split into max 2 parts
                
                # Convert string value to appropriate type
                parsed_value = self._parse_env_value(value)
                
                # Build nested dict
                current = config
                for part in parts[:-1]:
                    if part not in current:
                        current[part] = {}
                    current = current[part]
                current[parts[-1]] = parsed_value
        
        return config
    
    def _parse_env_value(self, value: str) -> Any:
        """Parse environment variable string to appropriate type."""
        # Handle booleans
        if value.lower() in ('true', '1', 'yes', 'on'):
            return True
        if value.lower() in ('false', '0', 'no', 'off'):
            return False
        
        # Handle numbers
        try:
            if '.' in value:
                return float(value)
            return int(value)
        except ValueError:
            pass
        
        # Return as string
        return value
    
    def _deep_merge(self, base: Dict, override: Dict) -> Dict:
        """Deep merge two dictionaries, deeply copying nested structures."""
        import copy
        result = copy.deepcopy(base)
        
        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._deep_merge(result[key], value)
            else:
                result[key] = value
        
        return result
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value by dot-notation key.
        
        Args:
            key: Configuration key (e.g., 'smart_waiting.enabled')
            default: Default value if key not found
        
        Returns:
            Configuration value
        """
        parts = key.split('.')
        current = self._config
        
        for part in parts:
            if isinstance(current, dict) and part in current:
                current = current[part]
            else:
                return default
        
        return current
    
    def set(self, key: str, value: Any) -> None:
        """
        Set configuration value by dot-notation key.
        
        Args:
            key: Configuration key (e.g., 'smart_waiting.enabled')
            value: Value to set
        """
        parts = key.split('.')
        current = self._config
        
        for part in parts[:-1]:
            if part not in current:
                current[part] = {}
            current = current[part]
        
        current[parts[-1]] = value
    
    def to_dict(self) -> Dict:
        """Export configuration as dictionary."""
        return self._config.copy()
    
    def save_to_file(self, filepath: str) -> None:
        """Save current configuration to JSON file."""
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(path, 'w') as f:
            json.dump(self._config, f, indent=2)


# Global config instance
_global_config: Optional[Config] = None


def get_config() -> Config:
    """Get global configuration instance."""
    global _global_config
    if _global_config is None:
        _global_config = Config()
    return _global_config


def set_config(config: Config) -> None:
    """Set global configuration instance."""
    global _global_config
    _global_config = config
