# ERP 全面集成重构设计

> 日期：2026-04-11
> 基于：沟通记录 3/16、3/21、4/10
> 目标：跑通「Excel导入 → 前置API(含缓存) → AI执行UI → 断言(含缓存验证)」完整链路

## 1. 背景

### 1.1 现状

aiDriveUITest 平台已实现：
- Excel 导入/导出（模板、预览、确认）
- 前置条件执行（Python exec + 变量传递）
- 外部断言桥接（通过 `external_precondition_bridge.py` 调用 webseleniumerp 的 PcAssert/MgAssert/McAssert）
- AI Agent 执行（browser-use + Playwright）
- SSE 实时推送 + 批量执行

webseleniumerp 项目已实现（他手写的框架）：
- 完整的 ERP API 封装（30+ 模块）
- 多账号管理（user_info.py，6+ 角色）
- 参数缓存（file_cache_manager.py，JSON 文件）
- 断言系统（base_assertions + base_assertions_field）

### 1.2 缺失能力

| 缺失 | 4/10 沟通中的描述 |
|------|-------------------|
| 参数缓存 | 查询 API → 缓存物品编号(key='i') → 执行后验证编号出现在结果中 |
| 多账号登录 | 不同用例使用不同账号，账号不能写死在 Excel，从 user_info.py 读取 |
| 登录 URL 管理 | 写死在代码里，不进 Excel |
| Excel 模板适配 | 支持 `{点击}/{输入}/{调用方法}` 格式，新增「登录角色」列 |

## 2. 整体架构

```
┌─────────────────────────────────────────────────────────────────┐
│                      Excel 用例模板                              │
│  登录角色 | 前置条件(含缓存) | 步骤描述 | 断言(含缓存验证)         │
└───────────────────────────┬─────────────────────────────────────┘
                            │ 导入
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                   TestFlowService (新增)                         │
│  编排完整测试流程：                                              │
│  1. AccountService.resolve(role) → 登录凭证                     │
│  2. CacheService.create(run_id) → 缓存上下文                    │
│  3. PreconditionService.execute() → 执行前置+缓存               │
│  4. AgentService.run() → AI 执行 UI                             │
│  5. AssertionService.execute() → 执行断言+缓存验证               │
│  6. CacheService.cleanup() → 清理                               │
└───────────────────────────┬─────────────────────────────────────┘
                            │
              ┌─────────────┼─────────────┐
              ▼             ▼             ▼
     AccountService  CacheService   (现有模块)
     (新增)          (新增)         PreconditionService
     读取账号配置     内存KV缓存     AgentService
     提供 token      cache(key,val)  AssertionService
     多角色支持       cached(key)
```

## 3. CacheService（参数缓存）

### 3.1 设计

```python
# backend/core/cache_service.py

class CacheService:
    """每次 Run 独立的内存缓存，替代 webseleniumerp 的 JSON 文件方案"""

    def __init__(self):
        self._store: dict[str, Any] = {}

    def cache(self, key: str, value: Any) -> Any:
        """缓存值，返回 value 本身（方便链式调用）"""
        self._store = {**self._store, key: value}
        return value

    def cached(self, key: str) -> Any:
        """读取缓存值，不存在则抛 KeyError"""
        if key not in self._store:
            raise KeyError(f"缓存 key '{key}' 不存在")
        return self._store[key]

    def has(self, key: str) -> bool:
        return key in self._store

    def all(self) -> dict:
        """返回所有缓存（用于断言对比）"""
        return dict(self._store)

    def clear(self) -> None:
        self._store = {}
```

### 3.2 使用流程

对应他描述的「销售出库」用例：

1. **前置条件中缓存**：
```python
items = context.get_data('PcImport', 'inventory_list', i=2, j=13)
articles_no = items[0]['imei']
context.cache('i', articles_no)  # 缓存物品编号到 key='i'
```

2. **步骤描述中引用**：
```
步骤5：{输入}物品编号{{cached:i}}
```
PreconditionService 的 Jinja2 替换会将 `{{cached:i}}` 替换为实际缓存的物品编号。

3. **断言中验证**：
```python
cached_no = cache.cached('i')
result = execute_assertion_method(...)
# 验证缓存的物品编号出现在销售列表中
assert cached_no in [item['articlesNo'] for item in result]
```

### 3.3 与 PreconditionService 集成

在 `PreconditionService` 的 `ContextWrapper` 中增加：

```python
class ContextWrapper:
    def __init__(self, cache: CacheService):
        self._vars = {}
        self._cache = cache

    def cache(self, key: str, value: Any) -> Any:
        return self._cache.cache(key, value)

    def cached(self, key: str) -> Any:
        return self._cache.cached(key)
```

前置条件代码中可直接调用 `context.cache('i', value)` 和 `context.cached('i')`。

### 3.4 生命周期

- **创建**：Run 开始时由 TestFlowService 创建
- **传递**：通过参数传给 PreconditionService 和 AssertionService
- **销毁**：Run 结束时自动销毁（内存中，无需清理文件）

## 4. AccountService（多账号登录）

### 4.1 设计

```python
# backend/core/account_service.py

@dataclass(frozen=True)
class AccountInfo:
    account: str
    password: str
    role: str
    user_id: int | None = None
    merchant_id: int | None = None

class AccountService:
    """多账号管理，从 user_info.py 配置读取"""

    ROLE_MAP = {
        'main': ('main_account', 'password'),
        'special': ('special_account', 'password'),
        'vice': ('vice_account', 'password'),
        'camera': ('camera_account', 'password'),
        'platform': ('platform_account', 'super_admin_password'),
        'super': ('super_admin_account', 'super_admin_password'),
        'bot': ('bot_phone', 'password'),
        'idle': ('idle_account', 'password'),
    }

    def __init__(self):
        self._config = self._load_config()

    def _load_config(self) -> dict:
        """从 webseleniumerp/config/user_info.py 加载配置"""
        # 通过 external_precondition_bridge 加载
        ...

    def resolve(self, role: str) -> AccountInfo:
        """根据角色名返回登录信息"""
        if role not in self.ROLE_MAP:
            raise ValueError(f"未知角色: {role}")
        account_field, password_field = self.ROLE_MAP[role]
        account = self._config[account_field]
        password = self._config[password_field]
        return AccountInfo(
            account=account,
            password=password,
            role=role,
        )

    def get_login_url(self) -> str:
        """返回写死的登录 URL"""
        from backend.config import get_settings
        settings = get_settings()
        return settings.erp_login_url  # 新增配置项
```

### 4.2 Excel 使用

Excel 中新增「登录角色」列，值为角色 ID：
- `main` - 主账号（奥特曼18admin）
- `special` - 库管账号
- `vice` - 帮买账号
- `camera` - 拍机账号
- `platform` - 平台账号
- `super` - 超管账号

登录 URL 从 `settings.py` 的 `ERP_LOGIN_URL` 读取，不暴露在 Excel 中。

### 4.3 AI Agent 集成

TestFlowService 在构建任务描述时自动注入登录步骤：

```
步骤0（自动注入）：打开 {login_url}，输入账号 {account}，输入密码 {password}，点击登录按钮
步骤1（用户定义）：{点击}库存管理
...
```

## 5. Excel 模板新格式

### 5.1 列定义

| 列名 | 必填 | 类型 | 说明 |
|------|------|------|------|
| 任务名称 | 是 | text | 用例名称 |
| 登录角色 | 是 | text | 角色 ID（main/special/vice/camera/platform/super） |
| 前置条件 | 否 | json | JSON 数组，支持缓存操作 |
| 任务描述 | 是 | text | AI 执行的步骤描述 |
| 最大步数 | 否 | int | 默认 20 |
| 断言 | 否 | json | JSON 数组，支持缓存验证 |

### 5.2 前置条件 JSON 格式

```json
[
  {
    "type": "cache",
    "description": "查询库存列表并缓存物品编号",
    "method": "PcImport.inventory_list",
    "params": {"data": "main", "i": 2, "j": 13},
    "cache_key": "i",
    "cache_field": "imei"
  },
  {
    "type": "code",
    "description": "生成随机物流单号",
    "code": "context['sf_no'] = random_sf()"
  }
]
```

两种前置条件类型：
- `cache`：调用外部数据方法，从返回结果中提取字段缓存
- `code`：执行 Python 代码（现有能力）

### 5.3 断言 JSON 格式

```json
[
  {
    "type": "external",
    "method": "PcAssert.sell_sale_item_list_assert",
    "params": {"data": "main"},
    "cache_key": "i",
    "match_field": "articlesNo",
    "expected": "exists"
  }
]
```

断言类型：
- `external`：调用外部断言方法
- `cache_verify`：验证缓存值在查询结果中存在

### 5.4 任务描述格式

支持变量替换：
- `{{变量名}}` - 前置条件中的变量
- `{{cached:key}}` - 缓存的值

示例：
```
步骤1：{点击}库存管理
步骤2：{点击}出库管理
步骤3：{点击}销售出库
步骤4：{点击}请选择客户{选择第二个}
步骤5：{输入}物品编号{{cached:i}}
步骤6：{点击}添加
步骤7：{输入}销售金额{150}
步骤8：{点击}确认
```

## 6. TestFlowService（流程编排）

### 6.1 设计

```python
# backend/core/test_flow_service.py

class TestFlowService:
    """编排完整的测试流程"""

    def __init__(
        self,
        account_service: AccountService,
        cache_service: CacheService,
        precondition_service: PreconditionService,
        agent_service: AgentService,
    ):
        self._accounts = account_service
        self._cache = cache_service
        self._preconditions = precondition_service
        self._agent = agent_service

    async def execute(self, task: Task, run: Run) -> None:
        # 1. 解析登录角色
        account = self._accounts.resolve(task.login_role)

        # 2. 创建缓存上下文
        cache = CacheService()

        # 3. 执行前置条件（含缓存写入）
        preconditions = self._parse_preconditions(task.preconditions)
        context = await self._preconditions.execute_all(
            preconditions, cache=cache
        )

        # 4. 构建完整任务描述（注入登录步骤 + 替换变量 + 替换缓存引用）
        description = self._build_description(
            task.description, account, context, cache
        )

        # 5. AI Agent 执行 UI 操作
        await self._agent.run_with_streaming(
            description, run, max_steps=task.max_steps
        )

        # 6. 执行断言（含缓存验证）
        assertions = self._parse_assertions(task.external_assertions)
        await self._execute_assertions(assertions, cache, run)

    def _build_description(
        self,
        description: str,
        account: AccountInfo,
        context: dict,
        cache: CacheService,
    ) -> str:
        """构建完整任务描述"""
        # 注入登录步骤
        login_url = self._accounts.get_login_url()
        login_prefix = (
            f"1. 打开 {login_url}\n"
            f"2. 在账号输入框输入 {account.account}\n"
            f"3. 在密码输入框输入 {account.password}\n"
            f"4. 点击登录按钮\n"
            f"5. 确认登录成功\n"
        )

        # 替换变量
        from jinja2 import Template
        template = Template(description)
        variables = {**context, 'cached': cache.all()}
        rendered = template.render(**variables)

        return login_prefix + rendered
```

### 6.2 与现有执行流程集成

当前执行流程入口在 `backend/api/routes/runs.py` 的 `run_agent_background()` 函数。

改造策略：
1. 保持现有 API 接口不变
2. 在 `run_agent_background()` 中检测 task 是否有 `login_role`
3. 如果有，走 TestFlowService 的新流程
4. 如果没有，走现有流程（向后兼容）

```python
# backend/api/routes/runs.py 改动点

async def run_agent_background(run_id: str, task: Task, ...):
    if task.login_role:
        # 新流程：通过 TestFlowService 编排
        flow = TestFlowService(...)
        await flow.execute(task, run)
    else:
        # 现有流程（向后兼容）
        ...  # 原有代码
```

## 7. 改动范围

### 7.1 新增文件

| 文件 | 说明 |
|------|------|
| `backend/core/cache_service.py` | 内存缓存服务 |
| `backend/core/account_service.py` | 多账号管理服务 |
| `backend/core/test_flow_service.py` | 测试流程编排服务 |

### 7.2 改动文件

| 文件 | 改动 |
|------|------|
| `backend/core/precondition_service.py` | ContextWrapper 增加 cache/cached 方法 |
| `backend/core/external_precondition_bridge.py` | 拆分重构，支持缓存操作 |
| `backend/utils/excel_template.py` | 更新模板列定义 |
| `backend/utils/excel_parser.py` | 适配新列格式 |
| `backend/api/routes/runs.py` | 集成 TestFlowService |
| `backend/db/models.py` | Task 增加 login_role 字段 |
| `backend/db/schemas.py` | Schema 增加 login_role |
| `backend/config/settings.py` | 增加 ERP_LOGIN_URL 配置 |
| 前端任务编辑页面 | 增加登录角色选择 |

### 7.3 不改动

| 模块 | 原因 |
|------|------|
| `backend/core/agent_service.py` | Agent 执行逻辑不变，只改输入 |
| `backend/core/assertion_service.py` | UI 断言保持不变 |
| `backend/core/batch_execution.py` | 批量执行逻辑不变 |
| `backend/core/event_manager.py` | SSE 事件机制不变 |
| `webseleniumerp/` | 不修改外部项目代码 |

## 8. 实施顺序建议

1. **Phase 1 - CacheService**：实现缓存服务，集成到 PreconditionService
2. **Phase 2 - AccountService**：实现多账号管理，读取 user_info.py
3. **Phase 3 - Excel 模板更新**：新增列定义，更新解析器
4. **Phase 4 - TestFlowService**：编排层，串联所有组件
5. **Phase 5 - 端到端验证**：用「销售出库」用例跑通完整链路
