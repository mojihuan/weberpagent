# Phase 15: 前端集成 - Research

**Researched:** 2026-03-18
**Domain:** React Frontend, TypeScript, Modal Component, API Integration
**Confidence:** HIGH

## Summary

This phase implements a visual operation code selector for the precondition editor in TaskForm. Users will click a button to open a modal that displays operation codes grouped by module (from the webseleniumerp project), select multiple codes, and have Python code automatically generated and appended to the precondition textarea.

**Primary recommendation:** Create a new `OperationCodeSelector` modal component that follows existing project patterns (ConfirmModal, TaskFormModal). Use the existing `apiClient` pattern to fetch operations from `/external-operations` endpoint (Phase 14 complete). Store new types in `types/index.ts` and create new API module at `api/externalOperations.ts`.

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

#### UI 集成方式
- **按钮触发模式**: 在前置条件 textarea 旁边添加「选择操作码」按钮
- 点击按钮打开 Modal 选择器
- **保留手动编辑能力**: 用户仍可手动编辑 textarea 中的代码
- 按钮位置：textarea 上方或右侧，与「添加前置条件」按钮对齐

#### 选择器 UI 形态
- **Modal 弹窗**: 弹出模态窗口显示操作码分组列表
- 适合一次性选择多个操作码的场景
- Modal 尺寸：中等宽度（约 600px），高度自适应
- 包含「确认」和「取消」按钮

#### Modal 内部结构
- **顶部搜索框**: 支持按操作码（如 FA1）或描述搜索
- **分组列表**: 按模块分组显示（如「配件管理 - 采购」、「财务」）
- 每个操作码显示：代码 + 描述 + 复选框
- **已选区域**: 底部显示已选中操作码列表，每个带删除按钮

#### 搜索功能
- **需要搜索**: Modal 中增加搜索框
- 搜索范围：操作码（code）+ 描述（description）
- 实时过滤，输入即搜索
- 无结果时显示「未找到匹配的操作码」

#### 代码插入行为
- **追加模式**: 选中的操作码生成的代码追加到现有代码后面
- 如果 textarea 为空，直接填入
- 如果有内容，在末尾添加换行后追加
- 支持**多次追加**：用户可以多次打开选择器添加不同操作码

#### 错误处理与空状态
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

### Deferred Ideas (OUT OF SCOPE)
- 拼音搜索支持 — 后续优化
- 操作码详情预览 — 点击操作码显示完整描述
- 最近使用的操作码 — 记住用户常用选择
- 端到端验证测试 — Phase 16

</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| FRONT-01 | 前置条件编辑器中添加操作码选择器组件 | TaskForm.tsx analysis, ConfirmModal pattern, Component structure |
| FRONT-02 | 操作码按模块分组显示 (配件、财务、运营、平台等) | API response structure (OperationsResponse.modules), Grouped rendering pattern |
| FRONT-03 | 支持多选操作码 | useState with Set<string>, Checkbox UI pattern |
| FRONT-04 | 选中操作码后自动生成 Python 代码模板 | POST /api/external-operations/generate endpoint, Code insertion logic |

</phase_requirements>

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| react | 19.2.0 | UI framework | Project standard |
| typescript | 5.9.3 | Type safety | Project standard |
| lucide-react | 0.577.0 | Icons | Project standard (X, Check, ChevronDown, etc.) |
| sonner | 2.0.7 | Toast notifications | Project standard for error handling |
| tailwindcss | 4.2.1 | Styling | Project standard |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| @tanstack/react-query | 5.90.21 | Server state management | Already in project, but not required for this feature |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| Manual useState | react-query useQuery | react-query adds caching/refresh, but manual fetch is simpler for this use case |
| Custom debounce | lodash.debounce | Native setTimeout sufficient for 300ms delay |

**Installation:** No new dependencies required. All needed packages are in `frontend/package.json`.

## Architecture Patterns

### Recommended Component Structure
```
frontend/src/
├── api/
│   └── externalOperations.ts     # NEW: API module for external-operations endpoint
├── components/
│   ├── TaskModal/
│   │   ├── TaskForm.tsx          # MODIFY: Add selector button
│   │   └── OperationCodeSelector.tsx  # NEW: Modal component
│   └── shared/
│       ├── ConfirmModal.tsx      # REFERENCE: Modal pattern
│       └── LoadingSpinner.tsx    # REFERENCE: Loading state
└── types/
    └── index.ts                  # MODIFY: Add external operation types
```

### Pattern 1: Modal Component Structure
**What:** Fixed overlay with backdrop, centered content, z-index 50
**When to use:** All modal dialogs in this project
**Example:**
```typescript
// Source: frontend/src/components/shared/ConfirmModal.tsx (lines 32-62)
// Pattern: fixed inset-0 z-50, backdrop with onClick, relative content

export function OperationCodeSelector({ open, onClose, onConfirm }: Props) {
  if (!open) return null

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center">
      <div className="fixed inset-0 bg-black/50" onClick={onClose} />
      <div className="relative bg-white rounded-xl shadow-xl w-full max-w-2xl mx-4 max-h-[80vh] overflow-hidden">
        {/* Modal content */}
      </div>
    </div>
  )
}
```

### Pattern 2: API Client Usage
**What:** Use existing apiClient wrapper for all API calls
**When to use:** All frontend API requests
**Example:**
```typescript
// Source: frontend/src/api/tasks.ts (lines 1-14)
// Pattern: Named export object with async methods using apiClient

import { apiClient } from './client'

export const externalOperationsApi = {
  async list(): Promise<OperationsResponse> {
    return apiClient<OperationsResponse>('/external-operations')
  },

  async generate(operationCodes: string[]): Promise<GenerateResponse> {
    return apiClient<GenerateResponse>('/external-operations/generate', {
      method: 'POST',
      body: JSON.stringify({ operation_codes: operationCodes }),
    })
  },
}
```

### Pattern 3: Form State Management
**What:** React useState with controlled components, immutable updates
**When to use:** All form state in this project
**Example:**
```typescript
// Source: frontend/src/components/TaskModal/TaskForm.tsx (lines 89-105)
// Pattern: useState for form data, immutable updates with spread operator

const [selectedCodes, setSelectedCodes] = useState<Set<string>>(new Set())

const handleToggleCode = (code: string) => {
  setSelectedCodes(prev => {
    const next = new Set(prev)
    if (next.has(code)) {
      next.delete(code)
    } else {
      next.add(code)
    }
    return next
  })
}
```

### Anti-Patterns to Avoid
- **Direct DOM manipulation:** Never use `document.getElementById` for form values; use React state
- **Mutation of state:** Always create new arrays/objects when updating state
- **Inline styles:** Use Tailwind classes consistently
- **Hardcoded API URLs:** Use API_BASE from client.ts

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Toast notifications | Custom toast | sonner toast | Already integrated, handles auto-dismiss |
| Loading state | Custom spinner | LoadingSpinner component | Already exists in shared/ |
| API error handling | Custom error logic | apiClient (auto-retry, toast) | Built-in network retry, error toasts |
| Modal backdrop | Custom overlay | Existing modal pattern | Consistent UX, proven z-index handling |

**Key insight:** The project has established patterns for modals, API calls, and loading states. Reuse these patterns for consistency and reduced risk.

## Common Pitfalls

### Pitfall 1: 503 Error Not Handled Gracefully
**What goes wrong:** Button remains clickable when external module unavailable, user gets confusing error
**Why it happens:** Not checking `available` flag before enabling button
**How to avoid:** Fetch operations on component mount, check `response.available` and `error` field, disable button when unavailable
**Warning signs:** Button shows loading forever, or user sees generic "请求失败" toast

### Pitfall 2: Code Insertion Not Handling Empty Textarea
**What goes wrong:** Generated code not properly formatted when textarea is empty vs has existing content
**Why it happens:** Not checking if existing value is empty or has trailing newline
**How to avoid:**
```typescript
const appendCode = (existing: string, newCode: string) => {
  if (!existing.trim()) return newCode
  return existing.endsWith('\n') ? existing + newCode : existing + '\n' + newCode
}
```
**Warning signs:** Code has double newlines or no newline between existing and new code

### Pitfall 3: Search Not Filtering Grouped Data
**What goes wrong:** Search only filters flat list, groups remain visible even when empty
**Why it happens:** Not filtering at module level, only at operation level
**How to avoid:** Filter modules array, remove empty modules after filtering operations
**Warning signs:** Empty groups shown when searching, or groups not updating

### Pitfall 4: Selection State Lost on Modal Reopen
**What goes wrong:** User selections cleared when closing and reopening modal
**Why it happens:** Selection state inside modal component, reset on unmount
**How to avoid:** Either lift selection state to parent, or accept as acceptable UX (fresh selection each open)
**Warning signs:** User complaints about lost selections

## Code Examples

### API Types (for types/index.ts)
```typescript
// Source: Backend API contract from external_operations.py

export interface OperationItem {
  code: string
  description: string
}

export interface ModuleGroup {
  name: string
  operations: OperationItem[]
}

export interface OperationsResponse {
  available: boolean
  modules: ModuleGroup[]
  total: number
  error?: string
}

export interface GenerateRequest {
  operation_codes: string[]
}

export interface GenerateResponse {
  code: string
}
```

### Debounced Search Hook
```typescript
// Pattern: 300ms debounce for search input
import { useState, useEffect } from 'react'

function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState(value)

  useEffect(() => {
    const handler = setTimeout(() => setDebouncedValue(value), delay)
    return () => clearTimeout(handler)
  }, [value, delay])

  return debouncedValue
}

// Usage in component
const [searchQuery, setSearchQuery] = useState('')
const debouncedQuery = useDebounce(searchQuery, 300)

useEffect(() => {
  // Filter operations based on debouncedQuery
}, [debouncedQuery])
```

### Grouped Filtering Logic
```typescript
// Pattern: Filter operations within modules, remove empty modules
const filterModules = (modules: ModuleGroup[], query: string): ModuleGroup[] => {
  if (!query.trim()) return modules

  const lowerQuery = query.toLowerCase()
  return modules
    .map(module => ({
      ...module,
      operations: module.operations.filter(
        op => op.code.toLowerCase().includes(lowerQuery) ||
              op.description.toLowerCase().includes(lowerQuery)
      )
    }))
    .filter(module => module.operations.length > 0)
}
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Class components | Functional components with hooks | Project start | Simpler state management |
| CSS modules | Tailwind CSS | Project start | Faster styling, no CSS files |
| Prop drilling | Context (minimal) | Project start | Limited scope, useState sufficient |

**Deprecated/outdated:**
- None relevant to this phase; project uses modern React patterns

## Open Questions

1. **Should selection persist across modal opens?**
   - What we know: CONTEXT.md doesn't specify, says "Claude's Discretion"
   - What's unclear: User preference for keeping selections
   - Recommendation: Start fresh each modal open (simpler), add persistence if users request it

2. **Should groups be collapsible?**
   - What we know: CONTEXT.md says "Claude's Discretion"
   - What's unclear: Complexity vs. utility tradeoff
   - Recommendation: Start with all groups expanded (simpler), add collapse if many groups exist

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | None configured (frontend has no test setup) |
| Config file | None |
| Quick run command | N/A |
| Full suite command | N/A |

### Phase Requirements -> Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| FRONT-01 | Selector button renders, triggers modal | Manual | N/A | N/A |
| FRONT-02 | Operations grouped by module | Manual | N/A | N/A |
| FRONT-03 | Multiple selection with checkboxes | Manual | N/A | N/A |
| FRONT-04 | Code generated and appended | Manual | N/A | N/A |

### Sampling Rate
- **Per task commit:** Manual verification in browser
- **Per wave merge:** Manual E2E test
- **Phase gate:** Full manual test before /gsd:verify-work

### Wave 0 Gaps
- [ ] `frontend/vitest.config.ts` - Vitest configuration
- [ ] `frontend/src/__tests__/` - Test directory
- [ ] `frontend/package.json` - Add vitest, @testing-library/react
- [ ] Framework install: `cd frontend && npm install -D vitest @testing-library/react jsdom`

**Note:** Frontend has no test infrastructure. This phase will rely on manual testing. Consider adding test infrastructure in a future phase.

## Sources

### Primary (HIGH confidence)
- `frontend/src/components/TaskModal/TaskForm.tsx` - Current precondition editor implementation
- `frontend/src/components/shared/ConfirmModal.tsx` - Modal pattern reference
- `frontend/src/api/client.ts` - API client pattern
- `backend/api/routes/external_operations.py` - API contract definition
- `backend/core/external_precondition_bridge.py` - Code generation logic

### Secondary (MEDIUM confidence)
- `frontend/src/api/tasks.ts` - API module pattern reference
- `frontend/src/types/index.ts` - Type definition patterns
- `frontend/package.json` - Dependency versions

### Tertiary (LOW confidence)
- N/A - All findings verified from project source code

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - All dependencies already in project
- Architecture: HIGH - Clear existing patterns to follow
- Pitfalls: HIGH - Based on analysis of existing code and common React issues

**Research date:** 2026-03-18
**Valid until:** 30 days (stable React patterns, project-specific code)
