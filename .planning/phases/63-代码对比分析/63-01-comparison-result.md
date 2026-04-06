# Phase 63-01: v0.4.0 vs 当前版本配置对比结果

**生成时间:** 2026-04-06
**对比范围:** v0.4.0 tag vs HEAD (main branch)
**核心文件:** `backend/core/agent_service.py`
**浏览器库版本:** browser-use 0.12.2（v0.4.0 与当前版本相同，无变化）

---

## run_simple 方法对比 (D-01)

| 配置项 | v0.4.0 值 | 当前值 | 变更提交 |
|--------|-----------|--------|----------|
| Agent class | `Agent` | `Agent` | -- (未变) |
| task | `task` | `task` | -- (未变) |
| llm | `create_llm(config)` | `create_llm(config)` | -- (未变) |
| browser_session | `None (未传递)` | `create_browser_session()` | f951791 |
| max_actions_per_step | `5` | `5` | -- (未变) |
| **Headless 模式** | **Auto-detect (macOS 下为 headed)** | **显式 True** | **f951791** |
| Chrome args | `None (browser-use 默认)` | `6 个 SERVER_BROWSER_ARGS + --headless=new` | f951791 + browser-use 内部 |
| Viewport | `None (自动)` | `1920x1080` | c84f4e1 |

**v0.4.0 代码片段:**
```python
agent = Agent(
    task=task,
    llm=llm,
    max_actions_per_step=5,
)
# browser-use 默认: headless=None -> auto-detect -> macOS headed, Linux server headless
```

**当前代码片段:**
```python
browser_session = create_browser_session()  # BrowserProfile(headless=True, ...)
agent = Agent(
    task=task,
    llm=llm,
    browser_session=browser_session,
    max_actions_per_step=5,
)
```

---

## run_with_streaming 方法对比 (D-01)

| 配置项 | v0.4.0 值 | 当前值 | 变更提交 |
|--------|-----------|--------|----------|
| Agent class | `Agent` | `MonitoredAgent` | e2157a1 |
| task | `actual_task` | `actual_task` | -- (未变) |
| llm | `create_llm(config)` | `create_llm(config)` | -- (未变) |
| browser_session | `None (未传递)` | `create_browser_session()` | f951791 |
| max_actions_per_step | `5` | `5` | -- (未变) |
| register_new_step_callback | `stepCallback` | `stepCallback` | -- (未变) |
| **Headless 模式** | **Auto-detect (macOS 下为 headed)** | **显式 True** | **f951791** |
| Chrome args | `None (browser-use 默认)` | `6 个 SERVER_BROWSER_ARGS + --headless=new` | f951791 + browser-use 内部 |
| Viewport | `None (自动)` | `1920x1080` | c84f4e1 |
| extend_system_message | `None` | `ENHANCED_SYSTEM_MESSAGE` | 9fc9f44 |
| loop_detection_window | `20 (browser-use 默认)` | `10` | 9fc9f44 |
| max_failures | `5 (browser-use 默认)` | `4` | 9fc9f44 |
| planning_replan_on_stall | `3 (browser-use 默认)` | `2` | 9fc9f44 |
| enable_planning | `True (browser-use 默认)` | `True (显式传递)` | 9fc9f44 |
| stall_detector | `N/A` | `StallDetector()` | e2157a1/20efd65 |
| pre_submit_guard | `N/A` | `PreSubmitGuard()` | e2157a1/20efd65 |
| task_progress_tracker | `N/A` | `TaskProgressTracker()` | e2157a1/20efd65 |
| run_logger | `N/A` | `RunLogger(run_id)` | 380be48 |
| available_file_paths | `N/A` | `scan_test_files()` | 7ba3f6b |
| DOM patch | `N/A` | `apply_dom_patch()` | b586b54 |
| self._browser_session | `N/A` | `stored for callback access` | (post-f951791) |

**v0.4.0 代码片段:**
```python
agent = Agent(
    task=actual_task,
    llm=llm,
    max_actions_per_step=5,
    register_new_step_callback=stepCallback,
)
# 无 BrowserSession, 无监控参数, 无 DOM patch
```

**当前代码片段:**
```python
browser_session = create_browser_session()
agent = MonitoredAgent(
    task=actual_task,
    llm=llm,
    browser_session=browser_session,
    available_file_paths=file_paths,
    max_actions_per_step=5,
    register_new_step_callback=stepCallback,
    extend_system_message=ENHANCED_SYSTEM_MESSAGE,
    loop_detection_window=10,
    max_failures=4,
    planning_replan_on_stall=2,
    enable_planning=True,
    stall_detector=stall_detector,
    pre_submit_guard=pre_submit_guard,
    task_progress_tracker=task_progress_tracker,
    run_logger=run_logger,
)
```

---

## Playwright/Browser 配置对比 (DIFF-02)

| 配置项 | v0.4.0 | 当前 | 来源 |
|--------|--------|------|------|
| headless | `None (auto-detect)` | `True (显式)` | f951791 |
| BrowserProfile class | `未使用` | `BrowserProfile(headless=True, ...)` | f951791 |
| BrowserSession class | `未使用` | `BrowserSession(browser_profile=...)` | f951791 |
| Chrome args (项目) | `无` | `--no-sandbox, --disable-setuid-sandbox, --disable-dev-shm-usage, --disable-gpu, --disable-software-rasterizer, --disable-extensions` | f951791 |
| Chrome args (browser-use) | `无` | `--headless=new` (CHROME_HEADLESS_ARGS, 当 headless=True 时自动附加) | browser-use 内部 |
| ViewportSize | `None (自动)` | `1920x1080` | c84f4e1 |
| 最终 Chrome 启动参数总计 | `0 个` | `7 个` (6 项目 + 1 browser-use) | f951791 + browser-use |

**create_browser_session() 当前实现:**
```python
SERVER_BROWSER_ARGS = [
    '--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage',
    '--disable-gpu', '--disable-software-rasterizer', '--disable-extensions',
]

def create_browser_session() -> BrowserSession:
    from browser_use.browser.profile import ViewportSize
    browser_profile = BrowserProfile(
        headless=True,
        args=SERVER_BROWSER_ARGS,
        viewport=ViewportSize(width=1920, height=1080),
    )
    return BrowserSession(browser_profile=browser_profile)
```

**browser-use 内部 headless 处理 (profile.py):**
```python
# line 1176-1178: 当 headless=None 时自动检测
if self.headless is None:
    self.headless = not has_screen_available  # macOS=False(headed), Linux server=True(headless)

# line 80-82: headless=True 时附加参数
CHROME_HEADLESS_ARGS = ['--headless=new']
# line 863: *(CHROME_HEADLESS_ARGS if self.headless else [])
```

---

## 根因分析

### 核心变更

**提交 `f951791` (2026-03-24)** — 为 Linux 服务器部署添加 `BrowserSession(headless=True)`

这是浏览器窗口不再弹出的直接原因。该提交引入了 `create_browser_session()` 函数，显式设置 `headless=True`。

### 影响范围

- `create_browser_session()` 被 `run_simple()` 和 `run_with_streaming()` 两个方法共享
- 本地开发环境也通过此函数创建浏览器会话，因此本地开发也使用 headless 模式
- v0.4.0 时不传递 `browser_session` 参数，browser-use 默认 `headless=None`，触发自动检测:
  - **macOS（有显示器）**: `headless=False` (headed, 弹出浏览器窗口)
  - **Linux server（无显示器）**: `headless=True` (headless, 后台运行)
- 显式 `headless=True` 覆盖了 browser-use 的自动检测，导致所有环境都使用 headless

### 次要变更（不影响浏览器模式）

以下变更为增量修改，不改变浏览器的 headless/headed 行为:

| 变更 | 提交 | 影响 |
|------|------|------|
| MonitoredAgent 替代 Agent | e2157a1 | Agent 级别监控，不影响浏览器配置 |
| ENHANCED_SYSTEM_MESSAGE | 9fc9f44 | Prompt 优化，不涉及浏览器 |
| loop_detection_window/max_failures 参数调优 | 9fc9f44 | Agent 行为调优 |
| stall_detector/pre_submit_guard/task_progress_tracker | e2157a1/20efd65 | 监控组件 |
| RunLogger | 380be48 | 结构化日志 |
| ViewportSize(1920x1080) | c84f4e1 | 渲染区域固定，不改变 headless/headed |
| apply_dom_patch() | b586b54 | DOM 序列化补丁，绕过 headless 问题 |
| scan_test_files + available_file_paths | 7ba3f6b | 文件上传支持 |

### 关键提交时间线

```
v0.4.0          baseline -- 无 BrowserSession，无 headless 配置（自动检测）
f951791 (Mar 24) ROOT CAUSE -- BrowserSession(headless=True) 为服务器部署
c84f4e1 (Mar 31) ViewportSize(1920x1080) 添加
e2157a1 (Apr  ) Agent -> MonitoredAgent
9fc9f44 (Apr  ) ENHANCED_SYSTEM_MESSAGE + Agent 参数调优
380be48 (Apr  ) RunLogger 集成
20efd65 (Apr  ) 检测器绑定到 step_callback
b586b54 (Apr  ) apply_dom_patch() 添加到执行路径
7ba3f6b (Apr  ) scan_test_files + available_file_paths
HEAD            当前状态: 所有监控 + DOM patches + headless
```

---

## Headless vs Headed DOM 渲染差异分析 (D-03)

### Chromium --headless=new 渲染引擎

Chromium 112+ 的 "new headless" 模式使用与 headed Chrome **完全相同的 Blink 渲染引擎**。

- **静态内容**: DOM 树结构与 headed 模式完全相同
- **CSS 计算**: 布局、样式计算、渲染管线一致
- **JavaScript 执行**: V8 引擎相同，所有 JS 行为一致
- **参考来源**: Chromium 官方文档 (chromium.org/developers/design-documents/headless)

**结论**: 对于静态 DOM 结构，headless 和 headed 模式无差异。

### 交互状态差异

虽然渲染引擎相同，但以下交互相关行为在 headless 模式下存在差异:

**1. 焦点/悬停状态**
- Headless 模式无真实鼠标光标
- Playwright/browser-use 通过程序模拟点击事件 (dispatchEvent)
- CSS `:hover` 和 `:focus` 伪类触发方式可能不同
- 模拟点击不会产生真实的光标轨迹和 hover 过渡效果

**2. Ant Design click-to-edit 行为**
- Ant Design 可编辑表格通常在 `<td>` 单元格显示文本内容，点击后显示 `<input>` 元素
- 这是 JavaScript 驱动的交互（React state change）
- 在 headless 模式下:
  - 点击事件会被分发 (Playwright 的 `page.click()` 正常处理)
  - input 应该出现在 DOM 中 (JavaScript 正常执行，React 重新渲染)
  - **但**: 时序差异可能导致 browser-use DOM 序列化器在 input 完全渲染前捕获状态
  - browser-use 在每个 step 截取 DOM 快照时，如果 React 还未完成重渲染，序列化结果可能缺少 input 元素

**3. 可访问性树差异**
- Headless Chromium 可能构建略有不同的可访问性树 (Accessibility Tree)
- browser-use 使用可访问性树进行元素索引
- "屏幕外" 或尺寸为零的元素可能在 headless 模式下被排除在 AX 树之外
- Ant Design 表格中某些隐藏状态下的 input 可能因此丢失

### DOM Patch 评估

v0.8.1 的 `backend/agent/dom_patch.py` 包含 5 个补丁，逐一分析:

**Patch 1: _patch_is_interactive — 恢复 ERP 元素的交互标记**
- 功能: 扩展 `ClickableElementDetector.is_interactive`，识别 ERP 特定 CSS class (`hand`, `el-checkbox`) 的元素和含文本内容的 `<td>` 单元格为可交互
- 解决: ERP 表格中的操作链接（class="hand"）和 checkbox 在 DOM 序列化时被标记为非交互，无法被 Agent 定位

**Patch 2: _patch_paint_order_remover — 防止 ERP 节点被边界框过滤排除**
- 功能: 在 `PaintOrderRemover.calculate_paint_order` 运行后，重置带 ERP CSS class 节点的 `ignored_by_paint_order` 标志
- 解决: ERP 子元素（span.hand, .el-checkbox__inner）因边界框计算被父 `<tr>` 吸收，失去独立索引

**Patch 3: _patch_should_exclude_child — 阻止 ERP 节点被排除**
- 功能: 对有 ERP CSS class 的节点，`_should_exclude_child` 始终返回 False
- 解决: 防止 ERP 可交互元素因边界框过滤被从 DOM 树中移除

**Patch 4: _patch_assign_interactive_indices — 强制 ERP 表格 input 获得交互索引**
- 功能: 检测 `<td>` 内的 `<input>` 元素（placeholder 匹配 ERP 字段如"销售金额"等），强制分配交互索引
- 解决: 这些 input 在 Chromium AX 树中缺少 `snapshot_node`，导致被 browser-use 跳过

**Patch 5: _is_textual_td_cell — 标记含文本内容的 `<td>` 为可交互**
- 功能: 作为 Patch 1 的扩展，检测 `<td>` 内有文本内容的单元格（click-to-edit 入口），标记为交互元素
- 解决: Ant Design click-to-edit 表格中，`<td>` 显示文本值，点击后才显示 `<input>`。这些 `<td>` 本身需要可点击才能触发编辑模式
- 注: Patch 5 和 Patch 1 都在 `_patch_is_interactive()` 中实现，逻辑上分为两个检测条件

### 评估结论

- **DOM Patch 是合理的绕行方案** (MEDIUM confidence)
- 在 DOM 序列化层面操作，不依赖 headed 模式特性
- 确保元素在 DOM dump 中可见，无论渲染模式
- 5 个 patch 分别解决不同的 AX 树/序列化遗漏问题
- **局限性**: patch 针对 ERP 特定 CSS class 和 placeholder 硬编码，对其他 Web 应用可能不适用
- **建议**: 在 headed 模式下重新测试以确认根因（超出本阶段范围，记录在 Phase 64 建议）

### 置信度表

| 声明 | 置信度 | 来源 |
|------|--------|------|
| Headless 使用相同渲染引擎 | HIGH | Chromium 官方文档 |
| 焦点/悬停模拟有差异 | HIGH | Playwright 文档 + Chromium 架构 |
| 静态内容 DOM 树相同 | HIGH | Chromium 官方文档 |
| Click-to-edit input 时序可能有差异 | MEDIUM | 渲染管线行为推断 |
| DOM Patch 是合理绕行方案 | MEDIUM | dom_patch.py 代码分析 |
| AX 树在 headless 下可能有差异 | MEDIUM | Chromium 架构推断 |
| ERP 子元素被 paint order 吸收 | HIGH | dom_patch.py + 实际调试日志 |
| headless=True 是根因 | HIGH | git diff + 代码追踪确认 |

---

## browser-use 版本对比 (DIFF-03)

| 项目 | v0.4.0 | 当前 | 是否变化 |
|------|--------|------|----------|
| pyproject.toml 依赖声明 | `browser-use>=0.12.2` | `browser-use>=0.12.2` | **无变化** |
| 安装版本 | 0.12.2 | 0.12.2 | **无变化** |

**结论**: browser-use 库版本在 v0.4.0 到当前版本之间没有变化。所有行为差异来自项目级别的配置变更（显式 `headless=True`、SERVER_BROWSER_ARGS 等），而非库 API 变化。

---

## Agent 配置演变历史 (DIFF-04)

| 时期 | 涉及提交 | 浏览器配置 | Agent 配置 |
|------|----------|------------|------------|
| v0.4.0 (baseline) | -- | 无（auto-detect） | Agent, 3 个参数 |
| 服务器部署 | f951791 | BrowserSession(headless=True, 5 args) | Agent + browser_session |
| Viewport | c84f4e1 | + ViewportSize(1920x1080) | -- |
| 监控体系 | e2157a1, 9fc9f44, 380be48 | -- | MonitoredAgent + 10 个参数 |
| DOM 修复 | b586b54 | -- | apply_dom_patch() |
| 文件上传 | 7ba3f6b | -- | available_file_paths |
| 当前 (HEAD) | 全部以上 | BrowserSession(headless=True, 6 args, 1920x1080) | MonitoredAgent + 13 个参数 |

**注意**: SERVER_BROWSER_ARGS 从 5 个增加到 6 个（添加了 `--disable-extensions`），发生在 f951791 之后的某个提交。
