# Phase 54: 文件导入 - Context

**Gathered:** 2026-03-31
**Status:** Ready for planning

<domain>
## Phase Boundary

验证并增强 Agent 文件上传能力。让 Agent 能通过 browser-use 的 `upload_file(index, path)` action 上传 Excel 和图片文件，完成 ERP 数据导入。

**不包含：**
- 修改 browser-use 源码
- 前端文件上传 API（仅 Agent 端）
- 键盘操作（Phase 52 已完成）
- 表格交互（Phase 53 已完成）
- 断言与缓存（Phase 55）
- E2E 综合验证（Phase 56）

</domain>

<decisions>
## Implementation Decisions

### 文件准备与存储
- **D-01:** 测试用 Excel 和图片文件预先放置在服务器 `data/test-files/` 目录下，不需要 API 动态传入
- **D-02:** Agent 服务启动时扫描 `data/test-files/` 目录，将所有文件路径自动加入 `available_file_paths` 白名单。新增测试文件无需改代码

### Agent 参数配置
- **D-03:** 修改 `agent_service.py`，在创建 MonitoredAgent 时传入 `available_file_paths` 参数，值为扫描 `data/test-files/` 得到的文件路径列表

### Prompt 指导
- **D-04:** 添加 ENHANCED_SYSTEM_MESSAGE 第 8 段（文件上传），指导 Agent 遇到文件上传场景时使用 `upload_file` action 而非 `click`（browser-use 阻止 click file input）
- **D-05:** 场景-动作对格式，与 Phase 52/53 段落风格一致（Phase 52 D-01）
- **D-06:** 中文撰写，增量控制在 10 行以内（Phase 49 D-01、Phase 52 D-04）

### 验证场景
- **D-07:** Excel 导入使用采购单导入页面验证（IMP-01）
- **D-08:** 图片上传使用商品管理中的商品图片上传功能验证（IMP-02）

### Plan 结构
- **D-09:** 两个 Plan。Plan 54-01: 基础设施（test-files 目录 + available_file_paths + prompt 第 8 段 + 测试），Plan 54-02: ERP 场景验证（采购单 Excel 导入 + 商品图片上传）

### 测试策略
- **D-10:** 结构 + 关键词检查。测试 ENHANCED_SYSTEM_MESSAGE 包含文件上传关键词（upload_file、file input 等），不检查具体措辞（Phase 49 D-09 模式）

### Claude's Discretion
- ENHANCED_SYSTEM_MESSAGE 文件上传段落的具体措辞
- 测试用例的具体关键词列表
- `data/test-files/` 目录下需要准备的具体测试文件名和内容
- 验证步骤的具体 ERP 操作流程
- `available_file_paths` 扫描逻辑的具体实现

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### 需求与路线图
- `.planning/REQUIREMENTS.md` — IMP-01、IMP-02 文件导入需求定义
- `.planning/ROADMAP.md` — Phase 54 成功标准和计划结构

### 代码参考
- `backend/agent/prompts.py` — 现有 ENHANCED_SYSTEM_MESSAGE（7 段），将添加第 8 段
- `backend/core/agent_service.py` — Agent 创建处，需添加 `available_file_paths` 参数
- `backend/tests/unit/test_enhanced_prompt.py` — 现有 prompt 测试，需扩展文件上传测试

### browser-use 文件上传机制（只读参考）
- `.venv/lib/python3.11/site-packages/browser_use/tools/views.py:127-129` — UploadFileAction 模型：index（元素索引）+ path（文件路径）
- `.venv/lib/python3.11/site-packages/browser_use/tools/service.py:738-810` — upload_file action 实现：文件路径白名单校验、file input 元素查找、CDP DOM.setFileInputFiles
- `.venv/lib/python3.11/site-packages/browser_use/browser/watchdogs/default_action_watchdog.py:2576-2612` — on_UploadFileEvent：CDP DOM.setFileInputFiles 实际上传
- `.venv/lib/python3.11/site-packages/browser_use/browser/watchdogs/default_action_watchdog.py:348-354` — click file input 阻止：返回 validation_error

### 先前阶段上下文
- `.planning/phases/52-prompt/52-CONTEXT.md` — Phase 52 键盘操作 Prompt 决策（场景-动作对格式、否定指令模式、两 plan 结构）
- `.planning/phases/53-prompt/53-CONTEXT.md` — Phase 53 表格交互 Prompt 决策（追加段落模式、关键词测试检查）

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `backend/agent/prompts.py` ENHANCED_SYSTEM_MESSAGE：现有 7 段 prompt 结构（45 行），可直接追加第 8 段
- `backend/tests/unit/test_enhanced_prompt.py`：现有测试模式（关键词检查 + 行数限制），可扩展文件上传测试
- `backend/core/agent_service.py`：MonitoredAgent 创建处，已有 extend_system_message 注入，需添加 available_file_paths

### Established Patterns
- Agent 构造在 agent_service.py 中注入参数（Phase 49 D-07）
- 新段落追加模式：保留现有段落，追加新段（Phase 52 D-02、Phase 53 D-01）
- 场景-动作对格式："场景 → 动作"（Phase 52 D-01）
- Qwen 3.5 Plus 对精短指令遵守度更高（Phase 49 D-01）
- 测试模式：关键词检查 + 行数限制（Phase 52 D-10、Phase 53 D-10）

### Integration Points
- `prompts.py` — 追加文件上传段落到 ENHANCED_SYSTEM_MESSAGE（第 8 段）
- `agent_service.py` — 修改 MonitoredAgent 创建处，添加 available_file_paths 参数
- `test_enhanced_prompt.py` — 添加文件上传关键词断言
- `data/test-files/` — 新建测试文件目录，放置 Excel 和图片文件

### 关键技术约束
- browser-use 阻止 click 操作 file input 元素，返回 validation_error
- Agent 必须使用 `upload_file(index, path)` action 而非 click
- `upload_file` 需要文件路径在 `available_file_paths` 白名单中
- 文件必须存在于服务器本地文件系统
- 文件不能为空（0 bytes 会报错）

</code_context>

<specifics>
## Specific Ideas

- 文件上传 prompt 场景示例：
  - "导入 Excel → 定位 file input 元素，用 upload_file(index, 'data/test-files/import.xlsx') 上传"
  - "上传图片 → 定位图片上传 file input，用 upload_file(index, 'data/test-files/product.jpg') 上传"
- 需要否定指令：明确告知 Agent 不要 click file input 元素（会被 browser-use 拦截）
- 采购单导入页面通常有"导入"按钮，点击后出现 file input
- 商品管理中商品详情页通常有图片上传区域

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope.

</deferred>

---

*Phase: 54-import*
*Context gathered: 2026-03-31*
