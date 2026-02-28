#!/bin/bash
# Test playwright-enhance with real websites

set -e

echo "🌐 Testing playwright-enhance on Real Websites"
echo "=============================================="
echo ""

# Create temp directory
TEMP_DIR=$(mktemp -d)
cd "$TEMP_DIR"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Cleanup
cleanup() {
    echo ""
    echo "🧹 Cleaning up..."
    deactivate 2>/dev/null || true
    cd /
    rm -rf "$TEMP_DIR"
}
trap cleanup EXIT

# Setup environment
echo -e "${BLUE}📦 Setting up environment...${NC}"
python3 -m venv venv
source venv/bin/activate
pip install --quiet playwright-enhance
playwright install chromium --quiet

# Test websites
declare -a WEBSITES=(
    "https://example.com|Example Domain"
    "https://news.ycombinator.com|Hacker News"
    "https://github.com|GitHub"
    "https://www.wikipedia.org|Wikipedia"
)

echo ""
echo -e "${YELLOW}Testing with real websites...${NC}"
echo ""

# Create test script
cat > test_websites.py << 'PYTHON_EOF'
import sys
import time
from playwright.sync_api import sync_playwright
from playwright_enhance import enhance

def test_website(url, expected_title_part):
    """Test a website and measure performance"""
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            
            # Test with enhancement
            enhanced = enhance(browser, {
                'smart_waiting': {'enabled': True}
            })
            
            start = time.time()
            page = enhanced.new_page()
            page.goto(url, wait_until='domcontentloaded')
            load_time = time.time() - start
            
            title = page.title()
            
            # Check if title contains expected part
            if expected_title_part.lower() in title.lower():
                print(f'✅ {url}')
                print(f'   Title: {title[:60]}...' if len(title) > 60 else f'   Title: {title}')
                print(f'   Load time: {load_time:.2f}s')
                result = True
            else:
                print(f'❌ {url}')
                print(f'   Expected: {expected_title_part}')
                print(f'   Got: {title}')
                result = False
            
            browser.close()
            return result, load_time
            
    except Exception as e:
        print(f'❌ {url}')
        print(f'   Error: {str(e)}')
        return False, 0

if __name__ == '__main__':
    url = sys.argv[1]
    expected = sys.argv[2]
    success, load_time = test_website(url, expected)
    sys.exit(0 if success else 1)
PYTHON_EOF

# Test each website
SUCCESS_COUNT=0
FAIL_COUNT=0
TOTAL_TIME=0

for website_info in "${WEBSITES[@]}"; do
    IFS='|' read -r url expected_title <<< "$website_info"
    
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    
    if python test_websites.py "$url" "$expected_title"; then
        ((SUCCESS_COUNT++))
    else
        ((FAIL_COUNT++))
    fi
    
    echo ""
done

# Summary
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}Test Summary${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo "Total websites tested: $((SUCCESS_COUNT + FAIL_COUNT))"
echo -e "${GREEN}Successful: $SUCCESS_COUNT${NC}"
if [ $FAIL_COUNT -gt 0 ]; then
    echo -e "${RED}Failed: $FAIL_COUNT${NC}"
else
    echo "Failed: $FAIL_COUNT"
fi
echo ""

if [ $FAIL_COUNT -eq 0 ]; then
    echo -e "${GREEN}🎉 All website tests passed!${NC}"
    exit 0
else
    echo -e "${RED}⚠️  Some tests failed${NC}"
    exit 1
fi
