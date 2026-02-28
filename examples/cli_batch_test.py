"""
CLI 批量测试工具

使用 playwright-enhance-cli 对多个网站进行批量性能测试和对比。
"""

import asyncio
import json
import subprocess
import sys
import time
from pathlib import Path
from typing import Dict, List
from datetime import datetime


# 测试网站列表
TEST_SITES = [
    {
        'name': 'Example Domain',
        'url': 'https://example.com',
        'description': '简单静态页面',
    },
    {
        'name': 'Wikipedia',
        'url': 'https://www.wikipedia.org',
        'description': '复杂内容网站',
    },
    {
        'name': 'Hacker News',
        'url': 'https://news.ycombinator.com',
        'description': '快速加载网站',
    },
    {
        'name': 'GitHub',
        'url': 'https://github.com',
        'description': '现代 Web 应用',
    },
]


class CLIBatchTester:
    """CLI 批量测试工具"""
    
    def __init__(self, runs: int = 3, headless: bool = True):
        self.runs = runs
        self.headless = headless
        self.results = []
        
        # 创建结果目录
        self.result_dir = Path('cli_test_results') / datetime.now().strftime('%Y%m%d_%H%M%S')
        self.result_dir.mkdir(parents=True, exist_ok=True)
    
    def run_cli_command(self, command: List[str]) -> Dict:
        """运行 CLI 命令并返回结果"""
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=True
            )
            return {
                'success': True,
                'stdout': result.stdout,
                'stderr': result.stderr,
            }
        except subprocess.CalledProcessError as e:
            return {
                'success': False,
                'stdout': e.stdout,
                'stderr': e.stderr,
                'error': str(e),
            }
    
    def benchmark_site(self, site: Dict) -> Dict:
        """对单个网站进行基准测试"""
        print(f"\n{'='*60}")
        print(f"🧪 测试: {site['name']}")
        print(f"📍 URL: {site['url']}")
        print(f"📝 说明: {site['description']}")
        print('='*60)
        
        mode = '--headless' if self.headless else '--no-headless'
        output_file = self.result_dir / f"{site['name'].lower().replace(' ', '_')}.json"
        
        command = [
            sys.executable, '-m', 'playwright_enhance.cli.main',
            'compare',
            site['url'],
            mode,
            '--runs', str(self.runs),
            '-o', str(output_file),
        ]
        
        print(f"\n运行命令: {' '.join(command)}")
        print(f"运行次数: {self.runs}")
        print()
        
        start_time = time.time()
        result = self.run_cli_command(command)
        duration = time.time() - start_time
        
        if result['success']:
            # 读取结果
            with open(output_file) as f:
                data = json.load(f)
            
            print(f"✅ 测试完成 (耗时: {duration:.1f}s)")
            print(f"   原生平均: {data['native']['average']:.3f}s")
            print(f"   增强平均: {data['enhanced']['average']:.3f}s")
            print(f"   性能提升: {data['improvement_percent']:.1f}% ({data['speedup']:.2f}x)")
            
            return {
                'site': site,
                'data': data,
                'duration': duration,
                'success': True,
            }
        else:
            print(f"❌ 测试失败: {result.get('error', 'Unknown error')}")
            return {
                'site': site,
                'success': False,
                'error': result.get('error'),
            }
    
    def run_all_tests(self):
        """运行所有测试"""
        print("="*60)
        print("🚀 Playwright CLI 批量性能测试")
        print("="*60)
        print(f"\n配置:")
        print(f"  - 测试网站数: {len(TEST_SITES)}")
        print(f"  - 每站运行: {self.runs} 次")
        print(f"  - 运行模式: {'无头' if self.headless else '可见'}")
        print(f"  - 结果目录: {self.result_dir}")
        print()
        
        for i, site in enumerate(TEST_SITES, 1):
            print(f"\n[{i}/{len(TEST_SITES)}] 测试 {site['name']}...")
            result = self.benchmark_site(site)
            self.results.append(result)
            
            # 避免请求过快
            if i < len(TEST_SITES):
                time.sleep(2)
        
        self.generate_summary()
    
    def generate_summary(self):
        """生成汇总报告"""
        print("\n" + "="*60)
        print("📊 批量测试汇总报告")
        print("="*60)
        
        successful_results = [r for r in self.results if r['success']]
        
        if not successful_results:
            print("\n❌ 没有成功的测试结果")
            return
        
        # 打印表格
        print(f"\n{'网站':<20} {'原生(s)':<10} {'增强(s)':<10} {'提升':<10} {'加速比':<10}")
        print("-"*60)
        
        total_improvement = 0
        total_speedup = 0
        
        for result in sorted(successful_results, 
                           key=lambda x: x['data']['improvement_percent'], 
                           reverse=True):
            site = result['site']
            data = result['data']
            
            print(f"{site['name']:<20} "
                  f"{data['native']['average']:<10.3f} "
                  f"{data['enhanced']['average']:<10.3f} "
                  f"{data['improvement_percent']:<9.1f}% "
                  f"{data['speedup']:<10.2f}x")
            
            total_improvement += data['improvement_percent']
            total_speedup += data['speedup']
        
        print("-"*60)
        avg_improvement = total_improvement / len(successful_results)
        avg_speedup = total_speedup / len(successful_results)
        
        print(f"{'平均':<20} {'':<10} {'':<10} {avg_improvement:<9.1f}% {avg_speedup:<10.2f}x")
        print("="*60)
        
        # 保存汇总报告
        summary = {
            'test_config': {
                'runs': self.runs,
                'headless': self.headless,
                'total_sites': len(TEST_SITES),
                'successful_tests': len(successful_results),
                'failed_tests': len(self.results) - len(successful_results),
            },
            'results': [
                {
                    'site': r['site']['name'],
                    'url': r['site']['url'],
                    'native_avg': r['data']['native']['average'],
                    'enhanced_avg': r['data']['enhanced']['average'],
                    'improvement_percent': r['data']['improvement_percent'],
                    'speedup': r['data']['speedup'],
                }
                for r in successful_results
            ],
            'summary': {
                'avg_improvement_percent': round(avg_improvement, 1),
                'avg_speedup': round(avg_speedup, 2),
            }
        }
        
        summary_file = self.result_dir / 'summary.json'
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)
        
        print(f"\n📄 汇总报告已保存到: {summary_file}")
        
        # 生成 Markdown 报告
        self.generate_markdown_report(summary)
    
    def generate_markdown_report(self, summary: Dict):
        """生成 Markdown 格式的报告"""
        markdown_file = self.result_dir / 'REPORT.md'
        
        with open(markdown_file, 'w') as f:
            f.write("# CLI 批量性能测试报告\n\n")
            f.write(f"**测试时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write("## 测试配置\n\n")
            config = summary['test_config']
            f.write(f"- 测试网站数: {config['total_sites']}\n")
            f.write(f"- 每站运行次数: {config['runs']}\n")
            f.write(f"- 运行模式: {'无头模式' if config['headless'] else '可见模式'}\n")
            f.write(f"- 成功测试: {config['successful_tests']}\n")
            f.write(f"- 失败测试: {config['failed_tests']}\n\n")
            
            f.write("## 测试结果\n\n")
            f.write("| 网站 | 原生 Playwright (s) | 增强版 (s) | 性能提升 | 加速比 |\n")
            f.write("|------|---------------------|-----------|----------|--------|\n")
            
            for result in summary['results']:
                f.write(f"| {result['site']} | "
                       f"{result['native_avg']:.3f} | "
                       f"{result['enhanced_avg']:.3f} | "
                       f"{result['improvement_percent']:.1f}% | "
                       f"{result['speedup']:.2f}x |\n")
            
            f.write(f"\n**平均性能提升**: {summary['summary']['avg_improvement_percent']}% "
                   f"({summary['summary']['avg_speedup']}x)\n\n")
            
            f.write("## 关键发现\n\n")
            
            # 找出最快和最慢的
            results = summary['results']
            best = max(results, key=lambda x: x['improvement_percent'])
            worst = min(results, key=lambda x: x['improvement_percent'])
            
            f.write(f"- 🏆 **最佳优化**: {best['site']} ({best['improvement_percent']:.1f}% 提升)\n")
            f.write(f"- 📊 **最小优化**: {worst['site']} ({worst['improvement_percent']:.1f}% 提升)\n")
            f.write(f"- ⚡ **平均加速比**: {summary['summary']['avg_speedup']}x\n\n")
            
            f.write("## 优化技术\n\n")
            f.write("Playwright-Enhance 通过以下技术实现性能提升：\n\n")
            f.write("1. **智能等待**: 动态超时调整 (3-10s vs 固定 30s)\n")
            f.write("2. **快速加载**: `domcontentloaded` vs `load` 事件\n")
            f.write("3. **资源预加载**: 后台预取资源\n")
            f.write("4. **操作优化**: 针对不同操作类型优化超时\n\n")
            
            f.write("---\n\n")
            f.write("*Generated by playwright-enhance CLI batch test tool*\n")
        
        print(f"📝 Markdown 报告已保存到: {markdown_file}")


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='CLI 批量性能测试工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 默认配置（3次运行，无头模式）
  python examples/cli_batch_test.py
  
  # 5次运行，可见模式
  python examples/cli_batch_test.py --runs 5 --visible
  
  # 快速测试（1次运行）
  python examples/cli_batch_test.py --runs 1
"""
    )
    
    parser.add_argument(
        '--runs', '-n',
        type=int,
        default=3,
        help='每个网站运行次数 (默认: 3)'
    )
    
    parser.add_argument(
        '--visible',
        action='store_true',
        help='使用可见模式（非无头）'
    )
    
    args = parser.parse_args()
    
    # 创建测试器并运行
    tester = CLIBatchTester(
        runs=args.runs,
        headless=not args.visible
    )
    
    try:
        tester.run_all_tests()
        
        print("\n" + "="*60)
        print("✅ 批量测试完成！")
        print("="*60)
        print(f"\n结果目录: {tester.result_dir}")
        print("\n生成的文件:")
        print(f"  - summary.json (JSON 格式汇总)")
        print(f"  - REPORT.md (Markdown 格式报告)")
        print(f"  - *.json (各网站详细结果)")
        print()
        
    except KeyboardInterrupt:
        print("\n\n⚠️  测试被用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ 测试出错: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
