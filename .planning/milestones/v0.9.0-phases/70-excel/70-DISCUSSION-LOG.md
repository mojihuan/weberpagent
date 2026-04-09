# Phase 70: Excel 模版设计 - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-04-08
**Phase:** 70-excel
**Areas discussed:** 前置条件列格式, 断言列格式, 模版下载 API 设计, 解析器错误处理

---

## 前置条件列填写格式

| Option | Description | Selected |
|--------|-------------|----------|
| 分号分隔 | 多个前置条件用分号隔开 | |
| 换行分隔 | 每个前置条件占一行（单元格内换行） | |
| 单条件限制 | 每个 Task 只能写一个前置条件 | |

**User's first response:** "这个前置条件有没有更好的方案，因为现在是ui可视化界面去进行生成代码，但是我这个excel就不想写代码"

**Follow-up — 替代方案选择:**

| Option | Description | Selected |
|--------|-------------|----------|
| 模版中去掉前置条件列 | 导入后通过 UI 补充 | |
| 自然语言描述 | QA 用中文描述，AI 执行 | |
| 简化 DSL | 如 login(admin,password) | |
| 操作名引用 | README sheet 列出操作名，QA 写操作名 | ✓ |

**User's second response:** "先把断言以及前置条件都改成 json填写吧 后续我有别的想法再优化，还有一个问题，有一个获取数据的操作这个该怎么办"

**Final decision:** JSON 格式填写前置条件，获取数据操作合并在前置条件 JSON 里

**Notes:** 用户从"操作名引用"改为"JSON 格式"，表示后续再优化为更友好的方式

---

## 断言列填写格式

| Option | Description | Selected |
|--------|-------------|----------|
| 操作名引用 | 和前置条件一样用操作名 | ✓ (后改为 JSON) |
| 模版中去掉断言列 | 导入后通过 UI 添加 | |
| JSON 格式 | 直接写 JSON 数组 | ✓ (最终选择) |

**User's choice:** JSON 格式（与前置条件保持一致）
**Notes:** 可选列，留空为空

---

## 模版下载 API 设计

### API 端点

| Option | Description | Selected |
|--------|-------------|----------|
| GET /tasks/template | 在现有 tasks 路由添加 | ✓ |
| 独立 /templates 路由 | 新建路由文件 | |

**User's choice:** GET /tasks/template

### 版本号

| Option | Description | Selected |
|--------|-------------|----------|
| 无版本号 | 简单优先 | ✓ |
| 带版本号 | README sheet 写版本号 | |

**User's choice:** 无版本号

---

## 解析器错误处理

### 错误收集策略

| Option | Description | Selected |
|--------|-------------|----------|
| Collect-all | 收集所有行错误 | ✓ |
| Fail-fast | 首行出错即停止 | |

**User's choice:** Collect-all（Phase 71 预览需要逐行错误信息）

### 类型转换策略

| Option | Description | Selected |
|--------|-------------|----------|
| 宽松模式 | 包容 QA 填写习惯 | ✓ |
| 严格模式 | 类型不匹配报错 | |

**User's choice:** 宽松模式

---

## Claude's Discretion

- 模版列头中英文名称选择
- 示例数据具体内容
- README sheet 说明格式
- 解析器代码结构
- 合并单元格检测实现

## Deferred Ideas

- 操作名引用模式（前置条件和断言）— 用户表示后续优化
- 管道分隔断言格式 — v2 (IMPT-05)
- 模版版本号机制 — 未来格式升级时考虑
