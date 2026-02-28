#!/bin/bash
# Publish to TestPyPI for testing

set -e

echo "🧪 Publishing to TestPyPI..."
echo "================================"

# Check if we're in the right directory
if [ ! -f "pyproject.toml" ]; then
    echo "❌ Error: pyproject.toml not found. Run this from the project root."
    exit 1
fi

# Clean old builds
echo "🧹 Cleaning old builds..."
rm -rf dist/ build/ *.egg-info

# Install build tools
echo "📦 Installing build tools..."
pip install --upgrade build twine

# Build package
echo "🔨 Building package..."
python -m build

# Check package
echo "✅ Checking package..."
twine check dist/*

# Upload to TestPyPI
echo "📤 Uploading to TestPyPI..."
echo ""
echo "You'll need your TestPyPI API token."
echo "Get it from: https://test.pypi.org/manage/account/token/"
echo ""

twine upload --repository testpypi dist/*

echo ""
echo "✅ Published to TestPyPI!"
echo ""
echo "Test installation with:"
echo "  pip install --index-url https://test.pypi.org/simple/ playwright-enhance"
echo ""
echo "View your package at:"
echo "  https://test.pypi.org/project/playwright-enhance/"
