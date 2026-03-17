# Phase 6: 接口断言集成 - Research

**Researched:** 2026-03-16
**Domain:** Python 断言框架， FastAPI + Pydantic + SQLAlchemy async
**Confidence:** HIGH

## Summary

本阶段实现接口断言功能，允许用户通过 API 调用验证测试结果。核心设计复用 Phase 5 的 `PreconditionService` 执行模式（`exec()` + 30秒超时 + Jinja2 变量替换），新增 `ApiAssertionService` 处理时间断言（±1分钟）、数据断言（精确/包含/小数近似匹配），并将断言结果集成到测试报告中。

**Primary recommendation:** 复用 Phase 5 的代码执行基础设施，扩展 `AssertionService` 支持新的断言类型，在 `run_agent_background` 中 UI 测试完成后执行接口断言。

<user_constraints>

## User Constraints (from CONTEXT.md)

### Locked Decisions

- **移植现有 BaseAssert 类** - 将现有项目的 BaseAssert 类移植到 aiDriveUITest
- 复用现有的多层封装设计（查询层 → 数据层 → 断言层 → 报告层）
- **Python 代码格式** - 与前置条件一致，用户直接写 Python 代码
- 通过 `context['变量名']` 存储结果，支持 Jinja2 变量替换
- **独立输入区域** - 在任务编辑页增加「接口断言」输入区域，与「前置条件」、「测试步骤」分开显示
- **UI 测试完成后执行** - 执行顺序：前置条件 → UI 测试 → 接口断言 → 生成报告
- **可以引用前置条件变量** - 接口断言代码可以引用前置条件中存储的变量
- **断言类型支持** - 精确匹配、包含匹配、时间断言（±1 分钟范围）、小数近似
- **多字段断言处理** - 合并为一条记录，显示各字段通过/失败状态
- **固定 ±1 分钟** - 时间断言范围，不提供配置选项
- **简洁模式错误信息** - 只显示不匹配的字段和预期/实际值对比
- **独立区域显示** - 在测试报告中新增「接口断言」区域

### Claude's Discretion

- 具体的 BaseAssert 类移植实现细节
- 前端接口断言输入组件样式（是否用 Monaco Editor）
- 小数近似的默认误差范围（如 0.01 或 0.001）
- 断言执行错误处理逻辑

### Deferred Ideas (OUT OF SCOPE)

None - 讨论保持在 Phase 范围内

</user_constraints>

<phase_requirements>

## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| API-01 | 用户可以通过 API 调用进行接口断言 | 复用 Phase 5 的 `exec()` 执行机制 + 外部模块路径配置 |
| API-02 | 用户可以进行时间断言（±1 分钟范围） | 使用 Python `datetime` + `timedelta` 进行时间范围比较 |
| API-03 | 用户可以进行数据断言（匹配预期值） | 支持精确匹配、包含匹配、小数近似三种断言类型 |
| API-04 | 断言结果展示在测试报告中 | 扩展 `ReportService` + `AssertionResult` 模型，前端新增断言结果展示组件 |

</phase_requirements>

## Standard Stack

### Core

| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| Python | 3.11+ | 主语言 | 项目要求 |
| FastAPI | 0.135.1+ | API 框架 | 现有项目已使用 |
| Pydantic | 2.4.0+ | 数据验证 | 现有项目已使用 |
| SQLAlchemy | 2.0.0+ | ORM | 现有项目已使用，async 支持 |
| Jinja2 | 3.1.6+ | 变量替换 | Phase 5 已集成 |
| pytest | 8.0.0+ | 测试框架 | 现有项目已使用 |
| pytest-asyncio | 0.24.0+ | 异步测试 | 现有项目已使用 |

### Supporting

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| aiosqlite | 0.20.0+ | 异步 SQLite | 数据库操作 |
| httpx | 0.28.1+ | HTTP 客户端 | API 调用测试 |
| python-dotenv | 1.0.0+ | 环境变量 | 配置管理 |

### Alternatives Considered

| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| 自定义 BaseAssert | assertpy 库 | assertpy 更通用，但自定义类更贴合现有项目三层架构 |
| 复杂断言语法 | DSL 解析器 | DSL 更安全，但 Python 代码更灵活、用户学习成本低 |

**Installation:**
```bash
# 已在 pyproject.toml 中配置，无需额外安装
uv sync
```

## Architecture Patterns

### Recommended Project Structure

```
backend/
├── core/
│   ├── api_assertion_service.py   # 新增：接口断言执行服务
│   ├── assertion_service.py       # 现有：UI 断言服务
│   ├── precondition_service.py    # 现有：前置条件服务（复用）
│   └── report_service.py          # 扩展：报告服务
├── db/
│   ├── models.py                  # 扩展：Task.api_assertions 字段
│   ├── schemas.py                 # 扩展：api_assertions 字段
│   └── repository.py              # 可能扩展
├── api/routes/
│   ├── tasks.py                   # 扩展：保存 api_assertions
│   └── runs.py                    # 扩展：执行流程集成
frontend/src/
├── components/
│   ├── TaskModal/
│   │   └── TaskForm.tsx           # 扩展：接口断言输入区域
│   └── Report/
│       └── ApiAssertionResults.tsx # 新增：接口断言结果展示
└── types/
    └── index.ts                   # 扩展：api_assertions 类型
```

### Pattern 1: ApiAssertionService 设计

**What:** 接口断言执行服务，复用 `PreconditionService` 的执行机制，新增断言判断逻辑

**When to use:** UI 测试完成后执行 API 断言

**Example:**
```python
# Source: 参考 Phase 5 PreconditionService + CONTEXT.md 决策
# backend/core/api_assertion_service.py

import asyncio
import logging
import time
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any

from jinja2 import Environment, StrictUndefined

logger = logging.getLogger(__name__)


@dataclass
class FieldAssertionResult:
    """单个字段断言结果"""
    field_name: str
    expected: Any
    actual: Any
    passed: bool = False
    message: str = ""
    assertion_type: str = "exact"  # exact, contains, time, decimal


@dataclass
class ApiAssertionResult:
    """接口断言执行结果"""
    index: int
    code: str
    success: bool = False
    error: str | None = None
    duration_ms: int = 0
    field_results: list[FieldAssertionResult] = field(default_factory=list)


class ApiAssertionService:
    """接口断言执行服务

    复用 PreconditionService 的 exec() 执行机制，
    新增断言判断逻辑（时间、精确匹配、包含匹配、小数近似）
    """

    # 时间断言默认容差（秒）
    TIME_TOLERANCE_SECONDS = 60  # ±1 分钟

    # 小数近似默认容差
    DECIMAL_TOLERANCE = 0.01

    def __init__(self, external_module_path: str | None = None):
        self.external_module_path = external_module_path
        self.context: dict[str, Any] = {}

    def check_time_within_range(
        self,
        actual_time: datetime | str,
        tolerance_seconds: int = 60
    ) -> tuple[bool, str]:
        """检查时间是否在当前时间 ±tolerance_seconds 范围内

        Args:
            actual_time: 实际时间（datetime 对象或 ISO 格式字符串）
            tolerance_seconds: 容差秒数，默认 60 秒（±1 分钟）

        Returns:
            (是否通过, 错误信息)
        """
        try:
            # 解析时间
            if isinstance(actual_time, str):
                # 尝试多种格式解析
                for fmt in ["%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d"]:
                    try:
                        actual = datetime.strptime(actual_time, fmt)
                        break
                    except ValueError:
                        continue
                else:
                    return False, f"无法解析时间格式: {actual_time}"
            else:
                actual = actual_time

            now = datetime.now()
            diff = abs((now - actual).total_seconds())

            if diff <= tolerance_seconds:
                return True, ""
            else:
                return False, f"时间差 {diff:.1f} 秒超出容差范围 ±{tolerance_seconds} 秒"

        except Exception as e:
            return False, f"时间断言错误: {str(e)}"

    def check_exact_match(
        self,
        actual: Any,
        expected: Any
    ) -> tuple[bool, str]:
        """精确匹配断言

        Args:
            actual: 实际值
            expected: 期望值

        Returns:
            (是否通过, 错误信息)
        """
        if actual == expected:
            return True, ""
        return False, f"期望 '{expected}'，实际 '{actual}'"

    def check_contains_match(
        self,
        actual: str,
        expected: str
    ) -> tuple[bool, str]:
        """包含匹配断言

        Args:
            actual: 实际字符串
            expected: 期望包含的字符串

        Returns:
            (是否通过, 错误信息)
        """
        if expected in str(actual):
            return True, ""
        return False, f"'{actual}' 不包含 '{expected}'"

    def check_decimal_approx(
        self,
        actual: float,
        expected: float,
        tolerance: float = 0.01
    ) -> tuple[bool, str]:
        """小数近似断言

        Args:
            actual: 实际值
            expected: 期望值
            tolerance: 容差，默认 0.01

        Returns:
            (是否通过, 错误信息)
        """
        diff = abs(actual - expected)
        if diff <= tolerance:
            return True, ""
        return False, f"差值 {diff} 超出容差 {tolerance}"

    # ... 更多方法见完整实现
```

### Pattern 2: 执行流程集成

**What:** 在 `run_agent_background` 中集成接口断言执行

**When to use:** UI 测试完成后、生成报告前

**Example:**
```python
# Source: backend/api/routes/runs.py 扩展

async def run_agent_background(
    run_id: str,
    task_id: str,
    task_name: str,
    task_description: str,
    max_steps: int,
    preconditions: list[str] | None = None,
    api_assertions: list[str] | None = None,  # 新增参数
):
    """后台执行 agent 任务"""

    # ... 现有代码 ...

    # === 前置条件执行 ===
    context: dict[str, Any] = {}
    if preconditions:
        # ... 现有前置条件执行代码 ...

    # === UI 测试执行 ===
    try:
        result = await agent_service.run_with_cleanup(...)
        # ... 现有 UI 断言评估代码 ...
    except Exception as e:
        # ... 错误处理 ...

    # === 接口断言执行（新增） ===
    if api_assertions:
        api_assertion_service = ApiAssertionService(external_module_path)
        api_assertion_service.context = context  # 复用前置条件上下文

        api_results = await api_assertion_service.execute_all(
            api_assertions,
            timeout_each=30.0
        )

        # 存储断言结果到数据库
        for api_result in api_results:
            if api_result.success:
                for field_result in api_result.field_results:
                    await assertion_result_repo.create(
                        run_id=run_id,
                        assertion_id=f"api_{api_result.index}",
                        status="pass" if field_result.passed else "fail",
                        message=field_result.message,
                        actual_value=str(field_result.actual),
                    )

        # 更新最终状态
        if any(not r.success for r in api_results):
            final_status = "failed"

    # === 生成报告 ===
    await report_service.generate_report(run_id)
```

### Pattern 3: 前端接口断言输入组件

**What:** 在 TaskForm 中添加接口断言输入区域

**When to use:** 任务创建/编辑页面

**Example:**
```tsx
// Source: frontend/src/components/TaskModal/TaskForm.tsx 扩展

interface FormData {
  // ... 现有字段 ...
  api_assertions: string[]  // 新增
}

// 在表单中添加接口断言输入区域
<div>
  <label className="block text-sm font-medium text-gray-700 mb-1">
    接口断言 <span className="text-gray-400 text-xs">(可选)</span>
  </label>
  <p className="text-xs text-gray-500 mb-2">
    输入 Python 代码进行 API 断言，支持时间断言、数据匹配等
  </p>
  <div className="space-y-2">
    {formData.api_assertions.map((assertion, index) => (
      <div key={index} className="flex gap-2">
        <textarea
          value={assertion}
          onChange={e => handleApiAssertionChange(index, e.target.value)}
          placeholder="例如：result = api.get_order({{order_id}}); assert result['status'] == 'success'"
          rows={4}
          className="flex-1 px-3 py-2 border border-gray-200 rounded-lg font-mono text-sm"
        />
        {formData.api_assertions.length > 1 && (
          <button onClick={() => handleRemoveApiAssertion(index)}>
            删除
          </button>
        )}
      </div>
    ))}
    <button onClick={handleAddApiAssertion}>
      + 添加接口断言
    </button>
  </div>
</div>
```

### Anti-Patterns to Avoid

- **在接口断言中执行 UI 操作** - 接口断言只用于 API 数据验证，不应启动浏览器
- **忽略前置条件上下文** - 必须传递 context 以支持变量引用
- **断言失败不记录详细信息** - 必须记录字段名、预期值、实际值以便调试
- **硬编码时间容差** - 使用常量定义，便于后续调整

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| 变量替换 | 自定义字符串解析 | Jinja2 (已有) | Phase 5 已集成，成熟稳定 |
| 代码执行 | 自定义解释器 | `exec()` + `asyncio.wait_for()` | Phase 5 已验证的模式 |
| 时间比较 | 手动计算秒数 | `datetime` + `timedelta` | Python 标准库，时区处理完善 |
| 异步执行 | 自定义线程池 | `loop.run_in_executor()` | Phase 5 已使用，可靠 |

**Key insight:** 本阶段核心是复用 Phase 5 的执行基础设施，新增断言判断逻辑，而非重新设计执行机制。

## Common Pitfalls

### Pitfall 1: 时间断言时区问题

**What goes wrong:** 服务器时间与 API 返回时间时区不一致，导致断言失败

**Why it happens:** API 返回的时间可能是 UTC，而 `datetime.now()` 是本地时间

**How to avoid:**
```python
# 使用 UTC 时间进行比较
from datetime import datetime, timezone

now = datetime.now(timezone.utc)
# 或者统一使用 naive datetime（假设都在同一时区）
now = datetime.now()
```

**Warning signs:** 时间断言频繁失败，但手动检查时间看起来正确

### Pitfall 2: 变量未定义错误

**What goes wrong:** 接口断言引用前置条件变量，但变量不存在

**Why it happens:** 前置条件执行失败或变量名拼写错误

**How to avoid:**
```python
# 使用 Jinja2 StrictUndefined 确保变量必须存在
from jinja2 import Environment, StrictUndefined

env = Environment(undefined=StrictUndefined)
# 变量不存在时会抛出 UndefinedError
```

**Warning signs:** 接口断言执行时报 `UndefinedError`

### Pitfall 3: 断言结果未持久化

**What goes wrong:** 断言执行成功但结果未保存到数据库

**Why it happens:** 忘记调用 `assertion_result_repo.create()`

**How to avoid:**
```python
# 每个断言结果都应保存
for field_result in api_result.field_results:
    await assertion_result_repo.create(
        run_id=run_id,
        assertion_id=f"api_{index}",
        status="pass" if field_result.passed else "fail",
        message=field_result.message,
        actual_value=str(field_result.actual),
    )
```

**Warning signs:** 报告中看不到接口断言结果

### Pitfall 4: exec() 安全风险

**What goes wrong:** 恶意代码通过接口断言执行

**Why it happens:** `exec()` 执行用户输入代码存在安全风险

**How to avoid:**
```python
# 限制执行环境（参考 Phase 5）
env = {
    '__builtins__': __builtins__,
    'context': self.context,
}
# 不要添加危险模块如 os, subprocess 等
```

**Warning signs:** 系统文件被修改、敏感信息泄露

## Code Examples

### 接口断言执行完整示例

```python
# Source: 参考 Phase 5 PreconditionService 设计
# backend/core/api_assertion_service.py

import asyncio
import logging
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

from jinja2 import Environment, StrictUndefined, UndefinedError

logger = logging.getLogger(__name__)


@dataclass
class FieldAssertionResult:
    """单个字段断言结果"""
    field_name: str
    expected: Any
    actual: Any
    passed: bool = False
    message: str = ""
    assertion_type: str = "exact"


@dataclass
class ApiAssertionResult:
    """接口断言执行结果"""
    index: int
    code: str
    success: bool = False
    error: str | None = None
    duration_ms: int = 0
    field_results: list[FieldAssertionResult] = field(default_factory=list)


class ApiAssertionService:
    """接口断言执行服务"""

    TIME_TOLERANCE_SECONDS = 60
    DECIMAL_TOLERANCE = 0.01

    def __init__(self, external_module_path: str | None = None):
        self.external_module_path = external_module_path
        self.context: dict[str, Any] = {}

    def _setup_execution_env(self) -> dict:
        """创建执行环境"""
        if self.external_module_path:
            path = Path(self.external_module_path)
            if path.exists() and str(path) not in sys.path:
                sys.path.insert(0, str(path))

        return {
            '__builtins__': __builtins__,
            'context': self.context,
            'assert_time': self._assert_time,
            'assert_exact': self._assert_exact,
            'assert_contains': self._assert_contains,
            'assert_decimal': self._assert_decimal,
        }

    def _assert_time(self, actual_time: Any) -> bool:
        """时间断言辅助函数"""
        passed, _ = self.check_time_within_range(actual_time)
        return passed

    def _assert_exact(self, actual: Any, expected: Any) -> bool:
        """精确匹配辅助函数"""
        passed, _ = self.check_exact_match(actual, expected)
        return passed

    def _assert_contains(self, actual: str, expected: str) -> bool:
        """包含匹配辅助函数"""
        passed, _ = self.check_contains_match(actual, expected)
        return passed

    def _assert_decimal(self, actual: float, expected: float, tolerance: float = 0.01) -> bool:
        """小数近似辅助函数"""
        passed, _ = self.check_decimal_approx(actual, expected, tolerance)
        return passed

    def check_time_within_range(
        self,
        actual_time: datetime | str,
        tolerance_seconds: int = 60
    ) -> tuple[bool, str]:
        """检查时间是否在范围内"""
        try:
            if isinstance(actual_time, str):
                for fmt in ["%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d"]:
                    try:
                        actual = datetime.strptime(actual_time, fmt)
                        break
                    except ValueError:
                        continue
                else:
                    return False, f"无法解析时间格式: {actual_time}"
            else:
                actual = actual_time

            now = datetime.now()
            diff = abs((now - actual).total_seconds())

            if diff <= tolerance_seconds:
                return True, ""
            return False, f"时间差 {diff:.1f} 秒超出容差 ±{tolerance_seconds} 秒"

        except Exception as e:
            return False, f"时间断言错误: {str(e)}"

    def check_exact_match(self, actual: Any, expected: Any) -> tuple[bool, str]:
        """精确匹配"""
        if actual == expected:
            return True, ""
        return False, f"期望 '{expected}'，实际 '{actual}'"

    def check_contains_match(self, actual: str, expected: str) -> tuple[bool, str]:
        """包含匹配"""
        if expected in str(actual):
            return True, ""
        return False, f"'{actual}' 不包含 '{expected}'"

    def check_decimal_approx(
        self,
        actual: float,
        expected: float,
        tolerance: float = 0.01
    ) -> tuple[bool, str]:
        """小数近似"""
        diff = abs(actual - expected)
        if diff <= tolerance:
            return True, ""
        return False, f"差值 {diff} 超出容差 {tolerance}"

    @staticmethod
    def substitute_variables(text: str, context: dict[str, Any]) -> str:
        """使用 Jinja2 进行变量替换"""
        if not text or '{{' not in text:
            return text

        env = Environment(
            variable_start_string='{{',
            variable_end_string='}}',
            undefined=StrictUndefined,
        )
        template = env.from_string(text)
        return template.render(**context)

    async def execute_single(
        self,
        code: str,
        index: int,
        timeout: float = 30.0
    ) -> ApiAssertionResult:
        """执行单个接口断言"""
        result = ApiAssertionResult(index=index, code=code)
        start_time = time.time()

        try:
            # 变量替换
            code = self.substitute_variables(code, self.context)
        except UndefinedError as e:
            result.error = f"变量未定义: {str(e)}"
            result.duration_ms = int((time.time() - start_time) * 1000)
            return result

        env = self._setup_execution_env()

        try:
            loop = asyncio.get_event_loop()
            await asyncio.wait_for(
                loop.run_in_executor(None, lambda: exec(code, env)),
                timeout=timeout
            )
            result.success = True
            logger.info(f"接口断言 {index} 执行成功")
        except asyncio.TimeoutError:
            result.error = f"执行超时（超过 {timeout} 秒）"
            logger.warning(f"接口断言 {index} 超时")
        except SyntaxError as e:
            result.error = f"语法错误: {e.msg} (行 {e.lineno})"
            logger.error(f"接口断言 {index} 语法错误: {e}")
        except AssertionError as e:
            result.error = f"断言失败: {str(e)}"
            logger.info(f"接口断言 {index} 断言失败: {e}")
        except Exception as e:
            result.error = f"执行错误: {str(e)}"
            logger.error(f"接口断言 {index} 执行错误: {e}", exc_info=True)

        result.duration_ms = int((time.time() - start_time) * 1000)
        return result

    async def execute_all(
        self,
        assertions: list[str],
        timeout_each: float = 30.0
    ) -> list[ApiAssertionResult]:
        """执行所有接口断言（不终止，收集所有结果）"""
        results = []

        for i, code in enumerate(assertions):
            if not code.strip():
                continue

            result = await self.execute_single(code, i, timeout_each)
            results.append(result)

        return results
```

### 数据库模型扩展

```python
# Source: backend/db/models.py 扩展

class Task(Base):
    """任务模型"""
    __tablename__ = "tasks"

    # ... 现有字段 ...

    # 接口断言（JSON 字符串数组）
    api_assertions: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
```

### 前端类型扩展

```typescript
// Source: frontend/src/types/index.ts 扩展

export interface Task {
  // ... 现有字段 ...
  api_assertions?: string[]
}

export interface CreateTaskDto {
  // ... 现有字段 ...
  api_assertions?: string[]
}
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| 硬编码断言 | Python 代码格式 | Phase 6 | 更灵活，支持复杂逻辑 |
| 无变量替换 | Jinja2 模板 | Phase 5 | 支持跨步骤数据传递 |
| 单一断言类型 | 多类型断言 | Phase 6 | 时间/精确/包含/小数 |

**Deprecated/outdated:**
- 简单的字符串匹配断言 → 替换为多类型断言系统
- 手动时间计算 → 替换为 `timedelta` 标准库

## Open Questions

1. **Monaco Editor 是否集成？**
   - What we know: CONTEXT.md 提到「Claude's Discretion」
   - What's unclear: 是否需要代码高亮功能
   - Recommendation: 初期使用简单 textarea，后续可升级为 Monaco Editor

2. **断言失败是否终止执行？**
   - What we know: 前置条件是 fail-fast，接口断言未明确
   - What's unclear: 接口断言失败后是否继续执行后续断言
   - Recommendation: 收集所有断言结果，不终止，便于用户看到完整问题列表

3. **小数近似默认容差？**
   - What we know: CONTEXT.md 提到 0.01 或 0.001
   - What's unclear: 最终选择哪个值
   - Recommendation: 使用 0.01（1% 误差），适用于金额等场景

## Validation Architecture

### Test Framework

| Property | Value |
|----------|-------|
| Framework | pytest 8.0.0 + pytest-asyncio 0.24.0 |
| Config file | pyproject.toml |
| Quick run command | `uv run pytest backend/tests/unit/test_api_assertion_service.py -v` |
| Full suite command | `uv run pytest backend/tests/ -v` |

### Phase Requirements → Test Map

| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| API-01 | API 调用断言执行 | unit | `uv run pytest backend/tests/unit/test_api_assertion_service.py::test_execute_single -x` | ❌ Wave 0 |
| API-01 | 外部模块加载 | unit | `uv run pytest backend/tests/unit/test_api_assertion_service.py::test_external_module -x` | ❌ Wave 0 |
| API-02 | 时间断言 ±1 分钟 | unit | `uv run pytest backend/tests/unit/test_api_assertion_service.py::test_time_assertion -x` | ❌ Wave 0 |
| API-03 | 精确匹配断言 | unit | `uv run pytest backend/tests/unit/test_api_assertion_service.py::test_exact_match -x` | ❌ Wave 0 |
| API-03 | 包含匹配断言 | unit | `uv run pytest backend/tests/unit/test_api_assertion_service.py::test_contains_match -x` | ❌ Wave 0 |
| API-03 | 小数近似断言 | unit | `uv run pytest backend/tests/unit/test_api_assertion_service.py::test_decimal_approx -x` | ❌ Wave 0 |
| API-04 | 断言结果存储 | unit | `uv run pytest backend/tests/unit/test_api_assertion_service.py::test_result_persistence -x` | ❌ Wave 0 |
| API-04 | 报告展示 | integration | `uv run pytest backend/tests/unit/test_report_service.py -x` | ✅ 已存在 |

### Sampling Rate

- **Per task commit:** `uv run pytest backend/tests/unit/test_api_assertion_service.py -v`
- **Per wave merge:** `uv run pytest backend/tests/ -v`
- **Phase gate:** Full suite green before `/gsd:verify-work`

### Wave 0 Gaps

- [ ] `backend/tests/unit/test_api_assertion_service.py` — covers API-01, API-02, API-03
- [ ] `backend/tests/unit/test_api_assertion_integration.py` — covers API-04 (报告集成)
- [ ] conftest.py fixtures for ApiAssertionService — shared test fixtures

*(Existing test infrastructure: `conftest.py` provides `db_session` fixture, `pytest.ini_options` configured)*

## Sources

### Primary (HIGH confidence)

- `.planning/phases/06-接口断言集成/06-CONTEXT.md` - 用户决策和约束
- `backend/core/precondition_service.py` - 执行模式参考
- `backend/core/assertion_service.py` - 现有断言服务架构
- `backend/api/routes/runs.py` - 执行流程集成点

### Secondary (MEDIUM confidence)

- [Python datetime comparison best practices](https://docs.python.org/3/library/datetime.html) - 官方文档
- [FastAPI async patterns](https://zhuanlan.zhihu.com/p/684096143) - FastAPI 全栈进阶
- [assertpy 断言库设计](https://blog.csdn.net/gitblog_00075/article/details/139109065) - Python 断言库参考

### Tertiary (LOW confidence)

- Web search for "BaseAssert 类 Python 断言库设计模式" - 需要结合现有项目验证

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - 复用 Phase 5 已验证的库和模式
- Architecture: HIGH - 基于 CONTEXT.md 明确决策
- Pitfalls: MEDIUM - 时间断言时区问题需要实际测试验证

**Research date:** 2026-03-16
**Valid until:** 30 days (stable architecture)
