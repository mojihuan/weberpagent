# Phase 28: 后端字段发现 - Research

**Researched:** 2026-03-21
**Domain:** Python AST parsing, field discovery API
**Confidence:** HIGH

## Summary

This phase implements AST-based parsing of `base_assertions_field.py` to discover approximately 300 assertion fields and expose them via a REST API endpoint. The implementation extends the existing `external_precondition_bridge.py` module, following patterns established in Phase 23 (method discovery).

**Primary recommendation:** Use Python `ast` module with `ast.NodeVisitor` pattern to parse the `param` dictionary, extracting field names, paths, and detecting time fields via the `self.get_formatted_datetime()` default value pattern.

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

#### AST 解析策略
- **D-01:** 扩展现有 `external_precondition_bridge.py`，新增 `parse_assertions_field()` 函数
- **D-02:** 使用 Python `ast` 模块解析 base_assertions_field.py，避免运行时依赖 BaseApi
- **D-03:** 解析目标：`assertive_field` 方法中的 `param = {...}` 字典，提取所有键名
- **D-04:** 与现有 `load_base_assertions_class()` 模式保持一致

#### 字段分组规则
- **D-05:** 使用命名模式推断分组，规则如下：
  - `sale*` → 销售相关
  - `purchase*` → 采购相关
  - `inventory*` → 库存相关
  - `order*` → 订单相关
  - `*Time` / `*time` → 时间字段
  - `accessoryOrderInfo.*` → 配件订单嵌套字段
  - 其他 → 通用字段
- **D-06:** 不维护手动分组配置文件

#### Description 生成逻辑
- **D-07:** 使用关键词映射表生成中文描述（约 50 个常用关键词）
- **D-08:** 映射表示例：
  ```python
  KEYWORD_MAPPINGS = {
      'create': '创建',
      'update': '更新',
      'delete': '删除',
      'time': '时间',
      'status': '状态',
      'order': '订单',
      'sale': '销售',
      'purchase': '采购',
      'inventory': '库存',
      # ... 约 50 个
  }
  ```
- **D-09:** 生成规则：camelCase → 分词 → 映射 → 拼接

#### 时间字段识别
- **D-10:** 使用后缀匹配判断 `is_time_field`
- **D-11:** 时间字段后缀：`Time`, `time`, `Date`, `date`
- **D-12:** 示例：`createTime`, `updateTime`, `saleTime`, `orderDate` → `is_time_field: true`

#### API 响应结构
- **D-13:** 复用现有分组响应格式

#### 缓存策略
- **D-14:** 与 Phase 23 一致：模块级单例 + 启动时缓存
- **D-15:** 不提供刷新端点，需重启应用刷新字段列表

### Claude's Discretion
- 关键词映射表的具体条目（约 50 个，可在实现时补充）
- 嵌套字段 path 的具体格式（如 `accessoryOrderInfo.fieldName` 或 `accessoryOrderInfo[fieldName]`）
- 边界情况处理（无法识别的字段名直接返回原名）

### Deferred Ideas (OUT OF SCOPE)
- 前端字段配置组件 — Phase 29
- 断言执行适配层 — Phase 30
- E2E 测试 — Phase 31
- 手动补充字段描述 — 工作量巨大，使用自动生成
- 缓存刷新端点 — 未来优化
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| FLD-01 | 使用 AST 解析 param 字典，提取所有字段 | `ast.NodeVisitor` pattern with `visit_Dict` method |
| FLD-02 | API 端点 GET /api/external-assertions/fields 返回字段列表 | Follow Phase 23 `/methods` endpoint pattern |
| FLD-03 | 字段列表包含 name, path, is_time_field, group | Dictionary structure analysis + naming pattern inference |
</phase_requirements>

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| `ast` | stdlib | Parse Python source code | Standard library, no dependencies, robust parsing |
| `pathlib` | stdlib | File path handling | Cross-platform path handling |
| `re` | stdlib | Regex for name splitting | Pattern matching for camelCase |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| `FastAPI` | 0.100+ | REST API framework | Already in use for all API routes |
| `Pydantic` | 2.0+ | Response models | Response validation |

### No New Dependencies Required

This phase uses only Python standard library (`ast`, `pathlib`, `re`) plus existing project dependencies.

## Architecture Patterns

### Recommended Project Structure

```
backend/
├── core/
│   └── external_precondition_bridge.py  # Extend with field discovery functions
└── api/
    └── routes/
        └── external_assertions.py        # Add /fields endpoint
```

### Pattern 1: AST Dictionary Extraction

**What:** Parse `param = {...}` dictionary using `ast.NodeVisitor`
**When to use:** Extracting static data structures from Python source without runtime import
**Example:**

```python
import ast
from pathlib import Path


class ParamDictVisitor(ast.NodeVisitor):
    """Extract the param dictionary from assertive_field method."""

    def __init__(self):
        self.param_dict = None

    def visit_FunctionDef(self, node):
        if node.name == 'assertive_field':
            for child in ast.walk(node):
                if isinstance(child, ast.Assign):
                    for target in child.targets:
                        if isinstance(target, ast.Name) and target.id == 'param':
                            self.param_dict = child.value
        self.generic_visit(node)


def parse_assertions_field_py(file_path: str) -> list[dict]:
    """Parse base_assertions_field.py and extract all fields."""
    source_code = Path(file_path).read_text(encoding='utf-8')
    tree = ast.parse(source_code)

    visitor = ParamDictVisitor()
    visitor.visit(tree)

    if visitor.param_dict is None:
        return []

    fields = []
    for key, value in zip(visitor.param_dict.keys, visitor.param_dict.values):
        if isinstance(key, ast.Constant) and isinstance(value, ast.Tuple):
            field_name = key.value
            path_node = value.elts[0]
            default_node = value.elts[1]

            # Extract path (first element of tuple)
            path = path_node.value if isinstance(path_node, ast.Constant) else field_name

            # Detect time field by checking if default is get_formatted_datetime()
            is_time = isinstance(default_node, ast.Call) and \
                      isinstance(default_node.func, ast.Attribute) and \
                      default_node.func.attr == 'get_formatted_datetime'

            fields.append({
                'name': field_name,
                'path': path,
                'is_time_field': is_time,
            })

    return fields
```

### Pattern 2: Field Group Inference

**What:** Infer field group from naming patterns
**When to use:** Categorizing 300+ fields without manual configuration

```python
GROUP_RULES = [
    (r'^sale', '销售相关'),
    (r'^purchase', '采购相关'),
    (r'^inventory', '库存相关'),
    (r'^order', '订单相关'),
    (r'^accessoryOrderInfo\.', '配件订单嵌套'),
    (r'^sales', '销售相关'),
    (r'Time$|time$|Date$|date$', '时间字段'),
]

def infer_field_group(field_name: str) -> str:
    """Infer field group from name using naming patterns."""
    import re
    for pattern, group in GROUP_RULES:
        if re.search(pattern, field_name):
            return group
    return '通用字段'
```

### Pattern 3: Chinese Description Generation

**What:** Generate Chinese descriptions from camelCase field names
**When to use:** Providing human-readable field descriptions without manual translation

```python
KEYWORD_MAPPINGS = {
    'create': '创建',
    'update': '更新',
    'delete': '删除',
    'time': '时间',
    'date': '日期',
    'status': '状态',
    'str': '字符串',
    'num': '数量',
    'price': '价格',
    'amount': '金额',
    'order': '订单',
    'sale': '销售',
    'sales': '销售',
    'purchase': '采购',
    'inventory': '库存',
    'user': '用户',
    'name': '名称',
    'no': '编号',
    'id': 'ID',
    'type': '类型',
    'desc': '描述',
    'remark': '备注',
    'audit': '审核',
    'check': '检查',
    'express': '快递',
    'logistics': '物流',
    'warehouse': '仓库',
    'supplier': '供应商',
    'brand': '品牌',
    'model': '型号',
    'channel': '渠道',
    'business': '业务',
    'finish': '完成',
    'complete': '完成',
    'cancel': '取消',
    'total': '总计',
    'sum': '合计',
    'count': '计数',
    'return': '退货',
    'receive': '接收',
    'send': '发送',
    'delivery': '配送',
    'sign': '签收',
    'pay': '支付',
    'refund': '退款',
    'adjustment': '调整',
    'receipt': '收据',
    'bill': '账单',
    'account': '账户',
    'balance': '余额',
    'revenue': '收入',
    'income': '收益',
    'cost': '成本',
    'revenue': '收入',
    'accessory': '配件',
    'quality': '质量',
    'repair': '维修',
    'batch': '批次',
    'settlement': '结算',
    'platform': '平台',
    'tenant': '租户',
    'help': '辅助',
    'shelf': '上架',
    'storage': '存储',
    'outbound': '出库',
    'inbound': '入库',
    'assign': '分配',
    'distributor': '配送员',
    'rider': '骑手',
    'consigner': '发货人',
    'operate': '操作',
    'nick': '昵称',
    'video': '视频',
    'image': '图片',
    'goods': '商品',
    'article': '物品',
    'state': '状态',
    'reason': '原因',
    'result': '结果',
    'recheck': '复核',
    'review': '审查',
    'expect': '预期',
    'guarantee': '保证',
    'final': '最终',
    'auto': '自动',
    'bid': '竞价',
    'auction': '拍卖',
    'appeal': '申诉',
    'first': '首次',
    'latest': '最新',
    'wait': '等待',
    'issue': '问题',
    'normal': '正常',
    'abnormal': '异常',
    'fineness': '成色',
    'imei': 'IMEI',
    'sku': 'SKU',
    'info': '信息',
    'detail': '详情',
    'list': '列表',
    'config': '配置',
    'timeout': '超时',
    'publish': '发布',
    'internal': '内部',
    'external': '外部',
}

def split_camel_case(name: str) -> list[str]:
    """Split camelCase name into words."""
    import re
    # Pattern: lowercase followed by uppercase, or uppercase followed by lowercase
    words = re.findall(r'[A-Z]?[a-z]+|[A-Z]+(?=[A-Z]|$)', name)
    return [w.lower() for w in words]

def generate_field_description(field_name: str) -> str:
    """Generate Chinese description from field name."""
    words = split_camel_case(field_name)
    translated = []
    for word in words:
        if word in KEYWORD_MAPPINGS:
            translated.append(KEYWORD_MAPPINGS[word])
        else:
            translated.append(word.capitalize())

    return ''.join(translated) if translated else field_name
```

### Anti-Patterns to Avoid

- **Runtime import of BaseApi:** Do NOT import and instantiate `AssertionsRes` to get fields at runtime - causes heavy dependency chain
- **Manual field enumeration:** Do NOT hardcode the 300+ field names - use AST parsing
- **Complex NLP for description:** Do NOT use external NLP libraries - simple keyword mapping is sufficient

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Dictionary key extraction | Regex parsing of source | `ast.NodeVisitor` | Handles nested structures correctly |
| Time field detection | Heuristic pattern matching | Check `self.get_formatted_datetime()` call | Accurate detection from actual code |
| Field grouping | Manual configuration file | Naming pattern inference | Self-maintaining as fields change |

## Common Pitfalls

### Pitfall 1: Incorrect Path Extraction from Tuple

**What goes wrong:** The `param` dictionary values are tuples `(path, default)`. Incorrectly accessing tuple elements leads to wrong paths.

**Why it happens:** AST tuple nodes have `elts` attribute (list of elements), not direct value access.

**How to avoid:**
```python
# CORRECT: Access tuple elements via elts
path_node = value.elts[0]  # First element
default_node = value.elts[1]  # Second element

# WRONG: Direct value access
path = value.value  # AttributeError
```

**Warning signs:** `AttributeError: 'Tuple' object has no attribute 'value'`

### Pitfall 2: Missing Nested Field Detection

**What goes wrong:** Fields like `purchaseAmount` that map to `accessoryOrderInfo.purchaseAmount` are not detected as nested fields.

**Why it happens:** The path (first tuple element) contains the nested path, but the field name does not.

**How to avoid:** Check if the extracted path contains a dot (`.`):
```python
is_nested = '.' in path
```

### Pitfall 3: Time Field False Positives

**What goes wrong:** Fields containing "time" in their name (like `timeoutConfiguration`) are incorrectly flagged as time fields.

**Why it happens:** Using name suffix matching alone without checking the actual default value.

**How to avoid:** Use the AST-based detection of `self.get_formatted_datetime()` as primary, with suffix matching as fallback only:
```python
# Primary: Check AST for get_formatted_datetime call
is_time = isinstance(default_node, ast.Call) and \
          isinstance(default_node.func, ast.Attribute) and \
          default_node.func.attr == 'get_formatted_datetime'

# Fallback: Suffix matching (only if AST detection fails)
if not is_time:
    is_time = field_name.endswith(('Time', 'time', 'Date', 'date'))
```

### Pitfall 4: Inconsistent API Response Format

**What goes wrong:** Fields API returns different structure than Methods API, causing frontend integration issues.

**Why it happens:** Implementing new response format instead of reusing existing patterns.

**How to avoid:** Follow the exact structure from Phase 23:
```python
# Same pattern as get_assertion_methods_grouped()
{
    "available": bool,
    "groups": [{"name": str, "fields": [...]}],
    "total": int
}
```

## Code Examples

### Complete Field Discovery Implementation

```python
# backend/core/external_precondition_bridge.py (additions)

import ast
from pathlib import Path

# Module-level cache for assertion fields
_assertion_fields_cache: list[dict] | None = None
_assertion_fields_error: str | None = None


def _get_assertions_field_path() -> str | None:
    """Get path to base_assertions_field.py from settings."""
    from backend.config import get_settings
    settings = get_settings()
    if not settings.weberp_path:
        return None
    return str(Path(settings.weberp_path) / "common" / "base_assertions_field.py")


class ParamDictVisitor(ast.NodeVisitor):
    """Extract the param dictionary from assertive_field method."""

    def __init__(self):
        self.param_dict = None

    def visit_FunctionDef(self, node):
        if node.name == 'assertive_field':
            for child in ast.walk(node):
                if isinstance(child, ast.Assign):
                    for target in child.targets:
                        if isinstance(target, ast.Name) and target.id == 'param':
                            self.param_dict = child.value
        self.generic_visit(node)


def parse_assertions_field_py(file_path: str) -> list[dict]:
    """Parse base_assertions_field.py and extract all fields.

    Args:
        file_path: Path to base_assertions_field.py

    Returns:
        List of field info dicts with name, path, is_time_field, group, description
    """
    source_code = Path(file_path).read_text(encoding='utf-8')
    tree = ast.parse(source_code)

    visitor = ParamDictVisitor()
    visitor.visit(tree)

    if visitor.param_dict is None:
        return []

    fields = []
    for key, value in zip(visitor.param_dict.keys, visitor.param_dict.values):
        if isinstance(key, ast.Constant) and isinstance(value, ast.Tuple):
            field_name = key.value
            path_node = value.elts[0]
            default_node = value.elts[1]

            # Extract path (first element of tuple)
            if isinstance(path_node, ast.Constant):
                path = path_node.value
            else:
                path = field_name

            # Detect time field by checking if default is get_formatted_datetime()
            is_time = isinstance(default_node, ast.Call) and \
                      isinstance(default_node.func, ast.Attribute) and \
                      default_node.func.attr == 'get_formatted_datetime'

            # Fallback: check suffix
            if not is_time:
                is_time = field_name.endswith(('Time', 'time', 'Date', 'date'))

            fields.append({
                'name': field_name,
                'path': path,
                'is_time_field': is_time,
                'group': infer_field_group(field_name),
                'description': generate_field_description(field_name)
            })

    return fields


def get_assertion_fields_grouped() -> dict:
    """Get assertion fields grouped by category.

    Returns:
        dict with available, groups, and total fields
    """
    global _assertion_fields_cache, _assertion_fields_error

    if _assertion_fields_cache is not None:
        return {
            'available': True,
            'groups': _group_fields(_assertion_fields_cache),
            'total': len(_assertion_fields_cache)
        }

    if _assertion_fields_error is not None:
        return {
            'available': False,
            'error': _assertion_fields_error,
            'groups': [],
            'total': 0
        }

    # Get file path
    file_path = _get_assertions_field_path()
    if file_path is None:
        _assertion_fields_error = "WEBSERP_PATH not configured"
        return {
            'available': False,
            'error': _assertion_fields_error,
            'groups': [],
            'total': 0
        }

    if not Path(file_path).exists():
        _assertion_fields_error = f"File not found: {file_path}"
        return {
            'available': False,
            'error': _assertion_fields_error,
            'groups': [],
            'total': 0
        }

    try:
        _assertion_fields_cache = parse_assertions_field_py(file_path)
        return {
            'available': True,
            'groups': _group_fields(_assertion_fields_cache),
            'total': len(_assertion_fields_cache)
        }
    except Exception as e:
        _assertion_fields_error = f"Failed to parse fields: {e}"
        return {
            'available': False,
            'error': _assertion_fields_error,
            'groups': [],
            'total': 0
        }


def _group_fields(fields: list[dict]) -> list[dict]:
    """Group fields by their group property."""
    groups_dict: dict[str, list] = {}
    for field in fields:
        group_name = field['group']
        if group_name not in groups_dict:
            groups_dict[group_name] = []
        groups_dict[group_name].append({
            'name': field['name'],
            'path': field['path'],
            'is_time_field': field['is_time_field'],
            'description': field['description']
        })

    return [
        {'name': name, 'fields': fields_list}
        for name, fields_list in sorted(groups_dict.items())
    ]
```

### API Route Addition

```python
# backend/api/routes/external_assertions.py (additions)

from backend.core.external_precondition_bridge import get_assertion_fields_grouped


class FieldInfo(BaseModel):
    """Single field info."""
    name: str
    path: str
    is_time_field: bool
    description: str


class FieldGroup(BaseModel):
    """Group of fields under a category."""
    name: str
    fields: list[FieldInfo]


class AssertionFieldsResponse(BaseModel):
    """Response model for listing assertion fields."""
    available: bool
    error: str | None = None
    groups: list[FieldGroup] = []
    total: int = 0


@router.get("/fields", response_model=AssertionFieldsResponse)
async def list_assertion_fields():
    """List all available assertion fields.

    Returns 503 if external module is not available.
    """
    result = get_assertion_fields_grouped()

    if not result['available']:
        raise HTTPException(
            status_code=503,
            detail={
                "message": "External assertion fields not available",
                "reason": result.get('error', 'Unknown error'),
                "fix": "Ensure WEBSERP_PATH is configured in .env"
            }
        )

    return AssertionFieldsResponse(
        available=True,
        groups=[FieldGroup(**g) for g in result['groups']],
        total=result['total']
    )
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Runtime import + reflection | AST parsing | Phase 28 | No BaseApi dependency, faster startup |
| Manual field documentation | Auto-generated descriptions | Phase 28 | Self-maintaining as fields change |
| Flat field list | Grouped by category | Phase 28 | Better UX for 300+ fields |

**Deprecated/outdated:**
- Runtime reflection via `AssertionsRes().assertive_field.__code__`: Requires full import chain, causes side effects

## Open Questions

1. **Should keyword mappings be externalized?**
   - What we know: 50+ keywords needed for good descriptions
   - What's unclear: Whether to keep inline or move to config file
   - Recommendation: Keep inline for Phase 28, consider externalization if maintenance becomes burdensome

2. **How to handle duplicate field names with different paths?**
   - What we know: `purchaseAmount` and `purchaseTime_2` both exist but map to different paths
   - What's unclear: Whether frontend needs both or should deduplicate by path
   - Recommendation: Return all fields as-is, let frontend decide deduplication strategy

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | pytest 8.0+ |
| Config file | `backend/tests/conftest.py` |
| Quick run command | `uv run pytest backend/tests/unit/test_external_assertion_fields.py -v` |
| Full suite command | `uv run pytest backend/tests/ -v` |

### Phase Requirements → Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| FLD-01 | AST 解析 param 字典 | unit | `pytest tests/unit/test_external_assertion_fields.py::test_parse_param_dict -v` | ❌ Wave 0 |
| FLD-02 | API 端点返回字段列表 | integration | `pytest tests/api/test_external_assertions_api.py::test_list_fields -v` | ❌ Wave 0 |
| FLD-03 | 字段包含 name, path, is_time_field, group | unit | `pytest tests/unit/test_external_assertion_fields.py::test_field_structure -v` | ❌ Wave 0 |

### Sampling Rate
- **Per task commit:** `uv run pytest backend/tests/unit/test_external_assertion_fields.py -v`
- **Per wave merge:** `uv run pytest backend/tests/ -v -k "field" --tb=short`
- **Phase gate:** Full suite green before `/gsd:verify-work`

### Wave 0 Gaps
- [ ] `backend/tests/unit/test_external_assertion_fields.py` — AST parsing tests
- [ ] `backend/tests/api/test_external_assertions_fields_api.py` — API endpoint tests
- [ ] Framework install: Already present (pytest)

## Sources

### Primary (HIGH confidence)
- [Python ast module documentation](https://docs.python.org/3/library/ast.html) - AST parsing API
- `/Users/huhu/project/webseleniumerp-master/common/base_assertions_field.py` - Actual file structure (310 lines)
- `/Users/huhu/project/weberpagent/backend/core/external_precondition_bridge.py` - Existing patterns to extend

### Secondary (MEDIUM confidence)
- [Stack Overflow: ast.NodeVisitor example](https://stackoverflow.com/questions/1515357/simple-example-of-how-to-use-ast-nodevisitor) - Visitor pattern usage
- `/Users/huhu/project/weberpagent/backend/api/routes/external_assertions.py` - API route patterns

### Tertiary (LOW confidence)
- Web search results for Python AST best practices - Verified against official docs

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - Using stdlib only, patterns well-established
- Architecture: HIGH - Extending existing module with proven patterns
- Pitfalls: HIGH - Based on actual file structure analysis

**Research date:** 2026-03-21
**Valid until:** 30 days (stable Python stdlib APIs)
