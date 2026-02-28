"""Integration tests for Playwright API compatibility."""

import pytest
from playwright.async_api import async_playwright
from playwright_enhance import enhance


@pytest.mark.asyncio
async def test_basic_navigation():
    """Test basic page navigation compatibility."""
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        enhanced_browser = enhance(browser)
        page = await enhanced_browser.new_page()
        
        # Test basic navigation
        response = await page.goto('https://example.com')
        assert response.status == 200
        
        # Test URL property
        assert 'example.com' in page.url
        
        await browser.close()


@pytest.mark.asyncio
async def test_element_interaction():
    """Test element interaction compatibility."""
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        enhanced_browser = enhance(browser)
        page = await enhanced_browser.new_page()
        
        await page.goto('data:text/html,<button id="btn">Click me</button>')
        
        # Test element selection
        button = await page.query_selector('#btn')
        assert button is not None
        
        # Test click
        await button.click()
        
        await browser.close()


@pytest.mark.asyncio
async def test_page_properties():
    """Test page property access compatibility."""
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        enhanced_browser = enhance(browser)
        page = await enhanced_browser.new_page()
        
        await page.goto('data:text/html,<title>Test Page</title>')
        
        # Test title
        title = await page.title()
        assert title == 'Test Page'
        
        # Test content
        content = await page.content()
        assert '<title>Test Page</title>' in content
        
        await browser.close()


@pytest.mark.asyncio
async def test_multiple_pages():
    """Test creating multiple enhanced pages."""
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        enhanced_browser = enhance(browser)
        
        # Create multiple pages
        page1 = await enhanced_browser.new_page()
        page2 = await enhanced_browser.new_page()
        
        await page1.goto('data:text/html,<h1>Page 1</h1>')
        await page2.goto('data:text/html,<h1>Page 2</h1>')
        
        content1 = await page1.content()
        content2 = await page2.content()
        
        assert 'Page 1' in content1
        assert 'Page 2' in content2
        
        await browser.close()


@pytest.mark.asyncio
async def test_enhance_existing_page():
    """Test enhancing an existing page."""
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        
        # Enhance existing page
        enhanced_page = enhance(page)
        
        await enhanced_page.goto('https://example.com')
        assert 'example.com' in enhanced_page.url
        
        await browser.close()


@pytest.mark.asyncio
async def test_plugin_enable_disable():
    """Test plugin enable/disable functionality."""
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        enhanced_browser = enhance(browser)
        
        # Register and enable a mock plugin
        from unittest.mock import Mock
        plugin = Mock()
        enhanced_browser.register_plugin('test_plugin', plugin)
        enhanced_browser.enable_plugin('test_plugin')
        
        # New pages should have plugin enabled
        page = await enhanced_browser.new_page()
        assert page._plugin_registry.is_enabled('test_plugin')
        
        # Disable plugin
        page.disable_plugin('test_plugin')
        assert not page._plugin_registry.is_enabled('test_plugin')
        
        await browser.close()
