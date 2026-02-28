# Publishing Checklist - 发布前检查清单

使用这个清单确保顺利发布到 PyPI。

---

## 📋 Phase 1: 发布前准备

### ✅ 代码质量

- [ ] **运行所有测试**
  ```bash
  pytest tests/ -v
  ```
  预期：56 passing, 83% coverage

- [ ] **代码格式检查**
  ```bash
  ruff check .
  black --check .
  ```
  预期：无错误

- [ ] **类型检查**
  ```bash
  mypy playwright_enhance/
  ```
  预期：无类型错误

- [ ] **安全扫描**
  ```bash
  pip install safety
  safety check
  ```
  预期：无已知漏洞

### ✅ 文档完整性

- [ ] **README.md 检查**
  - [ ] 安装说明清晰（GitHub 安装）
  - [ ] 示例代码可运行
  - [ ] 所有链接有效
  - [ ] Badge 显示正确

- [ ] **API 文档完整**
  - [ ] `docs/api-reference.md` 更新
  - [ ] `docs/cli-guide.md` 准确
  - [ ] `docs/performance.md` 有最新数据

- [ ] **CHANGELOG.md 更新**
  - [ ] 记录了所有新功能
  - [ ] 列出了 Breaking Changes
  - [ ] 版本号正确
  - [ ] 日期准确

- [ ] **示例代码测试**
  ```bash
  python examples/real_hackernews_test.py
  ```
  预期：成功运行

### ✅ 包配置

- [ ] **pyproject.toml 检查**
  - [ ] 版本号正确（`version = "0.1.0"`）
  - [ ] GitHub URLs 更新（`https://github.com/yanjunz/playwright-enhance`）
  - [ ] 依赖版本合理
  - [ ] Classifiers 准确

- [ ] **LICENSE 文件**
  - [ ] 存在且是 MIT License
  - [ ] 年份和作者正确

- [ ] **.gitignore 完整**
  - [ ] 排除 `dist/`, `build/`, `*.egg-info`
  - [ ] 排除 `__pycache__/`, `*.pyc`
  - [ ] 排除 `.pytest_cache/`, `htmlcov/`

### ✅ Git 状态

- [ ] **提交所有更改**
  ```bash
  git status
  ```
  预期：working tree clean

- [ ] **推送到 GitHub**
  ```bash
  git push origin master
  ```

- [ ] **检查 GitHub Actions**
  - 访问：https://github.com/yanjunz/playwright-enhance/actions
  - 预期：Tests 通过

---

## 🧪 Phase 2: TestPyPI 测试

### ✅ 构建和上传

- [ ] **清理旧构建**
  ```bash
  rm -rf dist/ build/ *.egg-info
  ```

- [ ] **构建包**
  ```bash
  python -m build
  ```
  预期：生成 `.whl` 和 `.tar.gz`

- [ ] **检查包**
  ```bash
  twine check dist/*
  ```
  预期：Checking distribution... PASSED

- [ ] **上传到 TestPyPI**
  ```bash
  ./scripts/publish_testpypi.sh
  ```
  或手动：
  ```bash
  twine upload --repository testpypi dist/*
  ```

### ✅ TestPyPI 验证

- [ ] **访问 TestPyPI 页面**
  - URL: https://test.pypi.org/project/playwright-enhance/
  - 检查：版本号、描述、链接

- [ ] **测试安装**
  ```bash
  # 在新的虚拟环境中
  python3 -m venv test_env
  source test_env/bin/activate
  pip install --index-url https://test.pypi.org/simple/ playwright-enhance
  ```

- [ ] **测试导入**
  ```bash
  python -c "from playwright_enhance import enhance; print('✅ OK')"
  ```

- [ ] **测试 CLI**
  ```bash
  playwright-enhance-cli --help
  ```

- [ ] **清理测试环境**
  ```bash
  deactivate
  rm -rf test_env
  ```

---

## 🚀 Phase 3: 正式发布到 PyPI

### ✅ 发布前最终检查

- [ ] **确认版本号**
  ```bash
  grep '^version = ' pyproject.toml
  ```
  当前应该是：`version = "0.1.0"`

- [ ] **创建 Git Tag**
  ```bash
  git tag -a v0.1.0 -m "Release v0.1.0 - Initial Alpha Release"
  git push origin v0.1.0
  ```

- [ ] **确认 TestPyPI 测试通过**
  - 回顾 Phase 2 的所有检查项

### ✅ 发布到 PyPI

- [ ] **运行发布脚本**
  ```bash
  ./scripts/publish_pypi.sh
  ```
  
  或手动：
  ```bash
  # 构建
  python -m build
  
  # 检查
  twine check dist/*
  
  # 上传
  twine upload dist/*
  ```

- [ ] **输入 PyPI API Token**
  - Username: `__token__`
  - Password: 你的 PyPI API Token
  - 获取 Token: https://pypi.org/manage/account/token/

### ✅ 发布后验证

- [ ] **访问 PyPI 页面**
  - URL: https://pypi.org/project/playwright-enhance/
  - 检查：版本、描述、README 渲染正确

- [ ] **测试全球安装**
  ```bash
  # 在新虚拟环境中
  python3 -m venv prod_test
  source prod_test/bin/activate
  
  # 等待 PyPI 同步（约 1-5 分钟）
  pip install playwright-enhance
  playwright install chromium
  
  # 运行示例
  python -c "
  from playwright.sync_api import sync_playwright
  from playwright_enhance import enhance
  
  with sync_playwright() as p:
      browser = p.chromium.launch()
      enhanced = enhance(browser)
      page = enhanced.new_page()
      page.goto('https://example.com')
      print(f'✅ Title: {page.title()}')
      browser.close()
  "
  
  deactivate
  rm -rf prod_test
  ```

---

## 📢 Phase 4: 发布宣传

### ✅ 更新 README

- [ ] **更新安装说明**
  ```bash
  # 修改 README.md
  ```
  
  更新为：
  ```markdown
  ### Installation
  
  ```bash
  # Install from PyPI
  pip install playwright-enhance
  
  # Install browser binaries
  playwright install chromium
  ```
  
  Or install from GitHub for latest development version:
  ```bash
  pip install git+https://github.com/yanjunz/playwright-enhance.git
  ```
  ```

- [ ] **添加 PyPI Badge**
  ```markdown
  [![PyPI](https://img.shields.io/pypi/v/playwright-enhance)](https://pypi.org/project/playwright-enhance/)
  [![Downloads](https://img.shields.io/pypi/dm/playwright-enhance)](https://pypi.org/project/playwright-enhance/)
  ```

- [ ] **提交更新**
  ```bash
  git add README.md
  git commit -m "docs: update installation to use PyPI"
  git push origin master
  ```

### ✅ GitHub Release

- [ ] **创建 GitHub Release**
  - 访问：https://github.com/yanjunz/playwright-enhance/releases/new
  - Tag: `v0.1.0`
  - Title: `Release v0.1.0 - Initial Alpha Release`
  - Description: 复制 CHANGELOG.md 内容

- [ ] **附加资产**
  - [ ] 上传 `.whl` 文件（可选）
  - [ ] 上传 `.tar.gz` 文件（可选）

### ✅ 社区宣传

- [ ] **社交媒体**
  - [ ] Twitter/X 发推
  - [ ] LinkedIn 分享
  - [ ] Reddit (r/Python, r/playwright)

- [ ] **开发者社区**
  - [ ] Dev.to 文章
  - [ ] Hacker News (Show HN)
  - [ ] Python Weekly

- [ ] **Playwright 社区**
  - [ ] Playwright Discord
  - [ ] Playwright GitHub Discussions

示例推文：
```
🚀 Introducing playwright-enhance v0.1.0!

Make Playwright 40-50% faster with smart waiting strategies.

✨ Features:
- Adaptive timeouts (no more 30s waits!)
- 100% Playwright API compatible
- CLI tool included

pip install playwright-enhance

https://github.com/yanjunz/playwright-enhance
```

---

## 🔄 Phase 5: 配置自动化

### ✅ GitHub Actions

- [ ] **添加 PyPI API Token 到 GitHub Secrets**
  - 访问：https://github.com/yanjunz/playwright-enhance/settings/secrets/actions
  - 添加：`PYPI_API_TOKEN`（你的 PyPI Token）

- [ ] **测试自动发布**
  - 创建新 release 时应自动触发
  - 检查：https://github.com/yanjunz/playwright-enhance/actions

### ✅ 设置 Webhooks（可选）

- [ ] **PyPI → Discord/Slack**
  - 新版本发布时通知团队

- [ ] **GitHub → 项目管理工具**
  - Release 时更新看板

---

## 📊 Phase 6: 监控和反馈

### ✅ 第一周检查

- [ ] **下载量统计**
  - 访问：https://pypistats.org/packages/playwright-enhance

- [ ] **GitHub Issues 跟踪**
  - 及时回复用户问题
  - 标记 bug 和 feature requests

- [ ] **收集反馈**
  - 社区反馈
  - 用户使用场景

### ✅ 第一月检查

- [ ] **规划 v0.1.1**
  - 修复发现的 bugs
  - 小功能改进

- [ ] **文档改进**
  - 根据用户反馈完善文档
  - 添加更多示例

---

## 🎯 常见问题

### Q: 如果发布后发现 bug 怎么办？

**立即修复发布新版本：**
```bash
# 1. 修复 bug
# 2. 更新版本号到 0.1.1
# 3. 更新 CHANGELOG.md
git add .
git commit -m "fix: critical bug in smart waiting"
git tag v0.1.1
git push origin master v0.1.1

# 4. 重新发布
./scripts/publish_pypi.sh
```

### Q: 可以删除已发布的版本吗？

**不能！** PyPI 不允许删除或替换已发布的版本。只能：
1. Yank（隐藏）该版本
2. 发布新版本

### Q: 如何回滚到旧版本？

用户可以指定版本安装：
```bash
pip install playwright-enhance==0.1.0
```

---

## ✅ 完成标志

当所有以上检查项都完成后：

- ✅ 包已成功发布到 PyPI
- ✅ 用户可以通过 `pip install playwright-enhance` 安装
- ✅ GitHub Release 已创建
- ✅ 文档已更新
- ✅ 社区已宣传

**🎉 恭喜！你的包现在可以像 Playwright 一样方便地使用了！**

---

## 📝 下次发布提醒

保存这个清单，每次发布新版本时都使用。

建议频率：
- **Bug 修复（0.1.x）** - 按需发布，通常每 1-2 周
- **小功能（0.x.0）** - 每月一次
- **大版本（1.0.0）** - 充分测试后发布
