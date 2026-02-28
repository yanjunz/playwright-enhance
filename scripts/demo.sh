#!/bin/bash
# 快速运行所有演示的脚本

echo "🎬 Playwright-Enhance 演示集"
echo "=" * 60

# 1. 基础示例
echo ""
echo "📚 1. 基础功能演示"
echo "运行: python examples/basic_usage.py"
echo "---"
python examples/basic_usage.py
echo ""

# 2. 性能对比
echo "=" * 60
echo "📊 2. Bilibili 性能对比"
echo "运行: python examples/bilibili_comparison.py"
echo "---"
python examples/bilibili_comparison.py
echo ""

# 3. 测试验证
echo "=" * 60
echo "🧪 3. 测试验证"
echo "运行: pytest -v"
echo "---"
python -m pytest -v --tb=no | tail -10
echo ""

echo "=" * 60
echo "✨ 所有演示完成！"
echo ""
echo "💡 下一步："
echo "  - 查看详细文档: cat docs/quick-start.md"
echo "  - 查看示例说明: cat examples/README.md"
echo "  - 运行完整测试: ./verify.sh"
echo "  - 真实浏览器测试: python examples/bilibili_comparison.py --real"
