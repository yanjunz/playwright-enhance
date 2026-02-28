# CLI 工具概览

Playwright-Enhance 提供了一套完整的命令行工具，用于性能测试、对比分析和批量评估。

## 工具列表

### 1. playwright-enhance-cli（核心 CLI 工具）

主要的命令行接口，提供多个实用命令。

```bash
playwright-enhance-cli [COMMAND] [OPTIONS]
```

**可用命令：**

| 命令 | 功能 | 示例 |
|------|------|------|
| `benchmark` | 性能基准测试 | `playwright-enhance-cli benchmark https://example.com` |
| `compare` | 增强版 vs 原生版对比 | `playwright-enhance-cli compare https://example.com --runs 5` |
| `config` | 配置管理 | `playwright-enhance-cli config init config.json` |
| `info` | 系统信息 | `playwright-enhance-cli info` |
| `run` | 运行测试脚本 | `playwright-enhance-cli run test.py` |
| `demo` | 演示服务器 | `playwright-enhance-cli demo` |

📖 **详细文档**: [docs/cli-guide.md](docs/cli-guide.md)

---

### 2. run_cli_comparison.sh（交互式对比测试）

交互式 Shell 脚本，提供菜单式的 CLI 性能测试。

```bash
./run_cli_comparison.sh
```

**功能特点：**
- ✅ 交互式菜单
- ✅ 4 种测试类型
- ✅ 预设 4 个网站
- ✅ 自动生成报告

**测试类型：**
1. 单网站基准测试
2. 单网站性能对比
3. 多网站批量测试
4. 自定义 URL 测试

📖 **详细文档**: [CLI_COMPARISON_GUIDE.md](CLI_COMPARISON_GUIDE.md)

---

### 3. cli_batch_test.py（批量测试工具）

Python 批量测试工具，自动测试多个网站并生成详细报告。

```bash
# 默认配置（3次运行）
python examples/cli_batch_test.py

# 5次运行，可见模式
python examples/cli_batch_test.py --runs 5 --visible
```

**生成报告：**
- `summary.json` - JSON 格式汇总
- `REPORT.md` - Markdown 格式报告
- `*.json` - 各网站详细结果

**测试网站：**
- Example Domain
- Wikipedia
- Hacker News
- GitHub

📖 **详细文档**: [CLI_COMPARISON_GUIDE.md](CLI_COMPARISON_GUIDE.md#方式-2-python-批量测试工具)

---

### 4. run_real_tests.sh（真实场景测试）

测试真实网站的具体操作流程（导航、搜索、点击等）。

```bash
./run_real_tests.sh
```

**测试场景：**
1. Wikipedia 测试（10步，稳定）
2. Hacker News 测试（10步，快速）
3. GitHub 测试（10步，复杂）
4. Bilibili 测试（5步，中文站点）

**运行模式：**
- 先运行原生版，再运行增强版
- 先运行增强版，再运行原生版
- 只运行增强版
- 只运行原生版

📖 **详细文档**: [REAL_TEST_GUIDE.md](REAL_TEST_GUIDE.md)

---

### 5. cli_demo.py（CLI 功能演示）

交互式演示脚本，展示 CLI 工具的各种功能。

```bash
python examples/cli_demo.py
```

**演示内容：**
1. 显示系统信息
2. 显示默认配置
3. 创建配置文件
4. 验证配置文件
5. 显示帮助信息

---

## 快速对比

### 工具选择指南

| 需求 | 推荐工具 | 理由 |
|------|----------|------|
| 快速单站测试 | `playwright-enhance-cli benchmark` | 最简单直接 |
| 详细性能对比 | `playwright-enhance-cli compare` | 多次运行统计 |
| 交互式测试 | `./run_cli_comparison.sh` | 菜单式操作 |
| 批量测试 | `python cli_batch_test.py` | 自动化报告 |
| 真实场景测试 | `./run_real_tests.sh` | 完整操作流程 |
| 学习 CLI | `python cli_demo.py` | 功能演示 |

### 测试类型对比

| 工具 | 测试内容 | 输出 | 适用场景 |
|------|----------|------|----------|
| `benchmark` | 页面加载时间 | 单次结果 | 快速验证 |
| `compare` | 多次平均性能 | 统计数据 | 详细分析 |
| `cli_batch_test.py` | 多站批量测试 | JSON + MD 报告 | 全面评估 |
| `run_real_tests.sh` | 真实操作流程 | 终端输出 | 实际场景 |

## 使用场景

### 场景 1: 快速验证性能

**需求**: 测试单个页面的加载性能

**方案**:
```bash
playwright-enhance-cli benchmark https://your-site.com
```

---

### 场景 2: 详细性能分析

**需求**: 获得稳定的性能对比数据

**方案**:
```bash
playwright-enhance-cli compare https://your-site.com --runs 5
```

---

### 场景 3: 多站点评估

**需求**: 测试多个网站，生成汇总报告

**方案**:
```bash
python examples/cli_batch_test.py --runs 3
```

---

### 场景 4: 交互式探索

**需求**: 灵活选择测试类型和网站

**方案**:
```bash
./run_cli_comparison.sh
```

---

### 场景 5: CI/CD 集成

**需求**: 自动化性能监控

**方案**:
```bash
#!/bin/bash
# 批量测试
python examples/cli_batch_test.py --runs 5

# 检查性能阈值
python check_performance.py cli_test_results/*/summary.json
```

---

### 场景 6: 真实场景验证

**需求**: 测试完整的用户操作流程

**方案**:
```bash
./run_real_tests.sh
# 选择具体测试场景
```

---

## 输出格式

### 终端输出（benchmark）

```
Benchmark Results
==================================================
URL:        https://example.com
Mode:       Enhanced
Load Time:  0.876s (876ms)
```

### 统计输出（compare）

```
Performance Comparison
============================================================
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

### JSON 输出（批量测试）

```json
{
  "test_config": {
    "runs": 3,
    "total_sites": 4
  },
  "summary": {
    "avg_improvement_percent": 48.3,
    "avg_speedup": 1.93
  }
}
```

### Markdown 报告（批量测试）

```markdown
# CLI 批量性能测试报告

## 测试结果

| 网站 | 原生 (s) | 增强版 (s) | 性能提升 | 加速比 |
|------|----------|-----------|----------|--------|
| Example | 2.456 | 1.234 | 49.8% | 1.99x |
...
```

## 性能指标说明

### 时间指标

- **Load Time**: 单次页面加载时间
- **Average**: 多次运行的平均时间
- **Min/Max**: 最快和最慢的加载时间

### 性能指标

- **Improvement**: 性能提升百分比 = (原生 - 增强) / 原生 × 100%
- **Speedup**: 加速比 = 原生时间 / 增强时间

### 性能等级

| 提升百分比 | 等级 | 说明 |
|-----------|------|------|
| > 60% | 🚀 优秀 | 显著提升 |
| 40-60% | ⚡ 良好 | 明显改善 |
| 20-40% | ✅ 可接受 | 适度提升 |
| < 20% | ⚠️  有限 | 轻微改善 |

## 最佳实践

### 1. 运行次数建议

- **快速测试**: 1-2 次
- **日常测试**: 3 次
- **正式评估**: 5 次或更多

### 2. 模式选择

- **性能测试**: 使用无头模式（更快，更稳定）
- **调试问题**: 使用可见模式（能看到操作）

### 3. 工具选择

- **单次快速**: `benchmark`
- **多次统计**: `compare`
- **批量测试**: `cli_batch_test.py`
- **交互式**: `run_cli_comparison.sh`
- **真实场景**: `run_real_tests.sh`

### 4. 结果分析

- 关注**平均值**，不要只看单次结果
- 对比 **Min/Max** 判断稳定性
- 查看**不同网站**的提升模式
- **多次运行**获得可靠数据

## 故障排除

### 问题 1: 命令未找到

```bash
playwright-enhance-cli: command not found
```

**解决方案**:
```bash
# 确保已安装
pip install playwright-enhance

# 或使用 Python 模块方式
python -m playwright_enhance.cli.main [COMMAND]
```

### 问题 2: 脚本无执行权限

```bash
./run_cli_comparison.sh: Permission denied
```

**解决方案**:
```bash
chmod +x run_cli_comparison.sh
chmod +x run_real_tests.sh
```

### 问题 3: 网络超时

测试某些网站时超时失败。

**解决方案**:
- 检查网络连接
- 尝试其他网站
- 增加运行次数以获得更稳定的结果

### 问题 4: 结果波动大

多次运行结果差异较大。

**解决方案**:
- 增加运行次数（--runs 5 或更多）
- 使用无头模式减少 GUI 开销
- 确保网络环境稳定
- 关闭其他消耗资源的程序

## 文档导航

### 快速开始
- 📖 [CLI_QUICKSTART.md](CLI_QUICKSTART.md) - CLI 快速入门
- 🚀 [docs/quick-start.md](docs/quick-start.md) - 整体快速开始

### 详细指南
- 📘 [docs/cli-guide.md](docs/cli-guide.md) - CLI 完整使用指南
- 📗 [CLI_COMPARISON_GUIDE.md](CLI_COMPARISON_GUIDE.md) - CLI 对比测试指南
- 📙 [REAL_TEST_GUIDE.md](REAL_TEST_GUIDE.md) - 真实场景测试指南

### 技术文档
- 💻 [docs/api-reference.md](docs/api-reference.md) - API 参考
- 📊 [docs/performance.md](docs/performance.md) - 性能优化指南
- 🏗️  [IMPLEMENTATION_STATUS.md](IMPLEMENTATION_STATUS.md) - 实现状态

## 快速命令参考

```bash
# === 核心 CLI 命令 ===

# 基准测试
playwright-enhance-cli benchmark https://example.com

# 性能对比（5次运行）
playwright-enhance-cli compare https://example.com --runs 5

# 生成配置文件
playwright-enhance-cli config init config.json --minimal

# 查看系统信息
playwright-enhance-cli info

# === 测试脚本 ===

# CLI 对比测试（交互式）
./run_cli_comparison.sh

# 批量测试（Python）
python examples/cli_batch_test.py --runs 3

# 真实场景测试
./run_real_tests.sh

# CLI 功能演示
python examples/cli_demo.py

# === 快捷方式 ===

# 快速单站测试
playwright-enhance-cli benchmark https://example.com

# 详细对比（推荐）
playwright-enhance-cli compare https://example.com --runs 5 -o results.json

# 可见模式调试
playwright-enhance-cli benchmark https://example.com --no-headless
```

---

**更多信息:**
- GitHub: https://github.com/playwright-enhance/playwright-enhance
- 文档: [docs/](docs/)
- 示例: [examples/](examples/)
