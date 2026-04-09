# Phase 71: 批量导入工作流 - Context

**Gathered:** 2026-04-08
**Status:** Ready for planning

<domain>
## Phase Boundary

QA 上传填写好的 Excel 后，可以在确认前预览解析结果（有效行绿色、无效行红色+错误信息），确认后系统批量创建所有 Task。

**Scope:**
- 前端上传交互（Modal 弹窗 + 拖拽/点击双模式）
- 后端两阶段 API（preview 解析预览 + confirm 批量创建）
- 前端预览展示（完整表格 + 摘要统计 + 错误行标红）
- 确认后原子性批量创建 Task（单事务，任一失败全部回滚）
- 文件格式/大小校验（.xlsx only, 5MB 上限）

**NOT in scope:**
- 批量执行（Phase 72）
- 批量进度 UI（Phase 73）
- CSV 导入、导出功能
- 错误标注 Excel 下载（v2 IMPT-04）
- 简化断言格式（v2 IMPT-05）

</domain>

<decisions>
## Implementation Decisions

### 上传交互体验
- **D-01:** 上传入口在 TaskListHeader 的「导入」按钮，点击后弹出 Modal 弹窗，不跳转页面
- **D-02:** Modal 内提供拖拽区 + 点击选择文件双模式，拖入文件时高亮提示
- **D-03:** 仅接受 .xlsx 格式，文件大小上限 5MB，不符合时前端即时提示（不等后端返回）

### 预览展示设计
- **D-04:** 预览使用完整表格展示所有列（任务名称、描述、URL、步数、前置条件、断言），与 Excel 模版列一一对应
- **D-05:** 表格顶部显示摘要统计（"有效 X 行，无效 Y 行"），错误行背景淡红色 + 错误信息显示在最后一列或行下方
- **D-06:** 预览表格在 Modal 内滚动显示，超过 Modal 高度时表头固定（sticky header）
- **D-07:** 存在无效行时"确认导入"按钮不可点击（disabled），防止脏数据进入系统

### API 设计与流程
- **D-08:** 两阶段重传模式 — POST /tasks/import/preview 上传文件返回预览 JSON；POST /tasks/import/confirm 重新上传同一文件进行批量创建。confirm 时重新解析，不缓存服务器状态
- **D-09:** 两个端点都在现有 tasks.py 路由文件中添加，与 /tasks/template 保持一致
- **D-10:** confirm 端点使用数据库事务包裹全部创建，任一失败全部回滚（符合 IMPT-03）
- **D-11:** 导入的 Task 状态为 draft（与手动创建一致）
- **D-12:** 后端也做文件格式/大小校验（防御性编程，不依赖前端校验）

### 前端状态管理
- **D-13:** 创建独立 ImportModal 组件（components/ImportModal/），与 TaskFormModal 同级
- **D-14:** Modal 内三步状态：上传 → 预览 → 确认/完成。每步有独立 loading 状态
- **D-15:** 确认成功后关闭 Modal + toast 提示成功 + 自动刷新任务列表
- **D-16:** 失败时 toast 显示错误信息，Modal 保持打开可重试
- **D-17:** 上传 API 使用原生 fetch + 复用 API_BASE 配置，绕过 apiClient 的 Content-Type: application/json

### Claude's Discretion
- Modal 的具体 UI 样式和布局（Tailwind CSS）
- 预览表格的列宽分配
- 错误信息的具体展示格式（列内 vs tooltip vs 行下方展开）
- Modal 尺寸（建议 large/wide 以容纳预览表格）
- 后端响应的具体 JSON 结构
- ImportModal 的内部子组件拆分

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Phase 70 产出（Phase 71 直接依赖）
- `backend/utils/excel_parser.py` — ExcelParser 核心解析逻辑，返回 ParseResult(rows, total_rows, has_errors)
- `backend/utils/excel_template.py` — TEMPLATE_COLUMNS 列合约定义（key/header/width/required/default）
- `backend/utils/excel_template.py` — generate_template() 模版生成函数

### Task 模型与 Schema
- `backend/db/schemas.py` — TaskCreate Pydantic schema（name, description, target_url, max_steps, preconditions, assertions 字段定义和验证规则）
- `backend/db/models.py` — Task ORM 模型（字段类型和 JSON 存储方式）
- `backend/db/repository.py` — TaskRepository.create() 批量创建入口

### 路由与 API 模式
- `backend/api/routes/tasks.py` — 现有 tasks 路由结构，导入端点在此添加
- `backend/api/main.py` — FastAPI app 初始化，路由注册方式

### 前端模式参考
- `frontend/src/api/client.ts` — apiClient 实现（Content-Type: application/json 默认值，需要绕过）
- `frontend/src/api/tasks.ts` — tasksApi 现有方法模式
- `frontend/src/components/TaskModal/` — TaskFormModal 组件结构参考（Modal 基础模式）
- `frontend/src/components/TaskList/TaskListHeader.tsx` — 导入按钮添加位置
- `frontend/src/pages/Tasks.tsx` — Tasks 页面状态管理参考

### 需求与研究文档
- `.planning/REQUIREMENTS.md` — IMPT-01, IMPT-02, IMPT-03 需求定义
- `.planning/STATE.md` — 关键决策：两阶段重传模式、FormData 上传需绕过 apiClient
- `.planning/research/SUMMARY.md` — v0.9.0 完整研究总结

### 前置阶段上下文
- `.planning/phases/70-excel/70-CONTEXT.md` — Phase 70 所有决策，包括 ExcelParser collect-all 策略和类型强制转换

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `excel_parser.parse_excel(buffer)` — Phase 70 完整实现的解析器，接收 BytesIO 返回 ParseResult(rows, total_rows, has_errors)
- `ParsedRow(row_number, data, errors)` — frozen dataclass，data 是 dict[str, Any]，errors 是 list[str]
- `TEMPLATE_COLUMNS` — 列合约定义，parser 和 generator 共用
- `TaskCreate` schema — 已有完整字段验证，ExcelParser 输出的 data dict 可直接用于 TaskCreate 校验
- `TaskRepository.create()` — 单条创建方法，批量需循环调用 + 事务包裹

### Established Patterns
- FastAPI UploadFile 用于文件上传端点
- Pydantic BaseModel 用于请求/响应验证
- APIRouter + Depends 模式用于路由
- 前端 Modal 组件模式（TaskFormModal 参考：useState 控制 open/close）
- toast (sonner) 用于成功/失败通知
- 前端 apiClient 统一错误处理 + 重试逻辑

### Integration Points
- `backend/api/routes/tasks.py` — 添加 POST /tasks/import/preview 和 POST /tasks/import/confirm
- `frontend/src/components/TaskList/TaskListHeader.tsx` — 添加「导入」按钮
- `frontend/src/api/tasks.ts` — 添加 uploadPreview() 和 uploadConfirm() 方法
- `frontend/src/pages/Tasks.tsx` — 控制 ImportModal 的打开/关闭 + 导入后刷新任务列表

### Known Constraints
- apiClient 默认 Content-Type: application/json，FormData 上传需绕过 — 使用原生 fetch + API_BASE
- SQLite WAL 模式下并发写锁竞争 — 批量创建需控制在一个事务内
- confirm 时重新解析文件（不缓存），前端需保留上传的 File 对象

</code_context>

<specifics>
## Specific Ideas

- 预览表格的列头应与 Excel 模版列头中文一致（任务名称、任务描述、目标URL、最大步数、前置条件、断言），降低 QA 认知负担
- 导入按钮建议放在「新建」按钮旁边，视觉层级低于新建（secondary variant）
- 错误行的错误信息应包含行号 + 字段 + 原因（ExcelParser 已返回 row_number + errors）

</specifics>

<deferred>
## Deferred Ideas

- 错误标注 Excel 文件下载（IMPT-04）— v2 需求，允许 QA 离线修复后重新上传
- 简化断言格式（IMPT-05）— v2 需求，管道分隔替代 JSON 数组
- CSV 导入支持 — Out of Scope，编码/换行/类型问题多
- Task 导出为 Excel — Out of Scope，需要 ID 保留和合并语义

</deferred>

---

*Phase: 71-批量导入工作流*
*Context gathered: 2026-04-08*
