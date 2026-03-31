# Phase 54: 文件导入 - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-03-31
**Phase:** 54-import
**Areas discussed:** 文件准备与存储, Prompt 指导, 验证场景选择, Plan 结构

---

## 文件准备与存储

| Option | Description | Selected |
|--------|-------------|----------|
| 预先放服务器 | 预先在服务器固定目录放好测试文件，Agent 直接引用路径 | ✓ |
| API 动态传入 | 前端上传文件到后端 API，后端保存后传路径给 Agent | |
| 先预置后扩展 | 先用预置文件验证，后续再加 API 动态传入 | |

**User's choice:** 预先放服务器
**Notes:** 简单可靠，适合自动化测试场景

## 文件存储目录

| Option | Description | Selected |
|--------|-------------|----------|
| data/test-files/ | 放在 data/test-files/ 目录下，Agent 启动时扫描自动注册 | ✓ |
| /tmp/ 固定路径 | 放在固定绝对路径如 /tmp/test-files/ | |
| 你决定 | Claude 决定，只要能跑通就行 | |

**User's choice:** data/test-files/
**Notes:** 与现有 data/ 目录结构一致

## available_file_paths 传递方式

| Option | Description | Selected |
|--------|-------------|----------|
| 启动时扫描 | Agent 服务启动时扫描 data/test-files/ 目录，自动加入 available_file_paths | ✓ |
| 硬编码列表 | 在 agent_service.py 中硬编码具体文件路径列表 | |
| 你决定 | Claude 决定 | |

**User's choice:** 启动时扫描

## Prompt 指导

| Option | Description | Selected |
|--------|-------------|----------|
| 添加第 8 段 | 添加 ENHANCED_SYSTEM_MESSAGE 第 8 段，指导 Agent 使用 upload_file | ✓ |
| 不添加 prompt | 不添加 prompt 段落，仅通过任务描述告知 | |
| 你决定 | Claude 根据实际测试结果判断 | |

**User's choice:** 添加第 8 段

## Excel 导入验证页面

| Option | Description | Selected |
|--------|-------------|----------|
| 采购单导入 | 采购管理模块通常有"导入"按钮 | ✓ |
| 库存导入 | 库存模块也有导入功能 | |
| 你决定 | Claude 根据 ERP 实际功能决定 | |

**User's choice:** 采购单导入

## 图片上传验证页面

| Option | Description | Selected |
|--------|-------------|----------|
| 商品图片上传 | 商品管理中的商品图片上传功能 | ✓ |
| 采购单附件 | 采购单附件上传图片 | |
| 你决定 | Claude 根据 ERP 实际功能决定 | |

**User's choice:** 商品图片上传

## Plan 结构

| Option | Description | Selected |
|--------|-------------|----------|
| 两个 Plan | 54-01 基础设施 + 54-02 ERP 验证，与 Phase 52/53 一致 | ✓ |
| 一个 Plan | 合并为一个 Plan | |
| 你决定 | Claude 决定 | |

**User's choice:** 两个 Plan

## Claude's Discretion

- ENHANCED_SYSTEM_MESSAGE 文件上传段落的具体措辞
- 测试用例的具体关键词列表
- data/test-files/ 目录下具体测试文件名和内容
- 验证步骤的具体 ERP 操作流程
- available_file_paths 扫描逻辑的具体实现

## Deferred Ideas

None — discussion stayed within phase scope.
