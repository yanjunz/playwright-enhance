## Context

OpenClaw等AI agent使用Playwright时面临严重的性能瓶颈：60-70%时间消耗在等待操作，15-20%消耗在元素定位。现有Playwright主要面向测试场景，缺乏针对AI agent高频操作、批量决策和语义理解的优化。

本设计通过wrapper模式在Playwright之上构建增强层，保持100%原生API兼容性的同时，提供6个核心capability的优化实现。目标是将整体操作速度提升3-5倍。

**技术约束**：
- 必须保持Playwright API完全兼容
- 支持Python和TypeScript两种语言
- 对OpenClaw用户零破坏性变更
- 优化特性可配置开关

## Goals / Non-Goals

**Goals:**
- 将等待时间减少50%以上（从60-70%降至30%以下）
- 将元素定位耗时减少60%以上（从15-20%降至5-8%）
- 提供AI友好的高级语义化API
- 保持100% Playwright原生API兼容性
- 支持渐进式采用，用户可选择性启用优化

**Non-Goals:**
- 不修改Playwright核心代码（通过wrapper实现）
- 不支持旧版本Playwright（仅支持1.40+）
- 不提供GUI管理界面（专注性能优化）
- 不处理浏览器引擎层面的优化（保持与上游一致）

## Decisions

### 1. 架构模式：Wrapper + Plugin

**决策**：采用透明wrapper模式 + 可选plugin架构

**理由**：
- **Wrapper模式**：拦截Playwright API调用，注入优化逻辑，对用户透明
- **Plugin架构**：各capability独立插件，用户可按需启用
- **优于Fork方案**：避免维护Playwright完整代码库，跟随上游更新更容易
- **优于Proxy方案**：直接扩展对象原型，性能开销更小

**实现方式**：
```python
# Python实现示例
from playwright.sync_api import Page as PlaywrightPage
from playwright_enhance import enhance

# 方式1：透明替换
page = enhance(browser.new_page())  # 返回增强版Page对象

# 方式2：显式配置
page = browser.new_page()
page.enable_smart_waiting()
page.enable_multi_locator()
```

### 2. 智能等待策略：自适应超时 + 页面状态预测

**决策**：基于页面负载状态动态调整超时时间

**理由**：
- 固定30秒超时在轻量级页面上浪费大量时间
- 页面加载有可预测的阶段性特征（DOMContentLoaded → networkIdle → 完全加载）
- 通过监听浏览器事件可实时感知页面状态

**技术方案**：
- 初始超时设置为5秒（而非30秒）
- 监听`domcontentloaded`, `load`, `networkidle`事件
- 根据页面复杂度（DOM节点数、网络请求数）动态调整
- 对于AI agent常访问的页面类型（表单、列表）建立超时profile

**替代方案（rejected）**：
- ❌ 机器学习预测超时时间：过度复杂，引入额外依赖
- ❌ 完全移除超时：会导致卡死问题

### 3. 多重元素定位：三层降级策略

**决策**：语义定位 → 视觉定位 → 传统DOM定位

**理由**：
- AI agent常用自然语言描述元素（"登录按钮"）
- 页面DOM结构经常变化，传统选择器脆弱
- 人类识别元素主要靠视觉特征（位置、颜色、形状）

**技术方案**：
1. **语义层**：使用accessibility tree + 元素文本内容匹配
   - 查询`aria-label`, `role`, `title`, `alt`属性
   - 模糊匹配元素内部文本（支持相似度算法）
   
2. **视觉层**：基于屏幕截图的计算机视觉识别
   - 使用OpenCV进行模板匹配
   - 缓存元素视觉特征（颜色直方图、边缘检测）
   - 仅在语义层失败时触发（避免性能开销）
   
3. **DOM层**：传统CSS/XPath选择器（fallback）

**替代方案（rejected）**：
- ❌ 仅依赖视觉识别：准确率不足，误识别风险高
- ❌ 使用AI大模型理解页面：延迟过高，成本不可控

### 4. 并发操作：操作队列 + 智能调度

**决策**：构建操作队列，识别可并发执行的操作

**理由**：
- AI agent常生成批量操作指令（如"填写表单的10个字段"）
- 许多操作之间无依赖关系，可并发执行
- 浏览器支持并发DOM操作（在不冲突的情况下）

**技术方案**：
- 用户提交操作时加入队列，不立即执行
- 分析操作依赖关系（读写冲突检测）
- 使用`Promise.all()`并发执行无依赖操作
- 对于有依赖的操作保持顺序执行

**并发安全保证**：
- 对同一元素的写操作串行化
- 页面导航操作阻塞所有其他操作
- 提供手动flush机制供用户控制

### 5. 智能缓存：多级缓存 + LRU淘汰

**决策**：三级缓存架构

**理由**：
- 元素定位结果可缓存（短期内选择器不变）
- 页面DOM快照可缓存（避免重复查询）
- 网络资源可缓存（减少重复加载）

**缓存层级**：
1. **L1 - 元素定位缓存**：
   - Key: `(url, selector)` → Value: `ElementHandle`
   - TTL: 5秒（防止DOM变化导致stale reference）
   - 自动失效：页面导航、DOM突变时清空
   
2. **L2 - 页面状态缓存**：
   - 缓存DOM树结构、accessibility tree
   - TTL: 10秒
   
3. **L3 - 资源缓存**：
   - 缓存静态资源（CSS、JS、图片）
   - 使用LRU策略，限制内存占用（默认100MB）

**缓存一致性**：
- 使用MutationObserver监听DOM变化
- 触发变化时invalidate相关缓存

### 6. AI友好API：语义化接口 + 批量操作

**决策**：在原生API之上提供高级接口

**理由**：
- Playwright原生API过于底层（需要精确选择器）
- AI agent更适合处理语义化指令
- 批量操作接口减少往返调用次数

**新增API设计**：
```python
# 语义化操作
await page.smart_click("登录按钮")  # 自动使用多重定位
await page.smart_fill("用户名输入框", "admin")

# 批量操作
await page.batch_execute([
    ("fill", "用户名", "admin"),
    ("fill", "密码", "123456"),
    ("click", "登录按钮")
])  # 内部优化为并发执行

# 上下文感知操作
await page.submit_form({
    "username": "admin",
    "password": "123456"
})  # 自动识别表单结构并填写
```

**向后兼容**：
- 保持所有原生API不变
- 新增API作为可选功能
- 通过`enable_ai_api()`显式启用

### 7. 性能监控：零侵入式追踪

**决策**：使用装饰器模式拦截所有操作，记录性能指标

**理由**：
- 了解性能瓶颈位置才能持续优化
- 轻量级监控（<2%性能开销）
- 可选启用，生产环境可关闭

**监控指标**：
- 每个操作的耗时（等待、定位、执行）
- 缓存命中率
- 并发度（同时执行的操作数）
- 失败重试次数

**输出方式**：
- 实时日志输出
- JSON格式性能报告
- 可视化面板（可选）

### 8. CLI支持：增强版命令行工具

**决策**：提供`playwright-enhance-cli`独立命令行工具，类似`playwright`原生CLI

**理由**：
- 方便快速测试和调试（无需编写代码）
- 支持脚本化自动化任务
- 为非开发用户提供低门槛入口
- 与原生`playwright`命令行保持一致的用户体验
- 独立CLI名称避免与核心库混淆，职责更清晰

**CLI功能设计**：

```bash
# 安装和初始化
playwright-enhance-cli install          # 安装浏览器（同playwright install）
playwright-enhance-cli codegen [url]    # 代码生成器（增强版，支持语义化操作）

# 执行操作（新增）
playwright-enhance-cli exec "打开百度 -> 搜索playwright -> 点击第一个结果"
playwright-enhance-cli run script.yaml  # 执行YAML格式的操作脚本

# 性能分析
playwright-enhance-cli benchmark [url]  # 对比原生vs增强版性能
playwright-enhance-cli profile script.py # 分析脚本性能瓶颈

# 配置管理
playwright-enhance-cli config set smart-waiting=true
playwright-enhance-cli config show

# 调试工具
playwright-enhance-cli inspect [url]    # 启动可视化调试器
playwright-enhance-cli cache stats      # 查看缓存统计信息
```

**YAML脚本格式**（便于AI agent生成）：
```yaml
# example.yaml
browser: chromium
headless: false
steps:
  - goto: "https://example.com"
  - smart_click: "登录按钮"
  - smart_fill: 
      field: "用户名"
      value: "admin"
  - batch_execute:
      - [fill, "密码", "123456"]
      - [click, "提交"]
```

**技术实现**：
- 基于`click`或`typer`构建CLI框架
- 复用核心增强引擎
- 支持管道操作：`echo "script" | playwright-enhance-cli exec -`
- 提供交互式REPL模式

**与playwright CLI的对比**：
| 功能 | playwright | playwright-enhance-cli |
|------|-----------|-------------------|
| 浏览器安装 | ✅ | ✅ |
| 代码生成 | ✅ 基础 | ✅ 增强（语义化） |
| 脚本执行 | ❌ | ✅ YAML/自然语言 |
| 性能分析 | ❌ | ✅ benchmark工具 |
| 批量操作 | ❌ | ✅ 支持 |

## Risks / Trade-offs

### 风险1：缓存导致stale reference错误
**影响**：缓存的ElementHandle可能因DOM变化失效
**缓解措施**：
- 设置短TTL（5秒）
- 捕获stale reference异常，自动重新定位
- 提供`page.clear_cache()`手动清理接口

### 风险2：视觉定位准确率不足
**影响**：误识别导致操作错误元素
**缓解措施**：
- 仅作为fallback策略（优先语义定位）
- 要求置信度>85%才返回结果
- 提供dry-run模式供用户验证

### 风险3：并发操作导致竞态条件
**影响**：并发写操作可能相互冲突
**缓解措施**：
- 保守的依赖分析（有疑问时串行执行）
- 对关键操作（导航、提交）强制串行
- 提供debug模式禁用并发

### 风险4：wrapper开销影响性能
**影响**：额外的拦截逻辑可能增加延迟
**缓解措施**：
- 基准测试显示wrapper开销<1ms
- 优化收益远大于开销（节省数百ms到数秒）
- 可通过配置完全禁用wrapper

### 风险5：依赖OpenCV增加安装复杂度
**影响**：视觉定位需要opencv-python依赖
**缓解措施**：
- 将视觉定位作为可选功能
- 提供纯Python fallback实现（基础图像处理）
- 预编译wheel包简化安装

### 风险6：CLI安全风险（执行任意命令）
**影响**：`playwright-enhance-cli exec`接受自然语言可能被注入恶意指令
**缓解措施**：
- 白名单机制：仅允许预定义的操作类型
- 沙箱模式：限制文件系统访问和网络请求
- 提供`--dry-run`模式预览操作
- 记录所有执行日志（审计用途）

## Migration Plan

### Phase 1: 独立包发布（v0.1.0）
- 发布`playwright-enhance` PyPI包
- 提供`playwright-enhance-cli`独立命令行工具
- 文档和示例代码
- 与OpenClaw团队合作进行集成测试

### Phase 2: 社区反馈迭代（v0.2.0 - v0.5.0）
- 收集性能指标和bug报告
- 优化算法参数（超时时间、缓存TTL等）
- 补充边缘场景处理
- 完善CLI功能（基于用户反馈）

### Phase 3: 稳定版本（v1.0.0）
- 功能冻结，专注稳定性和性能
- 完整的测试覆盖（>90%）
- 性能benchmark报告
- CLI工具成熟化

### 回滚策略
- 用户可随时切换回原生Playwright（移除enhance()调用）
- 保持向后兼容，不破坏现有代码
- 提供降级配置（逐个禁用优化特性）

## Open Questions

1. **视觉定位的准确率阈值**：需要实际测试确定合理的置信度阈值（当前设定85%）
2. **缓存内存限制**：默认100MB是否合理？需要根据典型使用场景调整
3. **TypeScript实现优先级**：先实现Python版本，还是同步开发两个语言版本？
4. **与其他AI agent框架的集成**：除了OpenClaw，是否需要适配LangChain、AutoGPT等框架？
5. **CLI自然语言解析**：使用简单规则引擎还是引入轻量级NLP模型？
6. **CLI跨平台支持**：Windows/Linux/macOS的命令行体验一致性如何保证？
5. **商业化策略**：保持完全开源，还是提供企业版增强功能？
