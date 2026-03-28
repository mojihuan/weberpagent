# Phase 49: 提示词优化与参数调优 - Research

**Phase:** 49
**Researched:** 2026-03-28

---

## 1. extend_system_message 机制

**源码路径:** `browser_use/agent/prompts.py:27-57`

```python
class SystemPrompt:
    def __init__(self, ..., extend_system_message: str | None = None, ...):
        # ...
        if extend_system_message:
            prompt += f'\n{extend_system_message}'
        self.system_message = SystemMessage(content=prompt, cache=True)
```

**关键发现:**
- `extend_system_message` 直接 append 到 base system prompt 末尾，用 `\n` 连接
- 不覆盖原有 system prompt，只是追加
- `override_system_message` 才是完全替换，我们不需要
- 注入时机：Agent 初始化时通过 `SystemPrompt` 构造函数，一次性注入
- 已有先例：`CHINESE_ENHANCEMENT` 就是这么用的

## 2. browser-use 内置参数默认值与效果

**源码路径:** `browser_use/agent/service.py:169-202`

| 参数 | 默认值 | Phase 49 目标值 | 效果 |
|------|--------|----------------|------|
| `max_failures` | 5 | 4 | 连续失败 N 次后强制终止。降到 4 更早停止 |
| `planning_replan_on_stall` | 3 | 2 | 连续失败 N 次后触发重规划。降到 2 更激进 |
| `loop_detection_window` | 20 | 10 | 循环检测窗口大小。降到 10 加速检测 |
| `enable_planning` | True | True | 启用内置 Planning 系统。确认开启即可 |

**参数传递链:** Agent.__init__() → AgentSettings → 实际使用

**关键行为:**
- `max_failures` 达到后会触发 "Force done action" (service.py:1558-1564)
- `planning_replan_on_stall` 在 `_should_replan()` 中检查 `consecutive_failures >= planning_replan_on_stall` (service.py:1446)
- `loop_detection_window` 赋给 `self.state.loop_detector.window_size` (service.py:427)

## 3. 当前 CHINESE_ENHANCEMENT 内容

**源码路径:** `backend/agent/prompts.py:5-41`

现有内容 5 个部分:
1. **元素识别优先级** — 文本 > placeholder > aria-label/title
2. **常见中文表单字段** — 用户名/密码/登录/搜索/取消映射
3. **错误处理策略** — 验证码等待/超时刷新/滚动查找/提交检查
4. **动作输出格式** — JSON 格式模板
5. **选择器策略** — text > role > CSS

**有价值可融入新 prompt 的部分:**
- 中文表单字段映射（第 2 部分）
- 选择器策略优先级（第 5 部分）
- 错误处理策略思路（第 3 部分）

**应删除的部分:**
- 动作输出格式（第 4 部分）— browser-use 已有内置输出格式，不需要重复

## 4. Agent 构造当前状态

**源码路径:** `backend/core/agent_service.py:296-302`

```python
agent = Agent(
    task=actual_task,
    llm=llm,
    browser_session=browser_session,
    max_actions_per_step=5,
    register_new_step_callback=step_callback,
)
```

**缺失的参数:**
- `extend_system_message` — 未传入
- `max_failures` — 使用默认 5
- `planning_replan_on_stall` — 使用默认 3
- `loop_detection_window` — 使用默认 20
- `enable_planning` — 默认 True（OK）

## 5. ENHANCED_SYSTEM_MESSAGE 设计要点

**4 部分 prompt 结构（来自 CONTEXT.md D-05）:**

### Part 1: click-to-edit 模式 (PRM-01)
- Ant Design 表格 `<td>` 在 DOM 快照中为空
- 需要先 click `<td>` 触发编辑模式 → 等待 `<input>` 出现 → 再 input 值
- 这是 ERP 表单的核心痛点

### Part 2: 失败恢复强制规则 (PRM-02)
- 同一元素 2 次失败后禁止重试相同操作
- 替代策略: `evaluate` 执行 JS / `find_elements` 精确查找 / 跳过该步骤
- 与 Phase 48 StallDetector 配合（检测器触发阈值也是 2 次）

### Part 3: 字段填写后验证 (PRM-03)
- 填写值后立即验证是否正确
- 可以用 evaluate JS 检查 input.value
- 防止值被填入错误字段

### Part 4: 提交前校验 (PRM-04)
- 提交前检查所有必填字段已填写
- 与 Phase 48 PreSubmitGuard 配合

## 6. 测试策略

**来自 CONTEXT.md D-09, D-10:**
- 关键词检查而非精确匹配
- 新建 `test_enhanced_prompt.py` 和 `test_agent_params.py`
- 测试 ENHANCED_SYSTEM_MESSAGE 包含: click-to-edit、失败、验证、提交
- 测试 Agent 构造传入正确参数值

---

## RESEARCH COMPLETE
