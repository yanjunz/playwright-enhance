# CLI Guide

Playwright-Enhance 提供了强大的命令行工具，用于性能测试、配置管理和基准测试。

## 安装

安装 playwright-enhance 后，CLI 工具会自动可用：

```bash
pip install playwright-enhance
```

## 使用方式

### 直接调用（推荐）

```bash
playwright-enhance-cli [COMMAND] [OPTIONS]
```

### 模块方式

```bash
python -m playwright_enhance.cli.main [COMMAND] [OPTIONS]
```

## 命令概览

```bash
playwright-enhance-cli --help
```

### 可用命令

| 命令 | 说明 |
|------|------|
| `benchmark` | 性能基准测试 |
| `compare` | 对比增强版和原生版性能 |
| `config` | 配置文件管理 |
| `info` | 显示系统信息 |
| `run` | 运行测试脚本 |
| `demo` | 启动演示服务器 |

## 详细命令说明

### 1. benchmark - 性能基准测试

测试单个 URL 的页面加载性能。

```bash
# 基本用法
playwright-enhance-cli benchmark https://example.com

# 可视化模式（非无头）
playwright-enhance-cli benchmark https://github.com --no-headless

# 使用原生 Playwright
playwright-enhance-cli benchmark https://example.com --native

# 使用配置文件
playwright-enhance-cli benchmark https://example.com -c config.json

# 保存结果到文件
playwright-enhance-cli benchmark https://example.com -o results.json --format json
```

**选项：**
- `--headless/--no-headless`: 是否无头模式（默认：是）
- `--enhanced/--native`: 使用增强版或原生版（默认：增强版）
- `--config, -c`: 配置文件路径
- `--output, -o`: 结果输出文件
- `--format`: 输出格式（json 或 text，默认：text）

**输出示例：**
```
Benchmark Results
==================================================
URL:        https://example.com
Mode:       Enhanced
Headless:   True
Title:      Example Domain
Load Time:  0.876s (876ms)
```

### 2. compare - 对比性能

对比增强版和原生版的性能差异，运行多次测试取平均值。

```bash
# 基本用法（默认 3 次）
playwright-enhance-cli compare https://example.com

# 运行 5 次测试
playwright-enhance-cli compare https://example.com --runs 5

# 可视化模式
playwright-enhance-cli compare https://github.com --no-headless --runs 3

# 保存详细结果
playwright-enhance-cli compare https://example.com --runs 5 -o comparison.json
```

**选项：**
- `--headless/--no-headless`: 是否无头模式
- `--runs, -n`: 每种模式运行的次数（默认：3）
- `--config, -c`: 配置文件路径
- `--output, -o`: 结果输出文件（JSON 格式）

**输出示例：**
```
Performance Comparison
============================================================
URL:        https://example.com
Runs:       3

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

### 3. config - 配置管理

管理 playwright-enhance 配置文件。

#### 3.1 显示配置

```bash
# 显示默认配置
playwright-enhance-cli config show

# 显示指定配置文件
playwright-enhance-cli config show --file config.json
```

#### 3.2 初始化配置文件

```bash
# 创建完整配置文件
playwright-enhance-cli config init config.json

# 创建最小配置文件
playwright-enhance-cli config init config.json --minimal
```

**最小配置示例：**
```json
{
  "smart_waiting": {
    "enabled": true,
    "initial_timeout": 5000,
    "max_timeout": 10000
  }
}
```

#### 3.3 验证配置文件

```bash
playwright-enhance-cli config validate config.json
```

### 4. info - 系统信息

显示 playwright-enhance 的安装和系统信息。

```bash
playwright-enhance-cli info
```

**输出示例：**
```
Playwright-Enhance Information
==================================================
Version:        0.1.0
Python:         3.12.9
Platform:       Darwin 24.6.0
Playwright:     1.40.0

Installation:
  Package:      playwright-enhance
  CLI Command:  playwright-enhance-cli

Features:
  ✓ Smart Waiting (adaptive timeouts)
  ✓ Core Architecture (plugin system)
  ⚠ Multi-Locator (coming soon)
  ⚠ Concurrent Engine (coming soon)
  ⚠ Cache System (coming soon)

Documentation:  https://github.com/playwright-enhance/playwright-enhance
```

### 5. run - 运行测试脚本

运行 Playwright 测试脚本，自动设置环境变量。

```bash
# 基本用法（增强模式，无头）
playwright-enhance-cli run examples/test.py

# 可视化模式
playwright-enhance-cli run examples/test.py --no-headless

# 原生 Playwright 模式
playwright-enhance-cli run examples/test.py --native

# 使用配置文件
playwright-enhance-cli run examples/test.py -c config.json
```

**选项：**
- `--headless/--no-headless`: 是否无头模式
- `--enhanced/--native`: 使用增强版或原生版
- `--config, -c`: 配置文件路径

**环境变量设置：**
- `PLAYWRIGHT_ENHANCE_ENABLED`: true/false
- `PLAYWRIGHT_HEADLESS`: true/false
- `PLAYWRIGHT_ENHANCE_CONFIG`: 配置文件路径

### 6. demo - 演示服务器

启动交互式演示服务器（开发中）。

```bash
# 默认端口 8080
playwright-enhance-cli demo

# 自定义端口
playwright-enhance-cli demo --port 3000
```

## 实用场景

### 场景 1: 快速性能测试

测试网站加载性能：

```bash
playwright-enhance-cli benchmark https://your-website.com
```

### 场景 2: 优化前后对比

对比优化效果：

```bash
# 测试原生版
playwright-enhance-cli benchmark https://your-website.com --native -o before.json

# 测试增强版
playwright-enhance-cli benchmark https://your-website.com --enhanced -o after.json

# 或直接使用 compare 命令
playwright-enhance-cli compare https://your-website.com --runs 5
```

### 场景 3: CI/CD 集成

在 CI/CD 管道中运行性能测试：

```bash
#!/bin/bash
# ci-performance-test.sh

# 运行对比测试
playwright-enhance-cli compare https://staging.example.com \
  --runs 5 \
  --headless \
  -o performance-report.json

# 检查性能提升是否达标
python check_performance.py performance-report.json
```

### 场景 4: 本地开发测试

开发时快速验证：

```bash
# 创建配置
playwright-enhance-cli config init dev-config.json --minimal

# 编辑配置文件（调整超时等参数）
# vim dev-config.json

# 运行测试
playwright-enhance-cli run tests/my_test.py -c dev-config.json --no-headless
```

### 场景 5: 多网站批量测试

批量测试多个网站：

```bash
#!/bin/bash
# batch-benchmark.sh

URLS=(
  "https://example.com"
  "https://github.com"
  "https://wikipedia.org"
)

for url in "${URLS[@]}"; do
  echo "Testing $url..."
  playwright-enhance-cli compare "$url" --runs 3 -o "results-$(echo $url | md5).json"
done
```

## 配置文件

### 完整配置示例

```json
{
  "smart_waiting": {
    "enabled": true,
    "initial_timeout": 5000,
    "max_timeout": 10000,
    "min_timeout": 1000
  },
  "multi_locator": {
    "enabled": false,
    "semantic_enabled": true,
    "visual_enabled": true,
    "visual_confidence_threshold": 0.85,
    "fuzzy_match_threshold": 0.75
  },
  "concurrent_engine": {
    "enabled": false,
    "max_concurrent_ops": 10,
    "auto_flush": true,
    "flush_interval": 100
  },
  "cache_system": {
    "enabled": false,
    "l1_ttl": 5000,
    "l2_ttl": 10000,
    "l3_max_size": 104857600,
    "lru_enabled": true
  },
  "perf_monitor": {
    "enabled": false,
    "detailed_timing": true,
    "output_format": "json",
    "output_file": null
  }
}
```

### 环境变量配置

也可以通过环境变量配置：

```bash
# 启用智能等待
export PLAYWRIGHT_ENHANCE_SMART_WAITING__ENABLED=true
export PLAYWRIGHT_ENHANCE_SMART_WAITING__INITIAL_TIMEOUT=3000

# 运行测试
playwright-enhance-cli benchmark https://example.com
```

## 输出格式

### JSON 输出格式

使用 `--format json` 或 `-o file.json` 可以获得结构化的 JSON 输出：

```json
{
  "url": "https://example.com",
  "enhanced": true,
  "headless": true,
  "load_time": 0.876,
  "load_time_ms": 876,
  "title": "Example Domain"
}
```

### 对比测试 JSON 输出

```json
{
  "url": "https://example.com",
  "runs": 5,
  "native": {
    "times": [2.234, 2.456, 2.678, 2.345, 2.567],
    "average": 2.456,
    "min": 2.234,
    "max": 2.678
  },
  "enhanced": {
    "times": [1.123, 1.234, 1.345, 1.189, 1.267],
    "average": 1.232,
    "min": 1.123,
    "max": 1.345
  },
  "improvement_percent": 49.8,
  "speedup": 1.99
}
```

## 故障排除

### 问题 1: 命令未找到

```bash
playwright-enhance-cli: command not found
```

**解决方案：**
```bash
# 确保已安装
pip install playwright-enhance

# 或使用模块方式
python -m playwright_enhance.cli.main [COMMAND]
```

### 问题 2: Playwright 未安装

```bash
playwright-enhance-cli benchmark https://example.com
# Error: Playwright browsers not found
```

**解决方案：**
```bash
playwright install chromium
```

### 问题 3: 配置文件无效

```bash
playwright-enhance-cli config validate config.json
# Error: Invalid configuration
```

**解决方案：**
```bash
# 重新生成配置文件
playwright-enhance-cli config init config.json

# 或检查 JSON 语法
python -m json.tool config.json
```

## 最佳实践

1. **性能测试建议**
   - 使用 `--runs 5` 或更多次数以获得稳定结果
   - 在相同网络条件下测试
   - 使用 `--headless` 模式以减少 GUI 开销

2. **配置管理**
   - 为不同环境创建不同的配置文件（dev、staging、prod）
   - 将配置文件加入版本控制
   - 使用 `--minimal` 生成最小配置，避免不必要的复杂性

3. **CI/CD 集成**
   - 使用 JSON 输出格式便于解析
   - 设置性能阈值检查
   - 保存历史测试结果用于趋势分析

4. **开发调试**
   - 使用 `--no-headless` 观察浏览器行为
   - 使用 `config show` 验证配置是否正确加载
   - 使用 `info` 检查安装状态

## 相关文档

- [快速开始指南](quick-start.md)
- [API 参考](api-reference.md)
- [性能优化指南](performance.md)
- [配置详解](../README.md#configuration)
