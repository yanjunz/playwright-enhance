#!/bin/bash

# 验证 run_cli_comparison.sh 脚本
# ================================

set -e

echo "======================================"
echo "🔍 验证 run_cli_comparison.sh"
echo "======================================"
echo ""

# 颜色输出
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 测试计数
total=0
passed=0
failed=0

# 测试函数
test_case() {
    local name=$1
    local test_choice=$2
    local mode_choice=$3
    local order_choice=$4
    
    echo ""
    echo -e "${BLUE}测试: ${name}${NC}"
    echo "--------------------------------------"
    
    total=$((total+1))
    
    # 运行测试（只运行增强版，快速测试）
    if echo -e "${test_choice}\n${mode_choice}\n3" | timeout 60 bash run_cli_comparison.sh > /tmp/cli_test_$total.log 2>&1; then
        echo -e "${GREEN}✅ 通过${NC}"
        passed=$((passed+1))
    else
        echo -e "${RED}❌ 失败${NC}"
        echo "详细日志: /tmp/cli_test_$total.log"
        failed=$((failed+1))
    fi
}

# 运行测试
echo "开始测试..."
echo ""

test_case "Hacker News - 无头模式 - 仅增强" "2" "2" "3"
test_case "Wikipedia - 无头模式 - 仅增强" "1" "2" "3"

# 汇总
echo ""
echo "======================================"
echo "📊 测试汇总"
echo "======================================"
echo ""
echo "  总计: $total"
echo -e "  ${GREEN}通过: $passed${NC}"
echo -e "  ${RED}失败: $failed${NC}"
echo ""

if [ $failed -eq 0 ]; then
    echo -e "${GREEN}✅ 所有测试通过！${NC}"
    exit 0
else
    echo -e "${RED}❌ 有测试失败${NC}"
    exit 1
fi
