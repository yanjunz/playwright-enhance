# Quick Start Guide

## Installation

```bash
pip install playwright-enhance
playwright install chromium
```

For development:
```bash
git clone <repo-url>
cd playwright-enhance
pip install -e ".[dev]"
```

## Basic Usage

### 1. Enhance a Browser

```python
from playwright.async_api import async_playwright
from playwright_enhance import enhance

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        
        # Enhance the browser
        enhanced_browser = enhance(browser)
        
        # All pages created will be enhanced
        page = await enhanced_browser.new_page()
        await page.goto('https://example.com')
        
        await browser.close()
```

### 2. Enhance an Existing Page

```python
# Create a normal page
page = await browser.new_page()

# Enhance it
from playwright_enhance import enhance
enhanced_page = enhance(page)

await enhanced_page.goto('https://example.com')
```

### 3. Enable Smart Waiting

```python
from playwright_enhance import enhance
from playwright_enhance.capabilities import SmartWaitingPlugin

# Create enhanced browser with config
browser = await p.chromium.launch()
enhanced = enhance(browser, {
    'smart_waiting': {
        'enabled': True,
        'initial_timeout': 3000,  # 3 seconds
        'max_timeout': 8000,      # 8 seconds max
    }
})

page = await enhanced.new_page()

# Register and enable the plugin
plugin = SmartWaitingPlugin(enhanced._config['smart_waiting'])
page.register_plugin('smart_waiting', plugin)
page.enable_plugin('smart_waiting')

# Now navigation uses adaptive timeouts
await page.goto('https://example.com')
```

## Configuration

### Three Ways to Configure

#### 1. Runtime Configuration

```python
from playwright_enhance import Config

config = Config(
    smart_waiting={
        'enabled': True,
        'initial_timeout': 4000
    }
)

enhanced = enhance(browser, config.to_dict())
```

#### 2. Environment Variables

```bash
export PLAYWRIGHT_ENHANCE_SMART_WAITING__ENABLED=true
export PLAYWRIGHT_ENHANCE_SMART_WAITING__INITIAL_TIMEOUT=5000
```

```python
config = Config()  # Will load from environment
```

#### 3. Configuration File

**config.json:**
```json
{
  "smart_waiting": {
    "enabled": true,
    "initial_timeout": 3000,
    "max_timeout": 8000
  }
}
```

```python
config = Config(config_file='config.json')
```

### Configuration Priority

Runtime > Environment Variables > Config File > Defaults

## Available Capabilities

### ✅ Smart Waiting (Implemented)

Reduces waiting time by 50% through:
- Dynamic timeout adjustment (1-10s instead of fixed 30s)
- Page state prediction
- Resource preloading

**Configuration:**
```python
{
    'smart_waiting': {
        'enabled': bool,
        'initial_timeout': int,  # milliseconds
        'min_timeout': int,
        'max_timeout': int,
    }
}
```

### 🚧 Multi-Locator (Coming Soon)

Intelligent element location with:
- Semantic matching (aria-label, text content)
- Visual recognition (OpenCV)
- DOM fallback (CSS/XPath)

### 🚧 AI API (Coming Soon)

High-level semantic operations:
```python
await page.smart_click("Login button")
await page.smart_fill("username", "admin")
await page.batch_execute([...])
```

### 🚧 Concurrent Engine (Coming Soon)

Parallel operation execution for 3-5x speedup.

### 🚧 Cache System (Coming Soon)

Three-level caching for repeated operations.

### 🚧 Performance Monitor (Coming Soon)

Real-time performance metrics and profiling.

## Plugin Management

### Register a Plugin

```python
from playwright_enhance.capabilities.smart_waiting import SmartWaitingPlugin

plugin = SmartWaitingPlugin(config)
page.register_plugin('smart_waiting', plugin)
```

### Enable/Disable

```python
# Enable
page.enable_plugin('smart_waiting')

# Check status
is_enabled = page._plugin_registry.is_enabled('smart_waiting')

# Disable
page.disable_plugin('smart_waiting')
```

### Create Custom Plugin

```python
class MyPlugin:
    async def before_goto(self, page, url, **kwargs):
        """Called before page.goto()"""
        print(f"About to navigate to: {url}")
        return None  # Return None to continue with original method
    
    async def after_goto(self, page, result, url, **kwargs):
        """Called after page.goto()"""
        print(f"Navigated to: {url}")
        return result  # Can modify result

# Register and enable
page.register_plugin('my_plugin', MyPlugin())
page.enable_plugin('my_plugin')
```

## Testing

### Run Tests

```bash
# All tests
pytest

# Specific capability
pytest tests/unit/test_smart_waiting.py

# With coverage
pytest --cov=playwright_enhance --cov-report=html
```

### Run Examples

```bash
python examples/basic_usage.py
```

## Next Steps

- Check out [API Reference](api-reference.md)
- See [Performance Guide](performance.md)
- Read [Implementation Status](../IMPLEMENTATION_STATUS.md)
- Explore [Examples](../examples/)

## Getting Help

- 🐛 [Report issues](https://github.com/yourusername/playwright-enhance/issues)
- 💬 [Discussions](https://github.com/yourusername/playwright-enhance/discussions)
- 📖 [Full Documentation](https://playwright-enhance.readthedocs.io)
