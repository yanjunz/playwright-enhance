# ⚡ 测试快速开始

5分钟完成全部验证！

## 🚀 一键验证（推荐）

```bash
cd /Users/yjzhuang/dev/playwright-enhance
./verify.sh
```

**输出示例**：
```
✅ 所有检查通过！项目可以发布。

📊 测试结果：56 passed in 7.76s
📈 覆盖率：397 statements, 69 missing, 83% coverage
```

---

## 📋 分步验证

### 1️⃣ 快速测试（10秒）

```bash
python -m pytest -v
# 期望: 56 passed ✅
```

### 2️⃣ 查看覆盖率（15秒）

```bash
python -m pytest --cov=playwright_enhance --cov-report=term-missing
# 期望: 83% coverage ✅
```

### 3️⃣ 运行示例（20秒）

```bash
python examples/basic_usage.py
# 期望: ✨ All examples completed! ✅
```

---

## 🎯 测试特定功能

### 配置系统

```bash
python -m pytest tests/unit/test_config.py -v
# 15个测试
```

### 包装器

```bash
python -m pytest tests/unit/test_wrapper.py -v
# 17个测试
```

### 智能等待

```bash
python -m pytest tests/unit/test_smart_waiting.py -v
# 18个测试
```

### 兼容性

```bash
python -m pytest tests/integration/test_compatibility.py -v
# 6个测试（需要Playwright浏览器）
```

---

## 📊 当前测试状态

| 类型 | 数量 | 状态 |
|------|------|------|
| 单元测试 | 50 | ✅ 全部通过 |
| 集成测试 | 6 | ✅ 全部通过 |
| 示例测试 | 5 | ✅ 全部通过 |
| **总计** | **56** | **✅ 100%** |

**覆盖率**: 83% (397 statements, 69 missing)

---

## 🐛 测试失败？

### 查看详细错误

```bash
python -m pytest -v --tb=long
```

### 调试单个测试

```bash
python -m pytest tests/unit/test_wrapper.py::TestEnhancedPage::test_async_method_proxy -v -s
```

### 进入调试器

```bash
python -m pytest --pdb
```

---

## ✅ 验证清单

完成所有检查后可以发布：

- [x] 所有测试通过 (56/56) ✅
- [x] 覆盖率 >80% (83%) ✅
- [x] 示例运行成功 (5/5) ✅
- [x] 无严重lint错误 ✅
- [ ] 代码格式化 (可选)
- [ ] 类型检查 (可选)
- [ ] 性能基准 (TODO)

---

## 📚 详细文档

完整测试指南：[docs/testing.md](docs/testing.md)

---

## 🎯 快速命令参考

```bash
# 运行所有测试
pytest -v

# 带覆盖率
pytest --cov=playwright_enhance --cov-report=html

# 只运行失败的
pytest --lf

# 运行示例
python examples/basic_usage.py

# 一键验证
./verify.sh

# 查看HTML报告
open htmlcov/index.html  # macOS
```

---

**当前状态**: ✅ **所有测试通过，可以使用！**

**时间**: 完整验证 < 30秒  
**结果**: 56/56 测试通过，83%覆盖率
