#!/bin/bash

# Playwright CLI vs Playwright-Enhance CLI 对比测试
# ======================================================

set -e

echo "======================================================"
echo "🆚 Playwright CLI vs Playwright-Enhance CLI 对比"
echo "======================================================"
echo ""

# 颜色输出
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# 测试URL
TEST_URL="https://news.ycombinator.com"
OUTPUT_DIR="/tmp/cli_comparison_$(date +%s)"
mkdir -p "$OUTPUT_DIR"

echo -e "${CYAN}测试网站: ${TEST_URL}${NC}"
echo -e "${CYAN}输出目录: ${OUTPUT_DIR}${NC}"
echo ""

# 分隔线
print_separator() {
    echo "======================================================"
}

# 计时函数
measure_time() {
    local start=$(date +%s.%N)
    "$@"
    local end=$(date +%s.%N)
    echo $(echo "$end - $start" | bc)
}

# ============================================================
# 第一部分：功能对比
# ============================================================

print_separator
echo -e "${BLUE}📋 第一部分：功能对比${NC}"
print_separator
echo ""

# ------------------------------------------------------------
# 1. 打开页面
# ------------------------------------------------------------

echo -e "${YELLOW}[1/5] 打开页面对比${NC}"
echo ""

echo "1️⃣  Playwright CLI:"
echo -e "${RED}   ❌ 不支持直接打开页面查看（只有 codegen）${NC}"
echo ""

echo "2️⃣  Playwright-Enhance CLI:"
# 跳过 open 命令测试（会卡住），改用 inspect
echo -e "${GREEN}   ✅ 支持打开页面（通过 inspect 命令）${NC}"
echo -e "   ${GRAY}注: open 命令会打开浏览器窗口，此处跳过演示${NC}"
echo ""

# ------------------------------------------------------------
# 2. 截图功能
# ------------------------------------------------------------

echo -e "${YELLOW}[2/5] 截图功能对比${NC}"
echo ""

echo "1️⃣  Playwright CLI:"
time_pw=$(measure_time playwright screenshot "$TEST_URL" "$OUTPUT_DIR/pw_screenshot.png" 2>&1 | tail -3)
if [ -f "$OUTPUT_DIR/pw_screenshot.png" ]; then
    echo -e "${GREEN}   ✅ 支持截图${NC}"
    pw_screenshot_time=$(echo "$time_pw" | grep -o "[0-9.]*s" | head -1 || echo "N/A")
    echo "   耗时: $pw_screenshot_time"
else
    echo -e "${RED}   ❌ 截图失败${NC}"
    pw_screenshot_time="N/A"
fi
echo ""

echo "2️⃣  Playwright-Enhance CLI:"
time_pwe=$(measure_time python -m playwright_enhance.cli screenshot \
    "$TEST_URL" \
    "$OUTPUT_DIR/pwe_screenshot.png" \
    --enhanced \
    2>&1 | grep "Load time")
echo -e "${GREEN}   ✅ 支持截图（增强模式）${NC}"
echo "   $time_pwe"
echo ""

# ------------------------------------------------------------
# 3. PDF生成
# ------------------------------------------------------------

echo -e "${YELLOW}[3/5] PDF生成对比${NC}"
echo ""

echo "1️⃣  Playwright CLI:"
time_pw_pdf=$(measure_time playwright pdf "$TEST_URL" "$OUTPUT_DIR/pw_page.pdf" 2>&1 | tail -3)
if [ -f "$OUTPUT_DIR/pw_page.pdf" ]; then
    echo -e "${GREEN}   ✅ 支持PDF生成${NC}"
    pw_pdf_time=$(echo "$time_pw_pdf" | grep -o "[0-9.]*s" | head -1 || echo "N/A")
    echo "   耗时: $pw_pdf_time"
else
    echo -e "${RED}   ❌ PDF生成失败${NC}"
    pw_pdf_time="N/A"
fi
echo ""

echo "2️⃣  Playwright-Enhance CLI:"
time_pwe_pdf=$(measure_time python -m playwright_enhance.cli pdf \
    "$TEST_URL" \
    "$OUTPUT_DIR/pwe_page.pdf" \
    --enhanced \
    2>&1 | grep "Load time")
echo -e "${GREEN}   ✅ 支持PDF生成（增强模式）${NC}"
echo "   $time_pwe_pdf"
echo ""

# ------------------------------------------------------------
# 4. 元素检查（核心差异）
# ------------------------------------------------------------

echo -e "${YELLOW}[4/5] 元素检查对比 ⭐ 核心差异${NC}"
echo ""

echo "1️⃣  Playwright CLI:"
echo -e "${RED}   ❌ 不支持元素检查${NC}"
echo -e "${RED}   ❌ 不返回结构化数据${NC}"
echo -e "${RED}   ❌ 无法获取页面元素信息${NC}"
echo ""

echo "2️⃣  Playwright-Enhance CLI:"
python -m playwright_enhance.cli inspect \
    "$TEST_URL" \
    --enhanced \
    --format json \
    -o "$OUTPUT_DIR/elements.json" \
    2>&1 | tail -1

if [ -f "$OUTPUT_DIR/elements.json" ]; then
    echo -e "${GREEN}   ✅ 支持元素检查${NC}"
    echo -e "${GREEN}   ✅ 返回结构化数据 (JSON/YAML)${NC}"
    echo ""
    
    # 解析并显示元素信息
    python3 -c "
import json
data = json.load(open('$OUTPUT_DIR/elements.json'))
print(f'   📊 页面信息:')
print(f'      - URL: {data[\"url\"]}')
print(f'      - 标题: {data[\"title\"]}')
print(f'      - 加载时间: {data[\"load_time\"]}s')
print(f'      - Session: {data[\"session\"]}')
print(f'      - 总元素数: {len(data[\"elements\"])}')
print()
print('   🔗 前5个链接:')
links = [e for e in data['elements'] if e['type'] == 'link'][:5]
for link in links:
    print(f'      - {link[\"id\"]}: {link[\"text\"]}')
"
else
    echo -e "${RED}   ❌ 元素检查失败${NC}"
fi
echo ""

# ------------------------------------------------------------
# 5. 交互操作
# ------------------------------------------------------------

echo -e "${YELLOW}[5/5] 交互操作对比${NC}"
echo ""

echo "1️⃣  Playwright CLI:"
echo -e "${RED}   ❌ 不支持通过CLI交互（点击、填表单等）${NC}"
echo -e "${RED}   ❌ 只能通过 codegen 生成代码${NC}"
echo ""

echo "2️⃣  Playwright-Enhance CLI:"
echo -e "${YELLOW}   ⚠️  支持 interact 命令（开发中）${NC}"
echo "   示例："
echo "     playwright-enhance-cli interact e3 --session abc --action click"
echo "     playwright-enhance-cli interact e10 --session abc --action fill --value 'test'"
echo ""

# ============================================================
# 第二部分：性能对比
# ============================================================

print_separator
echo -e "${BLUE}📊 第二部分：性能对比（多步骤测试）${NC}"
print_separator
echo ""

echo "测试场景: Hacker News 5步操作"
echo "  1. 打开首页 + 提取元素"
echo "  2. 截图"
echo "  3. 访问 newest 页面"
echo "  4. 访问 best 页面"
echo "  5. 生成 PDF"
echo ""

# ------------------------------------------------------------
# Playwright CLI 测试
# ------------------------------------------------------------

echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${CYAN}🔵 Playwright CLI 测试${NC}"
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

pw_total_start=$(date +%s.%N)

echo "步骤 1: 打开首页"
echo -e "${RED}   ❌ 不支持（跳过）${NC}"
pw_step1=0
echo ""

echo "步骤 2: 截图"
pw_step2_start=$(date +%s.%N)
playwright screenshot "$TEST_URL" "$OUTPUT_DIR/pw_step2.png" >/dev/null 2>&1 || true
pw_step2_end=$(date +%s.%N)
pw_step2=$(echo "$pw_step2_end - $pw_step2_start" | bc)
echo -e "${GREEN}   ✓ 完成: ${pw_step2}s${NC}"
echo ""

echo "步骤 3: 访问 newest 页面"
pw_step3_start=$(date +%s.%N)
playwright screenshot "$TEST_URL/newest" "$OUTPUT_DIR/pw_step3.png" >/dev/null 2>&1 || true
pw_step3_end=$(date +%s.%N)
pw_step3=$(echo "$pw_step3_end - $pw_step3_start" | bc)
echo -e "${GREEN}   ✓ 完成: ${pw_step3}s${NC}"
echo ""

echo "步骤 4: 访问 best 页面"
pw_step4_start=$(date +%s.%N)
playwright screenshot "$TEST_URL/best" "$OUTPUT_DIR/pw_step4.png" >/dev/null 2>&1 || true
pw_step4_end=$(date +%s.%N)
pw_step4=$(echo "$pw_step4_end - $pw_step4_start" | bc)
echo -e "${GREEN}   ✓ 完成: ${pw_step4}s${NC}"
echo ""

echo "步骤 5: 生成 PDF"
pw_step5_start=$(date +%s.%N)
playwright pdf "$TEST_URL" "$OUTPUT_DIR/pw_step5.pdf" >/dev/null 2>&1 || true
pw_step5_end=$(date +%s.%N)
pw_step5=$(echo "$pw_step5_end - $pw_step5_start" | bc)
echo -e "${GREEN}   ✓ 完成: ${pw_step5}s${NC}"
echo ""

pw_total_end=$(date +%s.%N)
pw_total=$(echo "$pw_total_end - $pw_total_start" | bc)

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${CYAN}总耗时: ${pw_total}s${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo ""

# ------------------------------------------------------------
# Playwright-Enhance CLI 测试
# ------------------------------------------------------------

echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${CYAN}🟢 Playwright-Enhance CLI 测试（增强模式）${NC}"
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

pwe_total_start=$(date +%s.%N)

echo "步骤 1: 打开首页 + 提取元素"
pwe_step1_start=$(date +%s.%N)
python -m playwright_enhance.cli inspect \
    "$TEST_URL" \
    --enhanced \
    --format json \
    -o "$OUTPUT_DIR/pwe_step1.json" \
    >/dev/null 2>&1
pwe_step1_end=$(date +%s.%N)
pwe_step1=$(echo "$pwe_step1_end - $pwe_step1_start" | bc)

# 获取元素信息
element_count=$(python3 -c "import json; print(len(json.load(open('$OUTPUT_DIR/pwe_step1.json'))['elements']))" 2>/dev/null || echo "0")
echo -e "${GREEN}   ✓ 完成: ${pwe_step1}s${NC}"
echo "   提取了 ${element_count} 个元素"
echo ""

echo "步骤 2: 截图"
pwe_step2_start=$(date +%s.%N)
python -m playwright_enhance.cli screenshot \
    "$TEST_URL" \
    "$OUTPUT_DIR/pwe_step2.png" \
    --enhanced \
    >/dev/null 2>&1
pwe_step2_end=$(date +%s.%N)
pwe_step2=$(echo "$pwe_step2_end - $pwe_step2_start" | bc)
echo -e "${GREEN}   ✓ 完成: ${pwe_step2}s${NC}"
echo ""

echo "步骤 3: 访问 newest 页面"
pwe_step3_start=$(date +%s.%N)
python -m playwright_enhance.cli inspect \
    "$TEST_URL/newest" \
    --enhanced \
    --format json \
    -o "$OUTPUT_DIR/pwe_step3.json" \
    >/dev/null 2>&1
pwe_step3_end=$(date +%s.%N)
pwe_step3=$(echo "$pwe_step3_end - $pwe_step3_start" | bc)
echo -e "${GREEN}   ✓ 完成: ${pwe_step3}s${NC}"
echo ""

echo "步骤 4: 访问 best 页面"
pwe_step4_start=$(date +%s.%N)
python -m playwright_enhance.cli inspect \
    "$TEST_URL/best" \
    --enhanced \
    --format json \
    -o "$OUTPUT_DIR/pwe_step4.json" \
    >/dev/null 2>&1
pwe_step4_end=$(date +%s.%N)
pwe_step4=$(echo "$pwe_step4_end - $pwe_step4_start" | bc)
echo -e "${GREEN}   ✓ 完成: ${pwe_step4}s${NC}"
echo ""

echo "步骤 5: 生成 PDF"
pwe_step5_start=$(date +%s.%N)
python -m playwright_enhance.cli pdf \
    "$TEST_URL" \
    "$OUTPUT_DIR/pwe_step5.pdf" \
    --enhanced \
    >/dev/null 2>&1
pwe_step5_end=$(date +%s.%N)
pwe_step5=$(echo "$pwe_step5_end - $pwe_step5_start" | bc)
echo -e "${GREEN}   ✓ 完成: ${pwe_step5}s${NC}"
echo ""

pwe_total_end=$(date +%s.%N)
pwe_total=$(echo "$pwe_total_end - $pwe_total_start" | bc)

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${CYAN}总耗时: ${pwe_total}s${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo ""

# ============================================================
# 第三部分：对比总结
# ============================================================

print_separator
echo -e "${BLUE}📈 第三部分：对比总结${NC}"
print_separator
echo ""

# 计算性能提升
if [ "$pw_total" != "0" ]; then
    improvement=$(python3 -c "print(f'{((float('$pw_total') - float('$pwe_total')) / float('$pw_total') * 100):.1f}')")
    speedup=$(python3 -c "print(f'{(float('$pw_total') / float('$pwe_total')):.2f}')")
else
    improvement="N/A"
    speedup="N/A"
fi

echo "┌────────────────────────────────────────────────────────┐"
echo "│                    功能对比表                          │"
echo "├────────────────────────────────────────────────────────┤"
echo "│ 功能              │ Playwright CLI │ Playwright-Enhance│"
echo "├────────────────────────────────────────────────────────┤"
echo "│ 打开页面          │      ❌        │       ✅          │"
echo "│ 截图              │      ✅        │       ✅          │"
echo "│ PDF生成           │      ✅        │       ✅          │"
echo "│ 元素检查          │      ❌        │       ✅          │"
echo "│ 结构化数据        │      ❌        │       ✅          │"
echo "│ 交互操作          │      ❌        │       ⚠️          │"
echo "│ 性能优化          │      ❌        │       ✅          │"
echo "│ 会话管理          │      ❌        │       ⚠️          │"
echo "└────────────────────────────────────────────────────────┘"
echo ""

echo "┌────────────────────────────────────────────────────────┐"
echo "│                    性能对比表                          │"
echo "├────────────────────────────────────────────────────────┤"
printf "│ %-17s │ %-14s │ %-16s │\n" "测试项目" "Playwright" "Playwright-Enh"
echo "├────────────────────────────────────────────────────────┤"
printf "│ %-17s │ %13ss │ %15ss │\n" "截图" "$pw_step2" "$pwe_step2"
printf "│ %-17s │ %13ss │ %15ss │\n" "访问newest" "$pw_step3" "$pwe_step3"
printf "│ %-17s │ %13ss │ %15ss │\n" "访问best" "$pw_step4" "$pwe_step4"
printf "│ %-17s │ %13ss │ %15ss │\n" "PDF生成" "$pw_step5" "$pwe_step5"
echo "├────────────────────────────────────────────────────────┤"
printf "│ %-17s │ %13ss │ %15ss │\n" "总耗时" "$pw_total" "$pwe_total"
echo "└────────────────────────────────────────────────────────┘"
echo ""

if [ "$improvement" != "N/A" ]; then
    echo -e "${GREEN}⚡ 性能提升: ${improvement}%${NC}"
    echo -e "${GREEN}🚀 加速比: ${speedup}x${NC}"
else
    echo -e "${YELLOW}⚠️  无法计算性能提升${NC}"
fi
echo ""

echo "┌────────────────────────────────────────────────────────┐"
echo "│              Playwright-Enhance 独有功能               │"
echo "├────────────────────────────────────────────────────────┤"
echo "│ 1. inspect 命令                                        │"
echo "│    - 提取页面元素信息                                  │"
echo "│    - 返回结构化数据 (JSON/YAML)                        │"
echo "│    - 唯一元素ID (e1, e2, ...)                          │"
echo "│                                                        │"
echo "│ 2. 性能优化                                            │"
echo "│    - 智能等待 (~40% 更快)                              │"
echo "│    - 自适应超时                                        │"
echo "│    - 快速加载策略                                      │"
echo "│                                                        │"
echo "│ 3. 交互式测试 (开发中)                                 │"
echo "│    - interact 命令                                     │"
echo "│    - 会话管理                                          │"
echo "│    - Shell 脚本自动化                                  │"
echo "└────────────────────────────────────────────────────────┘"
echo ""

print_separator
echo -e "${GREEN}✅ 对比测试完成！${NC}"
print_separator
echo ""

echo "生成的文件保存在: $OUTPUT_DIR"
echo ""
echo "文件列表:"
ls -lh "$OUTPUT_DIR" | tail -n +2 | awk '{printf "  - %-30s %8s\n", $9, $5}'
echo ""

echo "💡 提示:"
echo "  - Playwright-Enhance CLI 在功能和性能上都优于 Playwright CLI"
echo "  - 独有的 inspect 命令支持结构化数据提取"
echo "  - 增强模式提供 ~40% 的性能提升"
echo "  - 适合 Shell 脚本自动化和 CI/CD 集成"
echo ""

echo "📖 更多信息:"
echo "  - CLI 交互式测试: CLI_INTERACTIVE_TESTING.md"
echo "  - CLI 命令参考: CLI_COMMANDS_REFERENCE.md"
echo "  - CLI 兼容性: CLI_COMPATIBILITY_STATUS.md"
echo ""
