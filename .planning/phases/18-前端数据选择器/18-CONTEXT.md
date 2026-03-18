# Phase 18: 前端数据选择器 - Context

**Gathered:** 2026-03-18
**Status:** Ready for planning

<domain>
## Phase Boundary

在前置条件编辑器中添加数据获取方法选择器组件，让 QA 用户可以可视化选择数据获取方法、配置参数、设置字段提取路径和变量名，自动生成 Python 代码。

**Scope:**
- 在 TaskForm 前置条件 textarea 旁添加数据获取按钮
- 实现多步骤 Modal 组件（方法选择 → 参数配置 → 提取路径 → 变量命名）
- 调用后端 API 获取数据方法列表和执行预览
- 支持一次配置多个数据获取
- 选中后生成代码追加到 textarea

**Out of Scope:**
- 后端 API 实现（Phase 17 已完成）
- 代码执行与变量传递（Phase 19）
- 修改 webseleniumerp 项目代码

</domain>

<decisions>
## Implementation Decisions

### UI 集成方式
- **单 Modal 多步骤**: 四步流程：选择方法 → 配置参数 → 提取路径 → 变量命名
- **自由跳转**: 顶部显示步骤条，用户可点击任意步骤跳转
- **按钮触发**: 在前置条件 textarea 旁边添加「获取数据」按钮
- **保留手动编辑**: 用户仍可手动编辑 textarea 中的代码

### 方法选择步骤
- **分组列表**: 按类名分组显示（如 BaseParams, InventoryParams）
- **搜索功能**: 支持按方法名或描述搜索
- **复选多选**: 用户可选择多个方法（支持一次配置多数据源）
- **显示信息**: 每个方法显示名称、描述、参数数量

### 参数配置步骤
- **动态表单**: 根据 API 返回的参数签名动态生成输入框
- **必填标记**: 必填参数标 * 号，可选参数不标记
- **类型提示**: 输入框 placeholder 显示参数类型（如 int, str）
- **默认值预填**: 如果参数有默认值，自动填入输入框

### 数据预览
- **显示原始 JSON**: 调用 execute API 后显示原始 JSON 数据
- **错误处理**: 数据获取失败时显示错误信息，用户可修改参数重试
- **加载状态**: 执行时显示 loading 状态

### 字段提取路径
- **可视化选择**: 点击 JSON 树中的字段自动生成路径（如 [0].imei）
- **JSON 树展示**: 可展开/折叠的树形结构显示 JSON 数据
- **支持多字段**: 可从同一次数据获取中提取多个字段

### 变量命名
- **默认值策略**: 使用字段名作为默认值（如提取 [0].imei 时默认为 imei）
- **用户可编辑**: 变量名输入框可自由编辑
- **冲突检测**: 相同变量名时提示覆盖或重命名

### 多数据源管理
- **卡片列表**: 每个数据获取配置显示为一个卡片
- **卡片内容**: 方法名、参数摘要、提取路径、变量名
- **操作按钮**: 每个卡片可编辑或删除

### 代码生成
- **单行模式**: `imei = context.get_data('inventory_list_data', i=2, j=13)[0]['imei']`
- **追加模式**: 生成的代码追加到现有代码后面
- **多次追加**: 用户可以多次打开选择器添加不同数据获取

### 错误处理与空状态
- **禁用按钮 + 提示**: 外部模块不可用 (503) 时按钮置灰
- **加载状态**: 获取方法列表时按钮显示 loading
- **空结果提示**: 没有匹配方法时显示提示信息

### Claude's Discretion
- Modal 的具体样式（圆角、阴影、动画）
- 步骤条的样式和位置
- JSON 树的展开/折叠图标
- 搜索防抖时间（建议 300ms）
- 卡片的具体布局和间距

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### 后端 API 参考
- `backend/api/routes/external_data_methods.py` — 数据获取方法 API 端点定义、请求/响应模型
- `backend/core/external_precondition_bridge.py` — 数据方法执行逻辑

### 前端现有代码
- `frontend/src/components/TaskModal/OperationCodeSelector.tsx` — 现有操作码选择器组件模式
- `frontend/src/components/TaskModal/TaskForm.tsx` — 现有前置条件 textarea 实现
- `frontend/src/types/index.ts` — 前端类型定义
- `frontend/src/api/client.ts` — API 客户端封装

### 前置阶段参考
- `.planning/phases/15-前端集成/15-CONTEXT.md` — Phase 15 决策（Modal 模式、搜索、代码追加）
- `.planning/phases/17-后端数据获取桥接/17-CONTEXT.md` — Phase 17 决策（API 响应结构、执行模式）

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `frontend/src/components/TaskModal/OperationCodeSelector.tsx`:
  - Modal 结构和样式模式
  - 分组列表显示
  - 搜索过滤逻辑
  - 已选标签显示
  - 可直接复用和扩展
- `frontend/src/components/shared/ConfirmModal.tsx`: Modal 组件模式
- `frontend/src/components/shared/LoadingSpinner.tsx`: 加载状态组件

### Established Patterns
- **表单状态管理**: React useState + 受控组件
- **Modal 模式**: 固定定位 + backdrop
- **搜索过滤**: useMemo + 实时过滤
- **错误提示**: toast.error (sonner 库)
- **样式**: Tailwind CSS

### API 响应结构
```typescript
// GET /api/external-data-methods
interface DataMethodsResponse {
  available: boolean
  classes: Array<{
    name: string  // 如 "BaseParams"
    methods: Array<{
      name: string  // 如 "inventory_list_data"
      description: string
      parameters: Array<{
        name: string
        type: string
        required: boolean
        default: string | null
      }>
    }>
  }>
  total: number
  error?: string
}

// POST /api/external-data-methods/execute
interface ExecuteRequest {
  class_name: string
  method_name: string
  params: Record<string, any>
}

interface ExecuteResponse {
  success: boolean
  data?: Array<Record<string, any>>
  error?: string
  error_type?: string
}
```

### Integration Points
- `frontend/src/components/TaskModal/TaskForm.tsx` — 需添加数据获取按钮和 Modal 触发逻辑
- `frontend/src/api/` — 需新建 `externalDataMethods.ts` API 模块
- `frontend/src/types/index.ts` — 需添加数据方法相关类型

</code_context>

<specifics>
## Specific Ideas

- 步骤条使用数字圆圈样式，当前步骤高亮
- JSON 树使用缩进 + 连接线表示层级
- 卡片使用浅色背景区分不同数据获取配置
- 变量名输入框实时显示生成的代码预览

</specifics>

<deferred>
## Deferred Ideas

- 数据预览高级功能（表格视图、搜索过滤）— v2 需求
- 最近使用的数据获取方法 — 后续优化
- 数据缓存机制 — v2 需求
- 链式数据获取 — v2 需求

</deferred>

---
*Phase: 18-前端数据选择器*
*Context gathered: 2026-03-18*
