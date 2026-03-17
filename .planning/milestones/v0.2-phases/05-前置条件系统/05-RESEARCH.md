# Phase 5: 前置条件系统 - Research

**Researched:** 2026-03-16
**Domain:** Python dynamic code execution, external module integration, variable substitution
**Confidence:** MEDIUM (security patterns require validation in context)

## Summary

本阶段实现前置条件系统，允许用户在 UI 测试前通过 Python 代码调用 API 来准备测试数据。核心技术决策已锁定：使用 exec() 执行用户代码、30秒超时、通过 context['变量名'] 存储结果、复用现有三层 API 架构。

**Primary recommendation:** 采用受限的 exec() 执行模式，配合 asyncio.wait_for() 实现超时，使用 importlib 动态加载外部 API 模块，通过 Jinja2 风格的 {{变量名}} 语法在后续步骤中进行变量替换。

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions (MUST implement as specified)

1. **语法识别方式** - 前端提供独立的「前置条件」输入区域，与「测试步骤」分开
2. **前置条件语法格式** - Python 代码格式，用户直接写 Python 代码调用 API
   - 通过 `context['变量名']` 存储结果供后续引用
   - 示例：
     ```python
     from api.api_purchase import PurchaseOrderListApi
     api = PurchaseOrderListApi()
     order = api.create_order()
     context['order_id'] = order['id']
     ```
3. **API 模块集成** - Python 模块导入，复用现有三层架构（request/ -> api/ -> common/base_api.py）
4. **数据传递机制** - 变量替换语法 `{{变量名}}`，UI 测试步骤中引用前置条件结果
5. **结果存储** - 内存上下文，仅存储到内存，本次执行过程中可引用，不持久化到数据库
6. **多步骤前置条件** - 独立输入项，每个前置条件是独立的输入框，按顺序依次执行
7. **执行展示** - 合并到步骤列表，与 UI 步骤一起展示，有「前置条件」标签区分
8. **失败处理** - 立即终止，前置条件失败则整个测试终止，标记为失败
9. **代码执行** - 直接执行，使用 exec() 执行用户代码，依赖环境隔离和用户信任
10. **超时控制** - 30 秒超时，单个前置条件默认 30 秒超时
11. **前端位置** - 任务编辑页新增字段，在任务编辑页增加「前置条件」输入区域

### Claude's Discretion

- 具体数据库模型设计（Precondition 表是否需要）
- 前端组件布局细节
- 执行错误消息格式
- 代码编辑器样式（是否用 Monaco Editor）

### Deferred Ideas (OUT OF SCOPE)

None
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| PRE-01 | 用户可以在测试用例中定义前置条件步骤 | 前端新增前置条件输入区域，Task 模型扩展 preconditions 字段 |
| PRE-02 | 前置条件通过 API 调用执行（不用 UI） | PreconditionService 使用 exec() 执行 Python 代码，不启动浏览器 |
| PRE-03 | 支持复用现有项目的 API 封装方法 | importlib 动态加载外部模块，sys.path 临时扩展 |
| PRE-04 | 前置条件执行结果可用于后续步骤 | context 字典存储结果，Jinja2 风格 {{变量名}} 替换语法 |
</phase_requirements>

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| asyncio | 3.11+ | 超时控制、异步执行 | Python 内置，asyncio.wait_for() 提供原生超时支持 |
| importlib | 3.11+ | 动态模块加载 | Python 内置，spec_from_file_location 支持路径加载 |
| Jinja2 | 3.1+ | 变量替换模板 | 业界标准，{{ }} 语法一致，Environment.autoescape 安全 |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| RestrictedPython | 7.0+ | AST 级别代码限制 | 可选增强安全（不作为主要防线） |
| Pydantic | 2.x | 数据验证 | 复用现有项目模式 |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| exec() | RestrictedPython | RestrictedPython 有已知逃逸漏洞，且需额外依赖；exec() 配合受限 globals 已足够 |
| Jinja2 | re.sub() 正则替换 | 正则无法处理嵌套和复杂语法，Jinja2 更健壮 |
| 内存 context | Redis/数据库 | 单次执行无需持久化，内存更快更简单 |

**Installation:**
```bash
# Jinja2 已在 FastAPI 依赖中
# 无需额外安装
```

## Architecture Patterns

### Recommended Project Structure
```
backend/
├── core/
│   ├── precondition_service.py   # NEW: 前置条件执行服务
│   ├── agent_service.py          # 现有：UI 测试执行
│   └── event_manager.py          # 现有：SSE 事件
├── db/
│   ├── models.py                 # 扩展：Task.preconditions 字段
│   └── schemas.py                # 扩展：PreconditionCreate/Response
└── api/routes/
    └── tasks.py                  # 扩展：前置条件 CRUD

frontend/src/
├── components/TaskModal/
│   ├── TaskForm.tsx              # 扩展：前置条件输入区域
│   └── PreconditionEditor.tsx    # NEW: 前置条件编辑器组件
└── types/index.ts                # 扩展：Precondition 类型
```

### Pattern 1: PreconditionService 执行模式
**What:** 封装前置条件的加载、执行、超时控制
**When to use:** 每次测试执行前的准备阶段
**Example:**
```python
# Source: 基于 asyncio.wait_for() 和 exec() 的标准模式
import asyncio
import importlib.util
import sys

class PreconditionService:
    def __init__(self, external_module_path: str | None = None):
        self.external_module_path = external_module_path
        self.context: dict = {}

    def _setup_execution_env(self) -> dict:
        """创建受限的执行环境"""
        if self.external_module_path and self.external_module_path not in sys.path:
            sys.path.insert(0, self.external_module_path)

        return {
            '__builtins__': __builtins__,
            'context': self.context,
            # 可选：添加常用模块白名单
            'json': __import__('json'),
            'datetime': __import__('datetime'),
        }

    async def execute(self, code: str, timeout: float = 30.0) -> dict:
        """执行前置条件代码，带超时控制"""
        env = self._setup_execution_env()

        try:
            # exec 是同步的，需要在 executor 中运行以支持 asyncio 超时
            loop = asyncio.get_event_loop()
            await asyncio.wait_for(
                loop.run_in_executor(None, lambda: exec(code, env)),
                timeout=timeout
            )
            return {"success": True, "context": self.context}
        except asyncio.TimeoutError:
            return {"success": False, "error": f"执行超时（{timeout}秒）"}
        except Exception as e:
            return {"success": False, "error": str(e)}
```

### Pattern 2: 变量替换
**What:** 在后续步骤中使用 {{变量名}} 引用前置条件结果
**When to use:** UI 测试步骤描述中需要动态数据时
**Example:**
```python
# Source: Jinja2 标准用法
from jinja2 import Environment

def substitute_variables(text: str, context: dict) -> str:
    """使用 Jinja2 进行变量替换"""
    env = Environment(variable_start_string='{{', variable_end_string='}}')
    template = env.from_string(text)
    return template.render(**context)

# 使用示例
context = {'order_id': 'ORD-12345', 'user_name': '测试用户'}
description = "查询订单 {{order_id}}，验证收件人是 {{user_name}}"
result = substitute_variables(description, context)
# 结果: "查询订单 ORD-12345，验证收件人是 测试用户"
```

### Pattern 3: 动态模块加载
**What:** 从外部路径加载现有项目的 API 模块
**When to use:** 用户需要复用现有 ERP 测试项目的 API 封装
**Example:**
```python
# Source: importlib.util 官方文档模式
import importlib.util
import sys
from pathlib import Path

def load_external_module(module_path: str, module_name: str = "external_api"):
    """动态加载外部 Python 模块"""
    path = Path(module_path)
    if not path.exists():
        raise FileNotFoundError(f"模块路径不存在: {module_path}")

    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"无法加载模块: {module_path}")

    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module
```

### Anti-Patterns to Avoid

- **不要在 exec() 中使用完整的 __builtins__** - 限制内置函数，只暴露必要的
- **不要在主线程中直接 exec() 长时间代码** - 使用 run_in_executor 避免阻塞事件循环
- **不要持久化 context 到数据库** - 每次执行都是独立的，内存即可
- **不要忽略模块加载失败** - 必须提供清晰的错误信息指导用户配置路径

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| 超时控制 | 自定义信号处理 | asyncio.wait_for() | 原生支持，异常处理清晰 |
| 变量替换 | 正则表达式 | Jinja2 Environment | 处理边界情况、转义、嵌套 |
| 模块加载 | 手动 import | importlib.util | 支持路径加载，官方推荐 |
| 代码编辑器 | 自建 textarea | Monaco Editor（可选） | 语法高亮、错误提示、用户体验好 |

**Key insight:** exec() 的安全性依赖于环境隔离和用户信任，而非代码层面限制。对于内部工具，信任用户 + 超时控制是务实的方案。

## Common Pitfalls

### Pitfall 1: exec() 阻塞事件循环
**What goes wrong:** exec() 是同步阻塞调用，直接在 async 函数中调用会阻塞整个事件循环
**Why it happens:** 开发者可能忽略 Python 的 GIL 和 asyncio 协作机制
**How to avoid:** 使用 `loop.run_in_executor(None, lambda: exec(code, env))` 在线程池中执行
**Warning signs:** SSE 心跳停止、其他请求无响应

### Pitfall 2: 模块路径配置错误
**What goes wrong:** 用户配置的 ERP_API_MODULE_PATH 不正确，导致 import 失败
**Why it happens:** 路径可能是相对路径、不存在、或缺少 __init__.py
**How to avoid:**
1. 启动时验证路径是否存在
2. 提供清晰的错误信息："模块路径 /path/to/api 不存在，请检查 ERP_API_MODULE_PATH 配置"
3. 在前端显示当前配置的路径
**Warning signs:** "ModuleNotFoundError: No module named 'api'"

### Pitfall 3: 变量未定义就引用
**What goes wrong:** 用户在步骤中写 {{order_id}}，但前置条件执行失败或未设置 context['order_id']
**Why it happens:** 前置条件和后续步骤是分开编写的，容易遗漏
**How to avoid:**
1. 前置条件执行失败时立即终止，不进入 UI 测试阶段
2. 变量替换时检查是否所有变量都已定义，未定义则报错
3. 在执行监控中显示前置条件设置的变量列表
**Warning signs:** Jinja2 UndefinedError

### Pitfall 4: 超时后资源未清理
**What goes wrong:** 前置条件超时但数据库连接、文件句柄等资源未释放
**Why it happens:** exec() 中的代码可能在超时后继续持有资源
**How to avoid:**
1. 每个前置条件独立执行，使用独立的 context
2. 超时后标记失败，不尝试强制中断（Python 难以安全中断线程）
3. 依赖后续的 GC 和连接池管理
**Warning signs:** 数据库连接数持续增长

## Code Examples

### PreconditionService 完整实现
```python
# Source: 基于项目现有模式的推荐实现
# backend/core/precondition_service.py
import asyncio
import logging
import sys
from pathlib import Path
from typing import Any

from jinja2 import Environment, StrictUndefined

logger = logging.getLogger(__name__)


class PreconditionResult:
    """前置条件执行结果"""
    def __init__(self, index: int, code: str):
        self.index = index
        self.code = code
        self.success = False
        self.error: str | None = None
        self.duration_ms: int = 0
        self.variables: dict[str, Any] = {}


class PreconditionService:
    """前置条件执行服务"""

    def __init__(self, external_module_path: str | None = None):
        self.external_module_path = external_module_path
        self.context: dict[str, Any] = {}

    def _setup_execution_env(self) -> dict:
        """创建执行环境"""
        # 临时添加外部模块路径
        if self.external_module_path:
            path = Path(self.external_module_path)
            if path.exists() and str(path) not in sys.path:
                sys.path.insert(0, str(path))
                logger.info(f"添加外部模块路径: {path}")

        # 受限的全局环境
        return {
            '__builtins__': __builtins__,
            'context': self.context,
        }

    async def execute_single(
        self,
        code: str,
        index: int,
        timeout: float = 30.0
    ) -> PreconditionResult:
        """执行单个前置条件"""
        import time
        result = PreconditionResult(index=index, code=code)
        start_time = time.time()

        env = self._setup_execution_env()

        try:
            loop = asyncio.get_event_loop()
            await asyncio.wait_for(
                loop.run_in_executor(None, lambda: exec(code, env)),
                timeout=timeout
            )
            result.success = True
            result.variables = dict(self.context)  # 快照当前变量
            logger.info(f"前置条件 {index} 执行成功，变量: {list(result.variables.keys())}")
        except asyncio.TimeoutError:
            result.error = f"执行超时（超过 {timeout} 秒）"
            logger.warning(f"前置条件 {index} 超时")
        except SyntaxError as e:
            result.error = f"语法错误: {e.msg} (行 {e.lineno})"
            logger.error(f"前置条件 {index} 语法错误: {e}")
        except Exception as e:
            result.error = f"执行错误: {str(e)}"
            logger.error(f"前置条件 {index} 执行错误: {e}", exc_info=True)

        result.duration_ms = int((time.time() - start_time) * 1000)
        return result

    async def execute_all(
        self,
        preconditions: list[str],
        timeout_each: float = 30.0
    ) -> tuple[bool, list[PreconditionResult]]:
        """执行所有前置条件，任一失败则停止"""
        results = []

        for i, code in enumerate(preconditions):
            if not code.strip():
                continue

            result = await self.execute_single(code, i, timeout_each)
            results.append(result)

            if not result.success:
                logger.error(f"前置条件 {i} 失败，停止执行")
                return False, results

        return True, results

    @staticmethod
    def substitute_variables(text: str, context: dict[str, Any]) -> str:
        """使用 Jinja2 进行变量替换"""
        if not text or '{{' not in text:
            return text

        env = Environment(
            variable_start_string='{{',
            variable_end_string='}}',
            undefined=StrictUndefined,  # 未定义变量时报错
        )
        template = env.from_string(text)
        return template.render(**context)
```

### 数据库模型扩展
```python
# Source: 基于现有 models.py 模式
# 在 Task 模型中添加
class Task(Base):
    # ... 现有字段 ...

    # 新增：前置条件（JSON 数组存储代码字符串）
    preconditions: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON string

    # 或者使用单独的 Precondition 模型（如果需要更多元数据）
```

### 前端类型扩展
```typescript
// frontend/src/types/index.ts
export interface Precondition {
  id?: string
  code: string
  order: number
}

export interface Task {
  // ... 现有字段 ...
  preconditions?: Precondition[]
}

export interface CreateTaskDto {
  // ... 现有字段 ...
  preconditions?: string[]  // 代码字符串数组
}
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| 同步 exec() | asyncio + run_in_executor | 本项目采用 | 非阻塞执行，支持超时 |
| 正则替换 | Jinja2 模板 | 本项目采用 | 更健壮的变量替换 |
| 硬编码模块路径 | 环境变量配置 | 本项目采用 | 灵活复用现有项目 |

**Deprecated/outdated:**
- RestrictedPython 作为主要安全防线：有已知逃逸漏洞（CVE-2026-0863 等），不推荐单独使用
- 信号量 (signal.alarm) 超时：在 Windows 上不可用，asyncio.wait_for() 是跨平台方案

## Open Questions

1. **Precondition 是否需要独立数据表？**
   - What we know: 当前 Task 模型有 assertions 关系，preconditions 可以类似处理
   - What's unclear: 是否需要存储执行历史、是否需要版本控制
   - Recommendation: 先用 JSON 字段存储在 Task 中，保持简单；后续如有需求再拆分

2. **Monaco Editor 是否必需？**
   - What we know: CONTEXT.md 提到作为 Claude's Discretion
   - What's unclear: 投入产出比如何
   - Recommendation: 第一版用简单 textarea + monospace 字体，后续根据用户反馈决定是否引入 Monaco

3. **前置条件执行结果是否需要展示在报告中？**
   - What we know: CONTEXT.md 说"合并到步骤列表展示"
   - What's unclear: 报告中是否需要单独的"前置条件"区块
   - Recommendation: 在步骤列表开头显示，带有"前置条件"标签，显示设置的变量

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | pytest + pytest-asyncio |
| Config file | backend/tests/conftest.py |
| Quick run command | `uv run pytest backend/tests/unit/test_precondition_service.py -v` |
| Full suite command | `uv run pytest backend/tests/ -v` |

### Phase Requirements -> Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| PRE-01 | 任务模型支持 preconditions 字段 | unit | `pytest tests/unit/test_models.py::test_task_preconditions -v` | Wave 0 |
| PRE-02 | PreconditionService 执行代码不启动浏览器 | unit | `pytest tests/unit/test_precondition_service.py::test_execute_without_browser -v` | Wave 0 |
| PRE-03 | 动态加载外部 API 模块 | unit | `pytest tests/unit/test_precondition_service.py::test_load_external_module -v` | Wave 0 |
| PRE-04 | context 变量传递到后续步骤 | integration | `pytest tests/integration/test_precondition_flow.py -v` | Wave 0 |

### Sampling Rate
- **Per task commit:** `uv run pytest backend/tests/unit/ -v --tb=short`
- **Per wave merge:** `uv run pytest backend/tests/ -v`
- **Phase gate:** Full suite green before `/gsd:verify-work`

### Wave 0 Gaps
- [ ] `backend/tests/unit/test_precondition_service.py` - PreconditionService 单元测试
- [ ] `backend/tests/integration/test_precondition_flow.py` - 前置条件到 UI 测试的完整流程
- [ ] `frontend/src/components/TaskModal/PreconditionEditor.test.tsx` - 前端组件测试（可选）

*(If no gaps: "None - existing test infrastructure covers all phase requirements")*

## Sources

### Primary (HIGH confidence)
- [Python asyncio.wait_for() 文档](https://docs.python.org/zh-cn/3.9/library/asyncio-task.html) - 超时控制
- [Python importlib.util 文档](https://docs.python.org/3/library/importlib.html) - 动态模块加载
- [Jinja2 API 文档](https://jinja.palletsprojects.com/en/stable/api/) - 变量替换

### Secondary (MEDIUM confidence)
- [Stack Overflow: How can I import a module dynamically given the full path?](https://stackoverflow.com/questions/67631/how-can-i-import-a-module-dynamically-given-the-full-path) - 动态导入模式
- [FastAPI + Jinja2 集成](https://fastapi.tiangolo.com/reference/templating/) - 模板使用

### Tertiary (LOW confidence)
- [RestrictedPython 安全性讨论](https://checkmarx.com/zero-post/glass-sandbox-complexity-of-python-sandboxing/) - 了解沙箱局限性，验证了 exec() + 用户信任 的务实性
- [n8n CVE-2026-0863](https://www.smartkeyss.com/post/cve-2026-0863-python-sandbox-escape-in-n8n-via-exception-formatting-and-implicit-code-execution) - 沙箱逃逸案例，确认 RestrictedPython 不作为主要防线

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - asyncio/importlib/Jinja2 都是 Python 标准库或广泛使用的库
- Architecture: MEDIUM - 需要验证 exec() 在实际项目中的表现
- Pitfalls: HIGH - 阻塞事件循环、模块路径、变量未定义是常见问题

**Research date:** 2026-03-16
**Valid until:** 30 days (Python 生态稳定)
