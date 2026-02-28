#!/bin/bash
# Verify installation in a clean environment

set -e

echo "🧪 Verifying playwright-enhance installation..."
echo "=============================================="

# Create temporary virtual environment
TEMP_DIR=$(mktemp -d)
echo "📁 Creating test environment in $TEMP_DIR"

cd "$TEMP_DIR"
python3 -m venv test_env
source test_env/bin/activate

echo ""
echo "📦 Installing playwright-enhance from GitHub..."
pip install git+https://github.com/yanjunz/playwright-enhance.git

echo ""
echo "📦 Installing browser..."
playwright install chromium

echo ""
echo "✅ Testing import..."
python3 -c "
from playwright_enhance import enhance
print('✅ Import successful')

from playwright.sync_api import sync_playwright
print('✅ Playwright import successful')
"

echo ""
echo "✅ Testing CLI..."
playwright-enhance-cli --help

echo ""
echo "🎉 All verification tests passed!"
echo ""
echo "Cleaning up..."
deactivate
rm -rf "$TEMP_DIR"

echo "✅ Done!"
