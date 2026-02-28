"""
playwright-enhance: Performance-optimized Playwright wrapper for AI agents.

Provides intelligent waiting, multi-strategy element location, concurrent operations,
smart caching, and AI-friendly APIs while maintaining 100% Playwright compatibility.
"""

from playwright_enhance.core.wrapper import enhance, EnhancedPage, EnhancedBrowser
from playwright_enhance.core.config import Config, get_config, set_config

__version__ = "0.1.0"
__all__ = [
    "enhance",
    "EnhancedPage",
    "EnhancedBrowser",
    "Config",
    "get_config",
    "set_config",
]
