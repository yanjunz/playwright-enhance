# 🧪 Testing Production Release - 测试正式版本

发布到 PyPI 后，使用这些测试来验证正式版本是否正常工作。

---

## 🎯 测试目标

确保用户从 PyPI 安装的版本能够：
1. ✅ 正确安装（依赖完整）
2. ✅ 导入成功（所有模块可用）
3. ✅ 功能正常（API 工作正常）
4. ✅ 性能优化有效（速度提升明显）
5. ✅ CLI 工具可用
6. ✅ 真实网站测试通过

---

## 🚀 快速测试（2分钟）

### 方式 1: 一键完整测试（推荐）

```bash
# 运行完整测试套件（6个测试）
./scripts/test_production.sh
```

**包含的测试：**
- ✅ 导入测试
- ✅ 同步 API 测试
- ✅ 异步 API 测试
- ✅ CLI 工具测试
- ✅ 配置测试
- ✅ 性能检查

**预期输出：**
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

### 方式 2: 快速基础测试

```bash
# 快速测试安装和基本功能
./scripts/test_pypi_package.sh
```

**适用场景：** 快速验证包能否安装和运行

---

## 🌐 真实网站测试（3分钟）

测试在真实网站上的表现：

```bash
# 测试 4 个真实网站
./scripts/test_real_websites.sh
```

**测试的网站：**
- example.com
- Hacker News
- GitHub
- Wikipedia

**验证内容：**
- 页面加载成功
- 标题正确
- 性能提升明显

---

## 🐍 多 Python 版本测试（5分钟）

确保兼容 Python 3.8-3.12：

```bash
# 测试所有 Python 版本
./scripts/test_all_platforms.sh
```

**测试版本：**
- Python 3.8
- Python 3.9
- Python 3.10
- Python 3.11
- Python 3.12

---

## ✋ 手动测试

### 1. 安装测试

在**全新的环境**中测试：

```bash
# 创建新虚拟环境
python3 -m venv test_env
source test_env/bin/activate

# 从 PyPI 安装
pip install playwright-enhance

# 安装浏览器
playwright install chromium

# 检查版本
pip show playwright-enhance
```

### 2. 导入测试

```bash
python3 -c "
from playwright_enhance import enhance
from playwright_enhance.config import Config
print('✅ Import successful')
"
```

### 3. 同步 API 测试

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

### 4. 异步 API 测试

```bash
python3 << 'EOF'
import asyncio
from playwright.async_api import async_playwright
from playwright_enhance import enhance

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        enhanced = enhance(browser)
        
        page = await enhanced.new_page()
        await page.goto('https://example.com')
        
        title = await page.title()
        print(f'✅ Title: {title}')
        
        await browser.close()

asyncio.run(main())
EOF
```

### 5. CLI 工具测试

```bash
# 测试 help
playwright-enhance-cli --help

# 测试截图
playwright-enhance-cli screenshot https://example.com test.png --enhanced

# 验证文件
ls -lh test.png
```

### 6. 性能对比测试

```bash
python3 << 'EOF'
import time
from playwright.sync_api import sync_playwright
from playwright_enhance import enhance

# 测试标准 Playwright
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    
    start = time.time()
    page.goto('https://example.com')
    standard_time = time.time() - start
    
    browser.close()

# 测试增强版
with sync_playwright() as p:
    browser = p.chromium.launch()
    enhanced = enhance(browser)
    page = enhanced.new_page()
    
    start = time.time()
    page.goto('https://example.com')
    enhanced_time = time.time() - start
    
    browser.close()

print(f'Standard Playwright: {standard_time:.2f}s')
print(f'Playwright-Enhance: {enhanced_time:.2f}s')
print(f'Improvement: {((standard_time - enhanced_time) / standard_time * 100):.1f}%')
EOF
```

---

## 🔍 验证清单

### ✅ 安装验证

- [ ] 能从 PyPI 正常安装
- [ ] 无依赖冲突错误
- [ ] 浏览器安装成功
- [ ] 版本号正确

### ✅ 功能验证

- [ ] 能正常导入所有模块
- [ ] 同步 API 工作正常
- [ ] 异步 API 工作正常
- [ ] CLI 命令可用
- [ ] 配置系统正常

### ✅ 性能验证

- [ ] 页面加载速度提升 40-50%
- [ ] 自适应超时工作正常
- [ ] 没有额外的错误或警告

### ✅ 兼容性验证

- [ ] Python 3.8+ 都能正常运行
- [ ] 在 Linux/macOS/Windows 上都能用
- [ ] 与现有 Playwright 脚本兼容

---

## 📊 测试报告模板

完成测试后，可以用这个模板记录结果：

```markdown
## Test Report - playwright-enhance v0.1.0

### Environment
- OS: macOS 14.0
- Python: 3.11.5
- Install method: pip install playwright-enhance
- Date: 2024-02-28

### Test Results

| Test | Status | Time | Notes |
|------|--------|------|-------|
| Installation | ✅ PASS | 15s | No issues |
| Import | ✅ PASS | 0.1s | All modules OK |
| Sync API | ✅ PASS | 3.2s | Works correctly |
| Async API | ✅ PASS | 3.1s | Works correctly |
| CLI Tool | ✅ PASS | 5.0s | All commands OK |
| Performance | ✅ PASS | - | 45% improvement |
| Real Websites | ✅ PASS | 20s | 4/4 sites OK |

### Performance Comparison
- Standard Playwright: 5.2s
- Playwright-Enhance: 2.8s
- Improvement: 46%

### Issues Found
None

### Conclusion
✅ All tests passed. Package is ready for production use.
```

---

## 🐛 常见问题

### Q1: 安装失败 "No matching distribution found"

**原因：** PyPI 还没同步或版本不存在

**解决：**
```bash
# 等待几分钟后重试
pip install --upgrade pip
pip install playwright-enhance
```

### Q2: 浏览器安装失败

**原因：** playwright 未正确安装

**解决：**
```bash
pip install --upgrade playwright
playwright install chromium
```

### Q3: Import 错误 "No module named 'playwright_enhance'"

**原因：** 虚拟环境问题

**解决：**
```bash
# 确认安装在正确的环境
which python
pip list | grep playwright-enhance

# 重新安装
pip uninstall playwright-enhance
pip install playwright-enhance
```

### Q4: 性能没有提升

**原因：** 未启用增强模式

**解决：**
```python
# 确保使用 enhance() 包装
from playwright_enhance import enhance

enhanced = enhance(browser, {
    'smart_waiting': {'enabled': True}  # 必须启用
})
```

### Q5: CLI 命令找不到

**原因：** PATH 配置问题

**解决：**
```bash
# 检查安装位置
pip show -f playwright-enhance | grep playwright-enhance-cli

# 使用完整路径
python -m playwright_enhance.cli.main --help
```

---

## 🔧 调试技巧

### 启用详细输出

```python
import logging
logging.basicConfig(level=logging.DEBUG)

from playwright_enhance import enhance
# 会输出详细的调试信息
```

### 检查安装文件

```bash
# 查看安装的文件
pip show -f playwright-enhance

# 检查版本
python -c "import playwright_enhance; print(playwright_enhance.__version__)"
```

### 比较本地和 PyPI 版本

```bash
# 本地版本
cd /path/to/playwright-enhance
python -c "from playwright_enhance import enhance; print('Local OK')"

# PyPI 版本
python -m venv test_pypi
source test_pypi/bin/activate
pip install playwright-enhance
python -c "from playwright_enhance import enhance; print('PyPI OK')"
```

---

## 📈 性能基准测试

运行完整的性能基准测试：

```bash
# 在 PyPI 安装的版本上运行
python3 << 'EOF'
import time
import statistics
from playwright.sync_api import sync_playwright
from playwright_enhance import enhance

urls = [
    'https://example.com',
    'https://news.ycombinator.com',
    'https://github.com',
]

results = []

for url in urls:
    print(f'\nTesting {url}...')
    times = []
    
    for _ in range(3):
        with sync_playwright() as p:
            browser = p.chromium.launch()
            enhanced = enhance(browser)
            page = enhanced.new_page()
            
            start = time.time()
            page.goto(url, wait_until='domcontentloaded')
            elapsed = time.time() - start
            times.append(elapsed)
            
            browser.close()
    
    avg_time = statistics.mean(times)
    print(f'  Average: {avg_time:.2f}s')
    results.append((url, avg_time))

print('\n' + '='*50)
print('Summary:')
for url, avg_time in results:
    print(f'{url}: {avg_time:.2f}s')
EOF
```

---

## 🎯 下一步

测试通过后：

1. **更新文档**
   - README.md 添加 PyPI 安装说明
   - 更新版本 badge

2. **监控使用**
   - 查看 PyPI 下载量
   - 关注 GitHub Issues

3. **收集反馈**
   - 用户使用场景
   - 性能数据
   - Bug 报告

4. **规划下一版本**
   - 修复发现的问题
   - 添加新功能

---

## 🔗 相关资源

- **PyPI 页面**: https://pypi.org/project/playwright-enhance/
- **下载统计**: https://pypistats.org/packages/playwright-enhance
- **GitHub Issues**: https://github.com/yanjunz/playwright-enhance/issues
- **文档**: https://github.com/yanjunz/playwright-enhance/blob/master/docs/

---

## ✅ 测试完成标志

当所有以下检查项都通过时，版本就是稳定可用的：

- ✅ 自动化测试全部通过
- ✅ 手动测试功能正常
- ✅ 真实网站测试成功
- ✅ 性能提升达到预期
- ✅ 多 Python 版本兼容
- ✅ CLI 工具正常工作
- ✅ 无严重 Bug 或错误

**恭喜！你的包已经可以安全地供用户使用了！** 🎉
