# Phase 27: Unit Test Coverage - Context

**Gathered:** 2026-03-21
**Status:** Ready for planning

<domain>
## Phase Boundary

为 Phase 23-25 引入的断言组件添加单元测试覆盖，确保核心逻辑有 80%+ 测试保护。

**Scope:**
- `resolve_headers()` 单元测试（正常/异常路径）
- `_parse_assertion_error()` 单元测试（各种消息格式）
- `execute_assertion_method()` 单元测试（超时、错误分类、AssertionError 捕获）
- 新增代码覆盖率达到 80%+
- 测试添加到现有 `test_external_assertion_bridge.py`

**Out of Scope:**
- E2E 测试（Phase 26）
- 新功能开发
- 性能测试
- 前端测试

</domain>

<decisions>
## Implementation Decisions

### Mock 策略
- **完全 Mock 外部依赖** — 复用 Phase 21 模式，使用 monkeypatch/patch.object
- **不依赖真实 webseleniumerp 项目** — 测试隔离、执行快速
- **Mock LoginApi** — 使用 MagicMock 模拟 `login_api.headers.get()` 返回值
- **Mock 断言类实例** — 使用 MagicMock 模拟断言类实例和方法，控制返回值和异常
- **Mock 位置** — 使用 `patch.object` 或 monkeypatch 装饰器

### 边界场景覆盖

**resolve_headers() 测试用例:**
1. 成功路径 — 有效标识符返回对应 headers dict
2. None 参数 — 默认返回 'main' headers
3. 无效标识符 — 抛出 ValueError，包含有效标识符列表
4. LoginApi 不可用 — 抛出 RuntimeError

**_parse_assertion_error() 测试用例:**
1. 预期值格式 — `字段 'xxx' 预期值: 'expected', 实际值: 'actual'`
2. 预期包含格式 — `字段 'xxx' 预期包含: 'expected', 实际值: 'actual'`
3. 多字段消息 — 解析多个字段结果
4. 无法解析的消息 — 返回 `{'field': 'unknown', 'description': full_message}`
5. 中英文符号 — 支持中文冒号 `：` 和英文冒号 `:`

**execute_assertion_method() 测试用例:**
1. 成功路径 — 断言通过，返回 `passed: True`
2. AssertionError 捕获 — 断言失败，返回 `passed: False` + `field_results`
3. 超时 — 30 秒超时保护，返回 `error_type: TimeoutError`
4. 类不存在 — 返回 `error_type: NotFoundError`
5. 方法不存在 — 返回 `error_type: NotFoundError`
6. Headers 解析失败 — 返回 `error_type: HeaderResolutionError`
7. 外部模块不可用 — 返回 `error_type: ImportError`

### 覆盖率验证
- **工具**: pytest-cov（复用 Phase 21 模式）
- **命令**: `pytest --cov=backend.core.external_precondition_bridge --cov-report=term-missing backend/tests/unit/test_external_assertion_bridge.py`
- **目标**: 新增代码 80%+ 覆盖率
- **报告**: 生成 term-missing 报告查看未覆盖行

### 测试组织策略
- **文件位置**: 添加到现有 `backend/tests/unit/test_external_assertion_bridge.py`
- **命名规范**: 新增 `TestResolveHeaders`、`TestParseAssertionError`、`TestExecuteAssertionMethod` 测试类
- **理由**: 保持测试与代码位置对应，减少文件数量

### Claude's Discretion
- 具体 mock 设置细节
- 测试函数命名
- 是否添加 pytest markers (如 @pytest.mark.unit)
- fixture 复用策略

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### 需要测试的源代码
- `backend/core/external_precondition_bridge.py` — Phase 25 新增函数:
  - `resolve_headers()` (Line 644-678) — Headers 解析
  - `_parse_assertion_error()` (Line 681-718) — AssertionError 解析
  - `execute_assertion_method()` (Line 721+) — 断言执行引擎

### 现有测试文件
- `backend/tests/unit/test_external_assertion_bridge.py` — 现有断言桥接测试，需扩展
- `backend/tests/unit/test_precondition_service.py` — Phase 21 测试模式参考
- `backend/tests/unit/test_external_bridge.py` — Bridge 模块测试风格参考

### 前置阶段参考
- `.planning/phases/21-unit-test-coverage/21-CONTEXT.md` — Phase 21 测试决策（Mock 策略、覆盖率验证）
- `.planning/phases/25-assertion-execution-engine/25-CONTEXT.md` — Phase 25 设计决策（执行引擎逻辑）

</canonical_refs>

<code_context>
## Existing Code Insights

### 需要测试的核心代码

**resolve_headers() 函数** (external_precondition_bridge.py:644-678):
```python
def resolve_headers(identifier: str = 'main') -> dict:
    """Resolve header identifier to actual headers dict with auth tokens."""
    if identifier is None:
        identifier = 'main'

    if identifier not in VALID_HEADER_IDENTIFIERS:
        raise ValueError(f"Unknown header identifier: '{identifier}'...")

    login_api = _get_login_api()
    if login_api is None:
        raise RuntimeError("LoginApi not available...")

    return login_api.headers.get(identifier, login_api.headers['main'])
```

**_parse_assertion_error() 函数** (external_precondition_bridge.py:681-718):
```python
def _parse_assertion_error(error_message: str) -> list[dict]:
    """Parse AssertionError message to extract field-level results."""
    pattern = r"字段\s+['\"]([^'\"]+)['\"]\s+(预期值|预期包含):\s*['\"]([^'\"]*)['\"]..."
    # Returns list of {field, expected, actual, passed, comparison_type}
```

**execute_assertion_method() 函数** (external_precondition_bridge.py:721+):
```python
async def execute_assertion_method(
    class_name: str,
    method_name: str,
    headers: str | None = 'main',
    data: str = 'main',
    params: dict | None = None,
    timeout: float = 30.0
) -> dict:
    # Returns {success, passed, field_results, error, error_type, duration}
```

### 现有测试覆盖情况

**test_external_assertion_bridge.py:**
- `TestAssertionClassesDiscovery` — 4 个测试，覆盖断言类加载
- `TestParseDataOptions` — 3 个测试，覆盖 data 选项解析
- `TestParseParamOptions` — 4 个测试，覆盖 i/j/k 选项解析
- `TestExtractAssertionMethodInfo` — 3 个测试，覆盖方法信息提取
- `TestGetAssertionMethodsGrouped` — 2 个测试，覆盖方法分组

**缺失:** resolve_headers、_parse_assertion_error、execute_assertion_method 测试

### 测试模式参考

**Mock 模式** (from test_external_assertion_bridge.py):
```python
@pytest.fixture(autouse=True)
def reset_bridge_cache():
    """Reset bridge cache and settings cache before and after each test."""
    from backend.config import get_settings
    reset_cache()
    get_settings.cache_clear()
    yield
    reset_cache()
    get_settings.cache_clear()
```

**Monkeypatch 模式** (from Phase 21):
```python
def test_load_assertion_classes_unavailable(self, monkeypatch):
    from backend.config import get_settings
    monkeypatch.setenv('WEBSERP_PATH', '')
    get_settings.cache_clear()
    reset_cache()
    # Test code...
```

</code_context>

<specifics>
## Specific Ideas

- resolve_headers 测试应覆盖所有 7 个有效标识符 (main, idle, vice, special, platform, super, camera)
- _parse_assertion_error 测试应验证 comparison_type 正确区分 equals/contains
- execute_assertion_method 测试应验证 duration 字段被正确计算
- 测试失败时应记录完整堆栈到日志，但只返回摘要给调用方

</specifics>

<deferred>
## Deferred Ideas

- CI 集成覆盖率门槛 — 后续版本考虑
- 测试覆盖率徽章 — 后续版本考虑
- mutation testing — 后续版本考虑
- 共享 mock fixture 库 — 后续优化

</deferred>

---
*Phase: 27-unit-test-coverage*
*Context gathered: 2026-03-21*
