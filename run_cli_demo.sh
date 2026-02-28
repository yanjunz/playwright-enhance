#!/bin/bash

# Playwright CLI 快速演示脚本
# ========================================
# 非交互式，直接运行所有测试

set -e

# 颜色输出
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "======================================================"
echo "🚀 Playwright-Enhance CLI 快速演示"
echo "======================================================"
echo ""

# 测试 URL
URL="https://example.com"
NAME="Example Domain"

echo -e "${BLUE}📍 测试网站: ${NAME}${NC}"
echo -e "${BLUE}🔗 URL: ${URL}${NC}"
echo ""
echo "======================================================"

# 1. 基准测试 - 原生模式
echo ""
echo -e "${YELLOW}[1/4] 基准测试 - 原生 Playwright${NC}"
echo "------------------------------------------------------"
python -m playwright_enhance.cli benchmark "$URL" --headless --native

# 2. 基准测试 - 增强模式
echo ""
echo -e "${YELLOW}[2/4] 基准测试 - Playwright-Enhance${NC}"
echo "------------------------------------------------------"
python -m playwright_enhance.cli benchmark "$URL" --headless

# 3. 性能对比
echo ""
echo -e "${YELLOW}[3/4] 性能对比 (3 次运行)${NC}"
echo "------------------------------------------------------"
python -m playwright_enhance.cli compare "$URL" --headless --runs 3

# 4. 系统信息
echo ""
echo -e "${YELLOW}[4/4] 系统信息${NC}"
echo "------------------------------------------------------"
python -m playwright_enhance.cli info

echo ""
echo "======================================================"
echo -e "${GREEN}✅ 演示完成！${NC}"
echo "======================================================"
echo ""
echo "💡 后续步骤："
echo "  - 查看完整 CLI 指南: docs/cli-guide.md"
echo "  - 快速参考: CLI_QUICKSTART.md"
echo "  - 运行交互式测试: ./run_cli_comparison.sh"
echo ""
