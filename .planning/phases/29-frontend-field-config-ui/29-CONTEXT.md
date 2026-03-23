# Phase 29: 前端字段配置 UI - Context

**Gathered:** 2026-03-22
**Status:** Ready for planning

<domain>
## Phase Boundary

扩展 AssertionSelector 组件，支持三层参数配置（data、api_params、field_params），让 QA 用户可以为断言方法配置字段验证参数（如 `statusStr='已完成'`, `createTime='now'`）。此阶段专注于前端 UI 实现，后端字段发现（Phase 28）已完成，执行适配层（Phase 30）在后续阶段。

**Scope:**
- 扩展 AssertionConfig 类型，增加 `field_params` 字段
- 创建 FieldParamsEditor 组件（按分组浏览、搜索 300+ 字段）
- 时间字段值输入支持 "now" 快捷按钮
- 支持添加/删除多个字段配置
- 复用 Phase 28 的 `/api/external-assertions/fields` API

**Out of Scope:**
- 后端执行适配层（Phase 30）
- E2E 测试（Phase 31）
- 修改 base_assert.py

</domain>

<decisions>
## Implementation Decisions

### 三区域布局（采用 ROADMAP.md 设计）
- **D-01:** 断言配置弹窗分为三个垂直区域：
  1. 查询方法 (data) 选择
  2. API 筛选参数 (api_params) 配置
  3. 断言字段 (field_params) 配置
- **D-02:** 每个区域使用卡片式设计，边界清晰
- **D-03:** 复用现有 AssertionSelector Modal 结构

### 字段选择 UI 模式
- **D-04:** 复用现有可折叠分组模式（与断言方法选择一致）
- **D-05:** 支持搜索字段（按字段名和描述）
- **D-06:** 分组显示：销售相关、采购相关、库存相关、时间字段、通用字段
- **D-07:** 每个字段显示：checkbox + 字段名 + 描述 + 值输入框

### 字段值输入
- **D-08:** 普通字段：自由文本输入框
- **D-09:** 时间字段：输入框 + "now" 快捷按钮（点击后填入字符串 "now"）
- **D-10:** "now" 语义：前端传 "now" 字符串，后端在执行时转换为当前时间

### 多字段配置
- **D-11:** 支持添加/删除多个字段配置
- **D-12:** 每个字段配置包含：字段名、预期值
- **D-13:** 已配置字段显示为卡片列表，可编辑/删除

### 数据结构更新
- **D-14:** 扩展 AssertionConfig 类型：
  ```typescript
  interface AssertionConfig {
    className: string      // 如 "PcAssert"
    methodName: string     // 如 "attachment_inventory_list_assert"
    data: string           // 如 "main"
    api_params: {          // API 筛选参数
      i?: number
      j?: number
      k?: number
      headers?: string     // 如 "main"
    }
    field_params: Record<string, string>  // 字段验证参数
  }
  ```
- **D-15:** 向后兼容：`headers` 保留在顶层，同时支持 `api_params.headers`

### Claude's Discretion
- Modal 的具体宽度和高度
- 卡片的具体样式（圆角、阴影、边框）
- 搜索防抖时间（建议 300ms）
- 空状态提示文案

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### 前置阶段参考
- `.planning/phases/24-frontend-assertion-ui/24-CONTEXT.md` — Phase 24 决策（AssertionSelector 组件模式、参数配置 UI）
- `.planning/phases/28-backend-field-discovery/28-CONTEXT.md` — Phase 28 决策（字段 API 响应结构、分组规则）

### 后端 API 参考
- `backend/api/routes/external_assertions.py` — 断言方法 API 和字段 API 端点
- `backend/core/external_precondition_bridge.py` — 字段发现逻辑

### 前端现有代码
- `frontend/src/components/TaskModal/AssertionSelector.tsx` — 需扩展支持 field_params
- `frontend/src/types/index.ts` — 需更新 AssertionConfig 类型
- `frontend/src/api/externalAssertions.ts` — 需添加字段列表 API 调用

### 研究文档
- `.planning/ROADMAP.md` — Phase 29 UI Layout 设计（第 130-154 行）

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `frontend/src/components/TaskModal/AssertionSelector.tsx`:
  - 可折叠分组实现（`expandedPanels` state）
  - 搜索过滤逻辑（`filteredClasses` useMemo）
  - 参数配置 UI 模式
  - 可直接扩展支持 field_params
- `frontend/src/types/index.ts`:
  - `AssertionConfig` 类型定义
  - `AssertionMethodsResponse` 类型定义

### Established Patterns
- **表单状态管理**: React useState + 受控组件
- **Modal 模式**: 固定定位 + backdrop
- **搜索过滤**: useMemo + 实时过滤
- **分组展示**: 可折叠 Accordion
- **样式**: Tailwind CSS

### API 响应结构（Phase 28 已实现）
```typescript
// GET /api/external-assertions/fields
interface AssertionFieldsResponse {
  available: boolean
  groups: Array<{
    name: string  // 如 "销售相关"
    fields: Array<{
      name: string          // 如 "salesOrder"
      path: string          // 如 "salesOrder"
      is_time_field: boolean
      description: string   // 如 "销售订单"
    }>
  }>
  total: number
  error?: string
}
```

### Integration Points
- `frontend/src/components/TaskModal/AssertionSelector.tsx`:
  - 需添加 field_params 配置区域
  - 需调用 `/api/external-assertions/fields` API
- `frontend/src/types/index.ts`:
  - 需更新 AssertionConfig 类型
  - 需添加 AssertionFieldsResponse 类型
- `frontend/src/api/externalAssertions.ts`:
  - 需添加 `listFields()` 方法

### 需要新增的代码
| 组件 | 目的 | 参考模式 |
|------|------|----------|
| `FieldParamsEditor.tsx` | 字段选择 + 值配置组件 | 复制 AssertionSelector 分组逻辑 |
| `externalAssertions.listFields()` | 获取字段列表 API | 复用现有 apiClient |
| AssertionConfig 类型扩展 | 添加 field_params 字段 | 保持向后兼容 |

</code_context>

<specifics>
## Specific Ideas

- 时间字段输入框旁显示 "now" 按钮（蓝色小按钮）
- 已配置字段显示为标签，点击 × 删除
- 搜索框 placeholder: "搜索字段..."
- 分组标题显示字段数量（如 "销售相关 (15)"）

</specifics>

<deferred>
## Deferred Ideas

- 断言执行适配层 — Phase 30
- E2E 测试 — Phase 31
- 字段值预设选项（从历史记录学习）— 未来优化
- 最近使用的字段 — 后续优化

</deferred>

---
*Phase: 29-frontend-field-config-ui*
*Context gathered: 2026-03-22*
