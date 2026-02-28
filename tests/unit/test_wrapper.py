"""Unit tests for core wrapper functionality."""

import pytest
from unittest.mock import Mock, AsyncMock
from playwright_enhance.core.wrapper import (
    EnhancedPage,
    EnhancedBrowser,
    PluginRegistry,
    enhance,
)


class TestPluginRegistry:
    """Test plugin registry management."""
    
    def test_register_plugin(self):
        """Test plugin registration."""
        registry = PluginRegistry()
        plugin = Mock()
        
        registry.register("test_plugin", plugin)
        assert registry.get_plugin("test_plugin") is plugin
    
    def test_enable_disable_plugin(self):
        """Test enabling and disabling plugins."""
        registry = PluginRegistry()
        plugin = Mock()
        registry.register("test_plugin", plugin)
        
        # Initially disabled
        assert not registry.is_enabled("test_plugin")
        
        # Enable
        registry.enable("test_plugin")
        assert registry.is_enabled("test_plugin")
        
        # Disable
        registry.disable("test_plugin")
        assert not registry.is_enabled("test_plugin")
    
    def test_enable_unregistered_plugin(self):
        """Test that enabling unregistered plugin raises error."""
        registry = PluginRegistry()
        
        with pytest.raises(ValueError, match="not registered"):
            registry.enable("nonexistent")
    
    def test_get_enabled_plugins(self):
        """Test getting all enabled plugins."""
        registry = PluginRegistry()
        plugin1 = Mock()
        plugin2 = Mock()
        plugin3 = Mock()
        
        registry.register("plugin1", plugin1)
        registry.register("plugin2", plugin2)
        registry.register("plugin3", plugin3)
        
        registry.enable("plugin1")
        registry.enable("plugin3")
        
        enabled = registry.get_enabled_plugins()
        assert len(enabled) == 2
        assert "plugin1" in enabled
        assert "plugin3" in enabled
        assert "plugin2" not in enabled


class TestEnhancedPage:
    """Test enhanced page wrapper."""
    
    def test_init(self):
        """Test page initialization."""
        mock_page = Mock()
        config = {"test": "value"}
        
        enhanced = EnhancedPage(mock_page, config)
        assert enhanced._page is mock_page
        assert enhanced._config == config
    
    def test_transparent_attribute_access(self):
        """Test that non-method attributes are passed through."""
        mock_page = Mock()
        mock_page.url = "https://example.com"
        
        enhanced = EnhancedPage(mock_page)
        assert enhanced.url == "https://example.com"
    
    @pytest.mark.asyncio
    async def test_async_method_proxy(self):
        """Test that async methods are properly proxied."""
        mock_page = Mock()
        mock_page.goto = AsyncMock(return_value="result")
        
        enhanced = EnhancedPage(mock_page)
        result = await enhanced.goto("https://example.com")
        
        assert result == "result"
        mock_page.goto.assert_called_once_with("https://example.com")
    
    def test_sync_method_proxy(self):
        """Test that sync methods are properly proxied."""
        mock_page = Mock()
        mock_page.title = Mock(return_value="Page Title")
        
        enhanced = EnhancedPage(mock_page)
        result = enhanced.title()
        
        assert result == "Page Title"
        mock_page.title.assert_called_once()
    
    def test_plugin_registration(self):
        """Test plugin registration on page."""
        mock_page = Mock()
        enhanced = EnhancedPage(mock_page)
        plugin = Mock()
        
        enhanced.register_plugin("test_plugin", plugin)
        enhanced.enable_plugin("test_plugin")
        
        assert enhanced._plugin_registry.is_enabled("test_plugin")


class TestEnhancedBrowser:
    """Test enhanced browser wrapper."""
    
    def test_init(self):
        """Test browser initialization."""
        mock_browser = Mock()
        config = {"test": "value"}
        
        enhanced = EnhancedBrowser(mock_browser, config)
        assert enhanced._browser is mock_browser
        assert enhanced._config == config
    
    @pytest.mark.asyncio
    async def test_new_page_returns_enhanced(self):
        """Test that new_page returns an enhanced page."""
        mock_browser = Mock()
        mock_page = Mock()
        mock_browser.new_page = AsyncMock(return_value=mock_page)
        
        enhanced_browser = EnhancedBrowser(mock_browser)
        page = await enhanced_browser.new_page()
        
        assert isinstance(page, EnhancedPage)
        mock_browser.new_page.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_plugins_transferred_to_new_page(self):
        """Test that enabled plugins are transferred to new pages."""
        mock_browser = Mock()
        mock_page = Mock()
        mock_browser.new_page = AsyncMock(return_value=mock_page)
        
        enhanced_browser = EnhancedBrowser(mock_browser)
        plugin = Mock()
        enhanced_browser.register_plugin("test_plugin", plugin)
        enhanced_browser.enable_plugin("test_plugin")
        
        page = await enhanced_browser.new_page()
        assert page._plugin_registry.is_enabled("test_plugin")
    
    def test_attribute_proxy(self):
        """Test that browser attributes are proxied."""
        mock_browser = Mock()
        mock_browser.version = "1.40.0"
        
        enhanced = EnhancedBrowser(mock_browser)
        assert enhanced.version == "1.40.0"


class TestEnhanceFunction:
    """Test enhance() function."""
    
    def test_enhance_browser(self):
        """Test enhancing a browser object."""
        mock_browser = Mock()
        mock_browser.__class__.__name__ = "Browser"
        
        result = enhance(mock_browser)
        assert isinstance(result, EnhancedBrowser)
    
    def test_enhance_page(self):
        """Test enhancing a page object."""
        mock_page = Mock()
        mock_page.__class__.__name__ = "Page"
        
        result = enhance(mock_page)
        assert isinstance(result, EnhancedPage)
    
    def test_enhance_with_config(self):
        """Test enhancing with configuration."""
        mock_page = Mock()
        mock_page.__class__.__name__ = "Page"
        config = {"test": "value"}
        
        result = enhance(mock_page, config)
        assert result._config == config
    
    def test_enhance_invalid_type(self):
        """Test that enhancing invalid object raises error."""
        invalid_obj = Mock()
        invalid_obj.__class__.__name__ = "SomethingElse"
        
        with pytest.raises(TypeError, match="Cannot enhance"):
            enhance(invalid_obj)
