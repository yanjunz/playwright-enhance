"""
Core wrapper for Playwright objects with plugin support.

This module provides transparent wrapping of Playwright Page and Browser objects,
allowing capability plugins to enhance functionality while maintaining 100% API compatibility.
"""

from typing import Any, Callable, Dict, Optional, Set
from functools import wraps
import inspect


class PluginRegistry:
    """Registry for managing capability plugins."""
    
    def __init__(self):
        self._plugins: Dict[str, Any] = {}
        self._enabled: Set[str] = set()
    
    def register(self, name: str, plugin: Any) -> None:
        """Register a capability plugin."""
        self._plugins[name] = plugin
        
    def enable(self, name: str) -> None:
        """Enable a capability plugin."""
        if name not in self._plugins:
            raise ValueError(f"Plugin '{name}' not registered")
        self._enabled.add(name)
    
    def disable(self, name: str) -> None:
        """Disable a capability plugin."""
        self._enabled.discard(name)
    
    def is_enabled(self, name: str) -> bool:
        """Check if a plugin is enabled."""
        return name in self._enabled
    
    def get_plugin(self, name: str) -> Optional[Any]:
        """Get a plugin by name."""
        return self._plugins.get(name)
    
    def get_enabled_plugins(self) -> Dict[str, Any]:
        """Get all enabled plugins."""
        return {name: plugin for name, plugin in self._plugins.items() 
                if name in self._enabled}


class EnhancedPage:
    """
    Wrapper for Playwright Page with plugin support.
    
    Maintains 100% API compatibility while allowing plugins to intercept
    and enhance method calls.
    """
    
    def __init__(self, page: Any, config: Optional[Dict] = None):
        """
        Initialize enhanced page wrapper.
        
        Args:
            page: Native Playwright Page object
            config: Optional configuration dictionary
        """
        self._page = page
        self._config = config or {}
        self._plugin_registry = PluginRegistry()
        
    def __getattr__(self, name: str) -> Any:
        """
        Proxy attribute access to native page.
        
        Intercepts method calls to allow plugin enhancement while
        maintaining transparent access to all Playwright APIs.
        """
        attr = getattr(self._page, name)
        
        # If it's not a method, return as-is
        if not callable(attr):
            return attr
        
        # Wrap methods to allow plugin interception
        @wraps(attr)
        async def wrapper(*args, **kwargs):
            # Pre-hooks: allow plugins to modify args or skip execution
            for plugin_name, plugin in self._plugin_registry.get_enabled_plugins().items():
                if hasattr(plugin, f'before_{name}'):
                    hook = getattr(plugin, f'before_{name}')
                    result = await hook(self, *args, **kwargs)
                    if result is not None:
                        # Plugin handled the call
                        return result
            
            # Execute original method
            result = await attr(*args, **kwargs)
            
            # Post-hooks: allow plugins to modify result
            for plugin_name, plugin in self._plugin_registry.get_enabled_plugins().items():
                if hasattr(plugin, f'after_{name}'):
                    hook = getattr(plugin, f'after_{name}')
                    result = await hook(self, result, *args, **kwargs)
            
            return result
        
        # For sync methods
        if not inspect.iscoroutinefunction(attr):
            @wraps(attr)
            def sync_wrapper(*args, **kwargs):
                # Similar logic but for sync methods
                for plugin_name, plugin in self._plugin_registry.get_enabled_plugins().items():
                    if hasattr(plugin, f'before_{name}'):
                        hook = getattr(plugin, f'before_{name}')
                        result = hook(self, *args, **kwargs)
                        if result is not None:
                            return result
                
                result = attr(*args, **kwargs)
                
                for plugin_name, plugin in self._plugin_registry.get_enabled_plugins().items():
                    if hasattr(plugin, f'after_{name}'):
                        hook = getattr(plugin, f'after_{name}')
                        result = hook(self, result, *args, **kwargs)
                
                return result
            
            return sync_wrapper
        
        return wrapper
    
    def enable_plugin(self, name: str) -> None:
        """Enable a capability plugin."""
        self._plugin_registry.enable(name)
    
    def disable_plugin(self, name: str) -> None:
        """Disable a capability plugin."""
        self._plugin_registry.disable(name)
    
    def register_plugin(self, name: str, plugin: Any) -> None:
        """Register a capability plugin."""
        self._plugin_registry.register(name, plugin)


class EnhancedBrowser:
    """
    Wrapper for Playwright Browser with plugin support.
    
    Ensures that new pages are automatically enhanced.
    """
    
    def __init__(self, browser: Any, config: Optional[Dict] = None):
        """
        Initialize enhanced browser wrapper.
        
        Args:
            browser: Native Playwright Browser object
            config: Optional configuration dictionary
        """
        self._browser = browser
        self._config = config or {}
        self._plugin_registry = PluginRegistry()
    
    async def new_page(self, **kwargs) -> EnhancedPage:
        """
        Create a new enhanced page.
        
        Automatically wraps the page and applies enabled plugins.
        """
        page = await self._browser.new_page(**kwargs)
        enhanced_page = EnhancedPage(page, self._config)
        
        # Transfer enabled plugins to new page
        for plugin_name, plugin in self._plugin_registry.get_enabled_plugins().items():
            enhanced_page.register_plugin(plugin_name, plugin)
            enhanced_page.enable_plugin(plugin_name)
        
        return enhanced_page
    
    def __getattr__(self, name: str) -> Any:
        """Proxy other attributes to native browser."""
        return getattr(self._browser, name)
    
    def enable_plugin(self, name: str) -> None:
        """Enable a capability plugin for all new pages."""
        self._plugin_registry.enable(name)
    
    def disable_plugin(self, name: str) -> None:
        """Disable a capability plugin."""
        self._plugin_registry.disable(name)
    
    def register_plugin(self, name: str, plugin: Any) -> None:
        """Register a capability plugin."""
        self._plugin_registry.register(name, plugin)


def enhance(obj: Any, config: Optional[Dict] = None) -> Any:
    """
    Enhance a Playwright object with plugin support.
    
    Args:
        obj: Playwright Browser or Page object
        config: Optional configuration dictionary
    
    Returns:
        Enhanced wrapper object
    
    Examples:
        >>> browser = await playwright.chromium.launch()
        >>> enhanced_browser = enhance(browser)
        >>> page = await enhanced_browser.new_page()
        
        >>> page = await browser.new_page()
        >>> enhanced_page = enhance(page, config={'smart_waiting': True})
    """
    # Check object type by class name to avoid import issues
    class_name = obj.__class__.__name__
    
    if 'Browser' in class_name and 'Page' not in class_name:
        return EnhancedBrowser(obj, config)
    elif 'Page' in class_name:
        return EnhancedPage(obj, config)
    else:
        raise TypeError(f"Cannot enhance object of type {class_name}")
