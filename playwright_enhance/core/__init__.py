"""Core wrapper and configuration modules."""

from playwright_enhance.core.wrapper import enhance, EnhancedPage, EnhancedBrowser, PluginRegistry
from playwright_enhance.core.config import Config, get_config, set_config

__all__ = [
    "enhance",
    "EnhancedPage",
    "EnhancedBrowser",
    "PluginRegistry",
    "Config",
    "get_config",
    "set_config",
]
