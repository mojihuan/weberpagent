# Phase 29: 前端字段配置 UI - Research

**Researched:** 2026-03-22
**Domain:** React Frontend UI Components, Form State Management
**Confidence:** HIGH

## Summary

This phase extends the existing `AssertionSelector` component to support three-layer parameter configuration (data, api_params, field_params). The backend fields API is already complete from Phase 28, returning ~300 fields grouped by category. The implementation involves creating a new `FieldParamsEditor` sub-component that handles field selection with grouping, search, and "now" quick-button for time fields.

**Primary recommendation:** Extract field configuration into a dedicated `FieldParamsEditor` component, reuse the existing collapsible group pattern from `AssertionSelector`, and extend the `AssertionConfig` type to include `field_params: Record<string, string>`.

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions
- **D-01:** 断言配置弹窗分为三个垂直区域：1. 查询方法 (data) 选择，2. API 筛选参数 (api_params) 配置，3. 断言字段 (field_params) 配置
- **D-02:** 每个区域使用卡片式设计，边界清晰
- **D-03:** 复用现有 AssertionSelector Modal 结构
- **D-04:** 复用现有可折叠分组模式（与断言方法选择一致）
- **D-05:** 支持搜索字段（按字段名和描述）
- **D-06:** 分组显示：销售相关、采购相关、库存相关、时间字段、通用字段
- **D-07:** 每个字段显示：checkbox + 字段名 + 描述 + 值输入框
- **D-08:** 普通字段：自由文本输入框
- **D-09:** 时间字段：输入框 + "now" 快捷按钮（点击后填入字符串 "now"）
- **D-10:** "now" 语义：前端传 "now" 字符串，后端在执行时转换为当前时间
- **D-11:** 支持添加/删除多个字段配置
- **D-12:** 每个字段配置包含：字段名、预期值
- **D-13:** 已配置字段显示为卡片列表，可编辑/删除
- **D-14:** 扩展 AssertionConfig 类型（详见 CONTEXT.md）
- **D-15:** 向后兼容：headers 保留在顶层，同时支持 api_params.headers

### Claude's Discretion
- Modal 的具体宽度和高度
- 卡片的具体样式（圆角、阴影、边框）
- 搜索防抖时间（建议 300ms）
- 空状态提示文案

### Deferred Ideas (OUT OF SCOPE)
- 断言执行适配层 — Phase 30
- E2E 测试 — Phase 31
- 字段值预设选项（从历史记录学习）— 未来优化
- 最近使用的字段 — 后续优化

</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| UI-01 | 断言配置弹窗分为三个区域：data 选择、api_params、field_params | Three-layer layout pattern from ROADMAP.md lines 130-154; existing AssertionSelector structure provides foundation |
| UI-02 | field_params 支持按分组浏览、搜索字段（300+ 字段按命名模式分组） | Phase 28 API returns grouped fields; existing collapsible panel pattern in AssertionSelector.tsx lines 276-323 |
| UI-03 | 时间字段值输入有 "now" 快捷按钮 | API returns `is_time_field: boolean`; conditional button rendering pattern |
| UI-04 | 支持添加/删除多个字段配置 | Existing Map-based state pattern in AssertionSelector.tsx lines 31, 116-140 |
</phase_requirements>

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| React | 19.2.0 | UI framework | Project standard |
| TypeScript | 5.9.3 | Type safety | Project standard |
| Tailwind CSS | 4.2.1 | Styling | Project standard |
| lucide-react | 0.577.0 | Icons | Existing icons: Search, X, ChevronDown |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| @tanstack/react-query | 5.90.21 | API state management | Fetching fields from `/api/external-assertions/fields` |
| sonner | 2.0.7 | Toast notifications | Error handling (already in use) |

### No New Dependencies Required
All necessary dependencies are already installed. The implementation reuses existing patterns.

## Architecture Patterns

### Recommended Project Structure
```
frontend/src/
├── components/TaskModal/
│   ├── AssertionSelector.tsx      # Extend: add FieldParamsEditor integration
│   ├── FieldParamsEditor.tsx      # NEW: Field selection + value configuration
│   └── ...
├── types/
│   └── index.ts                   # Extend: add field_params to AssertionConfig
└── api/
    └── externalAssertions.ts      # Extend: add listFields() method
```

### Pattern 1: Collapsible Group Pattern (Reuse from AssertionSelector)
**What:** Accordion-style groups with expand/collapse, checkbox selection, search filtering
**When to use:** FieldParamsEditor needs identical pattern for 300+ fields across ~6 groups
**Example:**
```tsx
// Source: frontend/src/components/TaskModal/AssertionSelector.tsx lines 276-323
const togglePanel = (groupName: string) => {
  setExpandedPanels(prev => {
    const next = new Set(prev)
    if (next.has(groupName)) {
      next.delete(groupName)
    } else {
      next.add(groupName)
    }
    return next
  })
}

// Filtered groups with search
const filteredGroups = useMemo(() => {
  if (!searchQuery.trim()) return groups
  const query = searchQuery.toLowerCase()
  return groups
    .map(group => ({
      ...group,
      fields: group.fields.filter(
        f => f.name.toLowerCase().includes(query) ||
             f.description.toLowerCase().includes(query)
      )
    }))
    .filter(group => group.fields.length > 0)
}, [groups, searchQuery])
```

### Pattern 2: Map-based State for Multi-Select with Values
**What:** Use `Map<string, FieldConfig>` to track selected fields and their values
**When to use:** FieldParamsEditor needs to track both selection and value per field
**Example:**
```tsx
// Source: AssertionSelector.tsx lines 31, 116-140 (adapted for field_params)
interface FieldParamValue {
  name: string
  value: string
}

const [selectedFields, setSelectedFields] = useState<Map<string, FieldParamValue>>(new Map())

const updateFieldValue = (fieldName: string, value: string) => {
  setSelectedFields(prev => {
    const next = new Map(prev)
    const existing = next.get(fieldName)
    if (existing) {
      next.set(fieldName, { ...existing, value })
    }
    return next
  })
}
```

### Pattern 3: Conditional "now" Button for Time Fields
**What:** Render "now" button only when `is_time_field: true`
**Example:**
```tsx
// Source: ROADMAP.md design (lines 148-152)
{field.is_time_field && (
  <button
    type="button"
    onClick={() => updateFieldValue(field.name, 'now')}
    className="px-2 py-1 text-xs bg-blue-100 text-blue-700 rounded hover:bg-blue-200"
  >
    now
  </button>
)}
```

### Anti-Patterns to Avoid
- **Storing field_params as nested state:** Use flat `Record<string, string>` not nested objects
- **Not memoizing filtered groups:** 300+ fields need useMemo for search performance
- **Inline styles:** Use Tailwind classes consistently with existing components

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Search debounce | Custom setTimeout | useMemo + controlled input | React's controlled input is sufficient for this use case; 300ms visual delay acceptable |
| Modal structure | New Modal component | Copy AssertionSelector.tsx structure | Consistent UX, proven pattern |
| Group accordion | Custom accordion | Copy from AssertionSelector.tsx lines 276-323 | Reuses tested pattern |

**Key insight:** The existing AssertionSelector already implements all needed patterns. The FieldParamsEditor should be extracted as a sub-component with identical structure.

## Common Pitfalls

### Pitfall 1: State Synchronization Between Components
**What goes wrong:** FieldParamsEditor state not syncing with parent AssertionSelector
**Why it happens:** React state updates are asynchronous; Map mutations need immutable patterns
**How to avoid:** Use callback props to propagate changes; always create new Map instances
**Warning signs:** Selected fields not appearing in confirmation payload

### Pitfall 2: Missing Type Extension
**What goes wrong:** TypeScript errors when accessing `config.field_params`
**Why it happens:** AssertionConfig type not updated to include field_params
**How to avoid:** Update types/index.ts first; ensure backward compatibility with existing assertions
**Warning signs:** `Property 'field_params' does not exist on type 'AssertionConfig'`

### Pitfall 3: Search Performance with 300+ Fields
**What goes wrong:** UI lag when typing in search box
**Why it happens:** Filtering 300+ items on every keystroke without memoization
**How to avoid:** Use useMemo for filtered results; consider adding 300ms debounce if still slow
**Warning signs:** Noticeable delay between keystroke and results update

### Pitfall 4: API Error Handling
**What goes wrong:** Fields API returns 503 when external module unavailable
**Why it happens:** WEBSERP_PATH not configured or module not found
**How to avoid:** Reuse error handling pattern from AssertionSelector.tsx lines 161-162, 257-267
**Warning signs:** "External assertion fields not available" error

## Code Examples

### Type Extension (types/index.ts)
```typescript
// Source: CONTEXT.md decision D-14
export interface AssertionConfig {
  className: string      // e.g., "PcAssert"
  methodName: string     // e.g., "attachment_inventory_list_assert"
  headers: string        // e.g., "main" - backward compatible
  data: string           // e.g., "main"
  params: Record<string, number | string>  // i, j, k etc. filter parameters
  field_params: Record<string, string>     // NEW: field validation parameters
}

// NEW: API response types for fields
export interface AssertionFieldInfo {
  name: string
  path: string
  is_time_field: boolean
  description: string
}

export interface AssertionFieldGroup {
  name: string
  fields: AssertionFieldInfo[]
}

export interface AssertionFieldsResponse {
  available: boolean
  groups: AssertionFieldGroup[]
  total: number
  error?: string
}
```

### API Extension (api/externalAssertions.ts)
```typescript
// Add to existing externalAssertionsApi object
export const externalAssertionsApi = {
  async list(): Promise<AssertionMethodsResponse> {
    return apiClient<AssertionMethodsResponse>('/external-assertions/methods')
  },

  // NEW: Fetch available assertion fields
  async listFields(): Promise<AssertionFieldsResponse> {
    return apiClient<AssertionFieldsResponse>('/external-assertions/fields')
  },
}
```

### FieldParamsEditor Component Structure
```tsx
// Source: Pattern derived from AssertionSelector.tsx
interface FieldParamsEditorProps {
  selectedFields: Map<string, { name: string; value: string }>
  onChange: (fields: Map<string, { name: string; value: string }>) => void
}

export function FieldParamsEditor({ selectedFields, onChange }: FieldParamsEditorProps) {
  const [groups, setGroups] = useState<AssertionFieldGroup[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [searchQuery, setSearchQuery] = useState('')
  const [expandedPanels, setExpandedPanels] = useState<Set<string>>(new Set())

  // Fetch fields on mount
  useEffect(() => {
    const fetchFields = async () => {
      setLoading(true)
      try {
        const response = await externalAssertionsApi.listFields()
        if (response.available) {
          setGroups(response.groups)
          // Expand first group by default
          if (response.groups.length > 0) {
            setExpandedPanels(new Set([response.groups[0].name]))
          }
        } else {
          setError(response.error || 'Fields not available')
        }
      } catch {
        setError('Failed to load fields')
      } finally {
        setLoading(false)
      }
    }
    fetchFields()
  }, [])

  // Filter groups based on search
  const filteredGroups = useMemo(() => {
    if (!searchQuery.trim()) return groups
    const query = searchQuery.toLowerCase()
    return groups
      .map(group => ({
        ...group,
        fields: group.fields.filter(
          f => f.name.toLowerCase().includes(query) ||
               f.description.toLowerCase().includes(query)
        )
      }))
      .filter(group => group.fields.length > 0)
  }, [groups, searchQuery])

  // Toggle field selection
  const toggleField = (field: AssertionFieldInfo) => {
    onChange(prev => {
      const next = new Map(prev)
      if (next.has(field.name)) {
        next.delete(field.name)
      } else {
        next.set(field.name, { name: field.name, value: '' })
      }
      return next
    })
  }

  // Update field value
  const updateFieldValue = (fieldName: string, value: string) => {
    onChange(prev => {
      const next = new Map(prev)
      const existing = next.get(fieldName)
      if (existing) {
        next.set(fieldName, { ...existing, value })
      }
      return next
    })
  }

  // ... render JSX following AssertionSelector pattern
}
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Two-layer params (data, headers) | Three-layer params (data, api_params, field_params) | v0.4.1 | Supports field-level assertions |
| Inline field values in Python code | Structured field_params JSON | v0.4.1 | Enables visual configuration |

**Deprecated/outdated:**
- `params` field for everything: Now split into `params` (api_params) and `field_params`

## Open Questions

1. **Should field_params be optional in AssertionConfig?**
   - What we know: Existing assertions don't have field_params
   - What's unclear: Whether new assertions must have field_params
   - Recommendation: Make it optional (`field_params?: Record<string, string>`) for backward compatibility

2. **Should we show field count per group in collapsed state?**
   - What we know: ROADMAP.md shows "(15)" count next to group name
   - What's unclear: Whether filtered count or total count should display
   - Recommendation: Show total count (e.g., "销售相关 (15)") - simpler and more informative

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | None configured (frontend has no test framework) |
| Config file | None |
| Quick run command | N/A |
| Full suite command | N/A |

### Phase Requirements -> Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| UI-01 | Three-layer layout renders correctly | Visual verification | Manual | N/A |
| UI-02 | Field grouping and search work | Manual testing | Manual | N/A |
| UI-03 | "now" button appears for time fields | Manual testing | Manual | N/A |
| UI-04 | Add/remove field configurations | Manual testing | Manual | N/A |

### Sampling Rate
- **Per task commit:** Visual verification in browser
- **Per wave merge:** Manual UI testing
- **Phase gate:** All 4 UI requirements verified manually

### Wave 0 Gaps
- [ ] No frontend test framework configured - tests will be manual
- [ ] Consider adding Vitest + React Testing Library in future phase

**Note:** Frontend testing infrastructure not required for this phase per project conventions. Manual verification acceptable for UI components.

## Sources

### Primary (HIGH confidence)
- `frontend/src/components/TaskModal/AssertionSelector.tsx` - Existing implementation pattern (lines 1-471)
- `frontend/src/types/index.ts` - Type definitions (lines 308-316)
- `backend/api/routes/external_assertions.py` - Fields API endpoint (lines 138-160)
- `.planning/phases/29-frontend-field-config-ui/29-CONTEXT.md` - User decisions
- `.planning/ROADMAP.md` - UI layout design (lines 130-154)

### Secondary (MEDIUM confidence)
- `.planning/phases/24-frontend-assertion-ui/24-CONTEXT.md` - Phase 24 decisions (component patterns)
- `.planning/phases/28-backend-field-discovery/28-CONTEXT.md` - Phase 28 API response structure

### Tertiary (LOW confidence)
- None - all findings verified against code

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - All dependencies already installed and in use
- Architecture: HIGH - Existing AssertionSelector provides complete pattern reference
- Pitfalls: HIGH - Based on observed patterns in existing code

**Research date:** 2026-03-22
**Valid until:** 30 days (stable React patterns)
