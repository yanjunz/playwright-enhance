# 🧪 如何测试当前版本

**当前状态**: PyPI 尚未发布，可以从 GitHub 测试

---

## ⚠️ 重要说明

包**还没有发布到 PyPI**，所以：
- ❌ `pip install playwright-enhance` - 不可用
- ✅ `pip install git+https://github.com/...` - 可用

---

## 🚀 立即测试（2种方式）

### 方式 1: 一键测试脚本（推荐）

```bash
./scripts/test_github_install.sh
```

**测试内容**：
- ✅ 从 GitHub 安装
- ✅ 导入测试
- ✅ 基本功能测试
- ✅ CLI 工具测试

**预期输出**：
```
🎉 All Tests PASSED!

📊 Test Summary:
   ✅ Test 1: Import test
   ✅ Test 2: Basic functionality
   ✅ Test 3: CLI tool

✅ GitHub installation verified!
```

### 方式 2: 手动测试（3分钟）

```bash
# 1. 创建测试环境
python3 -m venv test_env
source test_env/bin/activate

# 2. 从 GitHub 安装
pip install git+https://github.com/yanjunz/playwright-enhance.git
playwright install chromium

# 3. 测试功能
python3 << 'EOF'
from playwright.sync_api import sync_playwright
from playwright_enhance import enhance

with sync_playwright() as p:
    browser = p.chromium.launch()
    enhanced = enhance(browser)
    page = enhanced.new_page()
    page.goto('https://example.com')
    print(f'✅ Title: {page.title()}')
    browser.close()
EOF

# 4. 测试 CLI
playwright-enhance-cli --help
playwright-enhance-cli screenshot https://example.com test.png --enhanced

# 5. 清理
deactivate
rm -rf test_env test.png
```

---

## 📦 发布到 PyPI 后

完成 PyPI 发布后，可以运行这些测试：

```bash
# 完整测试套件
./scripts/test_production.sh

# 快速测试
./scripts/test_pypi_package.sh

# 真实网站测试
./scripts/test_real_websites.sh
```

---

## 🎯 如何发布到 PyPI

查看详细指南：

1. **[QUICKSTART_PUBLISH.md](QUICKSTART_PUBLISH.md)** - 5分钟发布指南
2. **[PUBLISHING_CHECKLIST.md](PUBLISHING_CHECKLIST.md)** - 完整检查清单

**快速流程**：
```bash
# 1. 测试发布
./scripts/publish_testpypi.sh

# 2. 正式发布
git tag -a v0.1.0 -m "Release v0.1.0"
git push origin v0.1.0
./scripts/publish_pypi.sh

# 3. 验证
pip install playwright-enhance  # 等待1-5分钟后可用
```

---

## 📊 当前项目状态

查看：**[CURRENT_STATUS.md](CURRENT_STATUS.md)**

- ✅ 代码完成
- ✅ 测试通过（56个，83%覆盖）
- ✅ 文档完整
- ✅ GitHub 公开
- ⏳ PyPI 发布（待完成）

---

## 🔗 有用的链接

- **GitHub 仓库**: https://github.com/yanjunz/playwright-enhance
- **当前状态**: [CURRENT_STATUS.md](CURRENT_STATUS.md)
- **发布指南**: [QUICKSTART_PUBLISH.md](QUICKSTART_PUBLISH.md)
- **测试指南**: [TESTING_PRODUCTION.md](TESTING_PRODUCTION.md)

---

**现在就测试**: `./scripts/test_github_install.sh` 🚀
