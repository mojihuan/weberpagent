# Phase 19: 集成与变量传递 - Context

**Gathered:** 2026-03-18
**Status:** Ready for planning

<domain>
## Phase Boundary

将 DataMethodSelector 生成的代码与前置条件执行系统打通，实现：
1. 前端生成的数据获取代码正确包含 className
2. PreconditionService 执行环境中提供 context.get_data() 方法
3. 数据获取结果存入执行上下文
4. 测试步骤和接口断言中支持 {{变量名}} 变量替换

**Scope:**
- 修改前端代码生成格式，传递 className
- 实现 ContextWrapper 类，提供 get_data 方法
- 集成 ExternalPreconditionBridge.execute_data_method
- 确保变量替换在 Browser-Use 执行前和接口断言执行前发生

**Out of Scope:**
- 前端 DataMethodSelector 组件修改（Phase 18 已完成）
- 后端数据获取 API（Phase 17 已完成）
- 修改 webseleniumerp 项目代码

</domain>

<decisions>
## Implementation Decisions

### 代码生成格式 (INT-01)
- **修改前端代码格式**: 从 `context.get_data('method_name', i=2)` 改为 `context.get_data('ClassName', 'method_name', i=2)`
- **修改文件**: `frontend/src/components/TaskModal/TaskForm.tsx` 和 `DataMethodSelector.tsx`
- **格式示例**:
  ```python
  imei = context.get_data('BaseParams', 'inventory_list_data', i=2, j=13)[0]['imei']
  ```

### ContextWrapper 实现 (INT-02)
- **使用包装类**: 创建 `ContextWrapper` 类替代普通 dict
- **类定义位置**: `backend/core/precondition_service.py`
- **接口设计**:
  ```python
  class ContextWrapper:
      def __init__(self, bridge_module):
          self._data = {}
          self._bridge = bridge_module

      def get_data(self, class_name: str, method_name: str, **params) -> Any:
          """调用 ExternalPreconditionBridge.execute_data_method"""
          result = execute_data_method_sync(class_name, method_name, params)
          if not result['success']:
              raise DataMethodError(f"Data method failed: {class_name}.{method_name}({params}) - {result['error']}")
          return result['data']

      def __getitem__(self, key): return self._data[key]
      def __setitem__(self, key, value): self._data[key] = value
      def __contains__(self, key): return key in self._data
      def get(self, key, default=None): return self._data.get(key, default)
      def keys(self): return self._data.keys()
      def to_dict(self): return dict(self._data)
  ```

### 同步执行适配
- **问题**: `execute_data_method` 是 async，但前置条件执行使用 `exec()` 是同步
- **解决方案**: 创建 `execute_data_method_sync` 包装函数
- **实现方式**: 使用 `asyncio.run()` 在同步上下文中执行异步函数
- **注意**: 需要处理已在事件循环中的情况（使用 `nest_asyncio` 或检测事件循环）

### 变量替换集成 (INT-03)
- **替换时机**: Browser-Use 执行前统一替换（已实现于 `runs.py:129`）
- **替换范围**:
  - task_description（测试步骤）✓ 已实现
  - api_assertions（接口断言）✓ 本次确认支持
- **替换方法**: `PreconditionService.substitute_variables(text, context.to_dict())`
- **错误处理**: 使用 Jinja2 StrictUndefined，未定义变量抛出 UndefinedError

### 错误处理
- **get_data 失败**: 抛出 `DataMethodError` 异常，终止前置条件执行
- **错误信息格式**: 详细信息，包含 class_name、method_name、params 和原始错误
  ```
  DataMethodError: BaseParams.inventory_list_data(i=2, j=13) failed: Connection timeout
  ```
- **未定义变量**: 抛出 UndefinedError，终止测试执行（已实现）

### Claude's Discretion
- ContextWrapper 类的具体实现细节
- DataMethodError 异常类的定义位置
- execute_data_method_sync 的具体实现方式
- 接口断言变量替换的调用点位置

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### 核心代码参考
- `backend/core/precondition_service.py` — 前置条件执行服务，需添加 ContextWrapper 类
- `backend/core/external_precondition_bridge.py` — execute_data_method 函数，ContextWrapper 将调用此函数
- `backend/api/routes/runs.py` — 测试执行入口，变量替换调用点（第 129 行）
- `frontend/src/components/TaskModal/TaskForm.tsx` — 代码生成逻辑（第 210-238 行）
- `frontend/src/components/TaskModal/DataMethodSelector.tsx` — 代码生成逻辑（第 206-224 行）

### 前置阶段参考
- `.planning/phases/17-后端数据获取桥接/17-CONTEXT.md` — execute_data_method API 定义
- `.planning/phases/18-前端数据选择器/18-CONTEXT.md` — DataMethodConfig 类型定义、代码生成格式

### 类型定义
- `frontend/src/types/index.ts` — DataMethodConfig 接口（包含 className 字段）

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `backend/core/external_precondition_bridge.py`:
  - `execute_data_method()` — 异步执行数据方法，返回 `{"success": bool, "data": ..., "error": ...}`
  - `load_base_params_class()` — 延迟加载 BaseParams 类
  - `configure_external_path()` — 路径配置逻辑
- `backend/core/precondition_service.py`:
  - `_setup_execution_env()` — 创建 exec() 执行环境，需修改返回 ContextWrapper
  - `substitute_variables()` — Jinja2 变量替换，已实现
  - `get_context()` — 返回执行上下文，需修改返回 dict
- `backend/api/routes/runs.py`:
  - 第 124-129 行 — 变量替换调用点，已实现

### Established Patterns
- **执行环境**: `_setup_execution_env()` 返回的 dict 注入 exec() 全局命名空间
- **错误处理**: 失败时抛出异常，由 `execute_single()` 捕获并返回 `PreconditionResult`
- **超时保护**: 30 秒超时（与现有前置条件一致）
- **变量替换**: Jinja2 StrictUndefined 模式

### Current Code Generation (需修改)
```javascript
// TaskForm.tsx:219 - 当前格式（缺少 className）
const methodCall = `context.get_data('${config.methodName}', ${params})`

// 修改后格式
const methodCall = `context.get_data('${config.className}', '${config.methodName}', ${params})`
```

### Integration Points
- `PreconditionService.__init__()` — 需初始化 ContextWrapper
- `PreconditionService._setup_execution_env()` — 需返回 ContextWrapper 实例
- `PreconditionService.get_context()` — 需调用 `context.to_dict()`
- `runs.py` api_assertions 处理 — 需添加变量替换调用

</code_context>

<specifics>
## Specific Ideas

- ContextWrapper 应该继承 `collections.abc.MutableMapping` 以获得完整的 dict 接口
- 错误信息应该清晰显示完整的方法调用链，便于调试
- 接口断言的变量替换应该复用 `substitute_variables` 静态方法

</specifics>

<deferred>
## Deferred Ideas

- 数据缓存机制（避免同一方法多次调用）— v2 需求
- 链式数据获取（一个方法的输出作为另一个方法的输入）— v2 需求
- 异步前置条件执行（目前使用 run_in_executor）— 性能优化

</deferred>

---
*Phase: 19-集成与变量传递*
*Context gathered: 2026-03-18*
