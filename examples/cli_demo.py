"""
CLI 工具演示脚本

展示如何使用 playwright-enhance CLI 工具进行性能测试和配置管理。
"""

import subprocess
import sys


def run_command(cmd):
    """运行命令并打印输出"""
    print(f"\n{'='*60}")
    print(f"运行命令: {cmd}")
    print('='*60)
    result = subprocess.run(cmd, shell=True, capture_output=False)
    return result.returncode


def main():
    """演示 CLI 工具的各种功能"""
    
    print("Playwright-Enhance CLI 工具演示")
    print("="*60)
    
    commands = [
        # 1. 显示系统信息
        ("1. 显示系统信息", "python -m playwright_enhance.cli.main info"),
        
        # 2. 显示默认配置
        ("2. 显示默认配置", "python -m playwright_enhance.cli.main config show"),
        
        # 3. 创建配置文件
        ("3. 创建最小配置文件", "python -m playwright_enhance.cli.main config init demo-config.json --minimal"),
        
        # 4. 验证配置文件
        ("4. 验证配置文件", "python -m playwright_enhance.cli.main config validate demo-config.json"),
        
        # 5. 显示帮助信息
        ("5. 显示命令帮助", "python -m playwright_enhance.cli.main --help"),
    ]
    
    for description, cmd in commands:
        print(f"\n\n{description}")
        input("按 Enter 继续...")
        run_command(cmd)
    
    print("\n\n演示完成！")
    print("\n你可以尝试以下命令：")
    print("  - 性能测试: playwright-enhance-cli benchmark https://example.com")
    print("  - 性能对比: playwright-enhance-cli compare https://example.com --runs 3")
    print("  - 查看帮助: playwright-enhance-cli --help")
    
    # 清理演示文件
    import os
    if os.path.exists('demo-config.json'):
        os.remove('demo-config.json')
        print("\n已清理演示文件")


if __name__ == '__main__':
    main()
