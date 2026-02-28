#!/bin/bash
# Publish to PyPI (Production)

set -e

echo "🚀 Publishing to PyPI (Production)..."
echo "====================================="
echo ""
echo "⚠️  WARNING: This will publish to the REAL PyPI!"
echo "Make sure you've tested on TestPyPI first."
echo ""
read -p "Continue? (yes/no): " confirm

if [ "$confirm" != "yes" ]; then
    echo "❌ Aborted."
    exit 1
fi

# Check if we're in the right directory
if [ ! -f "pyproject.toml" ]; then
    echo "❌ Error: pyproject.toml not found. Run this from the project root."
    exit 1
fi

# Check git status
if [ -n "$(git status --porcelain)" ]; then
    echo "⚠️  Warning: You have uncommitted changes."
    git status --short
    echo ""
    read -p "Continue anyway? (yes/no): " confirm
    if [ "$confirm" != "yes" ]; then
        echo "❌ Aborted."
        exit 1
    fi
fi

# Get current version
VERSION=$(grep '^version = ' pyproject.toml | cut -d'"' -f2)
echo "📌 Current version: $VERSION"
echo ""

# Check if tag exists
if git rev-parse "v$VERSION" >/dev/null 2>&1; then
    echo "✅ Git tag v$VERSION exists"
else
    echo "⚠️  Git tag v$VERSION does not exist"
    read -p "Create tag now? (yes/no): " create_tag
    if [ "$create_tag" = "yes" ]; then
        git tag -a "v$VERSION" -m "Release v$VERSION"
        git push origin "v$VERSION"
        echo "✅ Tag created and pushed"
    fi
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

# Upload to PyPI
echo "📤 Uploading to PyPI..."
echo ""
echo "You'll need your PyPI API token."
echo "Get it from: https://pypi.org/manage/account/token/"
echo ""

twine upload dist/*

echo ""
echo "🎉 Successfully published to PyPI!"
echo ""
echo "Users can now install with:"
echo "  pip install playwright-enhance"
echo ""
echo "View your package at:"
echo "  https://pypi.org/project/playwright-enhance/"
echo ""
echo "Next steps:"
echo "1. Create GitHub Release: https://github.com/yanjunz/playwright-enhance/releases/new"
echo "2. Update README.md installation instructions"
echo "3. Announce on social media / community"
