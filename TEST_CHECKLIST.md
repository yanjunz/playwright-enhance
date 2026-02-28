# ✅ Production Testing Checklist - 正式版本测试清单

**快速检查已发布版本是否正常工作**

---

## 📊 当前状态

⚠️ **PyPI 尚未发布** - 包目前只能从 GitHub 安装

---

## 🚀 测试当前版本（GitHub）

### 一键测试（推荐）

```bash
# 测试 GitHub 安装版本
./scripts/test_github_install.sh
```

**包含测试**：
- ✅ GitHub 安装验证
- ✅ 导入测试
- ✅ 基本功能测试
- ✅ CLI 工具测试

---

## 🔜 等 PyPI 发布后

### 一键测试 PyPI 版本

```bash
# 方式 1: 完整测试套件（6个测试，约2分钟）
./scripts/test_production.sh

# 方式 2: 快速测试（基础功能，约30秒）
./scripts/test_pypi_package.sh

# 方式 3: 真实网站测试（4个网站，约3分钟）
./scripts/test_real_websites.sh

# 方式 4: 多 Python 版本测试（5分钟）
./scripts/test_all_platforms.sh
```

---

## ✋ 手动测试（5分钟）

### Step 1: 安装测试
```bash
# 新建虚拟环境
python3 -m venv test_pypi
source test_pypi/bin/activate

# 从 PyPI 安装
pip install playwright-enhance
playwright install chromium

# 检查版本
pip show playwright-enhance
```

### Step 2: 导入测试
```bash
python3 -c "
from playwright_enhance import enhance
from playwright_enhance.config import Config
print('✅ Import OK')
"
```

### Step 3: 功能测试
```bash
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
```

### Step 4: CLI 测试
```bash
# 帮助命令
playwright-enhance-cli --help

# 截图测试
playwright-enhance-cli screenshot https://example.com test.png --enhanced
ls -lh test.png
```

### Step 5: 清理
```bash
deactivate
rm -rf test_pypi test.png
```

---

## 📋 验证清单

### 基础功能
- [ ] 能从 PyPI 正常安装
- [ ] 导入成功，无报错
- [ ] 同步 API 工作正常
- [ ] 异步 API 工作正常
- [ ] CLI 命令可用

### 性能验证
- [ ] 页面加载速度有提升
- [ ] 没有额外的错误
- [ ] 超时设置生效

### 兼容性
- [ ] Python 3.8+ 兼容
- [ ] 与 Playwright 原生 API 兼容
- [ ] 真实网站测试通过

---

## 🎯 预期结果

### 完整测试套件输出
```
🎉 All Tests PASSED!

📊 Test Summary:
   ✅ Test 1: Import test
   ✅ Test 2: Sync API test
   ✅ Test 3: Async API test
   ✅ Test 4: CLI tool test
   ✅ Test 5: Configuration test
   ✅ Test 6: Performance check

✅ playwright-enhance v0.1.0 is working correctly!
```

### 性能提升
- 页面加载速度：**40-50% 更快**
- 操作超时：**60-70% 减少等待**

---

## 🐛 如果测试失败

### 安装失败
```bash
# 等待几分钟（PyPI 同步）后重试
pip install --upgrade pip
pip install playwright-enhance
```

### 导入失败
```bash
# 检查安装
pip list | grep playwright

# 重新安装
pip uninstall playwright-enhance
pip install playwright-enhance
```

### 性能没提升
```python
# 确保启用了增强模式
enhanced = enhance(browser, {
    'smart_waiting': {'enabled': True}
})
```

---

## 📊 测试报告模板

```markdown
## Test Report - v0.1.0

Date: 2024-02-28
Python: 3.11.5
OS: macOS

### Results
- ✅ Installation: PASS
- ✅ Import: PASS
- ✅ Sync API: PASS
- ✅ Async API: PASS
- ✅ CLI Tool: PASS
- ✅ Performance: 45% improvement

### Conclusion
All tests passed. Package ready for use.
```

---

## 🔗 详细文档

更多测试信息请查看：
- **[TESTING_PRODUCTION.md](TESTING_PRODUCTION.md)** - 完整测试指南

---

**开始测试：运行 `./scripts/test_production.sh`** 🚀
