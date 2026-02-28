#!/bin/bash

# Playwright-Enhance 真实测试运行脚本
# =====================================

set -e

echo "======================================"
echo "🧪 Playwright-Enhance 真实测试套件"
echo "======================================"
echo ""

# 颜色输出
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 显示菜单
echo "请选择要运行的测试："
echo ""
echo "  1. Wikipedia 测试 (10步, 稳定, 推荐)"
echo "  2. Hacker News 测试 (10步, 快速, 推荐)"
echo "  3. GitHub 测试 (10步, 需要稳定网络)"
echo "  4. Bilibili 测试 (5步, 中文站点)"
echo ""
echo "  5. 运行所有测试 (依次执行)"
echo ""

read -p "请输入选项 (1-5): " choice

# 模式选择
echo ""
echo "选择运行模式："
echo "  1. 可见模式 (推荐) - 可以看到浏览器操作"
echo "  2. 无头模式 - 后台运行，不显示浏览器"
echo ""

read -p "请输入模式 (1-2): " mode_choice

if [ "$mode_choice" = "1" ]; then
    MODE="--visible"
else
    MODE="--headless"
fi

# 运行顺序选择
echo ""
echo "选择运行顺序："
echo "  1. 先运行原生版，再运行增强版 (推荐) - 看到性能对比"
echo "  2. 先运行增强版，再运行原生版"
echo "  3. 只运行增强版"
echo "  4. 只运行原生版"
echo ""

read -p "请输入顺序 (1-4): " order_choice

echo ""
echo "======================================"

# 根据顺序选择添加参数
ORDER_PARAM=""
case $order_choice in
    1)
        ORDER_PARAM="--order native-first"
        ;;
    2)
        ORDER_PARAM="--order enhanced-first"
        ;;
    3)
        ORDER_PARAM="--only enhanced"
        ;;
    4)
        ORDER_PARAM="--only native"
        ;;
    *)
        ORDER_PARAM="--order native-first"
        ;;
esac

# 运行测试
case $choice in
    1)
        echo -e "${BLUE}🧪 运行 Wikipedia 测试${NC}"
        echo "======================================"
        python examples/real_wikipedia_test.py $MODE $ORDER_PARAM
        ;;
    2)
        echo -e "${BLUE}🧪 运行 Hacker News 测试${NC}"
        echo "======================================"
        python examples/real_hackernews_test.py $MODE $ORDER_PARAM
        ;;
    3)
        echo -e "${BLUE}🧪 运行 GitHub 测试${NC}"
        echo "======================================"
        python examples/real_github_test.py $MODE $ORDER_PARAM
        ;;
    4)
        echo -e "${BLUE}🧪 运行 Bilibili 测试${NC}"
        echo "======================================"
        python examples/bilibili_comparison.py $MODE $ORDER_PARAM
        ;;
    5)
        echo -e "${YELLOW}运行所有测试 (大约需要 5-10 分钟)${NC}"
        echo "======================================"
        echo ""
        
        echo -e "${BLUE}[1/4] Wikipedia 测试${NC}"
        python examples/real_wikipedia_test.py $MODE $ORDER_PARAM
        sleep 3
        
        echo ""
        echo -e "${BLUE}[2/4] Hacker News 测试${NC}"
        python examples/real_hackernews_test.py $MODE $ORDER_PARAM
        sleep 3
        
        echo ""
        echo -e "${BLUE}[3/4] GitHub 测试${NC}"
        python examples/real_github_test.py $MODE $ORDER_PARAM
        sleep 3
        
        echo ""
        echo -e "${BLUE}[4/4] Bilibili 测试${NC}"
        python examples/bilibili_comparison.py $MODE $ORDER_PARAM
        
        echo ""
        echo -e "${GREEN}✅ 所有测试完成！${NC}"
        ;;
    *)
        echo "无效选项"
        exit 1
        ;;
esac

echo ""
echo "======================================"
echo -e "${GREEN}✅ 测试完成！${NC}"
echo "======================================"
echo ""
echo "💡 提示："
echo "  - 性能提升主要来自智能超时和快速加载策略"
echo "  - 不同网站和网络环境结果会有差异"
echo "  - 多步骤场景的优化效果更明显"
echo ""
