# Playwright-Enhance CLI 命令参考

## 🎯 设计理念

**与 Playwright CLI 保持兼容**，所有标准命令都支持，并添加 `--enhanced` 选项启用智能优化。

---

## 📋 命令对照表

| Playwright 命令 | Playwright-Enhance 命令 | 增强选项 |
|----------------|------------------------|---------|
| `playwright open` | `playwright-enhance-cli open` | `--enhanced` |
| `playwright codegen` | `playwright-enhance-cli codegen` | ⚠️ 重定向到原生 |
| `playwright install` | `playwright-enhance-cli install` | ✅ 直接代理 |
| `playwright install-deps` | `playwright-enhance-cli install-deps` | ✅ 直接代理 |
| `playwright screenshot` | `playwright-enhance-cli screenshot` | `--enhanced` |
| `playwright pdf` | `playwright-enhance-cli pdf` | `--enhanced` |
| `playwright cr/ff/wk` | `playwright-enhance-cli cr/ff/wk` | `--enhanced` |
| ❌ 无 | `playwright-enhance-cli bench` | ✨ 新增 |
| ❌ 无 | `playwright-enhance-cli config` | ✨ 新增 |
| ❌ 无 | `playwright-enhance-cli info` | ✨ 新增 |

---

## 🚀 基础命令（与 Playwright 兼容）

### 1. open - 打开浏览器

```bash
# 原生模式（与 playwright open 相同）
playwright-enhance-cli open https://example.com

# 增强模式（启用智能等待）
playwright-enhance-cli open https://example.com --enhanced

# 指定浏览器
playwright-enhance-cli open https://github.com --browser firefox --enhanced

# 无头模式
playwright-enhance-cli open https://example.com --enhanced --headless
```

**选项**：
- `-b, --browser` - 浏览器类型（chromium, firefox, webkit）
- `--headless/--headed` - 无头或有界面模式
- `--enhanced/--native` - 增强或原生模式
- `-c, --config` - 配置文件路径

---

### 2. screenshot - 截图

```bash
# 原生模式
playwright-enhance-cli screenshot https://example.com output.png

# 增强模式（更快的页面加载）
playwright-enhance-cli screenshot https://example.com output.png --enhanced

# 全页截图
playwright-enhance-cli screenshot https://github.com page.png --enhanced --full-page

# 指定浏览器
playwright-enhance-cli screenshot https://example.com test.png --browser firefox --enhanced
```

**选项**：
- `-b, --browser` - 浏览器类型
- `--enhanced/--native` - 增强或原生模式
- `--full-page` - 全页截图
- `-c, --config` - 配置文件路径

**输出示例**：
```
Screenshot saved to: output.png
Load time (enhanced): 1.234s
```

---

### 3. pdf - 生成 PDF

```bash
# 原生模式
playwright-enhance-cli pdf https://example.com output.pdf

# 增强模式
playwright-enhance-cli pdf https://example.com output.pdf --enhanced
```

**注意**：仅支持 Chromium 浏览器。

---

### 4. 浏览器快捷命令

```bash
# Chromium
playwright-enhance-cli cr https://example.com --enhanced

# Firefox
playwright-enhance-cli ff https://example.com --enhanced

# WebKit
playwright-enhance-cli wk https://example.com --enhanced
```

等同于：
```bash
playwright-enhance-cli open https://example.com --browser chromium --enhanced
```

---

### 5. install - 安装浏览器

```bash
# 安装所有浏览器
playwright-enhance-cli install

# 安装特定浏览器
playwright-enhance-cli install chromium firefox

# 同时安装系统依赖
playwright-enhance-cli install --with-deps
```

**说明**：直接代理到 `playwright install`。

---

### 6. install-deps - 安装系统依赖

```bash
# 安装所有浏览器依赖
playwright-enhance-cli install-deps

# 安装特定浏览器依赖
playwright-enhance-cli install-deps chromium
```

---

### 7. codegen - 代码生成

```bash
playwright-enhance-cli codegen https://example.com
```

**说明**：重定向到原生 `playwright codegen`。代码生成后可以手动添加 `enhance()` 包装器。

---

## ⚡ 增强命令（新增功能）

### 1. bench run - 性能基准测试

对比增强版和原生版的性能差异。

```bash
# 基础用法
playwright-enhance-cli bench run https://example.com

# 多次运行（更准确）
playwright-enhance-cli bench run https://github.com --runs 5

# 指定浏览器
playwright-enhance-cli bench run https://example.com --browser firefox --runs 3

# 保存结果
playwright-enhance-cli bench run https://example.com -o results.json

# 可见模式
playwright-enhance-cli bench run https://example.com --headed
```

**选项**：
- `--runs, -n` - 运行次数（默认：3）
- `--browser, -b` - 浏览器类型
- `--headless/--headed` - 无头或有界面模式
- `--output, -o` - 保存结果到文件
- `--config, -c` - 配置文件路径

**输出示例**：
```
============================================================
Performance Benchmark Results
============================================================
URL:        https://example.com
Browser:    chromium
Runs:       3

Native Playwright:
  Average:  1.337s
  Min:      0.995s
  Max:      1.957s

Enhanced Playwright:
  Average:  1.02s
  Min:      0.985s
  Max:      1.048s

⚡ Improvement: 23.7% faster (1.31x speedup)
```

---

### 2. config - 配置管理

#### show - 显示当前配置
```bash
playwright-enhance-cli config show
```

**输出**：
```json
{
  "smart_waiting": {
    "enabled": true,
    "initial_timeout": 3000,
    "max_timeout": 8000
  }
}
```

---

#### init - 初始化配置文件
```bash
# 完整配置
playwright-enhance-cli config init config.json

# 最小配置
playwright-enhance-cli config init config.json --minimal
```

---

#### validate - 验证配置
```bash
playwright-enhance-cli config validate config.json
```

**输出**：
```
✅ Configuration valid: config.json
{
  "smart_waiting": {
    "enabled": true,
    ...
  }
}
```

---

### 3. info - 系统信息

```bash
playwright-enhance-cli info
```

**输出**：
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
```

---

## 🎨 使用场景

### 场景 1：快速截图
```bash
# 原生 Playwright
playwright screenshot https://example.com output.png

# Playwright-Enhance（更快）
playwright-enhance-cli screenshot https://example.com output.png --enhanced
```

---

### 场景 2：性能对比
```bash
# 测试你的网站
playwright-enhance-cli bench run https://your-site.com --runs 5

# 多个浏览器对比
playwright-enhance-cli bench run https://your-site.com -b chromium --runs 3
playwright-enhance-cli bench run https://your-site.com -b firefox --runs 3
playwright-enhance-cli bench run https://your-site.com -b webkit --runs 3
```

---

### 场景 3：调试页面
```bash
# 原生模式调试
playwright-enhance-cli open https://your-site.com

# 增强模式调试（看智能等待效果）
playwright-enhance-cli open https://your-site.com --enhanced --headed
```

---

### 场景 4：生成 PDF 报告
```bash
# 增强模式（更快加载）
playwright-enhance-cli pdf https://docs.example.com report.pdf --enhanced
```

---

## 📊 性能对比

### 简单页面（example.com）
```bash
playwright-enhance-cli bench run https://example.com --runs 5
```

**预期结果**：
- 原生：~1.0-1.2s
- 增强：~1.0-1.3s
- **差异**：持平或略慢（插件开销）

---

### 复杂页面（wikipedia.org）
```bash
playwright-enhance-cli bench run https://www.wikipedia.org --runs 5
```

**预期结果**：
- 原生：~4-6s
- 增强：~2-3s
- **提升**：40-50% 更快

---

### 重资源页面（github.com）
```bash
playwright-enhance-cli bench run https://github.com --runs 5
```

**预期结果**：
- 原生：~3-5s
- 增强：~2-3s
- **提升**：30-40% 更快

---

## 🔄 迁移指南

### 从 Playwright CLI 迁移

只需将 `playwright` 替换为 `playwright-enhance-cli`，并添加 `--enhanced`：

```bash
# 之前
playwright screenshot https://example.com output.png

# 之后
playwright-enhance-cli screenshot https://example.com output.png --enhanced
```

### 从旧版 CLI 迁移

旧命令：
```bash
playwright-enhance-cli benchmark https://example.com
playwright-enhance-cli compare https://example.com --runs 3
```

新命令：
```bash
# 单次测试
playwright-enhance-cli screenshot https://example.com test.png --enhanced

# 性能对比
playwright-enhance-cli bench run https://example.com --runs 3
```

---

## 💡 最佳实践

### 1. 默认使用增强模式
```bash
# 推荐：总是添加 --enhanced
playwright-enhance-cli screenshot https://example.com test.png --enhanced
```

### 2. 性能测试多次运行
```bash
# 至少 3-5 次获得稳定结果
playwright-enhance-cli bench run https://example.com --runs 5
```

### 3. 使用配置文件
```bash
# 创建配置
playwright-enhance-cli config init my-config.json --minimal

# 使用配置
playwright-enhance-cli screenshot https://example.com test.png --enhanced -c my-config.json
```

### 4. 保存基准结果
```bash
# 保存 JSON 用于后续分析
playwright-enhance-cli bench run https://example.com --runs 5 -o benchmark.json
```

---

## 🐛 故障排除

### 问题 1：命令未找到
```bash
# 确保已安装
pip install -e .

# 或使用模块方式
python -m playwright_enhance.cli <command>
```

---

### 问题 2：浏览器未安装
```bash
# 安装浏览器
playwright-enhance-cli install

# 或安装特定浏览器
playwright-enhance-cli install chromium
```

---

### 问题 3：增强模式无效果
```bash
# 检查配置
playwright-enhance-cli config show

# 确保使用 --enhanced 选项
playwright-enhance-cli screenshot https://example.com test.png --enhanced
```

---

## 📚 相关文档

- **CLI_QUICKSTART.md** - 快速开始指南（旧版命令）
- **docs/cli-guide.md** - 完整 CLI 使用文档
- **CLI_TOOLS_OVERVIEW.md** - CLI 工具概览
- **README.md** - 项目主文档

---

## 🎯 下一步

1. ✅ 与 Playwright CLI 完全兼容
2. ✅ 支持所有主要命令
3. ✅ 添加增强模式选项
4. 🚧 后续计划：
   - 添加 `show-trace` 命令支持
   - 更多浏览器配置选项
   - CI/CD 集成示例

---

**最后更新**: 2025-02-28
