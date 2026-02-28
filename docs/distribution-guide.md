# Playwright-Enhance 分发和安装指南

## 📦 当前状态

**playwright-enhance** 目前还 **未发布到 PyPI**，因此 `pip install playwright-enhance` 在任意机器上**无法直接执行**。

---

## 🎯 安装要求

### 系统要求

| 要求 | 说明 |
|------|------|
| **Python 版本** | >= 3.8 (支持 3.8, 3.9, 3.10, 3.11, 3.12) |
| **操作系统** | Linux, macOS, Windows |
| **内存** | 建议 >= 2GB |
| **磁盘空间** | ~500MB (包括浏览器二进制) |

### 依赖项

```toml
dependencies = [
    "playwright>=1.40.0",          # 核心依赖
    "opencv-python-headless>=4.8.0", # 图像处理
    "pyyaml>=6.0",                 # 配置文件支持
    "click>=8.1.0",                # CLI 工具
]
```

### 浏览器要求

Playwright 需要下载浏览器二进制文件：

```bash
playwright install chromium  # ~170MB
# 或者
playwright install          # 下载所有浏览器 (~500MB)
```

---

## 🚀 当前安装方式（开发版）

### 方式一：从源码安装（推荐）

```bash
# 1. 克隆仓库
git clone https://github.com/yourusername/playwright-enhance
cd playwright-enhance

# 2. 安装包
pip install -e .

# 3. 安装浏览器
playwright install chromium

# 4. 验证安装
playwright-enhance-cli info
```

**优点**:
- ✅ 可以修改源码
- ✅ 实时生效
- ✅ 适合开发和测试

**缺点**:
- ❌ 需要 git
- ❌ 需要克隆完整仓库

---

### 方式二：从本地 wheel 文件安装

```bash
# 1. 在开发机器上构建 wheel
cd playwright-enhance
pip install build
python -m build

# 生成文件:
# dist/playwright_enhance-0.1.0-py3-none-any.whl
# dist/playwright-enhance-0.1.0.tar.gz

# 2. 复制到目标机器并安装
pip install playwright_enhance-0.1.0-py3-none-any.whl

# 3. 安装浏览器
playwright install chromium

# 4. 验证
playwright-enhance-cli info
```

**优点**:
- ✅ 无需 git
- ✅ 可以分发给团队
- ✅ 安装快速

**缺点**:
- ❌ 需要手动分发文件
- ❌ 更新需要重新构建

---

### 方式三：直接从 GitHub 安装

```bash
# 从 GitHub 直接安装（需要 git）
pip install git+https://github.com/yourusername/playwright-enhance.git

# 安装浏览器
playwright install chromium

# 验证
playwright-enhance-cli info
```

**优点**:
- ✅ 一行命令
- ✅ 总是最新版本

**缺点**:
- ❌ 需要 git
- ❌ 需要网络访问 GitHub
- ❌ 较慢（需要下载整个仓库）

---

## 📤 发布到 PyPI（推荐用于生产）

### 准备工作

1. **注册 PyPI 账号**
   - 前往 https://pypi.org/account/register/
   - 前往 https://test.pypi.org/account/register/ (测试环境)

2. **配置 API Token**
   ```bash
   # 创建 ~/.pypirc
   [pypi]
   username = __token__
   password = pypi-AgEIcHlwaS5vcmcC...  # 你的 API token
   
   [testpypi]
   username = __token__
   password = pypi-AgEIcHlwaS5vcmcC...  # 测试环境 token
   ```

---

### 发布流程

#### 步骤 1: 准备发布

```bash
# 1. 确保版本号正确
# 编辑 pyproject.toml
version = "0.1.0"

# 2. 更新 CHANGELOG.md
## [0.1.0] - 2024-02-28
### Added
- Initial release
- Smart waiting capability
- CLI tool

# 3. 运行测试
pytest --cov=playwright_enhance

# 4. 清理旧构建
rm -rf dist/ build/ *.egg-info
```

---

#### 步骤 2: 构建包

```bash
# 安装构建工具
pip install build twine

# 构建 wheel 和 sdist
python -m build

# 检查生成的文件
ls -lh dist/
# playwright_enhance-0.1.0-py3-none-any.whl
# playwright-enhance-0.1.0.tar.gz

# 验证包
twine check dist/*
```

---

#### 步骤 3: 发布到 TestPyPI（测试）

```bash
# 上传到测试环境
twine upload --repository testpypi dist/*

# 测试安装
pip install --index-url https://test.pypi.org/simple/ playwright-enhance

# 验证
playwright-enhance-cli info
```

---

#### 步骤 4: 发布到 PyPI（正式）

```bash
# 确认一切正常后，上传到正式 PyPI
twine upload dist/*

# 验证（等待几分钟索引更新）
pip install playwright-enhance

# 🎉 现在全世界都可以安装了！
```

---

## 🌍 发布后的安装方式

### 用户安装（发布到 PyPI 后）

```bash
# 1. 安装 playwright-enhance
pip install playwright-enhance

# 2. 安装浏览器
playwright install chromium

# 3. 验证
playwright-enhance-cli info

# 4. 开始使用
python
>>> from playwright_enhance import enhance
>>> # 开始编码...
```

**就这么简单！** ✨

---

## 📋 不同场景的安装方案

### 场景一：开发者（贡献代码）

```bash
git clone https://github.com/yourusername/playwright-enhance
cd playwright-enhance
pip install -e ".[dev]"
playwright install chromium
pre-commit install
```

---

### 场景二：团队内部使用（未发布到 PyPI）

#### 方案 A: 私有 PyPI 服务器

```bash
# 1. 搭建私有 PyPI (使用 devpi)
pip install devpi-server devpi-client
devpi-server --start

# 2. 上传包
devpi use http://localhost:3141
devpi upload

# 3. 团队成员安装
pip install --index-url http://your-private-pypi playwright-enhance
```

#### 方案 B: 共享 wheel 文件

```bash
# 1. 构建 wheel
python -m build

# 2. 放到共享位置（NAS/内部服务器/S3）
cp dist/*.whl /path/to/shared/storage/

# 3. 团队成员安装
pip install /path/to/shared/storage/playwright_enhance-0.1.0-py3-none-any.whl
```

#### 方案 C: 内部 Git 仓库

```bash
# 从内部 GitLab/GitHub Enterprise 安装
pip install git+https://your-internal-git.com/team/playwright-enhance.git
```

---

### 场景三：CI/CD 环境

#### GitHub Actions

```yaml
# .github/workflows/test.yml
name: Test

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      
      - name: Install dependencies
        run: |
          pip install playwright-enhance  # 发布后
          # 或者
          pip install -e .                 # 开发版
          
      - name: Install browsers
        run: playwright install chromium
      
      - name: Run tests
        run: pytest
```

#### Docker

```dockerfile
# Dockerfile
FROM python:3.10-slim

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

# 安装 playwright-enhance
RUN pip install playwright-enhance

# 安装浏览器
RUN playwright install chromium
RUN playwright install-deps chromium

# 复制代码
COPY . /app
WORKDIR /app

CMD ["python", "your_script.py"]
```

---

### 场景四：生产环境

```bash
# 1. 使用 requirements.txt
echo "playwright-enhance==0.1.0" > requirements.txt
pip install -r requirements.txt

# 2. 使用 poetry
poetry add playwright-enhance

# 3. 使用 pipenv
pipenv install playwright-enhance

# 4. 安装浏览器
playwright install chromium
```

---

## 🔒 离线安装（无网络环境）

### 准备（在有网络的机器上）

```bash
# 1. 下载所有依赖
pip download playwright-enhance -d packages/

# 2. 下载浏览器
playwright install chromium
# 浏览器位置: ~/.cache/ms-playwright/

# 3. 打包
tar -czf playwright-enhance-offline.tar.gz \
    packages/ \
    ~/.cache/ms-playwright/
```

### 安装（在离线机器上）

```bash
# 1. 解压
tar -xzf playwright-enhance-offline.tar.gz

# 2. 安装包
pip install --no-index --find-links=packages/ playwright-enhance

# 3. 复制浏览器
cp -r ms-playwright ~/.cache/

# 4. 验证
playwright-enhance-cli info
```

---

## 📊 版本管理策略

### 语义化版本

```
0.1.0-alpha  ← 当前版本（开发中）
0.1.0        ← 第一个稳定版本
0.2.0        ← 新特性（向后兼容）
1.0.0        ← 第一个正式版本
1.0.1        ← Bug 修复
1.1.0        ← 新特性（向后兼容）
2.0.0        ← 破坏性更改
```

### 发布检查清单

- [ ] 所有测试通过 (`pytest`)
- [ ] 覆盖率 >= 80% (`pytest --cov`)
- [ ] 代码格式化 (`black`, `ruff`)
- [ ] 类型检查通过 (`mypy`)
- [ ] 更新 CHANGELOG.md
- [ ] 更新版本号 (`pyproject.toml`)
- [ ] 创建 Git tag
- [ ] 构建包 (`python -m build`)
- [ ] 检查包 (`twine check dist/*`)
- [ ] 上传到 TestPyPI 测试
- [ ] 上传到 PyPI

---

## 🛠️ 常见问题

### Q1: 为什么 `pip install playwright-enhance` 失败？

**A**: 目前包还未发布到 PyPI。请使用以下方式之一：

```bash
# 方式 1: 从源码安装
git clone https://github.com/yourusername/playwright-enhance
cd playwright-enhance
pip install -e .

# 方式 2: 从 GitHub 安装
pip install git+https://github.com/yourusername/playwright-enhance.git
```

---

### Q2: `playwright install` 失败怎么办？

**A**: 常见原因：

```bash
# 1. 网络问题（使用代理）
export PLAYWRIGHT_DOWNLOAD_HOST=https://npmmirror.com/mirrors/playwright/

# 2. 权限问题
sudo playwright install chromium  # 不推荐
# 或者
playwright install chromium --with-deps  # 安装系统依赖

# 3. 磁盘空间不足
df -h  # 检查空间
# Chromium 需要 ~170MB

# 4. 使用系统浏览器（高级）
export PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1
# 然后配置使用系统已有的 Chrome
```

---

### Q3: 在 Docker 中如何使用？

**A**: 参考上面的 Dockerfile 示例，关键点：

```dockerfile
# 安装系统依赖
RUN playwright install-deps chromium

# 或者使用官方基础镜像
FROM mcr.microsoft.com/playwright/python:v1.40.0
RUN pip install playwright-enhance
```

---

### Q4: 如何更新到最新版本？

```bash
# PyPI（发布后）
pip install --upgrade playwright-enhance

# 从 GitHub
pip install --upgrade git+https://github.com/yourusername/playwright-enhance.git

# 从源码（开发版）
cd playwright-enhance
git pull
pip install -e .
```

---

### Q5: 如何卸载？

```bash
# 卸载包
pip uninstall playwright-enhance

# 可选：删除浏览器
rm -rf ~/.cache/ms-playwright/
```

---

## 🎯 推荐的分发策略

### 当前阶段（Alpha）

**推荐**: Git 仓库 + wheel 文件

```bash
# 团队内部
pip install git+https://your-internal-git/playwright-enhance.git

# 或者构建 wheel 分发
python -m build
# 分发 dist/*.whl
```

---

### Beta 阶段

**推荐**: TestPyPI

```bash
pip install --index-url https://test.pypi.org/simple/ playwright-enhance
```

---

### 正式版本（v1.0.0）

**推荐**: PyPI

```bash
pip install playwright-enhance
```

---

## 📝 下一步行动

### 发布到 PyPI 前的准备

1. **完善文档** ✅
   - [x] README.md
   - [x] API Reference
   - [x] CLI Guide
   - [ ] 完整的用户手册

2. **提高测试覆盖率**
   - 当前: 83%
   - 目标: >= 90%

3. **创建 CHANGELOG.md**
   ```bash
   touch CHANGELOG.md
   # 记录所有版本变更
   ```

4. **设置 GitHub Actions**
   - 自动运行测试
   - 自动发布到 PyPI

5. **准备示例和教程**
   - 更多实际使用案例
   - 视频教程

---

## 📚 参考资源

- **[Python Packaging User Guide](https://packaging.python.org/)** - 官方打包指南
- **[PyPI](https://pypi.org/)** - Python 包索引
- **[TestPyPI](https://test.pypi.org/)** - 测试环境
- **[Twine Documentation](https://twine.readthedocs.io/)** - 上传工具文档
- **[Semantic Versioning](https://semver.org/)** - 版本号规范

---

## 🎉 总结

### 当前状态

- ❌ **未发布到 PyPI** - `pip install playwright-enhance` 无法执行
- ✅ **可从源码安装** - `git clone` + `pip install -e .`
- ✅ **可构建 wheel** - `python -m build`

### 推荐路径

1. **现在**: 使用 `git clone` 或 wheel 文件分发
2. **Beta**: 发布到 TestPyPI 测试
3. **正式**: 发布到 PyPI，全球可用

### 关键命令

```bash
# 开发安装
git clone <repo> && cd playwright-enhance && pip install -e .

# 构建分发
python -m build

# 发布测试
twine upload --repository testpypi dist/*

# 正式发布
twine upload dist/*
```

**准备好发布时告诉我，我可以帮助您完成整个流程！** 🚀
