# Phase 24: Frontend Assertion UI - Research

**Researched:** 2026-03-20
**Domain:** React Frontend UI Components (Modal, Forms, State Management)
**Confidence:** HIGH (existing patterns well-documented, no new dependencies)

## Summary

Phase 24 implements the frontend UI for configuring business assertions. The core deliverable is an `AssertionSelector` component that allows QA users to browse assertion methods grouped by class (PcAssert, MgAssert, McAssert), configure parameters (headers, data, i/j/k), and save structured configuration for Phase 25 execution engine.

**Primary recommendation:** Reuse the single-step Modal pattern from `OperationCodeSelector.tsx` (not the 4-step wizard from `DataMethodSelector.tsx`). Assertion configuration is simpler than data extraction - one modal with grouped list + parameter configuration is sufficient.

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions
- **单步 Modal**: 类似 OperationCodeSelector，一个 Modal 包含分组列表 + 参数配置
- **不分步**: 断言配置比数据获取简单，无需 4 步向导
- **Modal 结构**:
  1. 顶部：搜索框
  2. 左侧：按类分组的断言方法列表（可折叠）
  3. 右侧/下方：已选断言的参数配置区
  4. 底部：确认/取消按钮
- **断言区域改造**: 将现有「接口断言」区域改为「断言」区域
- **Tab 切换**:
  - Tab 1: 「接口断言」— 现有 Python 代码 textarea
  - Tab 2: 「业务断言」— 结构化配置区域
- **业务断言 UI**:
  - 顶部：添加断言按钮
  - 中部：已配置断言卡片列表
  - 每个卡片：方法名 + 参数摘要 + 编辑/删除按钮
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
- **headers 参数**: 下拉菜单，选项固定为 `['main', 'idle', 'vice', 'special', 'platform', 'super', 'camera']`
- **data 参数**: 下拉菜单，选项从 API 响应的 `data_options` 获取
- **i/j/k 参数**: 有选项时用下拉菜单，无选项时用输入框
- **Agent 完成后执行**: 业务断言在 Browser-Use agent 完成所有步骤后执行
- **不生成 Python 代码**: 存为结构化 JSON 供 Phase 25 解析
- **外部模块不可用**: 按钮置灰 + 提示信息
- **加载状态**: 获取方法列表时显示 loading
- **空结果提示**: 没有匹配方法时显示提示

### Claude's Discretion
- Modal 的具体样式（宽度、圆角、阴影）
- 卡片的具体布局和间距
- 搜索防抖时间（建议 300ms）
- Tab 切换动画

### Deferred Ideas (OUT OF SCOPE)
- 断言执行引擎 — Phase 25
- Agent 完成检测机制 — Phase 25
- 断言结果展示 — Phase 25+
- 断言执行预览（在 Modal 中测试断言）— 未来优化
- 最近使用的断言方法 — 后续优化
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| UI-01 | 创建 AssertionSelector 组件，展示按类分组的断言方法列表 | OperationCodeSelector.tsx provides exact pattern: grouped list with search, collapsible panels from DataMethodSelector.tsx |
| UI-02 | 提供 headers 参数下拉选择（main/idle/vice/special/platform/super/camera） | HEADERS_OPTIONS constant in backend/routes/external_assertions.py, dropdown UI pattern from DataMethodSelector parameter config |
| UI-03 | 提供 data 参数下拉选择（从方法发现中提取选项） | data_options field in AssertionMethodInfo from API response, dynamic dropdown based on selected method |
| UI-04 | 为 i/j/k 参数创建独立输入区域（API 过滤参数，与验证字段分开） | ParameterInfo with options array for dropdown, free text for no options |
| UI-05 | 支持搜索/过滤断言方法 | useMemo + searchQuery pattern from OperationCodeSelector.tsx lines 65-78 |
| UI-06 | 在 TaskForm 中集成断言配置（作为新 Tab 或折叠面板） | Tab switching pattern, formData state management, existing TaskForm.tsx structure |
</phase_requirements>

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| React | 19.2.0 | UI framework | Project standard |
| lucide-react | 0.577.0 | Icons | Used in existing components (X, Search, ChevronDown) |
| sonner | 2.0.7 | Toast notifications | apiClient uses for error display |
| Tailwind CSS | 4.2.1 | Styling | All components use Tailwind classes |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| @tanstack/react-query | 5.90.21 | Server state | Not needed - useState + useEffect pattern established |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| useState for modal state | Zustand/Jotai | Global state not needed - modal is local to TaskForm |
| Custom dropdown component | Radix UI Select | Adds dependency, Tailwind select sufficient for this use case |

**Installation:**
No new packages required. All dependencies already installed.

**Version verification:**
```bash
npm view react version      # 19.1.0 (project uses 19.2.0)
npm view lucide-react version  # 0.577.0 (current)
npm view sonner version     # 2.0.7 (current)
```

## Architecture Patterns

### Recommended Project Structure
```
frontend/src/
├── components/TaskModal/
│   ├── AssertionSelector.tsx    # NEW: Main modal component
│   ├── TaskForm.tsx             # MODIFY: Add Tab switching
│   ├── OperationCodeSelector.tsx # REFERENCE: Single-step modal pattern
│   └── DataMethodSelector.tsx   # REFERENCE: Collapsible groups pattern
├── api/
│   ├── externalAssertions.ts    # NEW: API client for /external-assertions
│   └── client.ts                # EXISTING: Base API client
└── types/
    └── index.ts                 # MODIFY: Add AssertionConfig type
```

### Pattern 1: Single-Step Modal with Collapsible Groups
**What:** A modal with search, grouped method list (collapsible), and parameter configuration in one view.
**When to use:** When configuration is simple enough to fit in single modal (unlike 4-step data extraction wizard).
**Example:**
```tsx
// Source: OperationCodeSelector.tsx pattern + DataMethodSelector.tsx collapsible groups
export function AssertionSelector({ open, onConfirm, onCancel }: AssertionSelectorProps) {
  const [methods, setMethods] = useState<AssertionMethodsResponse>({...})
  const [searchQuery, setSearchQuery] = useState('')
  const [selectedMethods, setSelectedMethods] = useState<Set<string>>(new Set())
  const [expandedPanels, setExpandedPanels] = useState<Set<string>>(new Set())
  const [configs, setConfigs] = useState<Map<string, AssertionConfig>>(new Map())

  // Filter methods based on search (OperationCodeSelector pattern)
  const filteredClasses = useMemo(() => {
    if (!searchQuery.trim()) return methods.classes
    const query = searchQuery.toLowerCase()
    return methods.classes
      .map(cls => ({
        ...cls,
        methods: cls.methods.filter(m =>
          m.name.toLowerCase().includes(query) ||
          m.description.toLowerCase().includes(query)
        )
      }))
      .filter(cls => cls.methods.length > 0)
  }, [methods.classes, searchQuery])

  // Toggle panel expansion (DataMethodSelector pattern)
  const togglePanel = (className: string) => {
    setExpandedPanels(prev => {
      const next = new Set(prev)
      if (next.has(className)) next.delete(className)
      else next.add(className)
      return next
    })
  }

  // Modal structure
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center">
      <div className="fixed inset-0 bg-black/50" onClick={onCancel} />
      <div className="relative bg-white rounded-xl shadow-xl w-full max-w-3xl mx-4 max-h-[80vh] overflow-hidden flex flex-col">
        {/* Header with search */}
        <div className="px-6 py-4 border-b border-gray-100">
          <h3 className="text-lg font-semibold">选择断言方法</h3>
          <div className="relative mt-3">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
            <input
              type="text"
              value={searchQuery}
              onChange={e => setSearchQuery(e.target.value)}
              placeholder="搜索断言方法..."
              className="w-full pl-10 pr-4 py-2 border border-gray-200 rounded-lg"
            />
          </div>
        </div>

        {/* Content: Grouped list + Config area */}
        <div className="flex-1 overflow-y-auto px-6 py-4">
          {/* Collapsible class groups */}
          {filteredClasses.map(cls => (
            <div key={cls.name} className="border border-gray-200 rounded-lg mb-2">
              <button onClick={() => togglePanel(cls.name)} className="w-full flex items-center justify-between px-4 py-3">
                <span className="font-medium">{cls.name}</span>
                <ChevronDown className={`transition-transform ${expandedPanels.has(cls.name) ? 'rotate-180' : ''}`} />
              </button>
              {expandedPanels.has(cls.name) && (
                <div className="p-2 space-y-1">
                  {cls.methods.map(m => (
                    <label key={m.name} className="flex items-center gap-3 p-2 rounded-lg hover:bg-gray-50 cursor-pointer">
                      <input type="checkbox" checked={selectedMethods.has(`${cls.name}:${m.name}`)} />
                      <span className="font-mono text-sm text-blue-600">{m.name}</span>
                      <span className="text-sm text-gray-600">{m.description}</span>
                    </label>
                  ))}
                </div>
              )}
            </div>
          ))}
        </div>

        {/* Footer */}
        <div className="flex justify-end gap-3 px-6 py-4 border-t border-gray-100">
          <button onClick={onCancel} className="px-4 py-2 text-gray-700 hover:bg-gray-100 rounded-lg">取消</button>
          <button onClick={() => onConfirm(Array.from(configs.values()))} className="px-4 py-2 bg-blue-500 text-white rounded-lg">确认</button>
        </div>
      </div>
    </div>
  )
}
```

### Pattern 2: Tab Switching in TaskForm
**What:** Convert the existing "接口断言" section to a tabbed interface with two tabs.
**When to use:** When adding a new type of assertion without disrupting existing functionality.
**Example:**
```tsx
// Source: Common tab pattern in React
const [assertionTab, setAssertionTab] = useState<'api' | 'business'>('api')

// In TaskForm JSX
<div>
  <label className="block text-sm font-medium text-gray-700 mb-1">断言</label>
  {/* Tab switcher */}
  <div className="flex gap-2 mb-3">
    <button
      type="button"
      onClick={() => setAssertionTab('api')}
      className={`px-3 py-1.5 rounded-lg text-sm font-medium ${
        assertionTab === 'api' ? 'bg-blue-100 text-blue-700' : 'bg-gray-100 text-gray-600'
      }`}
    >
      接口断言
    </button>
    <button
      type="button"
      onClick={() => setAssertionTab('business')}
      className={`px-3 py-1.5 rounded-lg text-sm font-medium ${
        assertionTab === 'business' ? 'bg-orange-100 text-orange-700' : 'bg-gray-100 text-gray-600'
      }`}
    >
      业务断言
    </button>
  </div>

  {/* Tab content */}
  {assertionTab === 'api' ? (
    // Existing api_assertions textarea
    <div>...</div>
  ) : (
    // New business assertions UI
    <BusinessAssertionsSection
      assertions={formData.assertions}
      onChange={(assertions) => setFormData(prev => ({ ...prev, assertions }))}
    />
  )}
</div>
```

### Pattern 3: Parameter Configuration with Dynamic Options
**What:** Render parameters based on API response structure - dropdown for options, input for free text.
**When to use:** When parameter options vary by method (data_options from API, i/j/k options from docstrings).
**Example:**
```tsx
// Source: DataMethodSelector.tsx parameter config pattern + API response structure
interface ParameterConfigProps {
  method: AssertionMethodInfo
  config: AssertionConfig
  headersOptions: string[]
  onUpdate: (updates: Partial<AssertionConfig>) => void
}

function ParameterConfig({ method, config, headersOptions, onUpdate }: ParameterConfigProps) {
  return (
    <div className="space-y-3">
      {/* Headers dropdown - fixed options */}
      <div className="flex items-center gap-3">
        <label className="w-24 text-sm text-gray-700">headers</label>
        <select
          value={config.headers}
          onChange={e => onUpdate({ headers: e.target.value })}
          className="flex-1 px-3 py-1.5 border border-gray-200 rounded-lg text-sm"
        >
          {headersOptions.map(opt => (
            <option key={opt} value={opt}>{opt}</option>
          ))}
        </select>
      </div>

      {/* Data dropdown - from method's data_options */}
      <div className="flex items-center gap-3">
        <label className="w-24 text-sm text-gray-700">data</label>
        <select
          value={config.data}
          onChange={e => onUpdate({ data: e.target.value })}
          className="flex-1 px-3 py-1.5 border border-gray-200 rounded-lg text-sm"
        >
          {method.data_options.map(opt => (
            <option key={opt} value={opt}>{opt}</option>
          ))}
        </select>
      </div>

      {/* i/j/k parameters - dropdown if options, input otherwise */}
      {method.parameters.map(param => (
        <div key={param.name} className="flex items-center gap-3">
          <label className="w-24 text-sm text-gray-700">{param.name}</label>
          {param.options.length > 0 ? (
            <select
              value={config.params[param.name] ?? ''}
              onChange={e => onUpdate({
                params: { ...config.params, [param.name]: parseInt(e.target.value) }
              })}
              className="flex-1 px-3 py-1.5 border border-gray-200 rounded-lg text-sm"
            >
              {param.options.map(opt => (
                <option key={opt.value} value={opt.value}>{opt.label}</option>
              ))}
            </select>
          ) : (
            <input
              type="number"
              value={config.params[param.name] ?? ''}
              onChange={e => onUpdate({
                params: { ...config.params, [param.name]: parseInt(e.target.value) }
              })}
              className="flex-1 px-3 py-1.5 border border-gray-200 rounded-lg text-sm"
            />
          )}
          {param.description && (
            <span className="text-xs text-gray-400">{param.description}</span>
          )}
        </div>
      ))}
    </div>
  )
}
```

### Anti-Patterns to Avoid
- **4-Step Wizard for Assertions**: Don't use DataMethodSelector's 4-step pattern. Assertion configuration is simpler - single modal is sufficient.
- **Generating Python Code**: Don't generate Python code like preconditions do. Store structured AssertionConfig[] for Phase 25 execution engine.
- **Separating Headers Resolution in Frontend**: Headers are just identifiers (strings) in UI. Resolution to actual tokens is Phase 25 backend responsibility.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Modal component | Custom modal with animation | Copy OperationCodeSelector.tsx structure | Proven pattern, ESC key support, backdrop click |
| Search/filter logic | Custom filter function | useMemo + lowercase includes pattern | Established in existing components |
| Collapsible panels | Custom accordion | Copy DataMethodSelector togglePanel pattern | Simple, works well |
| Toast notifications | Custom alert | sonner toast.error() | apiClient already uses it |
| Form state | Complex state library | React useState + Map for configs | Sufficient for this scope |

**Key insight:** The existing codebase has excellent patterns that can be directly reused. OperationCodeSelector provides the modal structure, DataMethodSelector provides collapsible groups and parameter configuration UI. Combine these two patterns.

## Common Pitfalls

### Pitfall 1: Treating All Parameters as Validation Fields
**What goes wrong:** i/j/k parameters are API filter parameters, not validation fields. If mixed, API calls return wrong data.
**Why it happens:** The API response structure separates `parameters` array (i/j/k with options) from validation kwargs, but UI might combine them.
**How to avoid:** Use the `parameters` array from API response for i/j/k config. Don't add a separate "validation fields" section - that's Phase 25 responsibility when executing assertions.
**Warning signs:** UI shows "field name" inputs for parameters that should be dropdowns.

### Pitfall 2: Not Handling External Module Unavailability
**What goes wrong:** API returns 503 when WEBSERP_PATH not configured. If not handled, UI shows confusing errors.
**Why it happens:** Following OperationCodeSelector pattern which checks `response.available` and shows error message.
**How to avoid:** Check `response.available` from API. Show grayed-out button with tooltip when unavailable. Display error message in modal if opened.
**Warning signs:** Button throws error when clicked, or modal shows generic "failed to fetch" message.

### Pitfall 3: Stale Selected Methods After Search
**What goes wrong:** User selects methods, then searches. When search clears, selections are lost or inconsistent.
**Why it happens:** Filtered list recreates method keys, selection state may not persist correctly.
**How to avoid:** Use unique key format `className:methodName` for selections. Store selections in Set that persists across filter changes.
**Warning signs:** Checked items become unchecked after search/filter.

### Pitfall 4: Not Resetting State on Modal Close
**What goes wrong:** Previous selections/configs persist when reopening modal for different assertions.
**Why it happens:** State initialized once on component mount, not reset when `open` prop changes.
**How to avoid:** Use useEffect with `open` dependency to reset state when modal opens (like OperationCodeSelector line 43-46).
**Warning signs:** Modal shows old selections when opened for new assertion.

## Code Examples

### API Response Types (from backend/routes/external_assertions.py)
```typescript
// Source: backend/api/routes/external_assertions.py
interface ParameterOption {
  value: number
  label: string
}

interface ParameterInfo {
  name: string
  description: string
  options: ParameterOption[]
}

interface AssertionMethodInfo {
  name: string
  description: string
  data_options: string[]
  parameters: ParameterInfo[]
}

interface AssertionClassGroup {
  name: string
  methods: AssertionMethodInfo[]
}

interface AssertionMethodsResponse {
  available: boolean
  headers_options: string[]
  classes: AssertionClassGroup[]
  total: number
  error?: string
}
```

### New Types to Add (frontend/src/types/index.ts)
```typescript
// Add to existing types/index.ts

// AssertionConfig - structured configuration for business assertions
export interface AssertionConfig {
  className: string      // e.g., "PcAssert"
  methodName: string     // e.g., "attachment_inventory_list_assert"
  headers: string        // e.g., "main"
  data: string           // e.g., "main"
  params: Record<string, number | string>  // i, j, k etc.
}

// Update CreateTaskDto to include assertions
export interface CreateTaskDto {
  name: string
  description: string
  target_url: string
  max_steps: number
  preconditions?: string[]
  api_assertions?: string[]
  assertions?: AssertionConfig[]  // NEW
}

// Update Task interface
export interface Task {
  id: string
  name: string
  description: string
  target_url: string
  max_steps: number
  preconditions?: string[]
  api_assertions?: string[]
  assertions?: AssertionConfig[]  // NEW
  status: 'draft' | 'ready'
  created_at: string
  updated_at: string
}
```

### API Client (frontend/src/api/externalAssertions.ts)
```typescript
// New file to create
import type { AssertionMethodsResponse } from '../types'
import { apiClient } from './client'

export const externalAssertionsApi = {
  /**
   * Fetch available assertion methods grouped by class.
   * Returns 503 if external module is not available.
   */
  async list(): Promise<AssertionMethodsResponse> {
    return apiClient<AssertionMethodsResponse>('/external-assertions/methods')
  },
}
```

### Assertion Card Component
```tsx
// Source: TaskForm.tsx card pattern + CONTEXT.md specs
interface AssertionCardProps {
  config: AssertionConfig
  onEdit: () => void
  onDelete: () => void
}

function AssertionCard({ config, onEdit, onDelete }: AssertionCardProps) {
  const paramsSummary = Object.entries(config.params)
    .map(([k, v]) => `${k}=${v}`)
    .join(', ')

  return (
    <div className="border border-orange-200 bg-orange-50 rounded-lg p-3">
      <div className="flex items-center justify-between">
        <div>
          <span className="font-mono text-sm text-blue-600">{config.methodName}</span>
          <span className="text-gray-400 mx-2">|</span>
          <span className="text-sm text-gray-600">
            headers={config.headers}, data={config.data}
            {paramsSummary && `, ${paramsSummary}`}
          </span>
        </div>
        <div className="flex gap-2">
          <button type="button" onClick={onEdit} className="text-sm text-blue-500 hover:text-blue-600">
            编辑
          </button>
          <button type="button" onClick={onDelete} className="text-sm text-red-500 hover:text-red-600">
            删除
          </button>
        </div>
      </div>
    </div>
  )
}
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Multi-step wizard for all selectors | Single-step modal for simple config | Phase 18-19 established pattern | Faster user workflow for assertions |
| Hardcoded parameter options | Dynamic options from API | Phase 23 implemented discovery | Accurate options per method |
| Python code generation | Structured JSON config | Phase 24 decision | Cleaner separation, Phase 25 execution |

**Deprecated/outdated:**
- Don't generate Python code for assertions (old precondition pattern) - use structured AssertionConfig instead

## Open Questions

1. **Should assertions support multi-select?**
   - What we know: CONTEXT.md says "支持多选断言方法"
   - What's unclear: Should multiple assertions of the same method with different params be allowed?
   - Recommendation: Yes, allow multiple configs of same method (e.g., different i values for same assertion)

2. **How to handle editing an existing assertion?**
   - What we know: Cards have "编辑" button
   - What's unclear: Should modal open with pre-filled config, or inline edit?
   - Recommendation: Open AssertionSelector modal with pre-filled selection and config (add `initialConfig?: AssertionConfig` prop)

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | Vitest (inferred from Vite project) |
| Config file | None detected - may need vitest.config.ts |
| Quick run command | `npm test -- --run` |
| Full suite command | `npm test` |

**Note:** No frontend tests currently exist. The project uses Playwright for E2E testing (Phase 26). Consider adding Vitest tests in Phase 27 unit test coverage phase.

### Phase Requirements -> Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| UI-01 | AssertionSelector displays grouped methods | unit | `npm test -- AssertionSelector.test.tsx --run` | No - Wave 0 |
| UI-02 | Headers dropdown shows fixed options | unit | `npm test -- AssertionSelector.test.tsx --run` | No - Wave 0 |
| UI-03 | Data dropdown shows method-specific options | unit | `npm test -- AssertionSelector.test.tsx --run` | No - Wave 0 |
| UI-04 | i/j/k parameters render as dropdown or input | unit | `npm test -- AssertionSelector.test.tsx --run` | No - Wave 0 |
| UI-05 | Search filters methods correctly | unit | `npm test -- AssertionSelector.test.tsx --run` | No - Wave 0 |
| UI-06 | TaskForm Tab switching works | unit | `npm test -- TaskForm.test.tsx --run` | No - Wave 0 |

### Sampling Rate
- **Per task commit:** Not applicable - no frontend tests yet
- **Per wave merge:** Manual verification in browser
- **Phase gate:** E2E tests in Phase 26 will cover UI flows

### Wave 0 Gaps
- [ ] `frontend/src/components/TaskModal/AssertionSelector.test.tsx` - unit tests for new component
- [ ] `frontend/src/components/TaskModal/TaskForm.test.tsx` - unit tests for Tab integration
- [ ] `frontend/vitest.config.ts` - test framework configuration
- [ ] Framework install: `npm install -D vitest @testing-library/react @testing-library/jest-dom jsdom`

*(Frontend testing infrastructure to be added in Phase 27 - Unit Test Coverage)*

## Sources

### Primary (HIGH confidence)
- `/Users/huhu/project/weberpagent/frontend/src/components/TaskModal/OperationCodeSelector.tsx` - Single-step modal pattern
- `/Users/huhu/project/weberpagent/frontend/src/components/TaskModal/DataMethodSelector.tsx` - Collapsible groups, parameter config
- `/Users/huhu/project/weberpagent/frontend/src/components/TaskModal/TaskForm.tsx` - Form state management, integration point
- `/Users/huhu/project/weberpagent/backend/api/routes/external_assertions.py` - API response structure
- `/Users/huhu/project/weberpagent/.planning/phases/24-frontend-assertion-ui/24-CONTEXT.md` - User decisions

### Secondary (MEDIUM confidence)
- `/Users/huhu/project/weberpagent/frontend/src/types/index.ts` - Type definitions pattern
- `/Users/huhu/project/weberpagent/frontend/src/api/externalOperations.ts` - API client pattern
- `/Users/huhu/project/weberpagent/frontend/src/api/externalDataMethods.ts` - API client pattern

### Tertiary (LOW confidence)
- None - all patterns verified from existing codebase

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - All dependencies already in use
- Architecture: HIGH - Existing components provide exact patterns to follow
- Pitfalls: HIGH - Based on analysis of existing codebase patterns and Phase 23 API structure

**Research date:** 2026-03-20
**Valid until:** 30 days (stable React patterns, no external API changes expected)
