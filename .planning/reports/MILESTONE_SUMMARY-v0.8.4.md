# Milestone v0.8.4 — Project Summary

**Generated:** 2026-04-07
**Purpose:** Team onboarding and project review

---

## 1. Project Overview

**aiDriveUITest** — AI 驱动的 UI 自动化测试平台。让 QA 用自然语言写测试用例，AI（基于 Browser-Use + 阿里云 Qwen 3.5 Plus）自动执行并生成测试报告。

**Core Value:** 让 QA 用自然语言写测试用例，AI 自动执行并生成报告。

**Target Users:** QA 测试人员

**Milestone v0.8.4 Goal:** 实施 v0.8.3 设计文档中的 Agent 表格交互优化策略，实现行标识定位、反重复机制、三级策略优先级和失败恢复。

## 2. Architecture & Technical Decisions

### 技术栈

| 层级 | 技术 |
|------|------|
| 前端 | React 18, TypeScript, Vite, Tailwind CSS |
| 后端 | Python 3.11, FastAPI, Pydantic, SQLAlchemy |
| AI | Browser-Use, 阿里云 Qwen 3.5 Plus |
| 浏览器 | Playwright (Chromium) |
| 通信 | REST API + SSE |
| 存储 | SQLite |

### 关键架构决策

- **Decision:** 所有优化融入现有 `dom_patch.py` 和 `prompts.py`，不新增独立模块
  - **Why:** 设计决策 — 减少模块间耦合，维护 monkey-patch 一致性
  - **Phase:** 66 (设计), 67-69 (实施)

- **Decision:** 行标识使用 IMEI 格式正则 `I\d{15}`，注入为 DOM dump HTML 注释
  - **Why:** ERP 销售出库表格的商品编号符合 IMEI 格式，注释格式不干扰 DOM 结构
  - **Phase:** 67-68

- **Decision:** 失败追踪通过 `_failure_tracker` 模块级字典，以 `backend_node_id` 为键
  - **Why:** 与 browser-use `_selector_map` 一致，简单直接；若跨 step 不稳定可回退复合键
  - **Phase:** 67

- **Decision:** 三级策略：可见 input → click-to-edit → evaluate JS，仅在失败元素上标注
  - **Why:** 避免未失败元素显示策略标注导致 Agent 偏向 evaluate JS
  - **Phase:** 68

- **Decision:** 失败检测集成在 agent_service.py inline step_callback，不碰 monitored_agent.py
  - **Why:** monitored_agent.py 的 create_step_callback 当前未使用，减少变更范围
  - **Phase:** 69

- **Decision:** Section 9 追加规则使用超紧凑单行格式（粗体标题 + 内容同行）
  - **Why:** 80 行 prompt 预算限制，76 行已用，仅剩 4 行
  - **Phase:** 69

- **Decision:** Mutable dict 闭包（`_prev_dom_hash_data`）存储跨步 dom_hash
  - **Why:** Python 闭包中简单变量赋值不会更新外部作用域，dict 可变容器可绑过此限制
  - **Phase:** 69

- **Decision:** 失败关键词门控使用 tuple `('失败', 'wrong', 'error', '无法', '不成功', '未成功')`
  - **Why:** '未成功' 而非 '未'，避免 "已完成" 等短语误触发
  - **Phase:** 69

## 3. Phases Delivered

| Phase | Name | Status | One-Liner |
|-------|------|--------|-----------|
| 67 | 基础层-行标识检测与失败追踪状态 | ✓ Complete | IMEI 行标识检测 + `_failure_tracker` 状态管理 + 三种失败模式检测器 |
| 68 | dom-patch | ✓ Complete | DOM dump 行标识注释注入 + 策略层级标注 + 失败动态标注 |
| 69 | prompt | ✓ Complete | step_callback 失败检测集成 + Section 9 四组操作规则追加 |

### Phase 67: 基础层 — 行标识检测与失败追踪状态

**目标:** 建立 DOM Patch 和 StallDetector 的三项基础能力

**交付物:**
- `_detect_row_identity()` — 从 ERP 表格 tr/td 子节点中提取 IMEI 格式行标识
- `_failure_tracker` 状态管理 — 模块级字典 + update/reset 函数，reset 独立于 `_PATCHED` 幂等保护
- `FailureDetectionResult` frozen dataclass + `detect_failure_mode()` — 三种失败模式检测（click_no_effect / wrong_column / edit_not_active）
- 29 个单元测试（14 + 15）

**关键决策:**
- wrong_column 检测优先于 click_no_effect（evaluation 关键词比 dom_hash 更具诊断价值）
- edit_not_active 仅在 action_name=="input" 时触发，防止 click 操作误判

### Phase 68: DOM Patch 增强

**目标:** DOM dump 序列化输出包含行标识注释和策略层级标注

**交付物:**
- `_node_annotations` sidecar 字典 — Patch 4 中为每个 ERP input 添加行归属和策略判定
- `_patch_serialize_tree_annotations()` — 合并 Patch 6+7，包裹 serialize_tree 注入注释
- 行标识注释 `<!-- 行: I01784004409597 -->` — 含商品编号的行上方显示
- 失败/策略标注 `<!-- 行内 input [...] -->` — 仅在已失败元素上显示
- 22 个单元测试（9 + 13）

**关键决策:**
- `_detect_row_identity_from_tr()` 独立创建（tr 节点本身无父级链可走）
- 策略降级在 serialize_tree 中实时重算（tracker 可能在 Patch 4 之后更新）

### Phase 69: 服务集成与 Prompt 规则

**目标:** 激活检测→追踪→标注→Prompt 完整链路

**交付物:**
- step_callback 中 `detect_failure_mode()` 调用链 — 关键词门控 → 检测 → 写入 tracker
- `_prev_dom_hash_data` 闭包变量 — 跨步 dom_hash 持久化
- Section 9 四组操作规则 — 行标识定位、反重复、策略优先级、失败恢复
- 12 个集成测试（6 + 6）

**关键决策:**
- update_failure_tracker 本地导入（避免循环依赖）
- 内层 try/except 非阻塞 — 失败检测错误不中断 step_callback
- 压缩到 4 行新规则，ENHANCED_SYSTEM_MESSAGE 恰好 80 行

## 4. Requirements Coverage

**15/15 v1 requirements met (100%)**

### 行标识定位 (OPTIMIZE-01)
- ✅ ROW-01: IMEI 行标识检测 — Phase 67
- ✅ ROW-02: DOM dump 行标识注释注入 — Phase 68
- ✅ ROW-03: 行归属标注 — Phase 68

### 反重复机制 (OPTIMIZE-02)
- ✅ ANTI-01: `_failure_tracker` 状态管理 — Phase 67
- ✅ ANTI-02: 失败元素动态标注 — Phase 68
- ✅ ANTI-03: step_callback 调用 `update_failure_tracker()` — Phase 69

### 策略优先级 (OPTIMIZE-03)
- ✅ STRAT-01: 三级策略可见性判定 — Phase 68
- ✅ STRAT-02: serialize_tree 策略标注注入 — Phase 68
- ✅ STRAT-03: 失败降级逻辑 — Phase 68

### 失败恢复 (OPTIMIZE-04)
- ✅ RECOV-01: 三种失败模式检测器 — Phase 67
- ✅ RECOV-02: step_callback 检测逻辑集成 — Phase 69
- ✅ RECOV-03: Section 9 失败恢复规则 — Phase 69

### Prompt 层集成
- ✅ PROMPT-01: 行标识使用规则 — Phase 69
- ✅ PROMPT-02: 反重复操作规则 — Phase 69
- ✅ PROMPT-03: 策略优先级规则 — Phase 69

## 5. Key Decisions Log

| ID | Decision | Phase | Rationale |
|----|----------|-------|-----------|
| 67-D01 | `_failure_tracker` 以 `backend_node_id` 为键 | 67 | 与 `_selector_map` 一致，不稳定时回退复合键 |
| 67-D02 | `FailureDetectionResult` frozen dataclass | 67 | 遵循 Phase 48 StallResult 不可变模式 |
| 67-D03 | `detect_failure_mode()` 作为 StallDetector 独立方法 | 67 | 职责分离，不扩大 `check()` 范围 |
| 67-D04 | wrong_column 优先于 click_no_effect | 67 | evaluation 关键词比 dom_hash 更具诊断价值 |
| 68-D01 | 两阶段注入：Patch 4 判定 + Patch 6/7 注入 | 68 | 职责分离，避免单一 wrapper 膨胀 |
| 68-D02 | HTML 注释格式 `<!-- 行: ... -->` | 68 | 不干扰 DOM 结构，Agent 可识别 |
| 68-D03 | 策略命名：1-原生 input / 2-需先 click / 3-evaluate JS | 68 | 描述性命名，看注释即懂操作方式 |
| 68-D04 | 标注仅对已失败元素显示 | 68 | 避免未失败元素策略标注导致 evaluate JS 偏差 |
| 69-D01 | 先 detect_failure_mode → 再 update_failure_tracker | 69 | 逻辑清晰，避免无谓写入 |
| 69-D02 | `_prev_dom_hash_data` 可变字典闭包 | 69 | 绕过 Python 闭包简单变量赋值限制 |
| 69-D03 | 失败关键词门控 | 69 | 减少无谓检测调用 |
| 69-D04 | 仅修改 agent_service.py inline step_callback | 69 | monitored_agent.py 死代码不碰 |
| 69-D05 | 超紧凑单行规则格式 | 69 | 80 行 prompt 预算限制 |

## 6. Tech Debt & Deferred Items

### 已知限制
- **PreSubmitGuard DOM 值提取** — 当前 `actual_values=None`，需实现 DOM 值读取才能主动拦截提交
- **backend_node_id 跨 step 稳定性** — Phase 67 假设稳定，若集成测试发现不稳定需回退复合键 `(tag_name, placeholder, row_identity)`
- **test_assertion_result_repo.py 预存错误** — Phase 03 遗留问题，与 v0.8.4 无关
- **5 个预存测试隔离问题** — test_external_bridge, test_browser_cleanup 等

### Deferred to Future
- **E2E 验证** — v0.8.4 全部为单元测试，需要 live Agent 执行验证完整链路
- **多表格类型通用化** — 当前只针对 ERP 销售出库表格
- **browser-use 版本升级** — 0.12.2 API 稳定，升级到 0.13+ 风险高
- **React 状态监听** — evaluate JS 绕过 React 状态管理是已知限制

### 测试质量备注
- Phase 69 TestStepCallbackPhase69 测试复制了检测逻辑而非测试生产代码路径。验证了算法正确性，但不防生产回归。生产代码已手动确认与测试逻辑匹配。

## 7. Getting Started

### 运行项目

```bash
# 后端
uv sync && uv run playwright install chromium
uv run uvicorn backend.api.main:app --reload --port 8080

# 前端
cd frontend && npm install && npm run dev
```

### 运行测试

```bash
# Phase 67-69 相关测试
uv run pytest backend/tests/unit/test_dom_patch_phase67.py -v
uv run pytest backend/tests/unit/test_dom_patch_phase68.py -v
uv run pytest backend/tests/unit/test_stall_detector_phase67.py -v
uv run pytest backend/tests/unit/test_agent_service.py::TestStepCallbackPhase69 -v
uv run pytest backend/tests/unit/test_enhanced_prompt.py::TestSection9Phase69 -v

# 全部单元测试
uv run pytest backend/tests/unit/ -v
```

### 关键目录

| 目录 | 说明 |
|------|------|
| `backend/agent/dom_patch.py` | DOM Patch 核心 — 5 patches + Phase 67/68 增强 |
| `backend/agent/stall_detector.py` | 停滞检测 + 失败模式检测 |
| `backend/agent/prompts.py` | ENHANCED_SYSTEM_MESSAGE — Agent 指令 |
| `backend/core/agent_service.py` | Agent 服务 — step_callback 集成 |
| `backend/tests/unit/` | 单元测试 |

### 入口阅读顺序

1. `backend/agent/dom_patch.py` — 理解 DOM Patch 架构和 monkey-patch 模式
2. `backend/agent/stall_detector.py` — 理解失败检测逻辑
3. `backend/core/agent_service.py` — 理解 step_callback 集成点
4. `backend/agent/prompts.py` — 理解 Agent 指令结构

---

## Stats

- **Timeline:** 2026-04-07 → 2026-04-07 (1 day)
- **Phases:** 3 / 3 complete
- **Plans:** 6 / 6 complete
- **Commits:** 25
- **Files changed:** 26 (+4,356 / -50)
- **Contributors:** xiaohu
- **Requirements:** 15 / 15 met (100%)
- **Tests added:** 63 (14 + 15 + 9 + 13 + 6 + 6)

---
*Generated: 2026-04-07*
