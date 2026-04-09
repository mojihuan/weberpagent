# Phase 70: Excel 模版设计 - Context

**Gathered:** 2026-04-08
**Status:** Ready for planning

<domain>
## Phase Boundary

生成标准化 .xlsx 模版 + openpyxl 解析器，建立列合约。QA 可以下载模版、填写测试用例、后端能可靠解析。

**Scope:**
- 模版生成（.xlsx 文件：列头 + 示例数据 + README sheet + 数据验证）
- ExcelParser 解析器（读取 .xlsx，返回结构化行数据）
- 模版下载 API 端点
- 解析器单元测试

**NOT in scope:**
- 文件上传/导入工作流（Phase 71）
- 预览/校验 UI（Phase 71）
- 批量执行（Phase 72）

</domain>

<decisions>
## Implementation Decisions

### 前置条件与断言列格式

- **D-01:** 前置条件列使用 JSON 格式填写，QA 在 Excel 单元格内直接写 JSON（如 `["code1", "code2"]`）
- **D-02:** 断言列使用 JSON 格式填写，QA 写 JSON 数组（如 `[{"methodName":"xxx","headers":"main"}]`）
- **D-03:** 前置条件列和断言列均为可选列，留空时解析为空（null/空数组），必填列只有任务名称和任务描述
- **D-04:** 获取数据操作合并在前置条件 JSON 里，不单独设列
- **D-05:** 后续可优化为"操作名引用"模式（更友好的填写方式），v1 先用 JSON

### 模版 API 设计

- **D-06:** 模版下载端点为 GET /tasks/template，在现有 tasks 路由文件中添加，返回 StreamingResponse (.xlsx)
- **D-07:** 模版不含版本号，简单优先。模版格式变化时解析器跟着变

### 解析器错误处理

- **D-08:** ExcelParser 使用 collect-all 策略，收集所有行的错误后一起返回（Phase 71 预览需要逐行错误信息）
- **D-09:** 类型强制转换使用宽松模式：数字转字符串、空单元格跳过、布尔转字符串，最大程度包容 QA 填写习惯

### Claude's Discretion

- 模版列头的中英文名称选择（README sheet 可用中文，列头建议中文以对齐 QA 习惯）
- 示例数据的具体内容
- README sheet 的说明格式和详细程度
- 解析器的具体代码结构（模块名、类名等）
- 合并单元格检测的具体实现方式

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Task 模型与 Schema
- `backend/db/schemas.py` — TaskCreate Pydantic schema（name, description, target_url, max_steps, preconditions, assertions 字段定义和验证规则）
- `backend/db/models.py` — Task ORM 模型（字段类型和 JSON 存储方式）

### 现有 Excel 使用模式
- `webseleniumerp/use_case/export.py` — 项目中已有的 openpyxl 使用参考

### 路由与 API 模式
- `backend/api/routes/tasks.py` — 现有 tasks 路由结构，模版下载端点应在此添加
- `backend/api/main.py` — FastAPI app 初始化，路由注册方式

### 研究文档
- `.planning/research/SUMMARY.md` — v0.9.0 完整研究总结（openpyxl 使用模式、架构建议、风险分析）
- `.planning/research/FEATURES.md` — v0.9.0 功能研究（Excel 填写格式讨论、操作名引用 vs JSON 方案对比）

### 需求文档
- `.planning/REQUIREMENTS.md` — TMPL-01, TMPL-02 需求定义

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `TaskCreate` schema (backend/db/schemas.py): 已有完整的字段验证（name min_length=1, max_steps ge=1 le=100），解析器输出应可直接用于 TaskCreate 校验
- `webseleniumerp/use_case/export.py`: 已有 openpyxl 使用模式可参考
- `TaskRepository.create()` (backend/db/repository.py): 可直接用于 Phase 71 批量创建

### Established Patterns
- Pydantic BaseModel 用于请求/响应验证（schemas.py 模式）
- APIRouter + Depends 模式用于路由（tasks.py 模式）
- snake_case 文件命名，PascalCase 类名（CONVENTIONS.md）
- frozen=True dataclass 用于不可变结果对象

### Integration Points
- `backend/api/routes/tasks.py` — 添加 GET /tasks/template 端点
- `backend/db/schemas.py` — ExcelParser 输出应对齐 TaskCreate 字段
- `backend/utils/` — ExcelParser 可作为新工具模块放置

</code_context>

<specifics>
## Specific Ideas

- 用户明确提到后续想把前置条件和断言的填写方式优化为"操作名引用"模式（在 README sheet 列出可用操作，QA 只写操作名），v1 先用 JSON 作为基础方案
- 用户提到"获取数据"操作需要考虑如何包含在内，决定合并在前置条件 JSON 里

</specifics>

<deferred>
## Deferred Ideas

- 操作名引用模式（前置条件和断言）— 更友好的填写方式，用户明确表示后续优化
- 管道分隔断言格式 (method|headers|data|params) — v2 REQUIREMENTS (IMPT-05)
- 模版版本号机制 — 当前不需要，未来格式升级时再考虑

</deferred>

---

*Phase: 70-excel*
*Context gathered: 2026-04-08*
