# Phase 121: 死代码清理 - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-04-29
**Phase:** 121-dead-code-cleanup
**Areas discussed:** 验证策略, Undefined Name 处理, 废弃模块删除范围, 清理范围

---

## 验证策略

| Option | Description | Selected |
|--------|-------------|----------|
| pyflakes + 启动检查 | pyflakes 零警告 + FastAPI 正常启动 | |
| 仅 FastAPI 启动检查 | 仅确认无 ImportError | |
| 启动 + API 端点冒烟测试 | 以上 + 手动调用关键 API 端点确认无 500 错误 | ✓ |

**User's choice:** 启动 + API 端点冒烟测试
**Notes:** 比 Phase 120 更严格的验证标准，确保无运行时 500 错误

---

## Undefined Name 处理

| Option | Description | Selected |
|--------|-------------|----------|
| 跳过，记录为已知 bug | 只做死代码清理，bug 另行处理 | |
| 顺手修复 | 减少后续工作量，避免意外触发 | ✓ |
| 推迟到 Phase 124 | 让函数/模块优化 phase 处理 | |

**User's choice:** 顺手修复
**Notes:** ChatOpenAI (factory.py:163) 和 ContextWrapper (external_precondition_bridge.py:1275) 两个 undefined name

---

## 废弃模块删除范围

| Option | Description | Selected |
|--------|-------------|----------|
| 全部删除 + storage/ 目录 | 删除 4 个文件 + 整个 storage/ 目录 | ✓ |
| 只删文件，保留目录 | 只删除 4 个 .py 文件，保留 storage/ 目录结构 | |

**User's choice:** 全部删除 + storage/ 目录
**Notes:** storage/ 目录只有 run_store.py、task_store.py、__init__.py 三个文件，全部无引用

---

## 清理范围

| Option | Description | Selected |
|--------|-------------|----------|
| 仅 backend/ | 只清理 Python 后端 | |
| backend/ + webseleniumerp/ | 后端 + 外部 Selenium 项目 | |
| backend/ + frontend/src/ | 后端 + 前端，不包括 webseleniumerp | ✓ |
| 全代码库 | 所有目录 | |

**User's choice:** backend/ + frontend/src/（不包括 webseleniumerp）
**Notes:** webseleniumerp 是外部项目，不做清理。前端 types/index.ts 有 54 个 export，部分可能未使用。

---

## Claude's Discretion

- 未使用 import 的具体删除顺序和批次划分
- 前端 TypeScript 未使用 export 的检测方式
- API 冒烟测试选择哪些端点
- 是否分 2 个 plan（backend 先行 + frontend 后行）

## Deferred Ideas

None — discussion stayed within phase scope
