# Agent 可靠性增强设计

**日期**: 2026-03-27
**状态**: 已确认
**方案**: 方案 A — 中间层 + Prompt 优化

## 背景

运行记录 `outputs/7fcea593` 暴露了 5 个核心问题：

1. **表格 click-to-edit 单元格不可见** — ERP 的 Ant Design 表格中，"销售金额"列的 `<td>` 在 DOM 快照中是空的，无子 `<input>` 元素，Agent 无法定位到真实输入框
2. **循环重试同一失败操作** — Agent 对同一 index 连续操作失败 12 步（step 16-27），浪费步数
3. **值被误填到其他字段** — 尝试设置 sales amount=150 时，150 被填入物流费用字段
4. **步骤遗漏** — 30 步限制中前面浪费太多步数，"金额=10"步骤完全遗漏
5. **提交前校验形同虚设** — 多个字段未正确填写就点了确认，"未收款"状态实际未切换

## 设计决策

| 决策项 | 选择 | 理由 |
|--------|------|------|
| 改进层面 | 中间层 + Prompt（综合方案） | 不侵入 browser-use 源码，升级安全 |
| LLM 模型 | 保持 Qwen 3.5 Plus | 通过工程手段弥补指令遵守能力不足 |
| 停滞阈值 | 2 次失败即切换 | 比 browser-use 默认建议更激进，适合步数紧张场景 |
| 提交校验 | 代码强制拦截 | 不依赖 LLM 自觉性 |

## 架构

```
AgentService.run_with_streaming()
  │
  ├── 创建 StallDetector（停滞检测器）
  ├── 创建 PreSubmitGuard（提交前校验器）
  ├── 创建 TaskProgressTracker（任务进度追踪器）
  │
  ├── 创建 Agent(
  │     task = actual_task,
  │     extend_system_message = ENHANCED_SYSTEM_MESSAGE,  ← 新增
  │     max_steps = max_steps,
  │     ...
  │   )
  │
  └── step_callback(browser_state, agent_output, step):
        │
        ├── [原有逻辑] 日志记录、DOM 保存、截图保存
        │
        ├── StallDetector.check(agent_output, dom_hash)
        │   └── 返回干预消息 → 注入到下一轮上下文
        │
        ├── PreSubmitGuard.check(agent_output, browser_session)
        │   └── 返回校验结果 → 阻止/放行提交
        │
        └── TaskProgressTracker.check(agent_output, step, max_steps)
            └── 返回进度提醒 → 注入到下一轮上下文
```

## 模块 1: StallDetector（停滞检测器）

**文件**: `backend/core/stall_detector.py`

### 追踪数据

```python
@dataclass
class StepRecord:
    step: int
    action_name: str
    target_index: int | None
    evaluation: str
    dom_hash: str
```

### 触发条件（满足任一）

1. 连续 2 次对同一 `target_index` 执行相同 `action_name` 且 `evaluation` 含 "fail"/"Failure"
2. 连续 3 步 DOM 哈希完全相同（页面无任何变化）

### 干预方式

检测到停滞时，生成强制提示消息，在下一次 LLM 调用前注入：

```
⚠️ 你已经对元素 [{index}] 尝试了 N 次相同操作均失败。
必须立即尝试不同的方法：
- 使用 evaluate 执行 JavaScript 直接操作 DOM
- 滚动页面寻找其他可交互元素
- 使用 find_elements 精确查找目标
```

### 消息注入机制

browser-use 的 `Agent` 类不直接支持在 step_callback 中注入消息。实现方式：

- **方案**: 在 step_callback 中将干预消息保存到 `AgentService` 的实例变量
- **注入点**: 通过 browser-use 的 `register_new_step_callback` 无法直接注入消息到 LLM 上下文
- **替代方案**: 在下一次 step 的 `browser_state` 之后，通过 `page.evaluate` 在页面中注入一个不可见的提示元素，使 DOM 快照中出现该提示文本
- **最终方案**: 修改 step_callback 为 Agent 子类的 `register_new_step_callback`，利用 browser-use 内部的 `MessageManager` 注入用户消息

> **注意**: 消息注入机制需要在实施阶段验证 browser-use 0.12.x 的 API 可行性。如果无法注入，退而求其次：在 `on_step` 回调中通过前端 UI 展示停滞警告，由人工干预。

## 模块 2: PreSubmitGuard（提交前校验器）

**文件**: `backend/core/pre_submit_guard.py`

### 工作流程

1. **识别提交意图**: 检测 `action_name == "click"` 且 `target_index` 对应的元素文本包含 "确认"/"提交"/"保存"

2. **执行字段校验**: 通过 `browser_session` 的 `page.evaluate()` 执行 JS 读取关键字段值

3. **期望值获取**: 从原始 `task` 描述中用正则提取：
   - `销售金额.*?(\d+\.?\d*)` / `sales.*?amount.*?(\d+\.?\d*)`
   - `物流费用.*?(\d+\.?\d*)` / `logistics.*?fee.*?(\d+\.?\d*)`
   - `金额.*?(\d+\.?\d*)`（非"销售金额"和"物流费用"的）
   - `未收款` / `unpaid`

4. **校验结果处理**:
   - 全部正确: 放行
   - 存在错误: 注入校验报告 `"✗ 销售金额: 期望 150, 实际 0.00"`，阻止本次 click

### JS 校验脚本模板

```javascript
// 读取表格中所有 spinbutton input 的值
const inputs = document.querySelectorAll('input[role=spinbutton]');
const fields = {};
inputs.forEach(input => {
    const label = input.closest('td')?.previousElementSibling?.textContent || '';
    fields[label] = input.value;
});

// 读取 radio 选中状态
const radios = document.querySelectorAll('[role=radio]');
const paymentStatus = Array.from(radios).find(r => r.getAttribute('aria-checked') === 'true')
    ?.closest('label')?.textContent?.trim() || '';

// 读取物流单号
const trackingInput = document.querySelector('input[placeholder*="物流单号"]');
const trackingNumber = trackingInput?.value || '';

return JSON.stringify({ fields, paymentStatus, trackingNumber });
```

## 模块 3: TaskProgressTracker（任务进度追踪器）

**文件**: `backend/core/task_progress_tracker.py`

### 任务解析

从 task 描述中提取结构化步骤列表，支持格式：
- `Step N: xxx`
- `第N步: xxx`
- `- [ ] xxx`（checkbox 列表）
- 数字编号 `1. xxx` / `2. xxx`

### 进度追踪

每步执行后，检查 `agent_output.evaluation_previous_goal` 和 `agent_output.memory`，将已完成的步骤标记为 done。

### 预警规则

| 条件 | 注入消息级别 |
|------|-------------|
| `remaining_steps < remaining_tasks * 1.5` | 警告：提醒加速 |
| `remaining_steps <= remaining_tasks` | 紧急：建议使用 evaluate 批量操作 |

## 模块 4: Prompt 优化

**文件**: `backend/agent/prompts.py`

### 新增 ENHANCED_SYSTEM_MESSAGE

合并替代现有的 `CHINESE_ENHANCEMENT`，分为 4 个部分：

**Part 1: 表格编辑模式**
- 解释 click-to-edit 模式的原理
- 操作流程：click td → 等待 input 出现 → input 值
- 识别特征：表格行中连续的空 `<td />` 元素

**Part 2: 失败恢复强制规则**
- 同一元素操作失败 2 次后禁止重试相同操作
- 强制使用 evaluate JS / find_elements / 滚动 等替代策略
- 在 memory 中记录失败历史

**Part 3: 字段填写后立即验证**
- 每填写一个数值字段后等待一步观察
- 使用 screenshot 对比确认值已正确填入

**Part 4: 中文表单操作增强**
- 保留现有 CHINESE_ENHANCEMENT 中的有价值内容
- 增加更多中文表单场景的元素映射

## 文件变更范围

| 文件 | 操作 | 说明 |
|------|------|------|
| `backend/core/stall_detector.py` | 新建 | 停滞检测器 |
| `backend/core/pre_submit_guard.py` | 新建 | 提交前校验器 |
| `backend/core/task_progress_tracker.py` | 新建 | 任务进度追踪器 |
| `backend/core/agent_service.py` | 修改 | 集成 3 个检测器，传入 extend_system_message |
| `backend/agent/prompts.py` | 修改 | 新增 ENHANCED_SYSTEM_MESSAGE |

## 风险与缓解

| 风险 | 缓解措施 |
|------|----------|
| browser-use 不支持 step_callback 中注入消息 | 退而求其次：前端 UI 展示停滞警告 |
| JS evaluate 在 ERP 系统中受限 | PreSubmitGuard 的 JS 脚本需针对目标 ERP 适配 |
| 正则提取期望值不准确 | 提取不到时跳过该字段校验，不阻塞流程 |
| StallDetector 误报（页面确实在加载） | DOM 哈希检测结合 evaluation 结果双重判断 |
