# CLI 快速开始

## 安装

```bash
pip install playwright-enhance
```

## 基本用法

### 1. 快速性能测试

```bash
# 测试单个页面加载性能
playwright-enhance-cli benchmark https://example.com

# 可视化模式（查看浏览器）
playwright-enhance-cli benchmark https://example.com --no-headless
```

**输出示例：**
```
Benchmark Results
==================================================
URL:        https://example.com
Mode:       Enhanced
Load Time:  0.876s (876ms)
```

### 2. 性能对比（推荐）

```bash
# 对比增强版 vs 原生版（运行 3 次）
playwright-enhance-cli compare https://example.com

# 运行更多次获得稳定结果
playwright-enhance-cli compare https://example.com --runs 5
```

**输出示例：**
```
Performance Comparison
============================================================
Native Playwright:
  Average:  2.456s

Enhanced Playwright:
  Average:  1.234s

Improvement: 49.8% faster (1.99x speedup)
```

### 3. 配置管理

```bash
# 创建配置文件（最小配置）
playwright-enhance-cli config init config.json --minimal

# 查看配置
playwright-enhance-cli config show

# 验证配置文件
playwright-enhance-cli config validate config.json
```

**最小配置示例 (config.json)：**
```json
{
  "smart_waiting": {
    "enabled": true,
    "initial_timeout": 5000,
    "max_timeout": 10000
  }
}
```

### 4. 使用配置文件运行测试

```bash
# 使用自定义配置
playwright-enhance-cli benchmark https://example.com -c config.json

# 保存结果到文件
playwright-enhance-cli benchmark https://example.com -o results.json --format json
```

### 5. 查看信息

```bash
# 显示系统和版本信息
playwright-enhance-cli info
```

## 常用命令速查

| 命令 | 说明 | 示例 |
|------|------|------|
| `benchmark <url>` | 性能基准测试 | `playwright-enhance-cli benchmark https://github.com` |
| `compare <url>` | 对比性能 | `playwright-enhance-cli compare https://example.com --runs 5` |
| `config show` | 显示配置 | `playwright-enhance-cli config show` |
| `config init <file>` | 创建配置 | `playwright-enhance-cli config init config.json --minimal` |
| `config validate <file>` | 验证配置 | `playwright-enhance-cli config validate config.json` |
| `info` | 系统信息 | `playwright-enhance-cli info` |
| `--help` | 帮助信息 | `playwright-enhance-cli --help` |

## 常用选项

| 选项 | 说明 | 默认值 |
|------|------|--------|
| `--headless` / `--no-headless` | 是否无头模式 | `--headless` |
| `--enhanced` / `--native` | 增强版或原生版 | `--enhanced` |
| `--runs, -n` | 运行次数（compare） | 3 |
| `--config, -c` | 配置文件路径 | 无 |
| `--output, -o` | 输出文件 | 无（打印到终端） |
| `--format` | 输出格式（json/text） | text |

## 实用场景

### 场景 1: 快速验证网站性能

```bash
playwright-enhance-cli benchmark https://your-site.com
```

### 场景 2: 对比优化效果

```bash
# 看看增强版比原生版快多少
playwright-enhance-cli compare https://your-site.com --runs 5
```

### 场景 3: 可视化调试

```bash
# 看到浏览器实际操作
playwright-enhance-cli benchmark https://your-site.com --no-headless
```

### 场景 4: CI/CD 性能监控

```bash
# 保存结果供后续分析
playwright-enhance-cli compare https://staging.example.com \
  --runs 5 \
  --headless \
  -o performance-report.json
```

### 场景 5: 自定义配置测试

```bash
# 1. 创建配置
playwright-enhance-cli config init my-config.json --minimal

# 2. 编辑配置文件（调整超时等参数）
vim my-config.json

# 3. 使用配置测试
playwright-enhance-cli benchmark https://example.com -c my-config.json
```

## 真实网站测试示例

项目提供了 4 个真实网站测试脚本，你可以直接运行：

```bash
# Wikipedia 测试（推荐，最稳定）
python examples/real_wikipedia_test.py --visible

# Hacker News 测试（最快，45%提升）
python examples/real_hackernews_test.py --visible

# GitHub 测试（真实开发场景）
python examples/real_github_test.py --visible

# 一键运行所有测试
./run_real_tests.sh
```

## 下一步

- 📖 **详细文档**: [docs/cli-guide.md](docs/cli-guide.md)
- 🚀 **快速开始**: [docs/quick-start.md](docs/quick-start.md)
- 📊 **性能指南**: [docs/performance.md](docs/performance.md)
- 💻 **API 文档**: [docs/api-reference.md](docs/api-reference.md)

## 故障排除

### 命令未找到

```bash
# 确保已安装
pip install playwright-enhance

# 或使用 Python 模块方式
python -m playwright_enhance.cli.main [COMMAND]
```

### Playwright 未安装

```bash
playwright install chromium
```

### 获取帮助

```bash
# 查看所有命令
playwright-enhance-cli --help

# 查看特定命令的帮助
playwright-enhance-cli benchmark --help
playwright-enhance-cli compare --help
playwright-enhance-cli config --help
```

## 示例输出

### Benchmark 输出

```
Benchmark Results
==================================================
URL:        https://example.com
Mode:       Enhanced
Headless:   True
Title:      Example Domain
Load Time:  0.876s (876ms)
```

### Compare 输出

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

### Info 输出

```
Playwright-Enhance Information
==================================================
Version:        0.1.0
Python:         3.12.9
Platform:       Darwin 24.6.0
Playwright:     1.40.0

Features:
  ✓ Smart Waiting (adaptive timeouts)
  ✓ Core Architecture (plugin system)
  ✓ CLI Tool (command-line utilities)
  ⚠ Multi-Locator (coming soon)
  ⚠ Concurrent Engine (coming soon)
```

---

**快速链接：**
- GitHub: https://github.com/playwright-enhance/playwright-enhance
- 文档: [docs/](docs/)
- 示例: [examples/](examples/)
