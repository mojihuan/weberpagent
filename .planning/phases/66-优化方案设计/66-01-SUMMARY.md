---
phase: 66-优化方案设计
plan: 01
subsystem: agent
tags: [dom-patch, prompt-engineering, erp-tables, browser-use, click-to-edit]

# Dependency graph
requires:
  - phase: 65-差距关联分析
    provides: 因果判定（headless 非唯一根因）+ 逐 Patch 有效性评估 + Section 9 保留建议
provides:
  - OPTIMIZE-01 设计: 按行定位 + 直接找 input 策略（行标识 + 行内 placeholder 匹配）
  - OPTIMIZE-02 设计: 反重复机制（_failure_tracker + 动态标注）
  - OPTIMIZE-03 设计: 三级策略优先级（原生 input > click-to-edit > evaluate JS）
  - OPTIMIZE-04 设计: 失败恢复策略（三种失败模式的统一规则表）
  - 16 项代码任务清单（去重、标注依赖关系）
affects: [phase-67-optimization-implementation]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - _failure_tracker 模块级状态跨 step_callback 和 DOM Patch 共享
    - DOM dump 注释注入模式（<!-- 标注 -->）引导 Agent 行为
    - 策略层级标注自动降级（策略 1 -> 2 -> 3）

key-files:
  created:
    - .planning/phases/66-优化方案设计/66-OPTIMIZE-DESIGN.md
  modified: []

key-decisions:
  - "行标识使用 IMEI 格式正则 I\\d{15} 匹配，注入为 DOM dump 注释 <!-- 行: I01784004409597 -->"
  - "反重复状态通过模块级变量 _failure_tracker 在 step_callback 和 DOM Patch 间共享，每次 run 重置"
  - "三级策略通过 DOM dump 标注实现，Agent 根据 <!-- 策略N: ... --> 注释自然选择操作方式"
  - "失败恢复为三种模式（点击无变化/误点错误列/编辑态误判）的统一规则表，复用 _failure_tracker"

patterns-established:
  - "DOM dump 注释注入: 通过 <!-- --> 注释向 Agent 传递结构化信息（行标识、策略层级、失败标注）"
  - "跨步骤状态共享: 模块级变量在 step_callback（写入）和 DOM Patch（读取）间共享失败历史"
  - "策略自动降级: 策略 1 失败 2 次降级为策略 2，策略 2 失败 2 次降级为策略 3"

requirements-completed: [OPTIMIZE-01, OPTIMIZE-02, OPTIMIZE-03, OPTIMIZE-04]

# Metrics
duration: 11min
completed: 2026-04-06
---

# Phase 66 Plan 01: Agent 表格交互优化设计文档 Summary

**四项 Agent 表格交互优化策略设计文档，覆盖行标识定位、反重复机制、三级策略优先级和失败恢复规则，输出 16 项可直接转化的代码任务**

## Performance

- **Duration:** 11 min
- **Started:** 2026-04-06T10:23:51Z
- **Completed:** 2026-04-06T10:34:45Z
- **Tasks:** 3
- **Files modified:** 1

## Accomplishments
- 生成 66-OPTIMIZE-DESIGN.md 设计文档（540 行），覆盖四项优化策略
- OPTIMIZE-01: 按行定位策略 -- 通过 `_patch_add_row_identity()` 为 `<tr>` 注入行标识，Agent 先锁定行再在行内找 input
- OPTIMIZE-02: 反重复机制 -- 通过 `_failure_tracker` + `_patch_dynamic_annotation()` 在序列化时动态标注失败元素
- OPTIMIZE-03: 三级策略优先级 -- 通过 DOM dump 标注 `<!-- 策略N -->` 让 Agent 自然选择操作方式
- OPTIMIZE-04: 失败恢复策略 -- 三种失败模式（点击无变化/误点错误列/编辑态误判）的统一检测-恢复规则表
- 通过 D-01~D-12 全部 12 项决策对照、ROADMAP 5 项成功标准、REQUIREMENTS 4 项需求覆盖验证

## Task Commits

Each task was committed atomically:

1. **Task 1: 文档框架 + OPTIMIZE-01 行定位策略 + OPTIMIZE-02 反重复机制** - `8b84c98` (docs)
2. **Task 2: OPTIMIZE-03 策略优先级 + OPTIMIZE-04 失败恢复 + 文档完整性检查** - included in `8b84c98` (docs) - all content created as single atomic document
3. **Task 3: 文档质量验证** - included in `8b84c98` (docs) - validation record section created as part of initial document

## Files Created/Modified
- `.planning/phases/66-优化方案设计/66-OPTIMIZE-DESIGN.md` - 四项 Agent 表格交互优化策略设计文档（540 行），含规则表、集成点、代码任务清单、验证记录

## Decisions Made
- 行标识使用 IMEI 格式正则 `I\d{15}` 匹配 `<td>` 文本，注入为 DOM dump 注释（Per D-07/D-08）
- 反重复状态通过模块级变量 `_failure_tracker` 跨 step_callback 和 DOM Patch 共享，与现有 `_PATCHED` 模式一致（Per D-10）
- 三级策略通过 DOM dump `<!-- 策略N: ... -->` 注释实现 Agent 自然选择，不需要修改 Agent 决策逻辑（Per D-11）
- 失败恢复的三种模式复用 `_failure_tracker` 的 `"mode"` 字段区分（Per D-12）
- 所有优化在 DOM Patch 层（dom_patch.py）和 Prompt 层（prompts.py）实现，不新增独立模块（Per D-04/D-05/D-06）

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered
None

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- 设计文档完成，包含 16 项代码任务清单（标注依赖关系和实施优先级）
- 后续实施阶段可按 T01-T16 顺序执行
- 测试验证方案已定义（A/B 对照测试）
- 需要先恢复 headed 模式（修改 `create_browser_session()` 中的 `headless=True`）才能进行有效测试

---
*Phase: 66-优化方案设计*
*Completed: 2026-04-06*
