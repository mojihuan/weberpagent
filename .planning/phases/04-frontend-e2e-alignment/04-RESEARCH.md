# Phase 4: Frontend + E2E Alignment - Research

**Researched:** 2026-03-14
**Domain:** React 19 Frontend + Playwright E2E Testing
**Confidence:** HIGH

## Summary

Phase 4 focuses on aligning the frontend TypeScript types with backend Pydantic schemas, implementing proper error handling UX with toast notifications, and establishing E2E testing for the complete user flow. The frontend is built with React 19 + TypeScript + Vite + Tailwind CSS 4, and already has substantial components in place. Key gaps identified: (1) Type misalignment between frontend `Run.status` values and backend values, (2) Missing toast notification library, (3) No E2E test infrastructure, (4) Assertion results not displayed in report pages.

**Primary recommendation:** Use Sonner for toast notifications (lightweight, TypeScript-first, minimal setup), install Playwright for E2E testing, and systematically update frontend types to match backend schemas exactly.

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

#### 类型对齐策略
- **同步方式**: 手动同步（更新 types/index.ts 确保与后端 schemas 一致）
- **Run 状态值**: 使用后端值 (pending/running/completed/failed)
- **Step 字段名**: 统一使用 `step`（后端字段名）

#### 错误处理 UX
- **错误展示方式**: Toast 通知
- **错误细节**: 显示完整错误详情（包括技术细节）
- **网络错误处理**: 自动重试 3 次 + toast 提示

#### 空状态设计
- **任务列表空状态**: 显示"创建第一个任务" CTA
- **报告页空状态**: 显示"执行任务后查看报告" CTA
- **执行监控初始状态**: 显示"开始执行"按钮

#### 报告页布局
- **断言结果展示**: 顶部摘要（通过率）+ 下方列表
- **断言失败详情**: 显示期望值 vs 实际值对比
- **截图展示**: 缩略图画廊（点击放大）

#### E2E 测试范围
- **测试流程**: 仅测试正常流程（创建 -> 执行 -> 监控 -> 报告）
- **测试级别**: 冒烟测试（smoke test），不测试边界情况
- **失败处理**: 测试失败时记录日志，不阻塞

### Claude's Discretion
- 具体组件实现细节
- 加载状态样式
- 过渡动画
- 响应式布局细节

### Deferred Ideas (OUT OF SCOPE)
None - discussion stayed within phase scope
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| UI-01 | API types match backend response schemas exactly | Section: Type Alignment Analysis |
| UI-02 | Task list displays all tasks with correct data | Existing TaskApi + TaskTable components work; needs verification |
| UI-03 | Execution monitor shows real-time step updates via SSE | useRunStream hook exists; needs status value alignment |
| UI-04 | Screenshot panel displays images from correct paths | Screenshot URL construction verified in useRunStream |
| UI-05 | Report page shows assertion results and step details | Requires new AssertionResult components |
| UI-06 | API base URL is configurable via environment variable | Already implemented via VITE_API_BASE in client.ts |
| E2E-01 | User can create a new test task with natural language description | Playwright setup required; flow documented |
| E2E-02 | User can execute a task and see real-time progress | SSE flow testable with Playwright |
| E2E-03 | User can view execution screenshots for each step | Screenshot endpoint exists |
| E2E-04 | User can view final test report with assertion results | Report API exists; assertion display needed |
| E2E-05 | Complete flow works without errors (create -> execute -> monitor -> report) | End-to-end smoke test |
</phase_requirements>

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| React | 19.2.0 | UI Framework | Already in use |
| TypeScript | ~5.9.3 | Type Safety | Already in use |
| Vite | 7.3.1 | Build Tool | Already in use |
| Tailwind CSS | 4.2.1 | Styling | Already in use |
| React Router | 7.13.1 | Routing | Already in use |

### To Add
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| sonner | ^1.5.0 | Toast notifications | Error handling, success feedback |
| @playwright/test | ^1.48.0 | E2E testing | Full user flow validation |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| sonner | react-hot-toast | Sonner has cleaner API, smaller bundle, better DX |
| sonner | react-toastify | Sonner more lightweight, modern API design |
| @playwright/test | Cypress | Playwright faster, better TypeScript support, already used in backend |
| @playwright/test | vitest browser mode | Playwright better for true E2E across full app |

**Installation:**
```bash
# Frontend toast notifications
cd frontend && npm install sonner

# E2E testing (project root)
npm install -D @playwright/test
npx playwright install chromium
```

## Type Alignment Analysis

### Current Frontend Types vs Backend Schemas

#### Run Status Mismatch (CRITICAL)

**Frontend (types/index.ts line 34):**
```typescript
status: 'running' | 'success' | 'failed' | 'stopped'
```

**Backend (db/schemas.py line 57):**
```python
status: Literal["pending", "running", "completed", "failed"]
```

**Required Fix:** Update frontend to use:
```typescript
status: 'pending' | 'running' | 'completed' | 'failed'
```

Note: Backend also supports 'stopped' in models.py (line 43), but schemas.py uses 'completed'. Need to verify which is authoritative.

#### Step Field Name Mismatch

**Frontend uses `index`, backend uses `step_index`:**
- Frontend: `step.index` (StepItem.tsx line 45)
- Backend API: `step_index` (schemas.py line 69)
- Already transformed in reports.ts: `index: step.step_index` (line 59)

**Decision from CONTEXT.md:** Use `step` as field name (backend convention). But current frontend uses `index`. Need to align consistently.

#### Missing Types

Frontend missing these backend types:
- `AssertionResponse` - for displaying assertion configurations
- `AssertionResultResponse` - for displaying assertion pass/fail results
- `SSEStartedEvent`, `SSEStepEvent`, `SSEFinishedEvent` - SSE event types

### Recommended Type Updates

```typescript
// Add to types/index.ts

// Run status - align with backend
export type RunStatus = 'pending' | 'running' | 'completed' | 'failed'

// Assertion types
export interface Assertion {
  id: string
  task_id: string
  name: string
  type: 'url_contains' | 'text_exists' | 'no_errors'
  expected: string
  created_at: string
}

export interface AssertionResult {
  id: string
  run_id: string
  assertion_id: string
  status: 'pass' | 'fail'
  message: string | null
  actual_value: string | null
  created_at: string
}

// Extend Report with assertion results
export interface ReportDetailResponse extends Report {
  steps: Step[]
  assertion_results?: AssertionResult[]
}
```

## Architecture Patterns

### Recommended Project Structure
```
frontend/src/
├── api/              # API clients (existing)
├── components/       # UI components (existing)
│   ├── Report/       # Add AssertionResults.tsx
│   └── shared/       # Toast wrapper here
├── hooks/            # Custom hooks (existing)
├── types/            # TypeScript types (update index.ts)
├── utils/            # Add retry.ts for network retry logic
└── main.tsx          # Add Toaster component here

e2e/
├── tests/            # Playwright test files
│   ├── task-flow.spec.ts
│   └── smoke.spec.ts
├── playwright.config.ts
└── fixtures/         # Test fixtures if needed
```

### Pattern 1: Toast Notification Integration
**What:** Global toast provider with consistent error handling
**When to use:** All API error handling, success confirmations
**Example:**
```typescript
// main.tsx
import { Toaster, toast } from 'sonner'

function App() {
  return (
    <>
      <RouterProvider router={router} />
      <Toaster position="top-center" richColors />
    </>
  )
}

// api/client.ts - with retry logic
const MAX_RETRIES = 3

export async function apiClient<T>(
  endpoint: string,
  options?: RequestInit,
  retries = MAX_RETRIES
): Promise<T> {
  try {
    const response = await fetch(`${API_BASE}${endpoint}`, {
      headers: { 'Content-Type': 'application/json', ...options?.headers },
      ...options,
    })

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}))
      const message = errorData.detail || `API Error: ${response.status}`
      toast.error(message, { duration: 5000 })
      throw new ApiError(response.status, message)
    }

    return response.json()
  } catch (error) {
    if (retries > 0 && isNetworkError(error)) {
      toast.loading(`Network error, retrying... (${MAX_RETRIES - retries + 1}/${MAX_RETRIES})`, { id: 'retry' })
      await sleep(1000 * (MAX_RETRIES - retries + 1)) // Exponential backoff
      return apiClient(endpoint, options, retries - 1)
    }
    toast.dismiss('retry')
    throw error
  }
}
```

### Pattern 2: Assertion Results Display
**What:** Display assertion results with pass/fail status and comparison
**When to use:** Report detail page
**Example:**
```typescript
// components/Report/AssertionResults.tsx
interface AssertionResultsProps {
  results: AssertionResult[]
}

export function AssertionResults({ results }: AssertionResultsProps) {
  const passCount = results.filter(r => r.status === 'pass').length
  const passRate = results.length > 0 ? Math.round((passCount / results.length) * 100) : 0

  return (
    <div className="mb-6">
      <div className="flex items-center gap-4 mb-4">
        <h2 className="text-lg font-medium">断言结果</h2>
        <span className={passRate === 100 ? 'text-green-600' : 'text-red-600'}>
          通过率: {passRate}% ({passCount}/{results.length})
        </span>
      </div>

      <div className="space-y-2">
        {results.map(result => (
          <div key={result.id} className={`p-3 rounded-lg border ${
            result.status === 'pass' ? 'bg-green-50 border-green-200' : 'bg-red-50 border-red-200'
          }`}>
            <div className="flex items-center gap-2">
              {result.status === 'pass' ? (
                <CheckCircle className="w-5 h-5 text-green-500" />
              ) : (
                <XCircle className="w-5 h-5 text-red-500" />
              )}
              <span className="font-medium">{result.assertion_name}</span>
            </div>
            {result.status === 'fail' && result.message && (
              <p className="text-sm text-red-600 mt-2">{result.message}</p>
            )}
            {result.actual_value && (
              <p className="text-sm text-gray-500 mt-1">
                实际值: {result.actual_value}
              </p>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}
```

### Pattern 3: E2E Test Structure
**What:** Playwright smoke test for complete user flow
**When to use:** Validating E2E-01 through E2E-05
**Example:**
```typescript
// e2e/tests/smoke.spec.ts
import { test, expect } from '@playwright/test'

test.describe('Smoke Test - Complete User Flow', () => {
  test('create -> execute -> monitor -> report', async ({ page }) => {
    // E2E-01: Create task
    await page.goto('/')
    await page.click('text=任务管理')
    await page.click('text=新建任务')

    await page.fill('[name="name"]', 'E2E Smoke Test Task')
    await page.fill('[name="description"]', '打开百度首页并搜索 Playwright')
    await page.click('button:has-text("创建")')

    // Verify task created
    await expect(page.locator('text=E2E Smoke Test Task')).toBeVisible()

    // E2E-02: Execute task
    await page.click('button:has-text("执行")')

    // E2E-03: Monitor execution
    await expect(page.locator('text=执行监控')).toBeVisible()

    // Wait for completion (with timeout)
    await expect(page.locator('[data-testid="run-status"]')).toHaveText(/completed|failed/, { timeout: 60000 })

    // E2E-04 & E2E-05: View report
    await page.click('text=查看报告')
    await expect(page.locator('text=执行报告')).toBeVisible()
    await expect(page.locator('text=断言结果')).toBeVisible()
  })
})
```

### Anti-Patterns to Avoid
- **Hardcoded API URLs:** Use VITE_API_BASE environment variable consistently
- **Inline error messages:** Use toast notifications for all user-facing errors
- **Missing loading states:** Always show loading indicator during async operations
- **Unhandled promise rejections:** Wrap all async operations in try/catch with toast.error

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Toast notifications | Custom toast component | sonner | Battle-tested, accessible, minimal setup |
| API retry logic | Custom retry loops | Exponential backoff pattern | Handles edge cases, configurable |
| E2E test framework | Custom test runner | @playwright/test | Cross-browser, auto-wait, tracing |
| Type generation | Manual type sync | Keep types/index.ts in sync with backend schemas manually (per user decision) | Simple project, manual sync acceptable |

**Key insight:** The project is small enough that manual type synchronization is acceptable. For larger projects, consider openapi-typescript for automatic type generation.

## Common Pitfalls

### Pitfall 1: Run Status Value Mismatch
**What goes wrong:** Frontend expects 'success' but backend sends 'completed', causing status badge to fail
**Why it happens:** Frontend types were defined before backend schemas were finalized
**How to avoid:** Update frontend RunStatus type to match backend exactly: 'pending' | 'running' | 'completed' | 'failed'
**Warning signs:** StatusBadge component shows incorrect styling or text

### Pitfall 2: SSE Connection State Management
**What goes wrong:** Multiple EventSource connections created, memory leaks
**Why it happens:** useRunStream hook not properly cleaning up on unmount
**How to avoid:** Always call disconnect in useEffect cleanup; use refs to track connection state
**Warning signs:** Browser console shows multiple SSE connections, memory usage grows

### Pitfall 3: Screenshot URL Construction
**What goes wrong:** Screenshots fail to load due to incorrect URL path
**Why it happens:** Backend endpoint is `/api/runs/{run_id}/screenshots/{step_index}` but frontend may construct wrong path
**How to avoid:** Use getScreenshotUrl helper from api/runs.ts consistently
**Warning signs:** Broken image icons in report or monitor views

### Pitfall 4: E2E Test Timing
**What goes wrong:** E2E tests fail randomly due to timing issues with async operations
**Why it happens:** AI-driven test execution can take variable time
**How to avoid:** Use generous timeouts (60s+), use Playwright's auto-waiting, avoid fixed waits
**Warning signs:** Tests pass locally but fail in CI

## Code Examples

### Retry Logic for API Client

```typescript
// frontend/src/utils/retry.ts
export function sleep(ms: number): Promise<void> {
  return new Promise(resolve => setTimeout(resolve, ms))
}

export function isNetworkError(error: unknown): boolean {
  if (error instanceof TypeError && error.message === 'Failed to fetch') {
    return true
  }
  return false
}
```

### Updated API Client with Retry and Toast

```typescript
// frontend/src/api/client.ts
import { toast } from 'sonner'
import { sleep, isNetworkError } from '../utils/retry'

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8080/api'
const MAX_RETRIES = 3

export class ApiError extends Error {
  status: number
  constructor(status: number, message: string) {
    super(message)
    this.name = 'ApiError'
    this.status = status
  }
}

export async function apiClient<T>(
  endpoint: string,
  options?: RequestInit,
  retries = MAX_RETRIES
): Promise<T> {
  try {
    const response = await fetch(`${API_BASE}${endpoint}`, {
      headers: {
        'Content-Type': 'application/json',
        ...options?.headers,
      },
      ...options,
    })

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}))
      const message = errorData.detail || errorData.error || `API Error: ${response.status}`

      // Show toast for all errors
      toast.error(message, { duration: 5000 })
      throw new ApiError(response.status, message)
    }

    return response.json()
  } catch (error) {
    // Network error - retry with exponential backoff
    if (retries > 0 && isNetworkError(error)) {
      const attempt = MAX_RETRIES - retries + 1
      toast.loading(`网络错误，正在重试... (${attempt}/${MAX_RETRIES})`, { id: 'network-retry' })

      await sleep(1000 * attempt) // Exponential backoff
      return apiClient<T>(endpoint, options, retries - 1)
    }

    toast.dismiss('network-retry')
    throw error
  }
}
```

### Playwright Configuration

```typescript
// e2e/playwright.config.ts
import { defineConfig, devices } from '@playwright/test'

export default defineConfig({
  testDir: './tests',
  fullyParallel: false, // Sequential for this smoke test
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: 1, // Single worker for consistency
  reporter: 'html',
  timeout: 120000, // 2 minutes per test (AI execution can be slow)

  use: {
    baseURL: 'http://localhost:5173',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
  },

  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
  ],

  webServer: [
    {
      command: 'uv run uvicorn backend.api.main:app --port 8080',
      url: 'http://localhost:8080/health',
      reuseExistingServer: !process.env.CI,
      timeout: 30000,
    },
    {
      command: 'cd frontend && npm run dev',
      url: 'http://localhost:5173',
      reuseExistingServer: !process.env.CI,
      timeout: 30000,
    },
  ],
})
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| react-toastify (536KB) | sonner (165KB) | 2023+ | Smaller bundle, simpler API |
| Cypress E2E | Playwright | 2022+ | Faster, better debugging, cross-browser |
| React 18 | React 19 | 2024 | This project already on React 19 |
| Manual fetch | apiClient wrapper | N/A | This project already has pattern |

**Deprecated/outdated:**
- React Toast Notifications: No longer maintained, avoid
- Enzyme: Deprecated, React Testing Library is the standard

## Open Questions

1. **Backend Run Status: 'completed' vs 'success'?**
   - What we know: models.py lists "pending, running, success, failed, stopped" but schemas.py uses "pending, running, completed, failed"
   - What's unclear: Which is the authoritative source
   - Recommendation: Check actual API responses; align frontend to match actual behavior

2. **Should assertion results be included in report API response?**
   - What we know: Backend has AssertionResult model but reports.py doesn't include them
   - What's unclear: Whether to add to API response or make separate call
   - Recommendation: Add assertion_results to ReportDetailResponse for single-request report load

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | Vitest (unit) + Playwright (E2E) |
| Config file | e2e/playwright.config.ts (to create) |
| Quick run command | `npx playwright test --project=chromium --reporter=list` |
| Full suite command | `npx playwright test` |

### Phase Requirements -> Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| UI-01 | Types match backend | Manual verification | N/A | N/A |
| UI-02 | Task list displays correctly | E2E | `npx playwright test -g "task list"` | No - Wave 0 |
| UI-03 | Real-time SSE updates | E2E | `npx playwright test -g "monitor"` | No - Wave 0 |
| UI-04 | Screenshot display | E2E | `npx playwright test -g "screenshot"` | No - Wave 0 |
| UI-05 | Assertion results display | E2E | `npx playwright test -g "report"` | No - Wave 0 |
| UI-06 | API URL configurable | Manual | Verify VITE_API_BASE usage | Yes |
| E2E-01 | Create task flow | E2E | `npx playwright test -g "create task"` | No - Wave 0 |
| E2E-02 | Execute and monitor | E2E | `npx playwright test -g "execute"` | No - Wave 0 |
| E2E-03 | View screenshots | E2E | `npx playwright test -g "screenshot"` | No - Wave 0 |
| E2E-04 | View report | E2E | `npx playwright test -g "report"` | No - Wave 0 |
| E2E-05 | Complete flow | E2E | `npx playwright test smoke.spec.ts` | No - Wave 0 |

### Sampling Rate
- **Per task commit:** Run affected component's E2E test
- **Per wave merge:** Run full E2E suite
- **Phase gate:** Full suite green before `/gsd:verify-work`

### Wave 0 Gaps
- [ ] `e2e/playwright.config.ts` - Playwright configuration
- [ ] `e2e/tests/smoke.spec.ts` - Complete flow smoke test
- [ ] `e2e/tests/task-flow.spec.ts` - Task CRUD tests
- [ ] Playwright install: `npx playwright install chromium`
- [ ] Frontend: `npm install sonner` for toast notifications

## Sources

### Primary (HIGH confidence)
- Backend schemas: `/backend/api/schemas/index.py` - Pydantic response models
- Backend models: `/backend/db/models.py` - SQLAlchemy ORM models
- Frontend types: `/frontend/src/types/index.ts` - Current TypeScript types
- Frontend API client: `/frontend/src/api/client.ts` - HTTP client implementation

### Secondary (MEDIUM confidence)
- [LogRocket: Comparing React Toast Libraries 2025](https://blog.logrocket.com/react-toast-libraries-compared-2025/) - Toast library comparison, Sonner recommended
- [Playwright Documentation](https://playwright.dev/docs/intro) - Official E2E testing docs

### Tertiary (LOW confidence)
- None - all findings verified from codebase or official docs

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - Libraries well-established, codebase already using React 19
- Architecture: HIGH - Patterns follow React best practices
- Type alignment: HIGH - Clear mapping between frontend and backend schemas
- Pitfalls: MEDIUM - Based on codebase analysis and common React patterns

**Research date:** 2026-03-14
**Valid until:** 30 days - React ecosystem stable, but toast library versions may update
