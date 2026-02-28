#!/bin/bash

# Hacker News 测试 - 通过 CLI 命令模拟
# ======================================================

set -e

echo "======================================================"
echo "🧪 Hacker News CLI 测试 (通过 playwright-enhance-cli)"
echo "======================================================"
echo ""

# 颜色输出
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 测试模式
MODE="--enhanced"
if [ "$1" = "--native" ]; then
    MODE="--native"
    echo -e "${YELLOW}运行模式: 原生 Playwright${NC}"
else
    echo -e "${YELLOW}运行模式: Playwright-Enhance${NC}"
fi
echo ""

# 临时文件
SESSION_FILE="/tmp/hn_session_$(date +%s).json"
mkdir -p /tmp/hn_test_screenshots

echo "======================================================"
echo "步骤 1: 打开 Hacker News 首页，提取元素"
echo "======================================================"
echo ""

python -m playwright_enhance.cli inspect \
    https://news.ycombinator.com \
    $MODE \
    --format json \
    -o "$SESSION_FILE"

# 解析 session ID 和元素
SESSION=$(python3 -c "import json; print(json.load(open('$SESSION_FILE'))['session'])")
LOAD_TIME=$(python3 -c "import json; print(json.load(open('$SESSION_FILE'))['load_time'])")

echo -e "${GREEN}✓ 首页加载完成: ${LOAD_TIME}s${NC}"
echo ""

# 提取一些关键元素
echo "提取的元素:"
python3 -c "
import json
data = json.load(open('$SESSION_FILE'))
print(f\"  - 总元素数: {len(data['elements'])}\")
# 打印前5个链接
links = [e for e in data['elements'] if e['type'] == 'link'][:5]
for link in links:
    print(f\"  - {link['id']}: {link['text']} ({link['href'][:50]})\")
"
echo ""

echo "======================================================"
echo "步骤 2: 截图保存首页"
echo "======================================================"
echo ""

python -m playwright_enhance.cli screenshot \
    https://news.ycombinator.com \
    /tmp/hn_test_screenshots/step1_homepage.png \
    $MODE

echo -e "${GREEN}✓ 首页截图已保存${NC}"
echo ""

echo "======================================================"
echo "步骤 3: 访问 newest 页面"
echo "======================================================"
echo ""

python -m playwright_enhance.cli inspect \
    https://news.ycombinator.com/newest \
    $MODE \
    --format json \
    -o "$SESSION_FILE"

LOAD_TIME=$(python3 -c "import json; print(json.load(open('$SESSION_FILE'))['load_time'])")
echo -e "${GREEN}✓ newest 页面加载完成: ${LOAD_TIME}s${NC}"
echo ""

echo "======================================================"
echo "步骤 4: 访问 best 页面"
echo "======================================================"
echo ""

python -m playwright_enhance.cli inspect \
    https://news.ycombinator.com/best \
    $MODE \
    --format json \
    -o "$SESSION_FILE"

LOAD_TIME=$(python3 -c "import json; print(json.load(open('$SESSION_FILE'))['load_time'])")
echo -e "${GREEN}✓ best 页面加载完成: ${LOAD_TIME}s${NC}"
echo ""

echo "======================================================"
echo "步骤 5: 生成 PDF"
echo "======================================================"
echo ""

python -m playwright_enhance.cli pdf \
    https://news.ycombinator.com \
    /tmp/hn_test_screenshots/hackernews.pdf \
    $MODE

echo -e "${GREEN}✓ PDF 已生成${NC}"
echo ""

echo "======================================================"
echo -e "${GREEN}✅ CLI 测试完成！${NC}"
echo "======================================================"
echo ""
echo "生成的文件:"
echo "  - 元素数据: $SESSION_FILE"
echo "  - 首页截图: /tmp/hn_test_screenshots/step1_homepage.png"
echo "  - PDF: /tmp/hn_test_screenshots/hackernews.pdf"
echo ""
echo "💡 注意:"
echo "  - 当前 CLI 支持: inspect, screenshot, pdf"
echo "  - 复杂交互 (点击、填表单) 需要 interact 命令 (开发中)"
echo "  - Session 管理和持久化浏览器状态正在开发"
echo ""
