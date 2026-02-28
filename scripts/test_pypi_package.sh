#!/bin/bash
# Quick test of package installation (PyPI or GitHub)

set -e

echo "🧪 Quick Package Installation Test"
echo "===================================="
echo ""

# Check if first argument is a flag
INSTALL_SOURCE="${1:-pypi}"

# Create temp directory
TEMP_DIR=$(mktemp -d)
echo "📁 Test directory: $TEMP_DIR"
cd "$TEMP_DIR"

# Cleanup function
cleanup() {
    echo ""
    echo "🧹 Cleaning up..."
    deactivate 2>/dev/null || true
    cd /
    rm -rf "$TEMP_DIR"
}
trap cleanup EXIT

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install package
echo ""
if [ "$INSTALL_SOURCE" = "github" ]; then
    echo "📥 Installing from GitHub..."
    pip install git+https://github.com/yanjunz/playwright-enhance.git
elif [ "$INSTALL_SOURCE" = "pypi" ]; then
    echo "📥 Installing from PyPI..."
    if pip install playwright-enhance 2>/dev/null; then
        echo "✅ PyPI installation successful"
    else
        echo "⚠️  PyPI installation failed (package not yet published?)"
        echo "📥 Falling back to GitHub installation..."
        pip install git+https://github.com/yanjunz/playwright-enhance.git
    fi
else
    # Treat as version number
    echo "📥 Installing version $INSTALL_SOURCE from PyPI..."
    pip install playwright-enhance==$INSTALL_SOURCE
fi

# Install browser
echo ""
echo "🌐 Installing Chromium..."
playwright install chromium --quiet

# Quick import test
echo ""
echo "✅ Testing import..."
python3 -c "
from playwright_enhance import enhance
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    enhanced = enhance(browser)
    page = enhanced.new_page()
    page.goto('https://example.com', wait_until='domcontentloaded')
    print(f'✅ Title: {page.title()}')
    browser.close()

print('✅ All tests passed!')
"

echo ""
echo "🎉 Package is working correctly!"
echo ""
echo "Installed version:"
pip show playwright-enhance | grep -E "Name|Version|Location"
