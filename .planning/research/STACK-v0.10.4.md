# Stack Research -- v0.10.4 Playwright Code Verification and Task Management UI

**Domain:** Playwright code verification, read-only code viewer, and pytest execution from web UI
**Researched:** 2026-04-23
**Confidence:** HIGH

## Recommended Stack

### Core Technologies (NEW additions only)

| Technology | Version | Purpose | Why Recommended |
|------------|---------|---------|-----------------|
| react-syntax-highlighter | ^16.1.1 | Read-only Python code viewer component | Drop-in React component with built-in Python support, zero-config inline styles (no CSS file needed), line numbers out of the box. Lighter than Monaco/CodeMirror for read-only use. Already bundles both Prism and Highlight.js engines. |
| @types/react-syntax-highlighter | ^15.5.13 | TypeScript definitions | Required for TypeScript projects. Covers all props including `showLineNumbers`, `wrapLongLines`, `customStyle`. |

### Why react-syntax-highlighter over alternatives

**Versus prism-react-renderer (2.4.1):** prism-react-renderer is leaner (render-props API, no built-in themes) but requires more boilerplate for the same result. For a read-only viewer, react-syntax-highlighter's `<SyntaxHighlighter>` with built-in styles is a better fit -- you write 5 lines of JSX instead of 20. prism-react-renderer is better when you need full control over token rendering or React Native support.

**Versus Shiki:** Shiki produces the most accurate highlighting (VS Code's TextMate engine) but is async-only, requires server-side rendering or await, and adds complexity for a simple code viewer. Shiki is ideal for static docs sites (VitePress, Astro), not a dynamic React panel.

**Versus Monaco Editor / CodeMirror:** Full editors are overkill for read-only display. Monaco adds ~4MB to the bundle. CodeMirror 6 requires significant setup. Both support read-only mode but you pay the cost of an entire editor for a viewer. Use these only if editing is needed later.

**Versus a `<pre>` tag with manual highlighting:** No syntax coloring makes Python code unreadable for QA users. The ~40KB gzipped cost of react-syntax-highlighter (with Prism Python grammar) is worth the UX improvement.

### Backend: NO new dependencies needed

The existing stack already has everything required:

| Existing Technology | Already Used For | New Use |
|---------------------|-----------------|---------|
| subprocess.run (stdlib) | SelfHealingRunner runs pytest via subprocess | Same pattern for UI-triggered pytest execution |
| asyncio.to_thread (stdlib) | SelfHealingRunner runs subprocess in thread | Same pattern to avoid blocking the event loop |
| FastAPI BackgroundTasks | run_agent_background in runs.py | Same pattern for async code execution endpoint |
| pathlib.Path (stdlib) | File I/O throughout codebase | Reading generated code file contents |
| Run.generated_code_path (DB field) | Already stores path to generated .py file | Read code from this path for viewer API |
| Run.healing_status (DB field) | Already tracks "pending/passed/failed/skipped" | Expose to frontend for code status indicator |
| Task.status (DB field) | "draft" / "ready" | Extend to include "success" |

## Supporting Libraries

### Frontend

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| react-syntax-highlighter Prism build | ^16.1.1 | Python code highlighting in viewer | Import `{ Prism as SyntaxHighlighter }` for lighter bundle vs hljs build |
| lucide-react (existing) | ^0.577.0 | Icons for "view code" and "run code" buttons | Already installed, use `Code2` / `Play` icons |

### Backend (all stdlib, no pip install)

| Module | Purpose | When to Use |
|--------|---------|-------------|
| subprocess | Run pytest for code verification | Existing SelfHealingRunner pattern |
| asyncio.to_thread | Non-blocking subprocess | Existing pattern |
| pathlib.Path | Read generated .py file contents | New API endpoint for code viewer |
| json (stdlib) | Parse pytest output | Existing pattern |

## Installation

```bash
# Frontend only -- one new dependency
cd frontend && npm install react-syntax-highlighter
cd frontend && npm install -D @types/react-syntax-highlighter

# Backend -- nothing to install
```

## Alternatives Considered

| Recommended | Alternative | When to Use Alternative |
|-------------|-------------|-------------------------|
| react-syntax-highlighter | prism-react-renderer | If you need maximum bundle size control, custom token rendering, or React Native support. Requires more boilerplate code. |
| react-syntax-highlighter | Shiki | If building a docs site with static rendering. Overkill for a dynamic React panel. Async API adds complexity. |
| react-syntax-highlighter | Monaco Editor | If you need code editing (not just viewing) in the future. ~4MB bundle cost. Would revisit if CODE-01 evolves to include code editing. |
| react-syntax-highlighter | `<pre>` tag (no library) | If bundle size is absolutely critical and you can accept plain monospaced text. Not recommended for QA users. |

## What NOT to Use

| Avoid | Why | Use Instead |
|-------|-----|-------------|
| Monaco Editor | 4MB+ bundle for a read-only viewer. Heavy initialization time. Memory intensive. | react-syntax-highlighter (40KB gzipped) |
| CodeMirror 6 | Complex setup, overkill for read-only. Requires @codemirror/lang-python, theme packages, etc. | react-syntax-highlighter |
| highlight.js directly | Requires DOM manipulation or dangerouslySetInnerHTML. react-syntax-highlighter wraps it properly for React. | react-syntax-highlighter (uses refractor/lowlight internally) |
| Shiki | Async-only API (codeToHtml is async), designed for build-time/static rendering. Requires createHighlighter init. Overkill for viewing a single file. | react-syntax-highlighter (synchronous, simpler) |
| Full IDE (Theia, etc.) | Absolutely not. This is a QA tool, not a developer IDE. | react-syntax-highlighter |

## Stack Patterns by Variant

**For the Code Viewer Panel (UI-02):**
- Use `{ Prism as SyntaxHighlighter }` from react-syntax-highlighter (Prism build, not Highlight.js)
- Prism's Python grammar is well-maintained and lighter than hljs
- Use `vscDarkPlus` theme from `react-syntax-highlighter/dist/esm/styles/prism` for VS Code-like appearance
- Enable `showLineNumbers` and `wrapLongLines` for readability

```tsx
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter'
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism'

function CodeViewer({ code }: { code: string }) {
  return (
    <SyntaxHighlighter
      language="python"
      style={vscDarkPlus}
      showLineNumbers
      wrapLongLines
      customStyle={{ borderRadius: '8px', margin: 0 }}
    >
      {code}
    </SyntaxHighlighter>
  )
}
```

**For the "Code" Column in Task List (UI-01):**
- No new dependency needed. Use existing lucide-react `Code2` icon
- Show a simple badge/icon based on whether the task has a run with `generated_code_path`
- Query: join tasks -> runs -> check if any run has non-null `generated_code_path`

**For "Run Code" Button (UI-03):**
- Reuse existing `SelfHealingRunner.run()` method directly -- it already handles:
  - Storage state injection (login auth)
  - Subprocess pytest execution with timeout
  - LLM retry loop on failure
  - Error output capture
- Add a new FastAPI endpoint `POST /runs/{run_id}/execute-code` that:
  1. Reads the run's `generated_code_path`
  2. Calls `SelfHealingRunner.run()` with the path
  3. Returns the `HealingResult`
- Alternatively, for simpler "just run it" without healing, call subprocess directly (existing pattern from SelfHealingRunner lines 187-199)

**For Task Status Extension (STATUS-01):**
- Extend `Task.status` from `"draft" | "ready"` to `"draft" | "ready" | "success"`
- Update `TaskUpdate.status` regex pattern in schemas.py
- Add "success" to frontend `StatusBadge` config
- Trigger: when a run's `healing_status` becomes "passed", mark the task as "success"

## Version Compatibility

| Package A | Compatible With | Notes |
|-----------|-----------------|-------|
| react-syntax-highlighter@16.1.1 | React 19.x | Compatible. Uses render functions, no deprecated lifecycle methods |
| react-syntax-highlighter@16.1.1 | @types/react-syntax-highlighter@15.5.13 | Types package is at 15.x but covers 16.x API. Standard pattern. |
| react-syntax-highlighter@16.1.1 | Vite 7.x | ESM imports work fine with `dist/esm/` paths |
| react-syntax-highlighter@16.1.1 | Tailwind CSS 4.x | No conflict. Inline styles by default, or set `useInlineStyles={false}` to use CSS classes with Tailwind |

## API Design for New Endpoints

### GET /runs/{run_id}/code
Returns the generated Playwright code content for viewing.

```python
# Response schema
class CodeResponse(BaseModel):
    code: str                    # Full file contents
    language: str = "python"     # Always Python (Playwright/pytest)
    file_path: str               # Original file path for display
    healing_status: str          # Current healing status
    last_modified: str | None    # File mtime
```

Implementation: Read `run.generated_code_path` from DB, then `Path(path).read_text()`. Return 404 if no code exists.

### POST /runs/{run_id}/execute-code
Triggers pytest execution of the generated code.

```python
# Request: empty body (run_id in URL is sufficient)
# Response:
class ExecuteCodeResponse(BaseModel):
    status: str          # "passed" | "failed" | "skipped"
    attempts: int        # Number of pytest attempts
    error_message: str   # Truncated error output on failure
    duration_ms: int     # Total execution time
```

Implementation: Reuse `SelfHealingRunner.run()` with the run's `generated_code_path` and `login_role`. Update healing status in DB after execution.

### GET /tasks (modify response)
Add `has_code` boolean field to `TaskResponse`:

```python
class TaskResponse(BaseModel):
    # ... existing fields ...
    has_code: bool = False  # True if any run has generated_code_path
```

Implementation: Subquery or join to check if any run for the task has a non-null `generated_code_path`.

## Sources

- [react-syntax-highlighter on NPM](https://www.npmjs.com/package/react-syntax-highlighter) -- verified latest version 16.1.1, Python support confirmed (HIGH confidence)
- [prism-react-renderer on NPM](https://www.npmjs.com/package/prism-react-renderer) -- version 2.4.1, evaluated as alternative (HIGH confidence)
- [Shiki vs Prism vs highlight.js comparison (pkgpulse.com)](https://www.pkgpulse.com/blog/shiki-vs-prismjs-vs-highlightjs-syntax-highlighting-javascript-2026) -- verified feature comparison, Feb 2026 data (MEDIUM confidence)
- [chsm.dev code highlighter comparison](https://chsm.dev/blog/2025/01/08/comparing-web-code-highlighters) -- performance benchmarks (MEDIUM confidence)
- Existing codebase analysis: `backend/core/self_healing_runner.py` (subprocess pattern), `backend/db/models.py` (Run.generated_code_path), `backend/api/routes/runs.py` (BackgroundTasks pattern) (HIGH confidence)
- FastAPI release notes -- version 0.133.1 (2026-02-25) confirms active maintenance (MEDIUM confidence)

---
*Stack research for: v0.10.4 Playwright code verification and task management UI integration*
*Researched: 2026-04-23*
