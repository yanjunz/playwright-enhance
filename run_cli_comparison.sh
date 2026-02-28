#!/bin/bash

# Playwright CLI vs Playwright-Enhance CLI 对比测试脚本
# ======================================================

set -e

echo "======================================================"
echo "🚀 Playwright CLI vs Playwright-Enhance CLI 对比"
echo "======================================================"
echo ""

# 颜色输出
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 检查依赖
echo "检查依赖..."
if ! command -v python &> /dev/null; then
    echo -e "${RED}❌ Python 未安装${NC}"
    exit 1
fi

# 测试网站列表
SITES=(
    "https://example.com:Example Domain"
    "https://www.wikipedia.org:Wikipedia"
    "https://news.ycombinator.com:Hacker News"
    "https://github.com:GitHub"
)

# 显示菜单
echo ""
echo "请选择测试类型："
echo ""
echo "  1. 单网站基准测试 (benchmark)"
echo "  2. 单网站性能对比 (compare)"
echo "  3. 多网站批量测试"
echo "  4. 自定义 URL 测试"
echo ""

read -p "请输入选项 (1-4): " test_choice

# 模式选择
echo ""
echo "选择运行模式："
echo "  1. 无头模式 (推荐) - 后台运行，更快"
echo "  2. 可见模式 - 可以看到浏览器操作"
echo ""

read -p "请输入模式 (1-2): " mode_choice

if [ "$mode_choice" = "1" ]; then
    MODE="--headless"
    MODE_TEXT="无头模式"
else
    MODE="--no-headless"
    MODE_TEXT="可见模式"
fi

echo ""
echo "======================================================"

# 函数：运行基准测试
run_benchmark() {
    local url=$1
    local name=$2
    
    echo ""
    echo -e "${BLUE}🧪 测试网站: ${name}${NC}"
    echo -e "${BLUE}📍 URL: ${url}${NC}"
    echo "------------------------------------------------------"
    
    echo ""
    echo -e "${YELLOW}[1/2] 原生 Playwright 测试...${NC}"
    python -m playwright_enhance.cli.main benchmark "$url" $MODE --native
    
    echo ""
    echo -e "${YELLOW}[2/2] Playwright-Enhance 测试...${NC}"
    python -m playwright_enhance.cli.main benchmark "$url" $MODE --enhanced
    
    echo "------------------------------------------------------"
}

# 函数：运行性能对比
run_compare() {
    local url=$1
    local name=$2
    local runs=$3
    
    echo ""
    echo -e "${BLUE}🧪 对比测试: ${name}${NC}"
    echo -e "${BLUE}📍 URL: ${url}${NC}"
    echo -e "${BLUE}🔄 运行次数: ${runs}${NC}"
    echo "------------------------------------------------------"
    
    python -m playwright_enhance.cli.main compare "$url" $MODE --runs $runs
    
    echo "------------------------------------------------------"
}

# 主测试逻辑
case $test_choice in
    1)
        # 单网站基准测试
        echo ""
        echo "选择测试网站："
        echo ""
        for i in "${!SITES[@]}"; do
            IFS=':' read -r url name <<< "${SITES[$i]}"
            echo "  $((i+1)). $name ($url)"
        done
        echo "  5. 自定义 URL"
        echo ""
        
        read -p "请输入选项 (1-5): " site_choice
        
        if [ "$site_choice" = "5" ]; then
            read -p "请输入 URL: " custom_url
            run_benchmark "$custom_url" "自定义网站"
        else
            idx=$((site_choice-1))
            if [ $idx -ge 0 ] && [ $idx -lt ${#SITES[@]} ]; then
                IFS=':' read -r url name <<< "${SITES[$idx]}"
                run_benchmark "$url" "$name"
            else
                echo -e "${RED}❌ 无效选项${NC}"
                exit 1
            fi
        fi
        ;;
        
    2)
        # 单网站性能对比
        echo ""
        echo "选择测试网站："
        echo ""
        for i in "${!SITES[@]}"; do
            IFS=':' read -r url name <<< "${SITES[$i]}"
            echo "  $((i+1)). $name ($url)"
        done
        echo "  5. 自定义 URL"
        echo ""
        
        read -p "请输入选项 (1-5): " site_choice
        
        echo ""
        read -p "运行次数 (默认 3): " runs
        runs=${runs:-3}
        
        if [ "$site_choice" = "5" ]; then
            read -p "请输入 URL: " custom_url
            run_compare "$custom_url" "自定义网站" $runs
        else
            idx=$((site_choice-1))
            if [ $idx -ge 0 ] && [ $idx -lt ${#SITES[@]} ]; then
                IFS=':' read -r url name <<< "${SITES[$idx]}"
                run_compare "$url" "$name" $runs
            else
                echo -e "${RED}❌ 无效选项${NC}"
                exit 1
            fi
        fi
        ;;
        
    3)
        # 多网站批量测试
        echo ""
        read -p "每个网站运行次数 (默认 3): " runs
        runs=${runs:-3}
        
        echo ""
        echo -e "${YELLOW}开始批量测试 (${#SITES[@]} 个网站)${NC}"
        echo "======================================================"
        
        mkdir -p cli_test_results
        timestamp=$(date +%Y%m%d_%H%M%S)
        result_dir="cli_test_results/${timestamp}"
        mkdir -p "$result_dir"
        
        for i in "${!SITES[@]}"; do
            IFS=':' read -r url name <<< "${SITES[$i]}"
            
            echo ""
            echo -e "${BLUE}[$((i+1))/${#SITES[@]}] 测试 ${name}${NC}"
            echo "======================================================"
            
            # 生成安全的文件名
            safe_name=$(echo "$name" | tr ' ' '_' | tr '[:upper:]' '[:lower:]')
            output_file="$result_dir/${safe_name}.json"
            
            python -m playwright_enhance.cli.main compare "$url" $MODE \
                --runs $runs \
                -o "$output_file"
            
            echo -e "${GREEN}✅ 结果已保存到: $output_file${NC}"
            
            sleep 2  # 避免请求过快
        done
        
        echo ""
        echo "======================================================"
        echo -e "${GREEN}✅ 批量测试完成！${NC}"
        echo "======================================================"
        echo ""
        echo "结果保存在: $result_dir"
        echo ""
        
        # 生成汇总报告
        echo "生成汇总报告..."
        python -c "
import json
import os
from pathlib import Path

result_dir = '$result_dir'
results = []

for file in Path(result_dir).glob('*.json'):
    with open(file) as f:
        data = json.load(f)
        results.append({
            'name': file.stem.replace('_', ' ').title(),
            'url': data['url'],
            'improvement': data['improvement_percent'],
            'speedup': data['speedup'],
            'native_avg': data['native']['average'],
            'enhanced_avg': data['enhanced']['average']
        })

# 按性能提升排序
results.sort(key=lambda x: x['improvement'], reverse=True)

print()
print('='*70)
print('📊 批量测试汇总报告')
print('='*70)
print()
print(f'{'网站':<20} {'原生(s)':<10} {'增强(s)':<10} {'提升':<10} {'加速比':<10}')
print('-'*70)

for r in results:
    print(f\"{r['name']:<20} {r['native_avg']:<10.3f} {r['enhanced_avg']:<10.3f} {r['improvement']:<9.1f}% {r['speedup']:<10.2f}x\")

print('-'*70)
avg_improvement = sum(r['improvement'] for r in results) / len(results)
avg_speedup = sum(r['speedup'] for r in results) / len(results)
print(f\"{'平均':<20} {'':<10} {'':<10} {avg_improvement:<9.1f}% {avg_speedup:<10.2f}x\")
print('='*70)
print()

# 保存汇总报告
summary_file = os.path.join(result_dir, 'summary.json')
with open(summary_file, 'w') as f:
    json.dump({
        'results': results,
        'summary': {
            'total_tests': len(results),
            'avg_improvement': round(avg_improvement, 1),
            'avg_speedup': round(avg_speedup, 2)
        }
    }, f, indent=2)

print(f'汇总报告已保存到: {summary_file}')
print()
"
        ;;
        
    4)
        # 自定义 URL 测试
        echo ""
        read -p "请输入要测试的 URL: " custom_url
        
        echo ""
        echo "选择测试类型："
        echo "  1. 基准测试 (benchmark)"
        echo "  2. 性能对比 (compare)"
        echo ""
        
        read -p "请输入选项 (1-2): " custom_choice
        
        if [ "$custom_choice" = "1" ]; then
            run_benchmark "$custom_url" "自定义网站"
        else
            read -p "运行次数 (默认 3): " runs
            runs=${runs:-3}
            run_compare "$custom_url" "自定义网站" $runs
        fi
        ;;
        
    *)
        echo -e "${RED}❌ 无效选项${NC}"
        exit 1
        ;;
esac

echo ""
echo "======================================================"
echo -e "${GREEN}✅ 测试完成！${NC}"
echo "======================================================"
echo ""
echo "💡 提示："
echo "  - Playwright-Enhance 通过智能等待和快速加载实现性能提升"
echo "  - 不同网站和网络环境结果会有差异"
echo "  - 建议运行 3-5 次获得稳定结果"
echo ""
echo "📖 更多信息："
echo "  - CLI 使用指南: docs/cli-guide.md"
echo "  - 快速开始: CLI_QUICKSTART.md"
echo "  - GitHub: https://github.com/playwright-enhance/playwright-enhance"
echo ""
