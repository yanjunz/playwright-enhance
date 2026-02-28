# Publishing Guide - 发布指南

让 `playwright-enhance` 像 Playwright 官方一样方便安装和使用。

---

## 🎯 目标用户体验

### Python 用户
```bash
# 最终目标 - 像 Playwright 一样简单
pip install playwright-enhance
playwright install chromium
```

### Node.js 用户（v0.2.0+）
```bash
npm install -D playwright-enhance
# 或
npx playwright-enhance
```

---

## 📦 阶段 1: PyPI 发布（立即可行）

### 当前状态
- ✅ GitHub 仓库已公开: `https://github.com/yanjunz/playwright-enhance`
- ✅ 包配置完整（`pyproject.toml`, `setup.py`）
- ✅ 依赖明确（playwright>=1.40.0）
- ⚠️ 需要更新 GitHub URLs

### 1.1 更新包配置

需要修改 `pyproject.toml` 中的 URLs：

```toml
[project.urls]
Homepage = "https://github.com/yanjunz/playwright-enhance"
Documentation = "https://github.com/yanjunz/playwright-enhance/blob/master/docs/"
Repository = "https://github.com/yanjunz/playwright-enhance"
"Bug Tracker" = "https://github.com/yanjunz/playwright-enhance/issues"
```

### 1.2 准备发布文件

确保以下文件完整：
- [x] `README.md` - 项目介绍
- [x] `LICENSE` - MIT 许可证
- [x] `CHANGELOG.md` - 版本历史（需创建）
- [x] `pyproject.toml` - 包元数据
- [x] `.gitignore` - 排除不必要文件

### 1.3 构建包

```bash
# 安装构建工具
pip install build twine

# 清理旧构建
rm -rf dist/ build/ *.egg-info

# 构建包
python -m build

# 验证构建结果
ls dist/
# 应该看到:
# playwright_enhance-0.1.0-py3-none-any.whl
# playwright-enhance-0.1.0.tar.gz
```

### 1.4 测试安装（TestPyPI）

```bash
# 注册 TestPyPI 账号: https://test.pypi.org/account/register/
# 配置 API Token: https://test.pypi.org/manage/account/token/

# 上传到 TestPyPI
python -m twine upload --repository testpypi dist/*

# 测试安装
pip install --index-url https://test.pypi.org/simple/ playwright-enhance

# 测试功能
python -c "from playwright_enhance import enhance; print('✅ Import successful')"
```

### 1.5 正式发布到 PyPI

```bash
# 注册 PyPI 账号: https://pypi.org/account/register/
# 配置 API Token: https://pypi.org/manage/account/token/

# 上传到 PyPI
python -m twine upload dist/*

# 等待几分钟后，用户就可以安装了：
pip install playwright-enhance
```

### 1.6 更新 README.md

发布后立即更新安装说明：

```markdown
### Installation

```bash
# Install playwright-enhance
pip install playwright-enhance

# Install browser binaries
playwright install chromium
```

Or install from GitHub for latest development version:
```bash
pip install git+https://github.com/yanjunz/playwright-enhance.git
```
```

---

## 🔄 阶段 2: 自动化发布流程

### 2.1 GitHub Actions - 自动发布

创建 `.github/workflows/publish.yml`：

```yaml
name: Publish to PyPI

on:
  release:
    types: [published]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install build twine
    
    - name: Build package
      run: python -m build
    
    - name: Publish to PyPI
      env:
        TWINE_USERNAME: __token__
        TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
      run: twine upload dist/*
```

### 2.2 版本发布流程

```bash
# 1. 更新版本号
# 编辑 pyproject.toml: version = "0.1.1"

# 2. 更新 CHANGELOG.md
git add CHANGELOG.md pyproject.toml
git commit -m "chore: bump version to 0.1.1"
git push

# 3. 创建 Git Tag
git tag v0.1.1
git push origin v0.1.1

# 4. 在 GitHub 创建 Release
# 访问: https://github.com/yanjunz/playwright-enhance/releases/new
# - Tag: v0.1.1
# - Title: Release v0.1.1
# - Description: 复制 CHANGELOG.md 内容

# 5. GitHub Actions 自动发布到 PyPI
```

---

## 🌐 阶段 3: npm/npx 支持（v0.2.0 计划）

### 3.1 Node.js 包结构

```
playwright-enhance/
├── package.json          # npm 包配置
├── src/
│   ├── index.ts         # 主入口
│   ├── enhance.ts       # 核心逻辑
│   └── cli.ts           # CLI 工具
├── dist/                # 编译后的 JS
├── tests/
└── README.md
```

### 3.2 package.json 配置

```json
{
  "name": "playwright-enhance",
  "version": "0.2.0",
  "description": "Performance-enhanced Playwright wrapper",
  "main": "dist/index.js",
  "types": "dist/index.d.ts",
  "bin": {
    "playwright-enhance": "./dist/cli.js"
  },
  "scripts": {
    "build": "tsc",
    "test": "jest",
    "prepublishOnly": "npm run build"
  },
  "keywords": ["playwright", "automation", "performance"],
  "author": "Playwright Enhance Team",
  "license": "MIT",
  "repository": {
    "type": "git",
    "url": "https://github.com/yanjunz/playwright-enhance.git"
  },
  "peerDependencies": {
    "@playwright/test": ">=1.40.0"
  },
  "devDependencies": {
    "@playwright/test": "^1.40.0",
    "typescript": "^5.0.0",
    "@types/node": "^20.0.0",
    "jest": "^29.0.0"
  }
}
```

### 3.3 TypeScript 实现示例

```typescript
// src/index.ts
import { Browser, BrowserContext, Page } from '@playwright/test';

export interface EnhanceConfig {
  smart_waiting?: {
    enabled: boolean;
    base_timeout?: number;
  };
  resource_hints?: {
    enabled: boolean;
  };
}

export function enhance(
  browser: Browser, 
  config: EnhanceConfig = {}
): Browser {
  // Wrap browser with performance enhancements
  const originalNewPage = browser.newPage.bind(browser);
  
  browser.newPage = async (options?) => {
    const page = await originalNewPage(options);
    
    if (config.smart_waiting?.enabled) {
      // Apply smart waiting strategies
      await page.setDefaultTimeout(
        config.smart_waiting.base_timeout || 5000
      );
    }
    
    return page;
  };
  
  return browser;
}
```

### 3.4 发布到 npm

```bash
# 1. 登录 npm（如果还没有账号，先注册: https://www.npmjs.com/signup）
npm login

# 2. 构建包
npm run build

# 3. 测试本地安装
npm pack
npm install ./playwright-enhance-0.2.0.tgz

# 4. 发布到 npm
npm publish

# 用户即可安装：
npm install playwright-enhance
```

### 3.5 支持 npx

无需额外配置，npm 发布后自动支持：

```bash
npx playwright-enhance screenshot https://example.com output.png
```

---

## 📋 发布清单（Checklist）

### ✅ 发布前准备

- [ ] **代码质量**
  - [ ] 所有测试通过（`pytest tests/`）
  - [ ] 代码覆盖率 >80%
  - [ ] 无 linter 错误（`ruff check .`）
  
- [ ] **文档完整**
  - [ ] README.md 包含清晰的安装说明
  - [ ] API 文档完整（`docs/api-reference.md`）
  - [ ] 示例代码可运行（`examples/`）
  - [ ] CHANGELOG.md 记录版本变更
  
- [ ] **包配置正确**
  - [ ] `pyproject.toml` 版本号正确
  - [ ] GitHub URLs 已更新为实际地址
  - [ ] 依赖版本范围合理
  - [ ] LICENSE 文件存在
  
- [ ] **安全检查**
  - [ ] 无敏感信息（API keys, tokens）
  - [ ] `.gitignore` 排除了临时文件
  - [ ] 依赖包无已知漏洞

### 🚀 发布步骤

#### Python (PyPI)
1. [ ] 在 TestPyPI 测试发布
2. [ ] 验证 TestPyPI 安装成功
3. [ ] 发布到正式 PyPI
4. [ ] 验证 PyPI 安装成功
5. [ ] 更新 README.md 安装说明
6. [ ] 创建 GitHub Release

#### Node.js (npm) - v0.2.0
1. [ ] TypeScript 实现完成
2. [ ] npm 包构建成功
3. [ ] 本地测试安装
4. [ ] 发布到 npm
5. [ ] 验证 npm/npx 安装
6. [ ] 更新多语言文档

---

## 🎓 最佳实践

### 语义化版本（SemVer）

遵循 [Semantic Versioning](https://semver.org/):

- **0.1.0** → 初始 Alpha 版本（当前）
- **0.2.0** → 添加 Node.js 支持（Breaking change in Alpha）
- **1.0.0** → 第一个稳定版本
- **1.1.0** → 新增功能（向后兼容）
- **1.1.1** → Bug 修复
- **2.0.0** → Breaking changes

### 版本发布节奏

```
Alpha (0.x.x)     → 每 2-4 周发布，快速迭代
Beta (1.0.0-beta) → 每 1-2 周发布，稳定测试
Stable (1.x.x)    → 每月发布小版本，每季度发布大版本
```

### CHANGELOG.md 格式

```markdown
# Changelog

All notable changes to this project will be documented in this file.

## [0.1.1] - 2024-02-28

### Added
- CLI support for `screenshot` and `pdf` commands
- Performance benchmarking tool

### Fixed
- Smart waiting timeout calculation bug
- Resource hints race condition

### Changed
- Default timeout from 5s to 8s for better compatibility

## [0.1.0] - 2024-02-20

### Added
- Initial release with Python support
- Smart waiting strategies
- CLI tool with enhanced mode
```

---

## 🔗 有用的资源

### Python 发布
- [Python Packaging Guide](https://packaging.python.org/)
- [PyPI Upload Tutorial](https://packaging.python.org/tutorials/packaging-projects/)
- [Twine Documentation](https://twine.readthedocs.io/)

### npm 发布
- [npm Publishing Guide](https://docs.npmjs.com/packages-and-modules/contributing-packages-to-the-registry)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/handbook/declaration-files/publishing.html)

### GitHub Actions
- [Publishing to PyPI](https://github.com/marketplace/actions/pypi-publish)
- [Publishing to npm](https://github.com/marketplace/actions/publish-to-npm)

### 版本管理
- [Semantic Versioning](https://semver.org/)
- [Conventional Commits](https://www.conventionalcommits.org/)

---

## 🚦 下一步行动

### 立即执行（本周）
1. ✅ 更新 `pyproject.toml` 中的 GitHub URLs
2. ✅ 创建 `CHANGELOG.md`
3. ✅ 在 TestPyPI 测试发布
4. ✅ 发布到正式 PyPI
5. ✅ 更新 README.md 安装说明

### 短期计划（1-2 周）
1. 设置 GitHub Actions 自动发布
2. 添加版本 badge 到 README
3. 创建 0.1.1 版本（bug fixes）

### 中期计划（1-2 月）
1. 开始 Node.js 版本开发（v0.2.0）
2. 完善 API 文档和示例
3. 收集社区反馈

### 长期计划（3-6 月）
1. 发布 1.0.0 稳定版本
2. 支持 Java 和 .NET
3. 建立社区贡献流程
