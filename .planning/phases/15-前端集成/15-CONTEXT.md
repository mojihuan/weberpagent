# Phase 15: 前端集成 - Context

**Gathered:** 2026-03-18
**Status:** Ready for planning

<domain>
## Phase Boundary

在前置条件编辑器中添加操作码选择器组件，让 QA 用户可以可视化选择前置条件操作码（如 FA1, HC1），而不是手动编写 Python 代码。

**Scope:**
- 在 TaskForm 前置条件 textarea 旁添加操作码选择按钮
- 实现操作码选择器 Modal 组件（分组显示、搜索、多选）
- 调用后端 API 获取操作码列表并生成代码
- 选中操作码后追加代码到 textarea

**Out of Scope:**
- 后端 API 实现（Phase 14 已完成）
- 端到端验证测试（Phase 16）
- 修改 webseleniumerp 项目代码

</domain>

<decisions>
## Implementation Decisions

### UI 集成方式
- **按钮触发模式**: 在前置条件 textarea 旁边添加「选择操作码」按钮
- 点击按钮打开 Modal 选择器
- **保留手动编辑能力**: 用户仍可手动编辑 textarea 中的代码
- 按钮位置：textarea 上方或右侧，与「添加前置条件」按钮对齐

### 选择器 UI 形态
- **Modal 弹窗**: 弹出模态窗口显示操作码分组列表
- 适合一次性选择多个操作码的场景
- Modal 尺寸：中等宽度（约 600px），高度自适应
- 包含「确认」和「取消」按钮

### Modal 内部结构
- **顶部搜索框**: 支持按操作码（如 FA1）或描述搜索
- **分组列表**: 按模块分组显示（如「配件管理 - 采购」、「财务」）
- 每个操作码显示：代码 + 描述 + 复选框
- **已选区域**: 底部显示已选中操作码列表，每个带删除按钮

### 搜索功能
- **需要搜索**: Modal 中增加搜索框
- 搜索范围：操作码（code）+ 描述（description）
- 实时过滤，输入即搜索
- 无结果时显示「未找到匹配的操作码」

### 代码插入行为
- **追加模式**: 选中的操作码生成的代码追加到现有代码后面
- 如果 textarea 为空，直接填入
- 如果有内容，在末尾添加换行后追加
- 支持**多次追加**：用户可以多次打开选择器添加不同操作码

### 错误处理与空状态
- **禁用按钮 + 提示**: 外部模块不可用 (503) 时
  - 按钮置灰，不可点击
  - 显示提示信息：「外部前置条件模块不可用，请检查 WEBSERP_PATH 配置」
  - 可参考后端 503 响应中的 `detail.fix` 字段
- **加载状态**: 获取操作码列表时按钮显示 loading 状态

### Claude's Discretion
- Modal 的具体样式（圆角、阴影、动画）
- 分组列表的折叠/展开行为
- 搜索防抖时间（建议 300ms）
- 已选操作码的最大数量限制（如需要）

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### 后端 API 参考
- `backend/api/routes/external_operations.py` — 操作码 API 端点定义、请求/响应模型
- `backend/core/external_precondition_bridge.py` — 操作码解析和代码生成逻辑

### 前端现有代码
- `frontend/src/components/TaskModal/TaskForm.tsx` — 现有前置条件 textarea 实现
- `frontend/src/types/index.ts` — 前端类型定义
- `frontend/src/api/client.ts` — API 客户端封装

### 前置阶段参考
- `.planning/phases/14-后端桥接模块/14-CONTEXT.md` — Phase 14 决策（API 响应结构、代码生成模板）
- `.planning/phases/13-配置基础/13-CONTEXT.md` — Phase 13 决策（WEBSERP_PATH 配置）

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `frontend/src/components/shared/ConfirmModal.tsx`: 现有 Modal 组件模式 — 可参考实现
- `frontend/src/components/shared/LoadingSpinner.tsx`: 加载状态组件
- `frontend/src/api/client.ts`: API 客户端 — 直接调用 `/external-operations` 端点

### Established Patterns
- **表单状态管理**: React useState + 受控组件
- **Modal 模式**: ConfirmModal 使用固定定位 + backdrop
- **错误提示**: toast.error (sonner 库)
- **样式**: Tailwind CSS

### API 响应结构
```typescript
// GET /api/external-operations
interface OperationsResponse {
  available: boolean
  modules: Array<{
    name: string  // 如 "配件管理 - 采购"
    operations: Array<{
      code: string  // 如 "FA1"
      description: string
    }>
  }>
  total: number
  error?: string
}

// POST /api/external-operations/generate
interface GenerateRequest {
  operation_codes: string[]  // ["FA1", "HC1"]
}

interface GenerateResponse {
  code: string  // 生成的 Python 代码
}
```

### Integration Points
- `frontend/src/components/TaskModal/TaskForm.tsx` — 需添加操作码选择按钮和 Modal 触发逻辑
- `frontend/src/api/` — 可能需要新建 `externalOperations.ts` API 模块
- `frontend/src/types/index.ts` — 可能需要添加操作码相关类型

</code_context>

<specifics>
## Specific Ideas

- 搜索框应支持拼音首字母搜索（如输入 "cg" 匹配 "采购"）—— 可作为后续优化
- 已选操作码在 Modal 底部以标签形式显示，点击 × 移除
- 分组列表可折叠，方便用户聚焦特定模块

</specifics>

<deferred>
## Deferred Ideas

- 拼音搜索支持 — 后续优化
- 操作码详情预览 — 点击操作码显示完整描述
- 最近使用的操作码 — 记住用户常用选择
- 端到端验证测试 — Phase 16

</deferred>

---

*Phase: 15-前端集成*
*Context gathered: 2026-03-18*
