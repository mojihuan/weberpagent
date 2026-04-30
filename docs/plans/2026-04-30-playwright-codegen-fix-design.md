# Playwright 测试代码生成修复设计

日期: 2026-04-30
状态: 已批准

## 问题

生成的 Playwright 测试代码无法运行 — 几乎所有 click/input 操作都输出 `TODO: 定位器缺失` 占位符。

## 根因

`interacted_element` 数据在 `extract_action_info()` (action_utils.py:23) 处丢失。`ActionModel.model_dump()` 不包含 `interacted_element`，但该数据可以从回调中已有的 `browser_state.dom_state.selector_map` + 动作 `index` 计算得到。

断裂数据流:
```
browser_state.dom_state.selector_map (有数据)
  + agent_output.action[0].get_index() (有数据)
  → _extract_agent_output() 只提取 action_name + action_params
  → action_dict = {action_name: action_params}  // 没有 interacted_element
  → ActionTranslator.translate() 读 action.get("interacted_element") → None
  → 生成 "TODO: 定位器缺失"
```

## 修复方案

### P0: 修复 interacted_element 数据管道

在 `_create_step_callback()` (agent_service.py:441) 中，从 `browser_state` 计算 `interacted_element` 并注入 `action_dict`:

- 数据来源: `browser_state.dom_state.selector_map` (回调中已有)
- 计算方式: 复用 `AgentHistory.get_interacted_element()` 的逻辑 (browser_use/agent/views.py:499-508)
- 注入位置: `action_dict["interacted_element"]`
- 改动范围: ~15 行代码，仅 agent_service.py

### P1: 语义优先定位器优化

调整 `LocatorChainBuilder` 定位器优先级:
- 提升 `getByRole` 与 `getByText` 并列第一
- 确保 role 定位器携带 `name` 属性
- 改动范围: locator_chain_builder.py 的优先级排序逻辑 (~30行)

### 后续迭代 (P2-P4)

| 优先级 | 改进项 | 借鉴来源 | 复杂度 |
|--------|--------|----------|--------|
| P2 | Precondition 合约扩展 | Test Agents seed-as-contract | 中 |
| P3 | 边生成边验证 | Generator live validation | 高 |
| P4 | LLM 自修复层 | Healer bounded repair | 高 |

## 借鉴的 Test Agents 设计模式

从 obsidian-wiki 知识库中的 Playwright Test Agents (Planner/Generator/Healer) 提取:

1. **语义优先定位器** — getByRole/getByText/getByLabel 优先于 CSS 路径
2. **有界自修复** — 只修复定位器漂移和时序问题，不修复业务逻辑变更
3. **Precondition 即合约** — seed 文件承担环境初始化、风格模板、入口状态三重角色
4. **分级验证循环** — 微观 (每步验证) + 宏观 (跨阶段验证)，中间产物人类可审

## 影响范围

- `backend/agent/action_utils.py` — 可能需要修改签名
- `backend/core/agent_service.py` — step_callback 中注入 interacted_element
- `backend/core/locator_chain_builder.py` — 定位器优先级调整 (P1)
- 不涉及前端改动
- 不涉及数据库 schema 变更
