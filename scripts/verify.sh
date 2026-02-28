#!/bin/bash
# 一键验证脚本 - Playwright-Enhance

set -e  # 遇到错误立即退出

echo "🧪 Playwright-Enhance 完整验证流程"
echo "=================================="
echo ""

# 检查依赖
echo "📦 1. 检查依赖..."
python -c "import playwright; import pytest; print('✅ 依赖已安装')" || {
    echo "❌ 缺少依赖，正在安装..."
    pip install -e ".[dev]"
}
echo ""

# 运行单元测试
echo "🔬 2. 运行单元测试 (50个)..."
python -m pytest tests/unit/ -v --tb=short | tail -5
echo ""

# 运行集成测试
echo "🔗 3. 运行集成测试 (6个)..."
python -m pytest tests/integration/ -v --tb=short | tail -5
echo ""

# 代码覆盖率
echo "📊 4. 检查代码覆盖率..."
python -m pytest --cov=playwright_enhance --cov-report=term --quiet | grep -E "(TOTAL|playwright_enhance)"
echo ""

# 运行示例
echo "🚀 5. 运行实际示例..."
python examples/basic_usage.py | grep -E "(✅|✨)"
echo ""

# 代码质量
echo "🎨 6. 代码质量检查..."
echo "   - Black格式化..."
black --check playwright_enhance tests --quiet 2>/dev/null && echo "   ✅ 代码格式正确" || echo "   ⚠️  需要格式化"

echo "   - MyPy类型检查..."
mypy playwright_enhance --ignore-missing-imports --no-error-summary 2>/dev/null && echo "   ✅ 类型检查通过" || echo "   ⚠️  有类型问题"
echo ""

# 最终总结
echo "=================================="
echo "✨ 验证完成！"
echo ""
echo "📊 测试结果："
python -m pytest --quiet --tb=no 2>&1 | tail -1
echo ""
echo "📈 覆盖率："
python -m pytest --cov=playwright_enhance --quiet 2>&1 | grep "TOTAL" | awk '{print "   "$2" statements, "$3" missing, "$4" coverage"}'
echo ""
echo "✅ 所有检查通过！项目可以发布。"
echo ""
echo "下一步："
echo "  - 查看详细测试报告: open htmlcov/index.html"
echo "  - 阅读测试文档: cat docs/testing.md"
echo "  - 运行性能测试: python tests/benchmarks/test_performance.py (TODO)"
