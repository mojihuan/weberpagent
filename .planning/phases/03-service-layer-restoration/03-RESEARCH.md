# Phase 3: Service Layer Restoration - Research

**Researched:** 2026-03-14
**Domain:** Service layer patterns (AssertionService, ReportService, SSE heartbeat, LLM retry)
**Confidence:** HIGH

## Summary

This phase focuses on restoring and enhancing four critical service layer components in the aiDriveUITest platform: AssertionService for validating test assertions against run results, ReportService for generating comprehensive test reports, SSE EventManager heartbeat mechanism for maintaining real-time connections, and LLM retry logic for resilient API calls.

**Primary recommendation:** Follow existing project patterns (Repository pattern, service layer separation, FastAPI BackgroundTasks) and use Tenacity library for LLM retry (already in dependencies). SSE heartbeat should use comment format (`:heartbeat`) per SSE specification.

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

**断言结果存储流程**
- 返回类型：AssertionService 返回 `AssertionResult` ORM 对象（非 dict）
- 存储位置：服务内存储 — AssertionService 接收 run_id，内部调用 AssertionResultRepository
- 失败详情：message 字段记录详细失败原因，如 "URL 不包含 'dashboard'，实际为 'login'"
- 断言类型：
  - `url_contains`（已有）— 检查 URL 是否包含期望字符串
  - `text_exists`（已有）— 检查页面是否包含期望文本
  - `no_errors`（已有）— 检查执行是否无错误
  - `element_exists`（新增）— 检查页面元素是否存在（CSS 选择器）
- 执行策略：所有断言独立执行，无依赖关系，执行完成后统一检查
- 断言层级：Task 级别（Phase 2 已确定）

**报告生成服务设计**
- 服务结构：新建 `ReportService` 类，与 AssertionService/AgentService 平级
- 生成时机：任务执行完成后自动生成，用户无需手动操作
- 报告内容：
  - 基础统计（通过/失败状态、步骤数、耗时）
  - 步骤详情（每个步骤的信息和截图链接）
  - 断言结果（每个断言的结果和失败原因）
  - 错误信息（执行过程中的错误和堆栈）
- 断言展示：显示通过率百分比
- 报告特性：不可变，不支持重新生成

**SSE 心跳实现**
- 心跳间隔：20 秒
- 事件格式：SSE 注释格式（`:heartbeat`），浏览器 EventSource 自动忽略
- 超时检测：只发送心跳，不检测客户端超时断开（依赖 TCP 层）

**LLM 重试机制**
- 重试策略：指数退避（1s → 2s → 4s）
- 最大重试次数：3 次
- 可重试错误：
  - 网络超时
  - 速率限制（429/503）
  - 响应格式错误
- 不可重试错误：
  - 认证失败
  - 配额不足
  - API Key 无效
- 实现位置：LLM Factory 层（`backend/llm/factory.py` 的 `create_llm()` 函数）
- 日志记录：详细日志（每次重试记录错误类型、等待时间、重试次数）

### Claude's Discretion

- AssertionService 具体方法签名设计
- ReportService 内部方法组织
- SSE 心跳在 EventManager 中的具体实现方式
- LLM 重试装饰器/包装函数的具体实现

### Deferred Ideas (OUT OF SCOPE)

None — 讨论保持在 Phase 范围内
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| SVC-01 | AssertionService validates assertions against run results | Existing AssertionService at `backend/core/assertion_service.py` provides foundation; needs ORM adaptation and new `element_exists` type |
| SVC-02 | ReportService generates test reports with all step details | New service class; ReportRepository exists at `backend/db/repository.py`; Report model at `backend/db/models.py` |
| SVC-03 | AgentService uses proper LLM configuration (temperature=0) | Settings already configures `llm_temperature=0.0`; `get_llm_config()` in `runs.py` passes it to AgentService |
| SVC-04 | SSE EventManager includes heartbeat events (15-30s interval) | EventManager at `backend/core/event_manager.py`; SSE heartbeat uses asyncio task with comment format |
| SVC-05 | All background tasks update database status on completion/error | Pattern established in `run_agent_background()` with try/except/finally blocks |
</phase_requirements>

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| tenacity | 8.0.0+ | Retry logic with exponential backoff | Already in dependencies; industry standard for Python retries |
| asyncio | stdlib | Async heartbeat task management | Native async support; used throughout codebase |
| FastAPI | 0.135.1+ | SSE streaming responses | Project's web framework; native SSE support |
| Pydantic | 2.4.0+ | Data validation and schemas | Project standard for all request/response models |
| SQLAlchemy | 2.0.0+ | ORM and async database operations | Project's data layer; async engine configured |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| pytest-asyncio | 0.24.0+ | Async test support | Testing all service layer components |
| pytest | 8.0.0+ | Test framework | All unit/integration tests |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| tenacity | backoff library | tenacity is already in dependencies; more feature-rich |
| SSE comment heartbeat | SSE data event | Comment format (`:heartbeat`) is invisible to EventSource clients; cleaner implementation |

**Installation:**
No new packages needed - all dependencies are already in `pyproject.toml`.

## Architecture Patterns

### Recommended Project Structure
```
backend/
├── core/
│   ├── assertion_service.py   # AssertionService (modify)
│   ├── report_service.py      # ReportService (NEW)
│   ├── agent_service.py       # AgentService (no changes needed)
│   └── event_manager.py       # EventManager (modify for heartbeat)
├── llm/
│   └── factory.py             # create_llm() with retry (modify)
├── db/
│   ├── models.py              # ORM models (already has AssertionResult)
│   └── repository.py          # Add AssertionResultRepository (NEW class)
└── api/routes/
    └── runs.py                # Background task integration (modify)
```

### Pattern 1: Service Layer Pattern
**What:** Services encapsulate business logic, use repositories for data access
**When to use:** All service classes (AssertionService, ReportService)
**Example:**
```python
# Source: existing project pattern from backend/core/agent_service.py
class AssertionService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.assertion_result_repo = AssertionResultRepository(session)

    async def evaluate_assertions(self, run_id: str, history: Any) -> list[AssertionResult]:
        # Get assertions for the task
        # Evaluate each assertion
        # Store results via repository
        # Return ORM objects
```

### Pattern 2: SSE Heartbeat with asyncio
**What:** Background task sends periodic heartbeat comments to keep connection alive
**When to use:** Long-running SSE connections in EventManager
**Example:**
```python
# Source: FastAPI SSE best practices + project requirements
class EventManager:
    async def _heartbeat_loop(self, run_id: str, interval: float = 20.0):
        """Send heartbeat comments periodically"""
        while not self.is_finished(run_id):
            await asyncio.sleep(interval)
            # SSE comment format - ignored by EventSource
            await self.publish(run_id, ":heartbeat\n\n")

    async def subscribe(self, run_id: str) -> AsyncGenerator[str | None, None]:
        # Start heartbeat task
        heartbeat = asyncio.create_task(self._heartbeat_loop(run_id))
        try:
            # ... existing subscription logic ...
        finally:
            heartbeat.cancel()
```

### Pattern 3: Tenacity Retry for LLM Calls
**What:** Decorator pattern with exponential backoff for transient errors
**When to use:** LLM API calls that may fail due to rate limits or network issues
**Example:**
```python
# Source: https://python.useinstructor.com/concepts/retrying/
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
    before_sleep_log,
)
import logging

logger = logging.getLogger(__name__)

# Define retryable exceptions
RETRYABLE_EXCEPTIONS = (
    TimeoutError,
    ConnectionError,
    # OpenAI-specific rate limit errors would go here
)

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=4),
    retry=retry_if_exception_type(RETRYABLE_EXCEPTIONS),
    before_sleep=before_sleep_log(logger, logging.WARNING),
)
def create_llm_with_retry(llm_config: dict | None = None) -> "ChatOpenAI":
    """Create LLM instance with retry logic"""
    # ... existing create_llm logic ...
```

### Anti-Patterns to Avoid
- **Storing assertion results as dict:** Must return ORM objects (AssertionResult) for consistency with other services
- **SSE data events for heartbeat:** Use comment format (`:heartbeat`) - data events trigger client-side handlers unnecessarily
- **Global retry configuration:** Retry parameters should be configurable but have sensible defaults
- **Silent retry failures:** Always log retry attempts with error type and wait time

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| LLM retry logic | Custom retry loops with sleep | tenacity library | Already in dependencies; handles exponential backoff, jitter, logging |
| SSE keep-alive | Polling from client | Server-side heartbeat comments | Reduces client complexity; SSE spec compliant |
| Assertion storage | Direct SQL in service | AssertionResultRepository | Follows Repository pattern; easier testing |

**Key insight:** The project already follows clean architecture patterns. New services should follow the same Repository pattern used by TaskRepository, RunRepository, etc.

## Common Pitfalls

### Pitfall 1: AssertionService Returns Dict Instead of ORM
**What goes wrong:** Services returning dict break type hints and don't integrate with existing response schemas
**Why it happens:** Existing `run_all_assertions()` returns `dict[str, bool]`
**How to avoid:** Create `AssertionResultRepository`, modify AssertionService to accept `session: AsyncSession`, return `list[AssertionResult]`
**Warning signs:** Type checker errors, missing `created_at` timestamps, no database persistence

### Pitfall 2: SSE Heartbeat Blocks Event Stream
**What goes wrong:** Heartbeat task blocks the main event stream from sending data
**Why it happens:** Using `await` in wrong place or not creating separate asyncio task
**How to avoid:** Use `asyncio.create_task()` for heartbeat loop, run in parallel with subscription
**Warning signs:** Events delayed by heartbeat interval, no events until heartbeat fires

### Pitfall 3: LLM Retry Catches Non-Retryable Errors
**What goes wrong:** Authentication failures or quota errors trigger infinite retries
**Why it happens:** Broad exception catching without filtering
**How to avoid:** Use `retry_if_exception_type()` with specific error types (TimeoutError, ConnectionError, rate limit errors)
**Warning signs:** Long delays on auth failures, logs showing 401/403 being retried

### Pitfall 4: Report Missing Assertion Results
**What goes wrong:** Report doesn't include assertion pass/fail details
**Why it happens:** ReportService doesn't query AssertionResult table
**How to avoid:** ReportService should call AssertionResultRepository to get all results for run_id
**Warning signs:** Report shows steps but no assertion section, assertion pass rate shows 0% when assertions exist

## Code Examples

### AssertionResultRepository (NEW)
```python
# Source: Following existing Repository pattern in backend/db/repository.py
from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.db.models import AssertionResult


class AssertionResultRepository:
    """断言结果仓库"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
        self,
        run_id: str,
        assertion_id: str,
        status: str,
        message: str | None = None,
        actual_value: str | None = None,
    ) -> AssertionResult:
        result = AssertionResult(
            run_id=run_id,
            assertion_id=assertion_id,
            status=status,
            message=message,
            actual_value=actual_value,
        )
        self.session.add(result)
        await self.session.commit()
        await self.session.refresh(result)
        return result

    async def list_by_run(self, run_id: str) -> List[AssertionResult]:
        stmt = (
            select(AssertionResult)
            .where(AssertionResult.run_id == run_id)
            .order_by(AssertionResult.created_at)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars())
```

### AssertionService with ORM (MODIFIED)
```python
# Source: Adapted from existing backend/core/assertion_service.py
from typing import Any
from sqlalchemy.ext.asyncio import AsyncSession
from backend.db.models import AssertionResult, Assertion
from backend.db.repository import AssertionResultRepository


class AssertionService:
    """断言服务 - 返回 ORM 对象"""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.result_repo = AssertionResultRepository(session)

    async def check_url_contains(self, history: Any, expected: str) -> tuple[bool, str, str]:
        """检查 URL 是否包含期望字符串

        Returns: (passed, message, actual_value)
        """
        try:
            if hasattr(history, "final_result") and history.final_result:
                url = getattr(history.final_result, "url", "")
                passed = expected in str(url)
                message = "" if passed else f"URL 不包含 '{expected}'，实际为 '{url}'"
                return passed, message, url
        except Exception as e:
            return False, f"检查失败: {str(e)}", ""
        return False, f"无法获取 URL", ""

    async def check_element_exists(self, history: Any, selector: str) -> tuple[bool, str, str]:
        """检查元素是否存在 (新增断言类型)

        Returns: (passed, message, actual_value)
        """
        # Implementation depends on browser state access
        # This is a placeholder - actual implementation needs DOM access
        try:
            if hasattr(history, "final_result") and history.final_result:
                # Would need to check browser state for element
                # For now, return based on no_errors check
                return True, "元素检查通过", selector
        except Exception as e:
            return False, f"元素检查失败: {str(e)}", ""
        return False, f"无法检查元素 '{selector}'", ""

    async def evaluate_all(
        self,
        run_id: str,
        assertions: list[Assertion],
        history: Any,
    ) -> list[AssertionResult]:
        """评估所有断言并存储结果"""
        results = []

        for assertion in assertions:
            if assertion.type == "url_contains":
                passed, message, actual = await self.check_url_contains(
                    history, str(assertion.expected)
                )
            elif assertion.type == "text_exists":
                passed, message, actual = self.check_text_exists(
                    history, str(assertion.expected)
                )
            elif assertion.type == "no_errors":
                passed = self.check_no_errors(history)
                message = "" if passed else "执行过程中存在错误"
                actual = "无错误" if passed else "有错误"
            elif assertion.type == "element_exists":
                passed, message, actual = await self.check_element_exists(
                    history, str(assertion.expected)
                )
            else:
                passed = False
                message = f"未知断言类型: {assertion.type}"
                actual = ""

            result = await self.result_repo.create(
                run_id=run_id,
                assertion_id=assertion.id,
                status="pass" if passed else "fail",
                message=message,
                actual_value=actual,
            )
            results.append(result)

        return results
```

### SSE Heartbeat in EventManager (MODIFIED)
```python
# Source: Modified from existing backend/core/event_manager.py
import asyncio
from collections import defaultdict
from typing import AsyncGenerator


class EventManager:
    def __init__(self, heartbeat_interval: float = 20.0):
        self._events: dict[str, list[str | None]] = defaultdict(list)
        self._subscribers: dict[str, list[asyncio.Queue]] = defaultdict(list)
        self._status: dict[str, str] = {}
        self._heartbeat_interval = heartbeat_interval
        self._heartbeat_tasks: dict[str, asyncio.Task] = {}

    async def _send_heartbeat(self, run_id: str):
        """Background task to send heartbeat comments"""
        while not self.is_finished(run_id):
            await asyncio.sleep(self._heartbeat_interval)
            if not self.is_finished(run_id):
                # SSE comment format - ignored by EventSource
                for queue in self._subscribers.get(run_id, []):
                    await queue.put(":heartbeat\n\n")

    async def subscribe(self, run_id: str) -> AsyncGenerator[str | None, None]:
        """Subscribe with heartbeat support"""
        queue: asyncio.Queue[str | None] = asyncio.Queue()
        self._subscribers[run_id].append(queue)

        # Start heartbeat task
        heartbeat_task = asyncio.create_task(self._send_heartbeat(run_id))
        self._heartbeat_tasks[run_id] = heartbeat_task

        try:
            # Send history first
            for event in self._events.get(run_id, []):
                yield event

            if self.is_finished(run_id):
                return

            # Wait for new events
            while True:
                event = await queue.get()
                yield event
                if event is None:
                    break
        finally:
            # Cleanup
            if queue in self._subscribers[run_id]:
                self._subscribers[run_id].remove(queue)
            heartbeat_task.cancel()
            if run_id in self._heartbeat_tasks:
                del self._heartbeat_tasks[run_id]
```

### LLM Retry with Tenacity (MODIFIED)
```python
# Source: Modified from existing backend/llm/factory.py
import logging
from typing import Type, Optional
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
    before_sleep_log,
)

logger = logging.getLogger(__name__)

# Retryable error types
RETRYABLE_ERRORS = (
    TimeoutError,
    ConnectionError,
    # Add OpenAI-specific rate limit errors if available
)


def _should_retry_llm_error(exception: Exception) -> bool:
    """Determine if error is retryable"""
    error_str = str(exception).lower()

    # Non-retryable patterns
    non_retryable = ["401", "403", "unauthorized", "invalid api key", "quota"]
    if any(pattern in error_str for pattern in non_retryable):
        return False

    # Retryable patterns
    retryable = ["429", "503", "timeout", "rate limit", "connection"]
    return any(pattern in error_str for pattern in retryable)


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=4),
    retry=retry_if_exception_type(RETRYABLE_ERRORS),
    before_sleep=before_sleep_log(logger, logging.WARNING),
    reraise=True,
)
def create_llm_with_retry(llm_config: dict | None = None) -> "ChatOpenAI":
    """Create browser-use compatible ChatOpenAI instance with retry logic

    Retry configuration:
    - Max attempts: 3
    - Wait: exponential (1s, 2s, 4s)
    - Retryable: Timeout, Connection, Rate limit (429/503)
    - Non-retryable: Auth failures (401/403), Quota, Invalid API Key
    """
    from browser_use.llm.openai.chat import ChatOpenAI as BrowserUseChatOpenAI

    config = llm_config or {}
    model = config.get("model", "gpt-4o")
    api_key = config.get("api_key")
    base_url = config.get("base_url")
    temperature = config.get("temperature", 0.0)

    attempt_number = create_llm_with_retry.retry.statistics.get("attempt_number", 0)
    if attempt_number > 0:
        logger.warning(
            f"LLM 调用重试，第 {attempt_number} 次，"
            f"等待 {create_llm_with_retry.retry.wait} 秒"
        )

    logger.info(f"create_llm: model={model}, base_url={base_url}, temperature={temperature}")

    try:
        llm = BrowserUseChatOpenAI(
            model=model,
            api_key=api_key,
            base_url=base_url,
            temperature=temperature,
        )
        logger.info(f"create_llm: 成功创建 ChatOpenAI, model={llm.model}")
        return llm
    except Exception as e:
        error_type = type(e).__name__
        logger.error(f"create_llm: 创建失败 - {error_type}: {e}")

        # Check if error should not be retried
        if not _should_retry_llm_error(e):
            logger.error(f"create_llm: 不可重试错误，放弃重试")
            raise

        raise  # Let tenacity handle retry
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| SSE without heartbeat | SSE with comment-format heartbeat | 2025+ | Prevents connection drops for long-running tasks |
| Manual retry loops | Tenacity decorator | Industry standard | Cleaner code, better logging, configurable |
| Dict returns from services | ORM object returns | Phase 3 | Type safety, consistent with existing patterns |

**Deprecated/outdated:**
- Custom retry logic with `while` loops and `time.sleep()`: Use tenacity instead
- SSE data events for heartbeat: Use comment format (`:heartbeat\n\n`)

## Open Questions

1. **element_exists assertion implementation**
   - What we know: Needs CSS selector, must check browser state
   - What's unclear: How to access browser DOM from AgentService history object
   - Recommendation: Check browser_use Agent history structure for DOM access; may need to capture during step execution

2. **ReportService integration with existing report creation**
   - What we know: ReportRepository.create() exists, reports currently created inline in runs.py
   - What's unclear: Should ReportService replace inline creation or be called after?
   - Recommendation: Extract report creation logic to ReportService, call from background task

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | pytest 8.0.0+ with pytest-asyncio 0.24.0+ |
| Config file | pyproject.toml (asyncio_mode = "auto") |
| Quick run command | `uv run pytest backend/tests/unit/test_assertion_service.py -x` |
| Full suite command | `uv run pytest backend/tests/ -v` |

### Phase Requirements -> Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| SVC-01 | AssertionService evaluates assertions and returns ORM objects | unit | `uv run pytest backend/tests/unit/test_assertion_service.py -x` | Needs creation |
| SVC-02 | ReportService generates reports with all details | unit | `uv run pytest backend/tests/unit/test_report_service.py -x` | Needs creation |
| SVC-03 | AgentService uses temperature=0 | unit | `uv run pytest backend/tests/unit/test_agent_service.py::test_llm_temperature -x` | Exists (partial) |
| SVC-04 | SSE EventManager sends heartbeat every 20s | unit | `uv run pytest backend/tests/unit/test_event_manager.py::test_heartbeat -x` | Needs creation |
| SVC-05 | Background tasks update status on completion/error | integration | `uv run pytest backend/tests/integration/test_runs.py -x` | Needs creation |

### Sampling Rate
- **Per task commit:** `uv run pytest backend/tests/unit/ -x`
- **Per wave merge:** `uv run pytest backend/tests/ -v`
- **Phase gate:** Full suite green before `/gsd:verify-work`

### Wave 0 Gaps
- [ ] `backend/tests/unit/test_assertion_service.py` - covers SVC-01 (AssertionService with ORM)
- [ ] `backend/tests/unit/test_report_service.py` - covers SVC-02 (ReportService)
- [ ] `backend/tests/unit/test_event_manager.py::test_heartbeat` - covers SVC-04 (heartbeat)
- [ ] `backend/tests/unit/test_llm_retry.py` - covers LLM retry logic
- [ ] `backend/tests/integration/test_runs_background.py` - covers SVC-05 (background task status)
- [ ] `backend/db/repository.py::AssertionResultRepository` - NEW class needed

## Sources

### Primary (HIGH confidence)
- Existing codebase: `backend/core/assertion_service.py`, `backend/core/event_manager.py`, `backend/llm/factory.py`
- Existing patterns: `backend/db/repository.py` (Repository pattern)
- pyproject.toml - dependency versions confirmed

### Secondary (MEDIUM confidence)
- [Instructor Retrying Docs](https://python.useinstructor.com/concepts/retrying/) - Tenacity patterns for LLM APIs
- [Tenacity Documentation](https://tenacity.readthedocs.io/) - Exponential backoff configuration

### Tertiary (LOW confidence)
- [Medium: Robust LLM API Strategies](https://ai.gopubby.com/robust-llm-api-strategies-retries-fallbacks-in-python-caf9efa96908) - General LLM retry patterns

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - All dependencies already in project
- Architecture: HIGH - Following existing Repository and Service patterns
- Pitfalls: HIGH - Based on analysis of existing code and common SSE/async patterns

**Research date:** 2026-03-14
**Valid until:** 30 days (stable patterns, well-established libraries)
