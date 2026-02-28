# CLI 对比测试指南

本指南介绍如何使用 CLI 工具对比 Playwright 和 Playwright-Enhance 的性能。

## 快速开始

### 方式 1: Shell 脚本（推荐）

```bash
# 运行交互式 CLI 对比测试
./run_cli_comparison.sh
```

**功能：**
- ✅ 交互式菜单选择
- ✅ 4 种测试类型（基准测试/性能对比/批量测试/自定义）
- ✅ 预设 4 个常用网站
- ✅ 可见/无头模式切换
- ✅ 自动生成汇总报告

### 方式 2: Python 批量测试工具

```bash
# 默认配置（3次运行，无头模式）
python examples/cli_batch_test.py

# 5次运行，可见模式
python examples/cli_batch_test.py --runs 5 --visible

# 快速测试（1次运行）
python examples/cli_batch_test.py --runs 1
```

**功能：**
- ✅ 批量测试多个网站
- ✅ 自动生成 JSON 和 Markdown 报告
- ✅ 详细的性能统计
- ✅ 结果可视化

## 测试类型

### 1. 单网站基准测试 (Benchmark)

对比单个网站在原生和增强版 Playwright 下的加载性能。

```bash
# 使用脚本
./run_cli_comparison.sh
# 选择: 1. 单网站基准测试

# 或直接使用 CLI
playwright-enhance-cli benchmark https://example.com
```

**输出示例：**
```
🧪 测试网站: Example Domain
------------------------------------------------------

[1/2] 原生 Playwright 测试...
Load Time:  2.456s (2456ms)

[2/2] Playwright-Enhance 测试...
Load Time:  1.234s (1234ms)
```

### 2. 单网站性能对比 (Compare)

运行多次测试，提供统计数据和性能提升百分比。

```bash
# 使用脚本
./run_cli_comparison.sh
# 选择: 2. 单网站性能对比

# 或直接使用 CLI
playwright-enhance-cli compare https://example.com --runs 5
```

**输出示例：**
```
Performance Comparison
============================================================
URL:        https://example.com
Runs:       5

Native Playwright:
  Average:  2.456s
  Min:      2.234s
  Max:      2.678s

Enhanced Playwright:
  Average:  1.234s
  Min:      1.123s
  Max:      1.345s

Improvement: 49.8% faster (1.99x speedup)
```

### 3. 多网站批量测试

对多个预设网站进行批量性能测试，自动生成汇总报告。

```bash
# 使用脚本（交互式）
./run_cli_comparison.sh
# 选择: 3. 多网站批量测试

# 或使用 Python 工具
python examples/cli_batch_test.py --runs 3
```

**输出示例：**
```
📊 批量测试汇总报告
======================================================================
网站                  原生(s)    增强(s)    提升       加速比    
----------------------------------------------------------------------
Example Domain        2.456      1.234      49.8%      1.99x
Wikipedia             5.234      2.678      48.8%      1.95x
Hacker News           3.456      1.789      48.2%      1.93x
GitHub                4.567      2.456      46.2%      1.86x
----------------------------------------------------------------------
平均                                        48.3%      1.93x
======================================================================
```

**生成的文件：**
- `cli_test_results/YYYYMMDD_HHMMSS/summary.json` - JSON 格式汇总
- `cli_test_results/YYYYMMDD_HHMMSS/REPORT.md` - Markdown 格式报告
- `cli_test_results/YYYYMMDD_HHMMSS/*.json` - 各网站详细结果

### 4. 自定义 URL 测试

测试任意自定义 URL。

```bash
# 使用脚本
./run_cli_comparison.sh
# 选择: 4. 自定义 URL 测试
# 输入: https://your-website.com

# 或直接使用 CLI
playwright-enhance-cli compare https://your-website.com --runs 3
```

## 预设测试网站

脚本包含 4 个预设网站：

| 网站 | URL | 特点 |
|------|-----|------|
| Example Domain | https://example.com | 简单静态页面 |
| Wikipedia | https://www.wikipedia.org | 复杂内容网站 |
| Hacker News | https://news.ycombinator.com | 快速加载网站 |
| GitHub | https://github.com | 现代 Web 应用 |

## 运行模式

### 无头模式（推荐）

后台运行，不显示浏览器窗口，速度更快。

```bash
./run_cli_comparison.sh
# 选择模式: 1. 无头模式
```

### 可见模式

显示浏览器窗口，可以看到实际操作过程，便于调试。

```bash
./run_cli_comparison.sh
# 选择模式: 2. 可见模式
```

## 批量测试报告

批量测试会自动生成两种格式的报告：

### JSON 格式 (summary.json)

```json
{
  "test_config": {
    "runs": 3,
    "headless": true,
    "total_sites": 4,
    "successful_tests": 4
  },
  "results": [
    {
      "site": "Example Domain",
      "url": "https://example.com",
      "native_avg": 2.456,
      "enhanced_avg": 1.234,
      "improvement_percent": 49.8,
      "speedup": 1.99
    }
  ],
  "summary": {
    "avg_improvement_percent": 48.3,
    "avg_speedup": 1.93
  }
}
```

### Markdown 格式 (REPORT.md)

完整的测试报告，包括：
- 测试配置
- 详细结果表格
- 关键发现
- 优化技术说明

## 实用场景

### 场景 1: 快速验证优化效果

```bash
# 测试单个页面
playwright-enhance-cli benchmark https://your-site.com
```

### 场景 2: 详细性能分析

```bash
# 运行 5 次获得稳定结果
playwright-enhance-cli compare https://your-site.com --runs 5
```

### 场景 3: 多站点性能评估

```bash
# 批量测试多个网站
python examples/cli_batch_test.py --runs 3
```

### 场景 4: CI/CD 性能监控

```bash
#!/bin/bash
# ci-performance-check.sh

# 运行批量测试
python examples/cli_batch_test.py --runs 5 > test_output.txt

# 检查性能是否达标（例如：平均提升 > 40%）
python -c "
import json
with open('cli_test_results/latest/summary.json') as f:
    data = json.load(f)
    improvement = data['summary']['avg_improvement_percent']
    if improvement < 40:
        print(f'❌ 性能未达标: {improvement}%')
        exit(1)
    else:
        print(f'✅ 性能达标: {improvement}%')
"
```

### 场景 5: 可视化调试

```bash
# 查看浏览器实际操作
./run_cli_comparison.sh
# 选择: 可见模式
```

## 命令行参数参考

### run_cli_comparison.sh

交互式脚本，无需参数。按提示选择即可。

### cli_batch_test.py

```bash
usage: cli_batch_test.py [-h] [--runs RUNS] [--visible]

可选参数:
  -h, --help            显示帮助信息
  --runs RUNS, -n RUNS  每个网站运行次数 (默认: 3)
  --visible             使用可见模式（非无头）
```

### playwright-enhance-cli

```bash
# benchmark 命令
playwright-enhance-cli benchmark <url> [OPTIONS]
  --headless/--no-headless  是否无头模式 (默认: --headless)
  --enhanced/--native       使用增强版或原生版 (默认: --enhanced)
  -c, --config PATH         配置文件路径
  -o, --output PATH         输出文件路径
  --format [json|text]      输出格式 (默认: text)

# compare 命令
playwright-enhance-cli compare <url> [OPTIONS]
  --headless/--no-headless  是否无头模式
  --runs, -n INTEGER        运行次数 (默认: 3)
  -c, --config PATH         配置文件路径
  -o, --output PATH         输出文件路径 (JSON格式)
```

## 结果解读

### 性能指标

- **Load Time (加载时间)**: 页面完全加载所需时间
- **Average (平均值)**: 多次运行的平均时间
- **Min/Max (最小/最大)**: 最快和最慢的加载时间
- **Improvement (提升百分比)**: 性能提升百分比 = (原生 - 增强) / 原生 × 100%
- **Speedup (加速比)**: 加速比 = 原生时间 / 增强时间

### 性能提升等级

| 提升百分比 | 等级 | 说明 |
|-----------|------|------|
| > 60% | 🚀 优秀 | 显著的性能提升 |
| 40-60% | ⚡ 良好 | 明显的性能改善 |
| 20-40% | ✅ 可接受 | 适度的性能提升 |
| < 20% | ⚠️  有限 | 轻微的性能改善 |

## 故障排除

### 问题 1: 命令未找到

```bash
./run_cli_comparison.sh: command not found
```

**解决方案：**
```bash
chmod +x run_cli_comparison.sh
./run_cli_comparison.sh
```

### 问题 2: CLI 工具未安装

```bash
python: No module named 'playwright_enhance.cli.main'
```

**解决方案：**
```bash
pip install -e .
```

### 问题 3: 网络超时

某些网站可能因网络问题导致测试失败。

**解决方案：**
- 检查网络连接
- 尝试其他网站
- 增加运行次数以获得更稳定的结果

### 问题 4: 结果差异大

多次运行结果差异较大。

**解决方案：**
- 增加运行次数（--runs 5 或更多）
- 使用无头模式减少 GUI 开销
- 确保网络环境稳定
- 关闭其他消耗资源的程序

## 最佳实践

1. **运行次数建议**
   - 快速测试: 1-2 次
   - 日常测试: 3 次
   - 正式评估: 5 次或更多

2. **模式选择**
   - 性能测试: 使用无头模式
   - 调试问题: 使用可见模式

3. **网站选择**
   - 简单页面: Example Domain
   - 复杂应用: GitHub, Wikipedia
   - 快速网站: Hacker News

4. **结果分析**
   - 关注平均值，不要只看单次结果
   - 对比 min/max 判断稳定性
   - 查看不同网站的提升模式

## 下一步

- 📖 **CLI 使用指南**: [docs/cli-guide.md](docs/cli-guide.md)
- 🚀 **快速开始**: [CLI_QUICKSTART.md](CLI_QUICKSTART.md)
- 💻 **API 文档**: [docs/api-reference.md](docs/api-reference.md)
- 🧪 **真实测试**: [REAL_TEST_GUIDE.md](REAL_TEST_GUIDE.md)

## 相关工具

- `run_real_tests.sh` - 真实网站测试脚本（Wikipedia/GitHub/HackerNews）
- `run_cli_comparison.sh` - CLI 对比测试脚本（本文档）
- `examples/cli_batch_test.py` - Python 批量测试工具
- `examples/cli_demo.py` - CLI 功能演示

---

**快速命令：**

```bash
# 1. 快速单站测试
playwright-enhance-cli benchmark https://example.com

# 2. 详细性能对比
playwright-enhance-cli compare https://example.com --runs 5

# 3. 批量测试
python examples/cli_batch_test.py

# 4. 交互式测试
./run_cli_comparison.sh
```
