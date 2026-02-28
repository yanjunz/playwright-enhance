#!/bin/bash
# Test GitHub installation (current available method)

set -e

echo "🧪 Testing playwright-enhance from GitHub"
echo "=========================================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Create temp directory
TEMP_DIR=$(mktemp -d)
echo -e "${BLUE}📁 Test directory: $TEMP_DIR${NC}"
cd "$TEMP_DIR"

# Cleanup
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
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
echo ""
echo -e "${BLUE}⬆️  Upgrading pip...${NC}"
pip install --upgrade pip --quiet

# Install from GitHub
echo ""
echo -e "${YELLOW}📥 Installing from GitHub...${NC}"
echo "   Repository: https://github.com/yanjunz/playwright-enhance"
echo ""

if pip install git+https://github.com/yanjunz/playwright-enhance.git --quiet 2>&1; then
    echo -e "${GREEN}✅ Installation successful${NC}"
else
    echo -e "${RED}❌ Installation failed${NC}"
    echo ""
    echo "Trying without --quiet flag..."
    if pip install git+https://github.com/yanjunz/playwright-enhance.git; then
        echo -e "${GREEN}✅ Installation successful (retry)${NC}"
    else
        exit 1
    fi
fi

# Check version
echo ""
echo -e "${BLUE}📋 Package information:${NC}"
pip show playwright-enhance | grep -E "Name|Version|Location|Requires"

# Install Playwright browsers
echo ""
echo -e "${BLUE}🌐 Installing Playwright browsers...${NC}"
if playwright install chromium --quiet; then
    echo -e "${GREEN}✅ Browser installation successful${NC}"
else
    echo -e "${RED}❌ Browser installation failed${NC}"
    exit 1
fi

# Test 1: Import
echo ""
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}Test 1: Import Test${NC}"
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
if python3 -c "
from playwright_enhance import enhance
from playwright_enhance.config import Config
print('✅ All imports successful')
"; then
    echo -e "${GREEN}✅ Test 1 PASSED${NC}"
else
    echo -e "${RED}❌ Test 1 FAILED${NC}"
    exit 1
fi

# Test 2: Basic functionality
echo ""
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}Test 2: Basic Functionality Test${NC}"
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
    page.goto('https://example.com', wait_until='domcontentloaded')
    title = page.title()
    
    print(f'✅ Page title: {title}')
    assert 'Example Domain' in title
    
    browser.close()
    print('✅ Basic functionality test successful')
EOF
then
    echo -e "${GREEN}✅ Test 2 PASSED${NC}"
else
    echo -e "${RED}❌ Test 2 FAILED${NC}"
    exit 1
fi

# Test 3: CLI tool
echo ""
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}Test 3: CLI Tool Test${NC}"
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

if command -v playwright-enhance-cli &> /dev/null; then
    echo -e "${GREEN}✅ CLI command found${NC}"
    
    if playwright-enhance-cli --help > /dev/null 2>&1; then
        echo -e "${GREEN}✅ CLI help command works${NC}"
    else
        echo -e "${RED}❌ CLI help failed${NC}"
        exit 1
    fi
    
    if playwright-enhance-cli screenshot https://example.com test.png --enhanced; then
        if [ -f "test.png" ]; then
            echo -e "${GREEN}✅ CLI screenshot works${NC}"
            rm -f test.png
        fi
    fi
    
    echo -e "${GREEN}✅ Test 3 PASSED${NC}"
else
    echo -e "${RED}❌ CLI command not found${NC}"
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
echo "   ✅ Test 2: Basic functionality"
echo "   ✅ Test 3: CLI tool"
echo ""
echo -e "${GREEN}✅ GitHub installation verified!${NC}"
echo ""
echo -e "${BLUE}Installation command for users:${NC}"
echo "   pip install git+https://github.com/yanjunz/playwright-enhance.git"
