# Phase 17: 后端数据获取桥接 - Research

**Researched:** 2026-03-18
**Domain:** Python introspection, FastAPI, external module bridging
**Confidence:** HIGH (based on existing Phase 14 patterns and comprehensive codebase analysis)

## Summary

Phase 17 扩展现有的 `external_precondition_bridge.py` 模块，添加对 `webseleniumerp/common/base_params.py` 中数据获取方法的支持。核心任务是扫描类中的公开方法，提取方法签名和参数信息，并通过新的 API 端点暴露方法列表和执行能力。

**Primary recommendation:** 复用 Phase 14 的桥接模块架构，使用 `inspect` 模块解析方法签名，扩展现有 API 路由模式创建 `/api/external-data-methods` 端点。

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions
- **解析方式**: 使用 `inspect.getsource` + 正则解析，复用 Phase 14 模式
- **扫描范围**: 扫描所有公开方法（不以 `_` 开头），不仅限于 `xxx_data()` 方法
- **参数类型**: 推断参数类型信息（从类型注解或默认值）
- **签名信息**: 包含参数名、类型、是否必需、默认值
- **分组方式**: 按类名分组（如 BaseParams, InventoryParams 等）
- **执行方式**: 在桥接模块中实现 `execute_data_method()`，直接调用 base_params.py 的方法
- **超时策略**: 30 秒超时（与 PreconditionService 一致）
- **错误处理**: 返回 HTTP 200 + 错误信息字段，便于前端展示和重试
- **缓存策略**: 方法签名启动时缓存，执行结果不缓存

### Claude's Discretion
- API 端点命名（`/external-data-methods` 或 `/data-methods`）
- 桥接模块的文件位置（复用 `external_precondition_bridge.py` 或新建文件）
- 参数类型推断的具体实现（优先使用类型注解，其次从默认值推断）
- 是否需要添加方法搜索/过滤功能

### Deferred Ideas (OUT OF SCOPE)
- 前端数据选择器组件 - Phase 18
- 字段提取路径配置 - Phase 18
- 前置条件代码生成 - Phase 19
- 数据缓存机制（避免重复查询）- v2 需求
- 方法搜索/过滤功能 - 可在 Phase 18 考虑

</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| DATA-01 | 扫描 base_params.py 获取所有 `xxx_data()` 方法的签名和参数信息 | 使用 `inspect.signature()` 提取方法签名，`inspect.getsource()` 解析方法源码获取描述 |
| DATA-02 | 提供数据获取方法列表 API（按模块分组，包含方法描述） | 复用 Phase 14 的 Pydantic response model 模式，按类名分组返回 |
| DATA-03 | 执行数据获取方法并返回 JSON 结果 | 扩展桥接模块添加 `execute_data_method()` 函数，复用 PreconditionService 的 30 秒超时模式 |

</phase_requirements>

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| FastAPI | 0.135.1+ | REST API framework | Existing backend framework |
| Pydantic | 2.4.0+ | Data validation/models | Existing validation layer |
| inspect | stdlib | Method introspection | Python built-in, reliable |
| asyncio | stdlib | Async execution | Existing async patterns |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| re | stdlib | Regex parsing | 复用 Phase 14 的源码解析模式 |
| typing | stdlib | Type hints | 参数类型推断 |
| logging | stdlib | Error tracking | 与现有模块一致 |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| inspect.signature | ast.parse | AST 更强大但复杂度高，signature 已足够 |
| 新建桥接文件 | 扩展现有文件 | 新文件隔离更好，但现有文件扩展更简单（已选定扩展） |

**Installation:** 无需新依赖，全部使用 Python 标准库

## Architecture Patterns

### Recommended Project Structure
```
backend/
├── core/
│   └── external_precondition_bridge.py  # 扩展此文件，添加数据方法支持
├── api/
│   └── routes/
│       └── external_data_methods.py     # 新建：数据方法 API 路由
└── tests/
    ├── unit/
    │   └── test_external_bridge.py      # 扩展：添加数据方法测试
    └── api/
        └── test_external_data_methods.py # 新建：API 集成测试
```

### Pattern 1: Method Introspection Pattern
**What:** 使用 `inspect.signature()` 提取方法参数信息
**When to use:** 扫描 base_params.py 类方法时
**Example:**
```python
import inspect
from typing import get_type_hints

def parse_method_signature(method: callable) -> dict:
    """Extract method signature information."""
    sig = inspect.signature(method)
    type_hints = get_type_hints(method)

    parameters = []
    for name, param in sig.parameters.items():
        if name == 'self':
            continue

        param_info = {
            "name": name,
            "type": type_hints.get(name, type(param.default)).__name__ if param.default != inspect.Parameter.empty else "Any",
            "required": param.default == inspect.Parameter.empty,
            "default": param.default if param.default != inspect.Parameter.empty else None
        }
        parameters.append(param_info)

    return {"parameters": parameters}

# Source: Python stdlib inspect module documentation
# https://docs.python.org/3/library/inspect.html
```

### Pattern 2: Class Method Discovery Pattern
**What:** 扫描模块中的所有类，提取公开方法
**When to use:** 初始化时缓存方法列表
**Example:**
```python
import inspect
from common.base_params import BaseParams  # Target module

def discover_class_methods(cls: type) -> list[dict]:
    """Discover all public methods in a class."""
    methods = []
    for name, method in inspect.getmembers(cls, predicate=inspect.isfunction):
        if not name.startswith('_'):
            methods.append({
                "name": name,
                "description": extract_description_from_docstring(method),
                "parameters": parse_method_signature(method)["parameters"]
            })
    return methods

# Source: Adapted from Phase 14 external_precondition_bridge.py pattern
```

### Pattern 3: API Response Model (from Phase 14)
**What:** 使用 Pydantic 定义响应结构
**When to use:** 所有 API 端点
**Example:**
```python
from pydantic import BaseModel
from typing import Optional

class ParameterInfo(BaseModel):
    """Single method parameter info."""
    name: str
    type: str
    required: bool
    default: Optional[str] = None

class MethodInfo(BaseModel):
    """Single data method info."""
    name: str
    description: str
    parameters: list[ParameterInfo]

class ClassGroup(BaseModel):
    """Group of methods under a class name."""
    name: str
    methods: list[MethodInfo]

class DataMethodsResponse(BaseModel):
    """Response model for listing data methods."""
    available: bool
    classes: list[ClassGroup] = []
    total: int = 0
    error: Optional[str] = None

# Source: backend/api/routes/external_operations.py (Phase 14)
```

### Pattern 4: Error Response Pattern (from CONTEXT.md)
**What:** 执行失败时返回 HTTP 200 + error 字段
**When to use:** 数据方法执行失败时
**Example:**
```python
class ExecuteResponse(BaseModel):
    """Response model for method execution."""
    success: bool
    data: Optional[list[dict]] = None
    error: Optional[str] = None
    error_type: Optional[str] = None  # ParameterError, SystemError, etc.

# Usage:
if parameter_error:
    return ExecuteResponse(success=False, error="参数 i 必须为整数", error_type="ParameterError")
```

### Anti-Patterns to Avoid
- **直接导入 base_params.py 而不隔离:** 会造成强耦合，应通过桥接模块
- **同步阻塞调用:** 必须使用 `asyncio.wait_for` 包装同步调用
- **缓存执行结果:** 数据可能变化，每次都应重新执行

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| 方法签名解析 | 手写正则解析参数 | `inspect.signature()` | 边界情况多，stdlib 已处理 |
| 类型推断 | 手动解析类型字符串 | `typing.get_type_hints()` | 处理泛型、Optional 等复杂类型 |
| 超时控制 | 手写超时逻辑 | `asyncio.wait_for()` | 可靠、可测试 |

**Key insight:** Python stdlib 的 `inspect` 模块已提供完整的方法内省能力，无需自行解析源码获取参数信息（除非需要提取 docstring 描述）

## Common Pitfalls

### Pitfall 1: 类实例化依赖外部配置
**What goes wrong:** `base_params.py` 中的类可能依赖 `config/settings.py` 中的 ERP 配置才能实例化
**Why it happens:** 类的 `__init__` 可能读取全局配置
**How to avoid:** 使用 try-except 包装实例化，返回明确的错误信息
**Warning signs:** `ImportError`, `ConfigError`, `KeyError` during instantiation

### Pitfall 2: 方法执行修改系统状态
**What goes wrong:** 调用数据方法可能意外修改 ERP 数据
**Why it happens:** 方法名可能误导（如 `xxx_data()` 不一定只读）
**How to avoid:** 在文档中明确警告，或只允许调用明确标记为查询的方法
**Warning signs:** 方法名包含 `create`, `update`, `delete` 等动词

### Pitfall 3: 参数类型转换失败
**What goes wrong:** 前端传字符串 "10"，方法期望整数 10
**Why it happens:** JSON 传输不保留类型信息
**How to avoid:** 根据参数签名自动转换类型，失败时返回 ParameterError
**Warning signs:** `TypeError`, `ValueError` during execution

### Pitfall 4: 大数据集响应超时
**What goes wrong:** 某些查询方法返回大量数据，超过 30 秒超时
**Why it happens:** 查询未分页或数据量大
**How to avoid:** 在 API 文档中建议用户使用分页参数（i, j）
**Warning signs:** 超时错误，前端显示不完整

## Code Examples

### Method Signature Extraction
```python
# Source: Python stdlib + project pattern
import inspect
from typing import get_type_hints, Any

def extract_method_info(cls: type, method_name: str) -> dict | None:
    """Extract method info including parameters with types."""
    method = getattr(cls, method_name, None)
    if not method or method_name.startswith('_'):
        return None

    try:
        sig = inspect.signature(method)
        type_hints = get_type_hints(method)
    except (ValueError, TypeError) as e:
        logger.warning(f"Cannot get signature for {method_name}: {e}")
        return None

    parameters = []
    for param_name, param in sig.parameters.items():
        if param_name == 'self':
            continue

        # Determine type
        param_type = type_hints.get(param_name, Any)
        type_str = getattr(param_type, '__name__', str(param_type))
        if type_str.startswith('typing.'):
            type_str = str(param_type).replace('typing.', '')

        # Determine if required and default value
        has_default = param.default != inspect.Parameter.empty
        parameters.append({
            "name": param_name,
            "type": type_str,
            "required": not has_default,
            "default": repr(param.default) if has_default else None
        })

    # Extract description from docstring
    docstring = method.__doc__ or ""
    description = docstring.strip().split('\n')[0] if docstring else method_name

    return {
        "name": method_name,
        "description": description,
        "parameters": parameters
    }
```

### Execute Method with Timeout
```python
# Source: backend/core/precondition_service.py pattern
import asyncio

async def execute_data_method(
    class_name: str,
    method_name: str,
    params: dict,
    timeout: float = 30.0
) -> dict:
    """Execute a data method with timeout protection."""
    cls = load_class(class_name)
    if cls is None:
        return {"success": False, "error": f"Class {class_name} not found", "error_type": "ImportError"}

    try:
        instance = cls()
        method = getattr(instance, method_name)

        # Wrap sync call in executor with timeout
        loop = asyncio.get_event_loop()
        result = await asyncio.wait_for(
            loop.run_in_executor(None, lambda: method(**params)),
            timeout=timeout
        )

        return {"success": True, "data": result}
    except asyncio.TimeoutError:
        return {"success": False, "error": f"Execution timeout ({timeout}s)", "error_type": "TimeoutError"}
    except TypeError as e:
        return {"success": False, "error": f"Parameter error: {e}", "error_type": "ParameterError"}
    except Exception as e:
        return {"success": False, "error": str(e), "error_type": "ExecutionError"}
```

### API Route Handler
```python
# Source: backend/api/routes/external_operations.py pattern
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/external-data-methods", tags=["external-data-methods"])

class ExecuteRequest(BaseModel):
    class_name: str
    method_name: str
    params: dict = {}

@router.post("/execute", response_model=ExecuteResponse)
async def execute_method(request: ExecuteRequest):
    """Execute a data method and return results."""
    if not is_available():
        raise HTTPException(
            status_code=503,
            detail={"message": "External module not available", "reason": get_unavailable_reason()}
        )

    result = await execute_data_method(
        request.class_name,
        request.method_name,
        request.params
    )
    return ExecuteResponse(**result)
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| 手动维护方法列表 | 自动扫描方法签名 | Phase 17 | 减少维护成本，自动同步 |
| 无参数类型信息 | 完整参数签名 | Phase 17 | 前端可动态生成表单 |

**Deprecated/outdated:**
- 无（此阶段为新增功能）

## Open Questions

1. **base_params.py 的类加载路径**
   - What we know: 类在 `common.base_params` 模块中
   - What's unclear: 具体有哪些类，类名是什么
   - Recommendation: 实现时先扫描模块获取所有类，支持动态发现

2. **方法描述提取**
   - What we know: 可从 docstring 提取
   - What's unclear: docstring 格式是否规范
   - Recommendation: 优先使用 docstring 第一行，回退到方法名

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | pytest 8.0.0+ |
| Config file | pyproject.toml `[tool.pytest.ini_options]` |
| Quick run command | `uv run pytest backend/tests/unit/test_external_bridge.py -x -v` |
| Full suite command | `uv run pytest backend/tests/ -v` |

### Phase Requirements -> Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| DATA-01 | 扫描方法获取签名 | unit | `uv run pytest backend/tests/unit/test_external_bridge.py::TestDataMethodsDiscovery -x` | No - Wave 0 |
| DATA-02 | 返回分组方法列表 | api | `uv run pytest backend/tests/api/test_external_data_methods.py::TestListDataMethods -x` | No - Wave 0 |
| DATA-03 | 执行方法返回结果 | api | `uv run pytest backend/tests/api/test_external_data_methods.py::TestExecuteDataMethod -x` | No - Wave 0 |

### Sampling Rate
- **Per task commit:** `uv run pytest backend/tests/unit/test_external_bridge.py -x`
- **Per wave merge:** `uv run pytest backend/tests/ -v`
- **Phase gate:** Full suite green before `/gsd:verify-work`

### Wave 0 Gaps
- [ ] `backend/tests/unit/test_external_bridge.py` - 添加 TestDataMethodsDiscovery 测试类
- [ ] `backend/tests/api/test_external_data_methods.py` - 新建文件，测试 API 端点
- [ ] conftest.py - 添加 `reset_data_methods_cache` fixture（如果需要）
- [ ] Mock base_params.py 类 - 测试需要模拟外部模块

## Sources

### Primary (HIGH confidence)
- `backend/core/external_precondition_bridge.py` - Phase 14 实现模式
- `backend/api/routes/external_operations.py` - API 路由模式
- `backend/core/precondition_service.py` - 超时和执行模式
- Python stdlib `inspect` module documentation - https://docs.python.org/3/library/inspect.html

### Secondary (MEDIUM confidence)
- `.planning/research/ARCHITECTURE.md` - ExternalPreconditionBridge 架构设计
- `.planning/phases/14-后端桥接模块/14-CONTEXT.md` - Phase 14 决策参考

### Tertiary (LOW confidence)
- 无

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - 复用现有技术栈，无新依赖
- Architecture: HIGH - 基于 Phase 14 已验证的模式
- Pitfalls: MEDIUM - 依赖对 base_params.py 的假设，实际实现时可能发现新问题

**Research date:** 2026-03-18
**Valid until:** 30 days (stable patterns, no external dependency changes expected)
