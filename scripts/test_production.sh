#!/bin/bash
# Test production installation from PyPI

set -e

echo "🧪 Testing playwright-enhance from PyPI (Production)"
echo "===================================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Create temporary directory
TEMP_DIR=$(mktemp -d)
echo -e "${BLUE}📁 Creating test environment in: $TEMP_DIR${NC}"
cd "$TEMP_DIR"

# Function to cleanup
cleanup() {
    echo ""
    echo -e "${BLUE}🧹 Cleaning up...${NC}"
    deactivate 2>/dev/null || true
    cd /
    rm -rf "$TEMP_DIR"
}
trap cleanup EXIT

# Create virtual environment
echo -e "${BLUE}📦 Creating virtual environment...${NC}"
python3 -m venv test_env
source test_env/bin/activate

# Upgrade pip
echo ""
echo -e "${BLUE}⬆️  Upgrading pip...${NC}"
pip install --upgrade pip --quiet

# Install from PyPI
echo ""
echo -e "${YELLOW}📥 Installing playwright-enhance from PyPI...${NC}"
echo "   Command: pip install playwright-enhance"
if pip install playwright-enhance; then
    echo -e "${GREEN}✅ Installation successful${NC}"
else
    echo -e "${RED}❌ Installation failed${NC}"
    exit 1
fi

# Check installed version
echo ""
echo -e "${BLUE}📋 Checking installed version...${NC}"
VERSION=$(pip show playwright-enhance | grep Version | cut -d' ' -f2)
echo -e "   Version: ${GREEN}${VERSION}${NC}"

# Install Playwright browsers
echo ""
echo -e "${BLUE}🌐 Installing Playwright browsers...${NC}"
if playwright install chromium --quiet; then
    echo -e "${GREEN}✅ Browser installation successful${NC}"
else
    echo -e "${RED}❌ Browser installation failed${NC}"
    exit 1
fi

# Test 1: Import test
echo ""
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}Test 1: Import Test${NC}"
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
if python3 -c "
from playwright_enhance import enhance
from playwright_enhance.config import Config, SmartWaitingConfig
print('✅ All imports successful')
"; then
    echo -e "${GREEN}✅ Test 1 PASSED${NC}"
else
    echo -e "${RED}❌ Test 1 FAILED${NC}"
    exit 1
fi

# Test 2: Basic functionality (sync)
echo ""
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}Test 2: Basic Sync API Test${NC}"
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
if python3 << 'EOF'
from playwright.sync_api import sync_playwright
from playwright_enhance import enhance

with sync_playwright() as p:
    browser = p.chromium.launch()
    enhanced = enhance(browser, {
        'smart_waiting': {'enabled': True}
    })
    
    page = enhanced.new_page()
    page.goto('https://example.com')
    title = page.title()
    
    print(f'✅ Page title: {title}')
    assert 'Example Domain' in title, 'Title check failed'
    
    browser.close()
    print('✅ Sync API test successful')
EOF
then
    echo -e "${GREEN}✅ Test 2 PASSED${NC}"
else
    echo -e "${RED}❌ Test 2 FAILED${NC}"
    exit 1
fi

# Test 3: Async functionality
echo ""
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}Test 3: Async API Test${NC}"
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
if python3 << 'EOF'
import asyncio
from playwright.async_api import async_playwright
from playwright_enhance import enhance

async def test_async():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        enhanced = enhance(browser, {
            'smart_waiting': {'enabled': True}
        })
        
        page = await enhanced.new_page()
        await page.goto('https://example.com')
        title = await page.title()
        
        print(f'✅ Page title: {title}')
        assert 'Example Domain' in title, 'Title check failed'
        
        await browser.close()
        print('✅ Async API test successful')

asyncio.run(test_async())
EOF
then
    echo -e "${GREEN}✅ Test 3 PASSED${NC}"
else
    echo -e "${RED}❌ Test 3 FAILED${NC}"
    exit 1
fi

# Test 4: CLI tool
echo ""
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}Test 4: CLI Tool Test${NC}"
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

# Check CLI exists
if command -v playwright-enhance-cli &> /dev/null; then
    echo -e "${GREEN}✅ CLI command found${NC}"
else
    echo -e "${RED}❌ CLI command not found${NC}"
    exit 1
fi

# Test CLI help
if playwright-enhance-cli --help > /dev/null 2>&1; then
    echo -e "${GREEN}✅ CLI help command works${NC}"
else
    echo -e "${RED}❌ CLI help command failed${NC}"
    exit 1
fi

# Test CLI screenshot
if playwright-enhance-cli screenshot https://example.com test_output.png --enhanced; then
    if [ -f "test_output.png" ]; then
        echo -e "${GREEN}✅ CLI screenshot command works${NC}"
        rm -f test_output.png
    else
        echo -e "${RED}❌ Screenshot file not created${NC}"
        exit 1
    fi
else
    echo -e "${RED}❌ CLI screenshot command failed${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Test 4 PASSED${NC}"

# Test 5: Configuration
echo ""
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}Test 5: Configuration Test${NC}"
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
if python3 << 'EOF'
from playwright_enhance.config import Config, SmartWaitingConfig, ResourceHintsConfig

# Test default config
config = Config()
print(f'✅ Default config created')

# Test custom config
custom_config = Config(
    smart_waiting=SmartWaitingConfig(
        enabled=True,
        base_timeout=5000
    ),
    resource_hints=ResourceHintsConfig(
        enabled=True
    )
)
print(f'✅ Custom config created')

# Test dict conversion
config_dict = custom_config.to_dict()
assert config_dict['smart_waiting']['enabled'] == True
print(f'✅ Config to dict conversion works')

print('✅ Configuration test successful')
EOF
then
    echo -e "${GREEN}✅ Test 5 PASSED${NC}"
else
    echo -e "${RED}❌ Test 5 FAILED${NC}"
    exit 1
fi

# Test 6: Performance check
echo ""
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}Test 6: Performance Check${NC}"
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
if python3 << 'EOF'
import time
from playwright.sync_api import sync_playwright
from playwright_enhance import enhance

# Test with enhancement
with sync_playwright() as p:
    browser = p.chromium.launch()
    enhanced = enhance(browser, {
        'smart_waiting': {'enabled': True}
    })
    
    start = time.time()
    page = enhanced.new_page()
    page.goto('https://example.com')
    enhanced_time = time.time() - start
    
    browser.close()

print(f'✅ Page load time: {enhanced_time:.2f}s')
assert enhanced_time < 10, f'Performance too slow: {enhanced_time:.2f}s'
print('✅ Performance check passed')
EOF
then
    echo -e "${GREEN}✅ Test 6 PASSED${NC}"
else
    echo -e "${RED}❌ Test 6 FAILED${NC}"
    exit 1
fi

# Summary
echo ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}🎉 All Tests PASSED!${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${BLUE}📊 Test Summary:${NC}"
echo "   ✅ Test 1: Import test"
echo "   ✅ Test 2: Sync API test"
echo "   ✅ Test 3: Async API test"
echo "   ✅ Test 4: CLI tool test"
echo "   ✅ Test 5: Configuration test"
echo "   ✅ Test 6: Performance check"
echo ""
echo -e "${GREEN}✅ playwright-enhance v${VERSION} is working correctly!${NC}"
echo ""
echo -e "${BLUE}Package info:${NC}"
pip show playwright-enhance
echo ""
echo -e "${GREEN}🚀 Production installation verified!${NC}"
