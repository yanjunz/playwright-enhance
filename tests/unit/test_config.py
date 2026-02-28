"""Unit tests for configuration management."""

import pytest
import json
import os
from pathlib import Path
from playwright_enhance.core.config import Config, get_config, set_config, DEFAULT_CONFIG


class TestConfig:
    """Test configuration management."""
    
    def test_default_config(self):
        """Test that default configuration is loaded."""
        config = Config()
        assert config.get('smart_waiting.enabled') is False
        assert config.get('smart_waiting.initial_timeout') == 5000
    
    def test_runtime_options(self):
        """Test runtime configuration overrides."""
        config = Config(smart_waiting={'enabled': True})
        assert config.get('smart_waiting.enabled') is True
    
    def test_get_with_default(self):
        """Test getting config with default value."""
        config = Config()
        assert config.get('nonexistent.key', 'default') == 'default'
    
    def test_set_config(self):
        """Test setting configuration values."""
        config = Config()
        config.set('smart_waiting.enabled', True)
        assert config.get('smart_waiting.enabled') is True
    
    def test_nested_config(self):
        """Test nested configuration access."""
        config = Config()
        assert isinstance(config.get('smart_waiting'), dict)
        assert config.get('smart_waiting.initial_timeout') == 5000
    
    def test_to_dict(self):
        """Test exporting configuration as dictionary."""
        config = Config()
        config_dict = config.to_dict()
        assert isinstance(config_dict, dict)
        assert 'smart_waiting' in config_dict
    
    def test_config_file_loading(self, tmp_path):
        """Test loading configuration from file."""
        config_file = tmp_path / "config.json"
        config_data = {
            "smart_waiting": {
                "enabled": True,
                "initial_timeout": 3000
            }
        }
        
        with open(config_file, 'w') as f:
            json.dump(config_data, f)
        
        config = Config(config_file=str(config_file))
        assert config.get('smart_waiting.enabled') is True
        assert config.get('smart_waiting.initial_timeout') == 3000
    
    def test_save_to_file(self, tmp_path):
        """Test saving configuration to file."""
        config = Config()
        config.set('smart_waiting.enabled', True)
        
        config_file = tmp_path / "output.json"
        config.save_to_file(str(config_file))
        
        assert config_file.exists()
        
        with open(config_file, 'r') as f:
            saved_data = json.load(f)
        
        assert saved_data['smart_waiting']['enabled'] is True
    
    def test_env_variable_loading(self, monkeypatch):
        """Test loading configuration from environment variables."""
        monkeypatch.setenv('PLAYWRIGHT_ENHANCE_SMART_WAITING__ENABLED', 'true')
        monkeypatch.setenv('PLAYWRIGHT_ENHANCE_SMART_WAITING__INITIAL_TIMEOUT', '3000')
        
        config = Config()
        assert config.get('smart_waiting.enabled') is True
        assert config.get('smart_waiting.initial_timeout') == 3000
    
    def test_config_priority(self, tmp_path, monkeypatch):
        """Test configuration priority: runtime > env > file > default."""
        # Create config file
        config_file = tmp_path / "config.json"
        with open(config_file, 'w') as f:
            json.dump({"smart_waiting": {"initial_timeout": 2000}}, f)
        
        # Set env variable (use double underscore format)
        monkeypatch.setenv('PLAYWRIGHT_ENHANCE_SMART_WAITING__INITIAL_TIMEOUT', '3000')
        
        # Runtime option should have highest priority
        config = Config(
            config_file=str(config_file),
            smart_waiting={'initial_timeout': 4000}
        )
        
        assert config.get('smart_waiting.initial_timeout') == 4000
    
    def test_parse_env_boolean(self):
        """Test parsing boolean environment variables."""
        config = Config()
        
        assert config._parse_env_value('true') is True
        assert config._parse_env_value('false') is False
        assert config._parse_env_value('1') is True
        assert config._parse_env_value('0') is False
        assert config._parse_env_value('yes') is True
        assert config._parse_env_value('no') is False
    
    def test_parse_env_number(self):
        """Test parsing numeric environment variables."""
        config = Config()
        
        assert config._parse_env_value('42') == 42
        assert config._parse_env_value('3.14') == 3.14
    
    def test_parse_env_string(self):
        """Test parsing string environment variables."""
        config = Config()
        
        assert config._parse_env_value('hello') == 'hello'
        assert config._parse_env_value('path/to/file') == 'path/to/file'


class TestGlobalConfig:
    """Test global configuration management."""
    
    def test_get_global_config(self):
        """Test getting global config instance."""
        config = get_config()
        assert isinstance(config, Config)
    
    def test_set_global_config(self):
        """Test setting global config instance."""
        custom_config = Config(smart_waiting={'enabled': True})
        set_config(custom_config)
        
        config = get_config()
        assert config.get('smart_waiting.enabled') is True
