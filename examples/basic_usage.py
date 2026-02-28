"""
Basic usage examples for playwright-enhance.

This demonstrates the core functionality currently implemented.
"""

import asyncio
from playwright.async_api import async_playwright
from playwright_enhance import enhance, Config


async def example_1_basic_enhancement():
    """Example 1: Basic browser enhancement."""
    print("=== Example 1: Basic Enhancement ===")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        
        # Enhance the browser - all new pages will be enhanced
        enhanced_browser = enhance(browser)
        
        page = await enhanced_browser.new_page()
        await page.goto('https://example.com')
        
        print(f"✅ Loaded: {page.url}")
        print(f"   Title: {await page.title()}")
        
        await browser.close()


async def example_2_smart_waiting():
    """Example 2: Enable smart waiting capability."""
    print("\n=== Example 2: Smart Waiting ===")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        
        # Configure with smart waiting enabled
        config = {
            'smart_waiting': {
                'enabled': True,
                'initial_timeout': 3000,  # 3 seconds initial
                'max_timeout': 8000,      # 8 seconds max
            }
        }
        
        enhanced_browser = enhance(browser, config)
        page = await enhanced_browser.new_page()
        
        # Enable the smart waiting plugin
        page.register_plugin('smart_waiting', 
                           __import__('playwright_enhance.capabilities.smart_waiting', 
                                    fromlist=['SmartWaitingPlugin']).SmartWaitingPlugin(config['smart_waiting']))
        page.enable_plugin('smart_waiting')
        
        print("✅ Smart waiting enabled")
        print(f"   Initial timeout: {config['smart_waiting']['initial_timeout']}ms")
        print(f"   Max timeout: {config['smart_waiting']['max_timeout']}ms")
        
        # Navigation will use adaptive timeouts
        await page.goto('https://example.com')
        print(f"✅ Loaded with smart waiting: {page.url}")
        
        await browser.close()


async def example_3_configuration_sources():
    """Example 3: Configuration from multiple sources."""
    print("\n=== Example 3: Configuration Sources ===")
    
    # Method 1: Runtime configuration
    config1 = Config(smart_waiting={'enabled': True, 'initial_timeout': 4000})
    print(f"✅ Runtime config: timeout = {config1.get('smart_waiting.initial_timeout')}ms")
    
    # Method 2: Environment variables (example)
    # export PLAYWRIGHT_ENHANCE_SMART_WAITING__ENABLED=true
    # export PLAYWRIGHT_ENHANCE_SMART_WAITING__INITIAL_TIMEOUT=5000
    import os
    os.environ['PLAYWRIGHT_ENHANCE_SMART_WAITING__ENABLED'] = 'true'
    os.environ['PLAYWRIGHT_ENHANCE_SMART_WAITING__INITIAL_TIMEOUT'] = '5000'
    
    config2 = Config()
    print(f"✅ Env config: enabled = {config2.get('smart_waiting.enabled')}")
    print(f"   Env config: timeout = {config2.get('smart_waiting.initial_timeout')}ms")
    
    # Method 3: Config file
    config_dict = {
        "smart_waiting": {
            "enabled": True,
            "initial_timeout": 6000
        }
    }
    
    import tempfile
    import json
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(config_dict, f)
        config_file = f.name
    
    config3 = Config(config_file=config_file)
    print(f"✅ File config: timeout = {config3.get('smart_waiting.initial_timeout')}ms")
    
    # Cleanup
    import os
    os.unlink(config_file)


async def example_4_plugin_management():
    """Example 4: Managing plugins dynamically."""
    print("\n=== Example 4: Plugin Management ===")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        enhanced_browser = enhance(browser)
        page = await enhanced_browser.new_page()
        
        # Register a plugin
        from playwright_enhance.capabilities.smart_waiting import SmartWaitingPlugin
        plugin = SmartWaitingPlugin({'initial_timeout': 3000})
        page.register_plugin('smart_waiting', plugin)
        
        print("✅ Plugin registered: smart_waiting")
        
        # Enable it
        page.enable_plugin('smart_waiting')
        print("✅ Plugin enabled")
        print(f"   Is enabled: {page._plugin_registry.is_enabled('smart_waiting')}")
        
        # Disable it
        page.disable_plugin('smart_waiting')
        print("✅ Plugin disabled")
        print(f"   Is enabled: {page._plugin_registry.is_enabled('smart_waiting')}")
        
        await browser.close()


async def example_5_enhance_existing_page():
    """Example 5: Enhance an existing page."""
    print("\n=== Example 5: Enhance Existing Page ===")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        
        # Create a normal page
        page = await browser.new_page()
        print("✅ Created normal Playwright page")
        
        # Enhance it
        enhanced_page = enhance(page)
        print("✅ Enhanced existing page")
        
        await enhanced_page.goto('https://example.com')
        print(f"✅ Loaded: {enhanced_page.url}")
        
        await browser.close()


async def main():
    """Run all examples."""
    print("🚀 Playwright-Enhance Examples\n")
    print("Current implementation includes:")
    print("  ✅ Core wrapper with plugin system")
    print("  ✅ Multi-source configuration")
    print("  ✅ Smart waiting capability")
    print("  ✅ 100% Playwright API compatibility")
    print()
    
    await example_1_basic_enhancement()
    await example_2_smart_waiting()
    await example_3_configuration_sources()
    await example_4_plugin_management()
    await example_5_enhance_existing_page()
    
    print("\n✨ All examples completed!")
    print("\nNext steps:")
    print("  - Check out the tests: pytest tests/")
    print("  - Read the docs: docs/")
    print("  - See implementation status: IMPLEMENTATION_STATUS.md")


if __name__ == "__main__":
    asyncio.run(main())
