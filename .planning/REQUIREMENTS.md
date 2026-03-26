# Requirements: v0.6.2 回归原生 browser-use

**Milestone:** v0.6.2
**Goal:** 移除所有自定义的 browser-use 扩展方法，完全依赖 browser-use 原生能力执行测试
**Created:** 2026-03-26

---

## Problem Context

**背景:** v0.6.0-v0.6.1 添加了大量自定义扩展来处理表格输入问题

**问题:**
- 这些扩展增加了维护成本
- 可能与 browser-use 更新不兼容
- 代码复杂度增加，难以调试

**决策:** 回归原生 browser-use 能力，简化代码

---

## In Scope (This Milestone)

### CLEANUP: 代码移除

- [x] **CLEANUP-01**: 移除 scroll_table_and_input 工具
  - 删除 `backend/agent/tools/` 目录（scroll_table_tool.py, __init__.py）
  - 移除 `backend/agent/__init__.py` 中的相关导出
  - **Complexity**: Low

- [x] **CLEANUP-02**: 移除 TD 后处理逻辑
  - 删除 `_post_process_td_click` 方法
  - 移除 step_callback 中的 TD 后处理调用
  - 移除 `td_post_process_result` 变量及相关逻辑
  - **Complexity**: Medium

- [x] **CLEANUP-03**: 移除 JavaScript fallback
  - 删除 `_fallback_input` 方法
  - 移除 step_callback 中的 fallback 调用逻辑
  - **Complexity**: Medium

- [x] **CLEANUP-04**: 移除元素诊断日志
  - 删除 `_collect_element_diagnostics` 方法
  - 移除 `element_diagnostics` 变量及相关逻辑
  - **Complexity**: Low

- [x] **CLEANUP-05**: 移除循环干预逻辑
  - 删除 `LoopInterventionTracker` 类
  - 移除 `tracker` 实例化及 `should_intervene()` 调用
  - 移除 `loop_intervention_data` 变量
  - **Complexity**: Medium

### SIMPLIFY: 代码简化

- [x] **SIMPLIFY-01**: 简化 step_callback
  - 保留基础日志（URL、DOM、动作、推理）
  - 保留截图保存
  - 保留 step_stats 基础统计（action_count, element_count）
  - 移除所有自定义扩展相关的调用
  - **Complexity**: Medium

- [x] **SIMPLIFY-02**: 清理导入和变量
  - 移除 `from backend.agent.tools import register_scroll_table_tool`
  - 移除 `tools = register_scroll_table_tool()` 调用
  - Agent 创建时不传入 `tools` 参数
  - **Complexity**: Low

### TEST: 测试更新

- [x] **TEST-01**: 更新单元测试
  - 移除 `test_scroll_table_tool.py` 测试文件
  - 更新 `test_agent_service.py` 中依赖自定义方法的测试
  - 确保现有测试通过
  - **Complexity**: Medium

### VALIDATE: 验证

- [ ] **VALIDATE-01**: 基础功能验证
  - 确保 Agent 仍能正常启动和执行
  - 确保 step_callback 正常记录日志
  - 确保截图正常保存
  - **Complexity**: Low

---

## Out of Scope

| Item | Reason |
|------|--------|
| 修改 browser-use 核心库 | 不需要 |
| 修改前端代码 | 与此次清理无关 |
| 修改测试报告系统 | 保持兼容 |
| 修改断言系统 | 与此次清理无关 |
| 修改前置条件系统 | 与此次清理无关 |

---

## Future Considerations

如果遇到表格输入问题:
1. 调整测试用例的描述方式
2. 使用 browser-use 原生的 scroll + click + input 组合
3. 等待 browser-use 官方解决

---

## Success Criteria

1. 所有自定义扩展方法被移除
2. Agent 仍能正常启动和执行
3. step_callback 保留基础日志功能
4. 截图保存功能正常
5. 所有测试通过

---

## Traceability

| REQ-ID | Phase | Status |
|--------|-------|--------|
| CLEANUP-01 | Phase 45 | Complete |
| CLEANUP-02 | Phase 45 | Complete |
| CLEANUP-03 | Phase 45 | Complete |
| CLEANUP-04 | Phase 45 | Complete |
| CLEANUP-05 | Phase 45 | Complete |
| SIMPLIFY-01 | Phase 46 | Complete |
| SIMPLIFY-02 | Phase 46 | Complete |
| TEST-01 | Phase 46 | Complete |
| VALIDATE-01 | Phase 47 | Pending |

---

*Requirements for milestone v0.6.2*
*Created: 2026-03-26*
