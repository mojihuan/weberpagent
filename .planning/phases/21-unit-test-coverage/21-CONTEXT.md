# Phase 21: Unit Test Coverage - Context

**Gathered:** 2026-03-19
**Status:** Ready for planning

<domain>
## Phase Boundary

为 Phase 17-19 引入的数据获取功能添加单元测试覆盖，确保核心逻辑有充分的测试保护。

**Scope:**
- ContextWrapper.get_data() 方法单元测试（正常/异常路径）
- execute_data_method_sync 包装函数单元测试
- 数据获取 API 端点单元测试（补充边界场景）
- 变量替换逻辑单元测试（验证现有覆盖）
- 新增代码覆盖率达到 80%+

**Out of Scope:**
- E2E 测试（Phase 20 已完成）
- Bug 修复（Phase 22）
- 新功能开发
- 性能测试

</domain>

<decisions>
## Implementation Decisions

### 测试组织策略
- **文件位置**: 添加到现有测试文件 `backend/tests/unit/test_precondition_service.py`
- **命名规范**: 新增 `TestContextWrapper` 和 `TestExecuteDataMethodSync` 测试类
- **理由**: 保持测试与代码位置对应，减少文件数量

### Mock 策略
- **外部依赖**: Mock `execute_data_method` 返回值，不依赖真实 webseleniumerp 项目
- **Mock 位置**: 使用 `patch.object` 或 `patch` 装饰器
- **好处**: 测试隔离、执行快速、无外部依赖

### 覆盖率验证
- **工具**: pytest-cov
- **命令**: `pytest --cov=backend/core --cov-report=term-missing backend/tests/unit/test_precondition_service.py`
- **目标**: 新增代码 80%+ 覆盖率
- **报告**: 生成 term-missing 报告查看未覆盖行

### ContextWrapper.get_data() 测试用例
- **成功路径**: `success=True` 时返回 `result['data']`
- **失败路径**: `success=False` 时抛出 `DataMethodError`，包含详细错误信息
- **错误类型覆盖**:
  1. `success=True, data=[...]` → 返回数据
  2. `success=False, error_type=ImportError` → 抛出 DataMethodError
  3. `success=False, error_type=NotFoundError` → 抛出 DataMethodError
  4. `success=False, error_type=TimeoutError` → 抛出 DataMethodError
  5. `success=False, error_type=ParameterError` → 抛出 DataMethodError
  6. `success=False, error_type=ExecutionError` → 抛出 DataMethodError

### ContextWrapper 字典接口测试
- `__getitem__`: 正常获取、KeyError
- `__setitem__`: 设置值
- `__contains__`: in 操作符
- `get`: 正常获取、默认值
- `keys`: 返回键集合
- `to_dict`: 返回字典副本

### execute_data_method_sync 测试用例
- **无事件循环**: 使用 `asyncio.run()` 执行
- **已有事件循环**: 使用 `nest_asyncio.apply()` 处理嵌套
- **返回值**: 透传 `execute_data_method` 结果

### 变量替换边界场景
- **已覆盖**: 基本替换、多变量、未定义变量、字典访问
- **补充场景**:
  - 列表索引访问 `{{items[0].name}}`
  - 嵌套字段路径 `{{data.level1.level2}}`
  - 空列表/空字典处理
  - 特殊字符在变量值中

### Claude's Discretion
- 具体 mock 设置细节
- 测试函数命名
- 是否添加 pytest markers (如 @pytest.mark.unit)

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### 需要测试的源代码
- `backend/core/precondition_service.py` — ContextWrapper 类、execute_data_method_sync 函数、PreconditionService.substitute_variables
- `backend/core/external_precondition_bridge.py` — execute_data_method 异步函数

### 现有测试文件
- `backend/tests/unit/test_precondition_service.py` — 现有 PreconditionService 测试，需扩展
- `backend/tests/api/test_external_data_methods.py` — API 端点测试，参考 mock 模式
- `backend/tests/unit/test_external_bridge.py` — Bridge 模块测试，参考测试风格

### 前置阶段参考
- `.planning/phases/19-集成与变量传递/19-CONTEXT.md` — ContextWrapper 设计决策、接口定义

</canonical_refs>

<code_context>
## Existing Code Insights

### 需要测试的核心代码

**ContextWrapper 类** (precondition_service.py:61-116):
```python
class ContextWrapper:
    def __init__(self):
        self._data: dict[str, Any] = {}

    def get_data(self, class_name: str, method_name: str, **params) -> Any:
        result = execute_data_method_sync(class_name, method_name, params)
        if not result['success']:
            raise DataMethodError(f"{class_name}.{method_name}(...) failed: {result['error']}")
        return result['data']

    # Dict-like interface: __getitem__, __setitem__, __contains__, get, keys, to_dict
```

**execute_data_method_sync 函数** (precondition_service.py:34-58):
```python
def execute_data_method_sync(class_name: str, method_name: str, params: dict) -> dict:
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        return asyncio.run(execute_data_method(class_name, method_name, params))

    nest_asyncio.apply()
    return asyncio.run(execute_data_method(class_name, method_name, params))
```

### 现有测试覆盖情况

**test_precondition_service.py:**
- `TestPreconditionService` — 16 个测试，覆盖基本执行流程
- `TestPreconditionServiceSubstitution` — 8 个测试，覆盖变量替换
- `TestPreconditionServiceExternalModule` — 5 个测试，覆盖外部模块加载
- `TestPreconditionServiceDynamicData` — 8 个测试，覆盖动态数据生成
- `TestPreconditionServiceBridgeIntegration` — 6 个测试，覆盖桥接集成

**缺失:** 直接测试 ContextWrapper.get_data() 和 execute_data_method_sync

### 测试模式参考

**Mock 模式** (from test_external_data_methods.py):
```python
with patch(
    'backend.api.routes.external_data_methods.execute_data_method',
    return_value={"success": True, "data": [...]}
):
    # test code
```

**异步测试模式** (from existing tests):
```python
@pytest.mark.asyncio
async def test_xxx(self, service):
    result = await service.execute_single(code, 0)
    assert result.success is True
```

</code_context>

<specifics>
## Specific Ideas

- 每个错误类型一个测试用例，确保 DataMethodError 包含完整的调用信息
- 测试 to_dict() 返回的是副本而非引用（修改副本不影响原数据）
- 测试 keys() 返回的是键的视图，反映实时数据
- execute_data_method_sync 测试应覆盖 `RuntimeError: no running event loop` 异常分支

</specifics>

<deferred>
## Deferred Ideas

- CI 集成覆盖率门槛 — 后续版本考虑
- 测试覆盖率徽章 — 后续版本考虑
- mutation testing — 后续版本考虑

</deferred>

---
*Phase: 21-unit-test-coverage*
*Context gathered: 2026-03-19*
