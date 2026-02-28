#!/bin/bash

# Playwright-Compatible CLI 演示
# ================================
# 展示与 Playwright CLI 兼容的命令

set -e

# 颜色输出
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "======================================================"
echo "🎭 Playwright-Compatible CLI 演示"
echo "======================================================"
echo ""
echo "演示 playwright-enhance-cli 与 playwright CLI 的兼容性"
echo ""

URL="https://example.com"

# 1. Screenshot
echo ""
echo -e "${YELLOW}[1/5] 截图命令 (screenshot)${NC}"
echo "------------------------------------------------------"
echo "命令: playwright-enhance-cli screenshot $URL /tmp/test-native.png"
python -m playwright_enhance.cli screenshot "$URL" /tmp/test-native.png

echo ""
echo "命令: playwright-enhance-cli screenshot $URL /tmp/test-enhanced.png --enhanced"
python -m playwright_enhance.cli screenshot "$URL" /tmp/test-enhanced.png --enhanced

# 2. PDF
echo ""
echo -e "${YELLOW}[2/5] PDF 生成命令 (pdf)${NC}"
echo "------------------------------------------------------"
echo "命令: playwright-enhance-cli pdf $URL /tmp/test-enhanced.pdf --enhanced"
python -m playwright_enhance.cli pdf "$URL" /tmp/test-enhanced.pdf --enhanced

# 3. Browser shortcuts
echo ""
echo -e "${YELLOW}[3/5] 浏览器快捷命令 (cr/ff/wk)${NC}"
echo "------------------------------------------------------"
echo "✅ 支持的快捷命令:"
echo "  - cr (Chromium)"
echo "  - ff (Firefox)"  
echo "  - wk (WebKit)"
echo ""
echo "示例: playwright-enhance-cli cr https://example.com --enhanced"
echo "（跳过实际运行，因为会打开浏览器）"

# 4. Install
echo ""
echo -e "${YELLOW}[4/5] 安装命令 (install/install-deps)${NC}"
echo "------------------------------------------------------"
echo "✅ 支持的安装命令:"
echo "  - playwright-enhance-cli install"
echo "  - playwright-enhance-cli install chromium firefox"
echo "  - playwright-enhance-cli install --with-deps"
echo "  - playwright-enhance-cli install-deps"
echo ""
echo "（跳过实际运行）"

# 5. Benchmark
echo ""
echo -e "${YELLOW}[5/5] 性能基准测试 (bench run)${NC}"
echo "------------------------------------------------------"
echo "命令: playwright-enhance-cli bench run $URL --runs 2"
python -m playwright_enhance.cli bench run "$URL" --runs 2

# Summary
echo ""
echo "======================================================"
echo -e "${GREEN}✅ 演示完成！${NC}"
echo "======================================================"
echo ""
echo "📊 命令对照:"
echo ""
echo "Playwright CLI              →  Playwright-Enhance CLI"
echo "------------------------------------------------------"
echo "playwright screenshot       →  playwright-enhance-cli screenshot [--enhanced]"
echo "playwright pdf              →  playwright-enhance-cli pdf [--enhanced]"
echo "playwright open             →  playwright-enhance-cli open [--enhanced]"
echo "playwright cr/ff/wk         →  playwright-enhance-cli cr/ff/wk [--enhanced]"
echo "playwright install          →  playwright-enhance-cli install"
echo "playwright install-deps     →  playwright-enhance-cli install-deps"
echo "playwright codegen          →  playwright-enhance-cli codegen (重定向)"
echo "(无)                        →  playwright-enhance-cli bench run (新增)"
echo "(无)                        →  playwright-enhance-cli config (新增)"
echo "(无)                        →  playwright-enhance-cli info (新增)"
echo ""
echo "💡 提示:"
echo "  - 所有命令都支持 --enhanced 选项启用智能优化"
echo "  - 完全兼容 Playwright CLI 命令格式"
echo "  - 新增性能测试和配置管理功能"
echo ""
echo "📖 完整命令参考: CLI_COMMANDS_REFERENCE.md"
echo ""
