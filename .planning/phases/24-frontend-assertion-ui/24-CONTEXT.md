# Phase 24: Frontend Assertion UI - Context

**Gathered:** 2026-03-20
**Status:** Ready for planning

<domain>
## Phase Boundary

在 TaskForm 中添加断言选择器组件，让 QA 用户可以可视化选择断言方法、配置参数（headers、data、i/j/k），配置存储为结构化数据供 Phase 25 执行引擎使用。

**Scope:**
- 创建 AssertionSelector 组件（单步 Modal，按类分组 + 搜索）
- 实现 headers/data 下拉选择、i/j/k 参数配置（下拉或输入框）
- 支持多选断言方法
- TaskForm 新增「断言」区域（Tab 切换接口断言/业务断言）
- 新增 `assertions` 字段存储结构化配置

**Out of Scope:**
- 后端断言执行引擎（Phase 25）
- Agent 完成检测机制（Phase 25）
- 断言结果展示（Phase 25+）

</domain>

<decisions>
## Implementation Decisions

### 组件模式
- **单步 Modal**: 类似 OperationCodeSelector，一个 Modal 包含分组列表 + 参数配置
- **不分步**: 断言配置比数据获取简单，无需 4 步向导
- **Modal 结构**:
  1. 顶部：搜索框
  2. 左侧：按类分组的断言方法列表（可折叠）
  3. 右侧/下方：已选断言的参数配置区
  4. 底部：确认/取消按钮

### UI 布局
- **断言区域改造**: 将现有「接口断言」区域改为「断言」区域
- **Tab 切换**:
  - Tab 1: 「接口断言」— 现有 Python 代码 textarea
  - Tab 2: 「业务断言」— 结构化配置区域
- **业务断言 UI**:
  - 顶部：添加断言按钮
  - 中部：已配置断言卡片列表
  - 每个卡片：方法名 + 参数摘要 + 编辑/删除按钮

### 数据存储
- **新字段**: `assertions: AssertionConfig[]`
- **不修改 `api_assertions`**: 保持为 `string[]`（Python 代码）
- **AssertionConfig 结构**:
  ```typescript
  interface AssertionConfig {
    className: string      // 如 "PcAssert"
    methodName: string     // 如 "attachment_inventory_list_assert"
    headers: string        // 如 "main"
    data: string           // 如 "main"
    params: Record<string, number | string>  // i, j, k 等参数
  }
  ```

### 方法选择
- **分组显示**: 按类分组（PcAssert, MgAssert, McAssert）
- **可折叠分组**: 默认展开第一个类，其他折叠
- **搜索功能**: 支持按方法名或描述搜索
- **多选支持**: 用户可选择多个断言方法
- **已选展示**: 选中后显示为标签，可单独删除

### 参数配置
- **headers 参数**: 下拉菜单，选项固定为 `['main', 'idle', 'vice', 'special', 'platform', 'super', 'camera']`
- **data 参数**: 下拉菜单，选项从 API 响应的 `data_options` 获取
- **i/j/k 参数**:
  - 有选项时：下拉菜单（如 `1: 待发货, 2: 待取件`）
  - 无选项时：输入框（自由输入）
  - 选项说明：显示在输入框旁作为提示

### 执行时机
- **Agent 完成后执行**: 业务断言在 Browser-Use agent 完成所有步骤后执行
- **Phase 25 职责**: 检测 agent 完成事件，读取 assertions 配置，执行断言
- **配置存储**: 不生成 Python 代码，存为结构化 JSON 供 Phase 25 解析

### 错误处理与空状态
- **外部模块不可用**: 按钮置灰 + 提示信息
- **加载状态**: 获取方法列表时显示 loading
- **空结果提示**: 没有匹配方法时显示提示

### Claude's Discretion
- Modal 的具体样式（宽度、圆角、阴影）
- 卡片的具体布局和间距
- 搜索防抖时间（建议 300ms）
- Tab 切换动画

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### 后端 API 参考
- `backend/api/routes/external_assertions.py` — 断言方法 API 端点定义、请求/响应模型
- `backend/core/external_precondition_bridge.py` — 断言方法发现逻辑（Phase 23 已扩展）

### 前端现有代码
- `frontend/src/components/TaskModal/OperationCodeSelector.tsx` — 单步 Modal 模式参考
- `frontend/src/components/TaskModal/DataMethodSelector.tsx` — 分组列表、搜索、多选模式参考
- `frontend/src/components/TaskModal/TaskForm.tsx` — 需改造断言区域
- `frontend/src/types/index.ts` — 需添加 AssertionConfig 类型
- `frontend/src/api/client.ts` — 需添加断言 API 调用

### 前置阶段参考
- `.planning/phases/23-backend-assertion-discovery/23-CONTEXT.md` — Phase 23 决策（API 响应结构、headers_options、data_options）
- `.planning/phases/18-前端数据选择器/18-CONTEXT.md` — Phase 18 决策（Modal 模式、搜索、分组）

### 研究文档
- `.planning/research/ARCHITECTURE.md` — ExternalPreconditionBridge 架构设计
- `.planning/research/PITFALLS.md` — 断言集成陷阱

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `frontend/src/components/TaskModal/OperationCodeSelector.tsx`:
  - 单步 Modal 结构
  - 分组列表 + 搜索模式
  - 多选逻辑
  - ESC 键关闭
  - 可直接复用大部分代码
- `frontend/src/components/TaskModal/DataMethodSelector.tsx`:
  - 可折叠分组实现
  - 参数配置 UI 模式
  - 可参考但断言不需要 4 步

### Established Patterns
- **表单状态管理**: React useState + 受控组件
- **Modal 模式**: 固定定位 + backdrop
- **搜索过滤**: useMemo + 实时过滤
- **错误提示**: toast.error (sonner 库)
- **样式**: Tailwind CSS

### API 响应结构（Phase 23 已实现）
```typescript
// GET /api/external-assertions/methods
interface AssertionMethodsResponse {
  available: boolean
  headers_options: string[]  // ['main', 'idle', 'vice', ...]
  classes: Array<{
    name: string  // 如 "PcAssert"
    methods: Array<{
      name: string
      description: string
      data_options: string[]  // ['main', 'a', 'b', ...]
      parameters: Array<{
        name: string
        description: string
        options: Array<{ value: number, label: string }>
      }>
    }>
  }>
  total: number
  error?: string
}
```

### Integration Points
- `frontend/src/components/TaskModal/TaskForm.tsx`:
  - 需改造「接口断言」区域为 Tab 切换
  - 需添加 AssertionSelector Modal 触发逻辑
  - 需处理 assertions 配置数据
- `frontend/src/types/index.ts`:
  - 需添加 AssertionConfig 类型
  - 需更新 CreateTaskDto、Task 类型
- `frontend/src/api/`:
  - 需新建 `externalAssertions.ts` API 模块
- `backend/api/routes/tasks.py`:
  - 需支持 assertions 字段的 CRUD

</code_context>

<specifics>
## Specific Ideas

- 断言卡片用浅色背景区分（如橙色边框表示业务断言）
- Tab 切换使用 pill 样式（圆角胶囊）
- 搜索框 placeholder: "搜索断言方法..."
- 已选断言显示为标签，点击 × 删除

</specifics>

<deferred>
## Deferred Ideas

- 断言执行引擎 — Phase 25
- Agent 完成检测机制 — Phase 25
- 断言结果展示 — Phase 25+
- 断言执行预览（在 Modal 中测试断言）— 未来优化
- 最近使用的断言方法 — 后续优化

</deferred>

---
*Phase: 24-frontend-assertion-ui*
*Context gathered: 2026-03-20*
