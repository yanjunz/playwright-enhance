#!/bin/bash

# 快速验证脚本 - 测试每个命令是否能正常完成

set -e

echo "🧪 验证 CLI 命令是否正常..."
echo ""

TEMP_DIR="/tmp/cli_test_$$"
mkdir -p "$TEMP_DIR"

echo "1️⃣  测试 playwright screenshot..."
playwright screenshot https://news.ycombinator.com "$TEMP_DIR/pw.png" >/dev/null 2>&1 && echo "✅ Playwright screenshot 正常" || echo "❌ Playwright screenshot 失败"

echo "2️⃣  测试 playwright pdf..."
playwright pdf https://news.ycombinator.com "$TEMP_DIR/pw.pdf" >/dev/null 2>&1 && echo "✅ Playwright pdf 正常" || echo "❌ Playwright pdf 失败"

echo "3️⃣  测试 playwright-enhance-cli screenshot..."
python -m playwright_enhance.cli screenshot https://news.ycombinator.com "$TEMP_DIR/pwe.png" --enhanced >/dev/null 2>&1 && echo "✅ PWE screenshot 正常" || echo "❌ PWE screenshot 失败"

echo "4️⃣  测试 playwright-enhance-cli pdf..."
python -m playwright_enhance.cli pdf https://news.ycombinator.com "$TEMP_DIR/pwe.pdf" --enhanced >/dev/null 2>&1 && echo "✅ PWE pdf 正常" || echo "❌ PWE pdf 失败"

echo "5️⃣  测试 playwright-enhance-cli inspect..."
python -m playwright_enhance.cli inspect https://news.ycombinator.com --enhanced --format json -o "$TEMP_DIR/pwe.json" >/dev/null 2>&1 && echo "✅ PWE inspect 正常" || echo "❌ PWE inspect 失败"

echo ""
echo "📊 生成的文件:"
ls -lh "$TEMP_DIR"

echo ""
echo "✅ 验证完成！"
echo "如果所有命令都正常，可以运行完整测试: bash cli_comparison_demo.sh"
