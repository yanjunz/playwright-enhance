#!/bin/bash
# Test installation on multiple Python versions

set -e

echo "🧪 Testing playwright-enhance on Multiple Python Versions"
echo "========================================================="
echo ""

# Python versions to test
PYTHON_VERSIONS=("3.8" "3.9" "3.10" "3.11" "3.12")

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

# Results array
declare -a RESULTS

# Test each Python version
for PY_VERSION in "${PYTHON_VERSIONS[@]}"; do
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}Testing Python $PY_VERSION${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    
    # Check if Python version is available
    if command -v "python$PY_VERSION" &> /dev/null; then
        TEMP_DIR=$(mktemp -d)
        cd "$TEMP_DIR"
        
        # Create virtual environment
        echo "📦 Creating virtual environment..."
        "python$PY_VERSION" -m venv "venv_$PY_VERSION"
        source "venv_$PY_VERSION/bin/activate"
        
        # Install and test
        if pip install --quiet playwright-enhance && \
           playwright install chromium --quiet && \
           python -c "from playwright_enhance import enhance; print('✅ OK')"; then
            echo -e "${GREEN}✅ Python $PY_VERSION: PASSED${NC}"
            RESULTS+=("${GREEN}✅ Python $PY_VERSION: PASSED${NC}")
        else
            echo -e "${RED}❌ Python $PY_VERSION: FAILED${NC}"
            RESULTS+=("${RED}❌ Python $PY_VERSION: FAILED${NC}")
        fi
        
        # Cleanup
        deactivate
        cd /
        rm -rf "$TEMP_DIR"
    else
        echo -e "${RED}⚠️  Python $PY_VERSION not installed${NC}"
        RESULTS+=("${RED}⚠️  Python $PY_VERSION: NOT INSTALLED${NC}")
    fi
    
    echo ""
done

# Summary
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}Test Summary${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
for result in "${RESULTS[@]}"; do
    echo -e "$result"
done
echo ""
