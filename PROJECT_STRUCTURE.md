# 项目结构

参考 [Playwright 官方项目](https://github.com/microsoft/playwright) 重构后的清晰目录结构。

## 📁 目录结构

```
playwright-enhance/
├── .github/              # GitHub Actions 配置 (待添加)
├── docs/                 # 📖 文档 (6个)
│   ├── api-reference.md
│   ├── cli-guide.md
│   ├── openclaw-integration.md
│   ├── performance.md
│   ├── quick-start.md
│   └── testing.md
├── examples/             # 🎯 示例代码 (4个文件)
│   ├── README.md
│   ├── basic_usage.py
│   ├── real_hackernews_test.py
│   └── real_wikipedia_test.py
├── playwright_enhance/   # 🔧 核心代码
│   ├── __init__.py
│   ├── capabilities/     # 增强功能
│   ├── cli/              # CLI 工具
│   ├── core/             # 核心增强
│   └── utils/            # 工具函数
├── scripts/              # 🚀 工具脚本 (7个)
│   ├── benchmark_bilibili.sh
│   ├── cli_comparison.sh
│   ├── demo.sh
│   ├── playwright_compatible_demo.sh
│   ├── test.sh
│   ├── verify.sh
│   └── verify_cli.sh
├── tests/                # 🧪 测试代码
│   ├── unit/             # 单元测试
│   ├── integration/      # 集成测试
│   └── performance/      # 性能测试
├── .gitignore
├── .pre-commit-config.yaml
├── CONTRIBUTING.md
├── README.md
├── pyproject.toml
├── pytest.ini
└── setup.py
```

---

## 📊 统计信息

### 清理前 vs 清理后

| 指标 | 清理前 | 清理后 | 改善 |
|------|--------|--------|------|
| **根目录 .md 文件** | 26 个 | 2 个 | ↓ 92% |
| **根目录 .sh 文件** | 10+ 个 | 0 个 | ↓ 100% |
| **示例文件** | 10 个 | 4 个 | ↓ 60% |
| **临时文档** | 25+ 个 | 0 个 | ✅ |
| **总文件数** | ~80+ | ~45 | ↓ 44% |

### 当前统计

- **根目录配置文件**: 5 个 (README, CONTRIBUTING, pyproject, pytest, setup)
- **文档**: 7 个 (docs/)
- **示例**: 4 个 (examples/)
- **脚本**: 8 个 (scripts/)
- **核心代码**: 4 个模块 (playwright_enhance/)
- **测试代码**: 3 个类型 (tests/)

---

## 🎯 各目录说明

### 1. `docs/` - 文档

| 文件 | 描述 | 读者 |
|------|------|------|
| `quick-start.md` | 快速开始指南 | 新手 |
| `cli-guide.md` | CLI 完整指南 | CLI 用户 |
| `comparison-guide.md` | 性能对比指南 ⭐ | 所有用户 |
| `api-reference.md` | API 参考文档 | 开发者 |
| `performance.md` | 性能优化指南 | 高级用户 |
| `testing.md` | 测试指南 | 开发者 |
| `openclaw-integration.md` | OpenClaw 集成 | 集成用户 |

---

### 2. `examples/` - 示例

| 文件 | 描述 | 复杂度 |
|------|------|--------|
| `README.md` | 示例说明 | - |
| `basic_usage.py` | 基础用法 | ⭐ |
| `real_hackernews_test.py` | Hacker News 真实测试 | ⭐⭐⭐ |
| `real_wikipedia_test.py` | Wikipedia 真实测试 | ⭐⭐⭐ |

**特点**:
- ✅ 由简到难
- ✅ 真实场景
- ✅ 完整注释
- ✅ 可直接运行

---

### 3. `scripts/` - 工具脚本

| 脚本 | 用途 | 耗时 |
|------|------|------|
| `compare.sh` | Playwright 对比测试 ⭐ | ~60s |
| `demo.sh` | 运行基础演示 | ~5s |
| `test.sh` | 运行所有测试 | ~30s |
| `verify.sh` | 验证环境配置 | ~3s |
| `cli_comparison.sh` | CLI 对比测试 | ~25s |
| `verify_cli.sh` | 验证 CLI 环境 | ~10s |
| `benchmark_bilibili.sh` | Bilibili 性能测试 | ~15s |
| `playwright_compatible_demo.sh` | 兼容性演示 | ~10s |

**使用方法**:

```bash
# Playwright 对比（推荐）⭐
bash scripts/compare.sh

# 快速验证
bash scripts/verify.sh

# 运行演示
bash scripts/demo.sh

# 运行测试
bash scripts/test.sh

# CLI 对比
bash scripts/cli_comparison.sh
```

---

### 4. `playwright_enhance/` - 核心代码

```
playwright_enhance/
├── __init__.py           # 主入口
├── capabilities/         # 增强功能
│   ├── smart_waiting.py
│   ├── auto_retry.py
│   └── ...
├── cli/                  # CLI 工具
│   ├── main.py
│   └── commands/
├── core/                 # 核心增强
│   ├── browser.py
│   ├── page.py
│   └── ...
└── utils/                # 工具函数
    ├── logger.py
    └── config.py
```

---

### 5. `tests/` - 测试代码

```
tests/
├── unit/                 # 单元测试
│   ├── test_core.py
│   ├── test_capabilities.py
│   └── test_utils.py
├── integration/          # 集成测试
│   ├── test_browser_integration.py
│   └── test_page_integration.py
└── performance/          # 性能测试
    ├── test_smart_waiting_performance.py
    └── test_retry_performance.py
```

---

## 🚀 快速开始

### 安装

```bash
pip install -e .
```

### 基础使用

```bash
# 查看文档
cat docs/quick-start.md

# 运行示例
python examples/basic_usage.py

# 运行测试
bash scripts/test.sh
```

### CLI 使用

```bash
# 查看帮助
playwright-enhance-cli --help

# 运行演示
bash scripts/demo.sh

# CLI 对比
bash scripts/cli_comparison.sh
```

---

## 📖 文档导航

### 新手入门

1. 阅读 `README.md` - 项目概览
2. 阅读 `docs/quick-start.md` - 快速开始
3. 运行 `examples/basic_usage.py` - 基础示例
4. 运行 `bash scripts/demo.sh` - 完整演示

### 深入学习

1. `docs/api-reference.md` - API 详细说明
2. `docs/cli-guide.md` - CLI 完整指南
3. `docs/performance.md` - 性能优化技巧
4. `examples/real_*_test.py` - 真实场景

### 开发贡献

1. `CONTRIBUTING.md` - 贡献指南
2. `docs/testing.md` - 测试规范
3. `bash scripts/test.sh` - 运行测试
4. `bash scripts/verify.sh` - 验证环境

---

## ✨ 设计原则

参考 [Playwright 官方项目](https://github.com/microsoft/playwright)：

1. **清晰的结构** - 每个目录职责明确
2. **完整的文档** - docs/ 目录统一管理
3. **实用的示例** - examples/ 由简到难
4. **便捷的脚本** - scripts/ 自动化常见任务
5. **标准的测试** - tests/ 分类清晰

---

## 🔄 版本历史

### v0.2.0 (2026-02-28) - 项目重构

**重大改进**:
- ✅ 删除 25+ 临时文档
- ✅ 删除 8+ 重复示例
- ✅ 整合 10+ 脚本到 scripts/
- ✅ 根目录 .md 文件从 26 个 → 2 个
- ✅ 根目录 .sh 文件从 10+ 个 → 0 个
- ✅ 参考 Playwright 官方结构

**文件变化**:
- 删除: 43 个文件
- 新增: scripts/ 目录
- 移动: 7 个脚本
- 清理: 12,639 行临时内容

**参考**: https://github.com/microsoft/playwright

---

## 📝 维护指南

### 添加新文档

```bash
# 放在 docs/ 目录
touch docs/new-feature.md
```

### 添加新示例

```bash
# 放在 examples/ 目录
touch examples/new_example.py
# 更新 examples/README.md
```

### 添加新脚本

```bash
# 放在 scripts/ 目录
touch scripts/new_tool.sh
chmod +x scripts/new_tool.sh
```

### 添加新测试

```bash
# 根据类型放在 tests/ 对应目录
touch tests/unit/test_new_feature.py
```

---

## 🎉 总结

清理后的项目结构：

- ✅ **更清晰** - 目录职责明确
- ✅ **更专业** - 参考官方标准
- ✅ **更易维护** - 文件组织合理
- ✅ **更易上手** - 文档完整清晰

**核心理念**: 保持简洁，专注核心，易于维护。

---

## 🔗 相关链接

- [Playwright 官方项目](https://github.com/microsoft/playwright)
- [Playwright 文档](https://playwright.dev/)
- [Python 项目结构最佳实践](https://docs.python-guide.org/writing/structure/)
