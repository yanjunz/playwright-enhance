# 🚀 Quick Start: Publish to PyPI

**5 分钟让用户可以 `pip install playwright-enhance`！**

---

## 🎯 目标

从当前状态（仅 GitHub 安装）→ 发布到 PyPI（全球 pip 安装）

---

## ✅ 前置要求

1. **PyPI 账号**
   - 注册：https://pypi.org/account/register/
   - 创建 API Token：https://pypi.org/manage/account/token/
   - 保存 Token（只显示一次！）

2. **TestPyPI 账号**（测试用）
   - 注册：https://test.pypi.org/account/register/
   - 创建 API Token：https://test.pypi.org/manage/account/token/

3. **本地环境**
   ```bash
   pip install build twine
   ```

---

## 🧪 Step 1: 测试发布到 TestPyPI（5 分钟）

### 1.1 运行测试
```bash
# 确保代码没问题
pytest tests/ -v
```

### 1.2 构建包
```bash
# 清理旧构建
rm -rf dist/ build/ *.egg-info

# 构建
python -m build

# 检查
twine check dist/*
```

### 1.3 上传到 TestPyPI
```bash
# 方式 1: 使用脚本（推荐）
./scripts/publish_testpypi.sh

# 方式 2: 手动上传
twine upload --repository testpypi dist/*
# Username: __token__
# Password: 粘贴你的 TestPyPI API Token
```

### 1.4 验证安装
```bash
# 新建虚拟环境测试
python3 -m venv test_env
source test_env/bin/activate

# 从 TestPyPI 安装
pip install --index-url https://test.pypi.org/simple/ playwright-enhance

# 测试导入
python -c "from playwright_enhance import enhance; print('✅ 成功!')"

# 清理
deactivate
rm -rf test_env
```

**✅ 如果测试通过，继续下一步！**

---

## 🚀 Step 2: 发布到 PyPI（2 分钟）

### 2.1 创建 Git Tag
```bash
# 确保代码已提交
git status  # 应该是 clean

# 创建版本标签
git tag -a v0.1.0 -m "Release v0.1.0 - Initial Alpha"
git push origin v0.1.0
```

### 2.2 发布到 PyPI
```bash
# 方式 1: 使用脚本（推荐，有安全检查）
./scripts/publish_pypi.sh

# 方式 2: 手动发布
python -m build
twine upload dist/*
# Username: __token__
# Password: 粘贴你的 PyPI API Token
```

### 2.3 等待 PyPI 同步
```bash
# 等待 1-5 分钟，然后测试
pip install playwright-enhance

# 成功！🎉
```

---

## 📢 Step 3: 更新文档（2 分钟）

### 3.1 更新 README.md
```bash
# 将安装说明改为：
### Installation

pip install playwright-enhance
playwright install chromium
```

### 3.2 创建 GitHub Release
访问：https://github.com/yanjunz/playwright-enhance/releases/new

- **Tag**: `v0.1.0`
- **Title**: `Release v0.1.0 - Initial Alpha Release`
- **Description**: 复制 `CHANGELOG.md` 内容

---

## 🎉 完成！

现在用户可以像使用 Playwright 一样方便地安装：

```bash
pip install playwright-enhance
```

---

## 🔍 验证成功

访问以下链接确认发布成功：

1. **PyPI 页面**: https://pypi.org/project/playwright-enhance/
2. **PyPI 统计**: https://pypistats.org/packages/playwright-enhance
3. **GitHub Release**: https://github.com/yanjunz/playwright-enhance/releases

---

## 🐛 如果出错怎么办？

### 错误 1: "Package name already exists"
- **原因**: 包名被占用
- **解决**: 更改 `pyproject.toml` 中的包名

### 错误 2: "Invalid credentials"
- **原因**: API Token 错误
- **解决**: 重新生成 Token，确保复制完整

### 错误 3: "File already exists"
- **原因**: 该版本已上传
- **解决**: 更新版本号（PyPI 不允许覆盖）

### 错误 4: README 渲染错误
- **原因**: Markdown 语法问题
- **解决**: 检查并修复 README.md，发布新版本

---

## 📋 下次发布（v0.1.1）

1. 修改 `pyproject.toml`: `version = "0.1.1"`
2. 更新 `CHANGELOG.md`
3. 运行 `./scripts/publish_pypi.sh`
4. 创建新的 GitHub Release

---

## 💡 提示

- **首次发布紧张？** 先在 TestPyPI 多练习几次
- **版本号规则**: 遵循 [Semantic Versioning](https://semver.org/)
- **发布频率**: Bug 修复随时发布，新功能每月一次

---

## 🔗 有用的资源

- [Python Packaging Guide](https://packaging.python.org/)
- [Twine Documentation](https://twine.readthedocs.io/)
- [完整发布清单](PUBLISHING_CHECKLIST.md)
- [详细发布指南](docs/publishing-guide.md)

---

**准备好了吗？运行 `./scripts/publish_testpypi.sh` 开始吧！** 🚀
