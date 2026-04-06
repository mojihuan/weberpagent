# Phase 63 Plan 02: browser-use 版本对比与配置演变时间线

**Created:** 2026-04-06
**Requirements:** DIFF-03, DIFF-04

---

## browser-use 版本对比 (DIFF-03)

### 版本对比表

| 项目 | v0.4.0 | 当前版本 | 是否变更 |
|------|--------|----------|----------|
| pyproject.toml 声明 | browser-use>=0.12.2 | browser-use>=0.12.2 | 无变更 |
| 安装版本 | 0.12.2 | 0.12.2 | 无变更 |
| BrowserSession API | 未使用 | 已使用 | -- (API 存在但项目未使用) |
| BrowserProfile API | 未使用 | 已使用 | -- (API 存在但项目未使用) |
| Agent API | 使用 | 使用 | 无变更 |

**验证方法:**
- v0.4.0 声明: `git show v0.4.0:pyproject.toml | grep "browser-use"` → `browser-use>=0.12.2`
- 当前声明: `grep "browser-use" pyproject.toml` → `browser-use>=0.12.2`
- 安装版本: `importlib.metadata.version('browser-use')` → `0.12.2`

### DIFF-03 结论

1. **browser-use 版本在 v0.4.0 和当前版本之间未变更**，始终为 0.12.2
2. 所有行为差异来自项目级配置变更，不是库 API 变更
3. browser-use 0.12.2 的 BrowserSession/BrowserProfile API 在 v0.4.0 时已存在，只是项目未使用
4. v0.4.0 使用 Agent 无浏览器配置，依赖 browser-use 自动检测（macOS=headed）
5. f951791 引入显式 BrowserSession(headless=True)，切换到手动配置

## browser-use API 演变背景

### Pre-0.12 时代 (已弃用)

- 使用 `Browser` 类直接管理浏览器实例
- 配置通过 `BrowserConfig` 传入
- 项目从未使用此 API（v0.4.0 已在 0.12.x 上）

### 0.12.x (当前 API)

- `BrowserSession` + `BrowserProfile` 替代了旧的 `Browser` 类
- 更好的关注点分离：BrowserProfile 管理配置，BrowserSession 管理生命周期
- Agent 类在整个版本链中未变更构造签名
- 项目在 f951791 迁移到新 API

### headless 参数行为

`BrowserProfile` 中 `headless` 参数的三种行为：

| 值 | 行为 | 使用场景 |
|----|------|----------|
| `None` (默认) | 自动检测：有显示器 → headed，无显示器 → headless | 开发环境友好 |
| `True` | 强制 headless 模式 | 服务器部署 |
| `False` | 强制 headed 模式 | 调试/演示 |

自动检测源码 (`.venv/lib/python3.11/site-packages/browser_use/browser/profile.py` lines 1176-1178):

```python
# if no headless preference specified, prefer headful if there is a display available
if self.headless is None:
    self.headless = not has_screen_available
```

当 `headless=True` 时，browser-use 内部自动添加 `--headless=new` Chrome 参数 (profile.py line 863):

```python
CHROME_HEADLESS_ARGS = ['--headless=new']
# Applied as: *(CHROME_HEADLESS_ARGS if self.headless else [])
```

---

## Agent/Browser 配置演变时间线 (DIFF-04)

### 演变时间线表

| 阶段 | 关键提交 | Browser 配置 | Agent 配置 | 影响范围 |
|------|----------|-------------|-----------|----------|
| v0.4.0 基线 | -- | None (自动检测) | Plain Agent, 3 参数 (task, llm, max_actions_per_step) | 无 |
| 服务器部署 | f951791 | BrowserSession(headless=True, 5 个 Chrome args) | Agent + browser_session 参数 | run_simple + run_with_streaming |
| Viewport 配置 | c84f4e1 | +ViewportSize(1920x1080) | 无变化 | browser_profile |
| Agent 监控化 | e2157a1 | 无变化 | run_with_streaming: MonitoredAgent 替代 Agent | run_with_streaming |
| 参数调优 | 9fc9f44 | 无变化 | +extend_system_message, loop_detection_window=10, max_failures=4, planning_replan_on_stall=2 | run_with_streaming |
| 日志集成 | 380be48 | 无变化 | +run_logger=RunLogger(run_id) | run_with_streaming |
| 检测器接线 | 20efd65 | 无变化 | +stall_detector, pre_submit_guard, task_progress_tracker (通过 step_callback) | run_with_streaming |
| DOM 修补 | b586b54 | 无变化 | +apply_dom_patch() 在执行路径中 | run_with_streaming |
| 文件上传 | 7ba3f6b | 无变化 | +available_file_paths=scan_test_files() | run_with_streaming |
| 当前 (HEAD) | 以上全部 | BrowserSession(headless=True, 6 args, 1920x1080) | MonitoredAgent + 13 参数 + DOM patch | run_simple (4 参数) + run_with_streaming (13+ 参数) |

### 配置快照 per Era

#### v0.4.0 基线

```python
# run_simple
agent = Agent(
    task=task,
    llm=llm,
    max_actions_per_step=5,
)
# browser-use 默认: headless=None -> 自动检测 -> macOS=headed

# run_with_streaming
agent = Agent(
    task=actual_task,
    llm=llm,
    max_actions_per_step=5,
    register_new_step_callback=step_callback,
)
```

#### f951791 (服务器部署)

```python
# 新增函数
SERVER_BROWSER_ARGS = [
    '--no-sandbox',
    '--disable-setuid-sandbox',
    '--disable-dev-shm-usage',
    '--disable-gpu',
    '--disable-software-rasterizer',
    '--disable-extensions',
]

def create_browser_session() -> BrowserSession:
    browser_profile = BrowserProfile(
        headless=True,
        args=SERVER_BROWSER_ARGS,
    )
    return BrowserSession(browser_profile=browser_profile)

# run_simple
browser_session = create_browser_session()
agent = Agent(
    task=task,
    llm=llm,
    browser_session=browser_session,
    max_actions_per_step=5,
)
```

#### c84f4e1 (Viewport 配置)

```python
def create_browser_session() -> BrowserSession:
    from browser_use.browser.profile import ViewportSize
    browser_profile = BrowserProfile(
        headless=True,
        args=SERVER_BROWSER_ARGS,
        viewport=ViewportSize(width=1920, height=1080),
    )
    return BrowserSession(browser_profile=browser_profile)
```

#### e2157a1 (Agent 监控化)

```python
# run_with_streaming
browser_session = create_browser_session()
agent = MonitoredAgent(
    task=actual_task,
    llm=llm,
    browser_session=browser_session,
    max_actions_per_step=5,
    register_new_step_callback=step_callback,
)
# MonitoredAgent 继承 Agent，覆盖 _prepare_context() 和 _execute_actions()
```

#### HEAD (当前)

```python
# run_simple (4 参数)
browser_session = create_browser_session()
agent = Agent(
    task=task,
    llm=llm,
    browser_session=browser_session,
    max_actions_per_step=5,
)

# run_with_streaming (13+ 参数)
browser_session = create_browser_session()
apply_dom_patch()
stall_detector = StallDetector()
pre_submit_guard = PreSubmitGuard()
task_progress_tracker = TaskProgressTracker()
file_paths = scan_test_files()
run_logger = RunLogger(run_id, str(self.output_dir))

agent = MonitoredAgent(
    task=actual_task,
    llm=llm,
    browser_session=browser_session,
    available_file_paths=file_paths,
    max_actions_per_step=5,
    register_new_step_callback=step_callback,
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

## 演变分析结论

### 三波变更

| 波次 | 提交范围 | 核心变更 | 对浏览器可见性的影响 |
|------|----------|----------|---------------------|
| 第 1 波: 服务器部署 | f951791, c84f4e1 | 引入 BrowserSession(headless=True) + viewport | **直接导致浏览器窗口消失** |
| 第 2 波: Agent 监控化 | e2157a1, 9fc9f44, 380be48, 20efd65 | MonitoredAgent + 参数调优 + 日志 + 检测器 | 无影响（Agent 层面，不涉及浏览器配置） |
| 第 3 波: 功能增强 | b586b54, 7ba3f6b | DOM 修补 + 文件上传支持 | 无影响（执行层面，不涉及浏览器配置） |

### 关键发现

1. **只有第 1 波（f951791）影响浏览器可见性** — 引入 `headless=True` 覆盖了 browser-use 的自动检测
2. 第 2、3 波为增量优化，不影响浏览器 headed/headless 模式
3. `run_simple` 方法只受第 1 波影响（添加 browser_session 参数，参数从 3 增至 4）
4. `run_with_streaming` 方法受所有 3 波影响（参数从 5 增至 13+）
5. 中间有多个已移除功能的提交（loop intervention、JS fallback、element diagnostics、TD post-processing），这些是 v0.6.2 回归原生 browser-use 时清理的代码，最终已被完全移除
6. `SERVER_BROWSER_ARGS` 数量始终为 6 个（f951791 起未增减），实际 Chrome 启动参数为 7 个（6 个项目参数 + browser-use 自动添加的 `--headless=new`）

### 参数数量演变

| 方法 | v0.4.0 参数数 | HEAD 参数数 | 增量 |
|------|-------------|-----------|------|
| run_simple | 3 (task, llm, max_actions_per_step) | 4 (+browser_session) | +1 |
| run_with_streaming | 5 (task, llm, max_actions_per_step, register_new_step_callback) | 13+ | +8 |

### 完整提交列表 (v0.4.0..HEAD, agent_service.py)

共 24 个提交修改了 agent_service.py：

```
f951791 fix: use BrowserSession for Linux server compatibility
3c798ab feat(39-01): integrate LoopInterventionTracker into step_callback
7f6e2b1 feat(39-02): enhance logging with detailed diagnostic info
22c877e feat(40-01): integrate scroll_table_and_input tool with AgentService
52e7039 feat(41-01): collect step statistics in agent_service step_callback
b1c9f6e fix(40-01): update scroll_table_tool for browser-use 0.2+ API
2dd22e1 feat(42-01): add TD post-processing for automatic input focus transfer
7e3de3e feat(43-01): implement _fallback_input method for JavaScript input fallback
aa59723 feat(43-01): integrate fallback input detection in step_callback
9d8786f feat(44-01): implement _collect_element_diagnostics method
0ebf64e feat(44-01): integrate diagnostics collection in step_callback
d2b2901 fix(44.1): add JSON parsing in _post_process_td_click
1eb7255 refactor(45-02): remove _post_process_td_click method and references
963ab66 refactor(45-03): remove JavaScript fallback and element diagnostics
c268391 refactor(45-04): remove LoopInterventionTracker class and all references
5b8796a fix: DOM生成始终为0且txt文件中DOM为空
380be48 feat(quick-w3d): integrate RunLogger into AgentService
9fc9f44 feat(49-02): wire ENHANCED_SYSTEM_MESSAGE and tune Agent parameters
e2157a1 feat(50-01): replace Agent with MonitoredAgent in run_with_streaming
20efd65 feat(50-02): wire detector calls into step_callback with monitor logging
0e8afab fix(51-02): fix run_logger.log() duplicate argument in step_callback
b586b54 fix(53-03): add apply_dom_patch() to actual agent execution path
7ba3f6b feat(54-01): add scan_test_files, available_file_paths injection, and Section 8 file upload prompt
c84f4e1 feat: 添加 viewport 大小配置到 BrowserProfile
```

注：按 git log 输出顺序（最新在前），提交时间从 v0.5.0 (2026-03-24) 到 v0.8.1 (2026-04-06)。
