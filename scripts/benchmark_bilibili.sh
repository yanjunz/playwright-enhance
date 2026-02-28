#!/bin/bash
# Bilibili 真实性能对比测试

echo "🎬 Bilibili 性能对比测试"
echo "=========================================="
echo ""
echo "选择测试模式："
echo ""
echo "  1. 真实测试（无头模式，后台运行）"
echo "  2. 真实测试（可见模式，可以看到浏览器操作）"
echo "  3. 快速演示（模拟数据，不需要网络）"
echo ""
echo -n "请选择 [1-3]: "

read choice

case $choice in
    1)
        echo ""
        echo "启动真实测试（无头模式）..."
        python examples/bilibili_comparison.py --headless
        ;;
    2)
        echo ""
        echo "启动真实测试（可见模式）..."
        python examples/bilibili_comparison.py --visible
        ;;
    3)
        echo ""
        echo "启动快速演示..."
        python examples/bilibili_comparison.py --demo
        ;;
    *)
        echo ""
        echo "❌ 无效选择"
        exit 1
        ;;
esac
