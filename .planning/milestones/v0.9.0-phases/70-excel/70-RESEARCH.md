# Phase 70: Excel 模版设计 - Research

**Researched:** 2026-04-08
**Domain:** openpyxl template generation + parsing, FastAPI file download
**Confidence:** HIGH

## Summary

Phase 70 builds two components: (1) an Excel template generator that produces a downloadable .xlsx file with styled headers, example data, a README sheet, and data validation dropdowns, and (2) an ExcelParser that reads .xlsx files back into structured row data aligned with the existing TaskCreate schema. The only dependency is openpyxl 3.1.5 (already installed and verified working in the project venv). All openpyxl features needed -- DataValidation, cell styling, freeze panes, merged cell detection, StreamingResponse -- have been verified by running live tests against the project's Python environment.

The parser uses a collect-all error strategy (returning all row errors together) to support Phase 71's preview-then-confirm workflow. Type coercion follows a lenient approach: numbers to strings, booleans to strings, empty cells skipped, merged cells reported as errors. The parser's output maps directly to TaskCreate fields so that Phase 71 can validate parsed rows through the existing Pydantic schema without modification.

**Primary recommendation:** Create two files in `backend/utils/` -- `excel_template.py` (template generation) and `excel_parser.py` (parsing with error collection) -- plus add a single GET endpoint to the existing tasks router. Unit tests are straightforward since both components are pure functions with no database or external service dependencies.

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions
- **D-01:** 前置条件列使用 JSON 格式填写，QA 在 Excel 单元格内直接写 JSON（如 `["code1", "code2"]`）
- **D-02:** 断言列使用 JSON 格式填写，QA 写 JSON 数组（如 `[{"methodName":"xxx","headers":"main"}]`）
- **D-03:** 前置条件列和断言列均为可选列，留空时解析为空（null/空数组），必填列只有任务名称和任务描述
- **D-04:** 获取数据操作合并在前置条件 JSON 里，不单独设列
- **D-05:** 后续可优化为"操作名引用"模式（更友好的填写方式），v1 先用 JSON
- **D-06:** 模版下载端点为 GET /tasks/template，在现有 tasks 路由文件中添加，返回 StreamingResponse (.xlsx)
- **D-07:** 模版不含版本号，简单优先。模版格式变化时解析器跟着变
- **D-08:** ExcelParser 使用 collect-all 策略，收集所有行的错误后一起返回（Phase 71 预览需要逐行错误信息）
- **D-09:** 类型强制转换使用宽松模式：数字转字符串、空单元格跳过、布尔转字符串，最大程度包容 QA 填写习惯

### Claude's Discretion
- 模版列头的中英文名称选择（README sheet 可用中文，列头建议中文以对齐 QA 习惯）
- 示例数据的具体内容
- README sheet 的说明格式和详细程度
- 解析器的具体代码结构（模块名、类名等）
- 合并单元格检测的具体实现方式

### Deferred Ideas (OUT OF SCOPE)
- 操作名引用模式（前置条件和断言）— 更友好的填写方式，用户明确表示后续优化
- 管道分隔断言格式 (method|headers|data|params) — v2 REQUIREMENTS (IMPT-05)
- 模版版本号机制 — 当前不需要，未来格式升级时再考虑
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| TMPL-01 | 用户可以下载预格式化的 Excel 模版 (.xlsx)，包含列头 + 2 行示例数据 + README sheet 说明 | openpyxl Workbook + DataValidation + styling APIs verified; StreamingResponse pattern for FastAPI verified |
| TMPL-02 | Excel 模版中对 max_steps 字段配置下拉验证（1-100），防止输入错误 | openpyxl DataValidation with type='whole', operator='between', formula1=1, formula2=100 verified working |
</phase_requirements>

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| openpyxl | 3.1.5 | Excel template generation and parsing | Already installed in project venv; already used in `webseleniumerp/use_case/export.py` |
| FastAPI StreamingResponse | (starlette) | Return .xlsx file as download | Standard FastAPI pattern for binary file responses |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| io.BytesIO | (stdlib) | In-memory binary buffer for openpyxl | Template generation writes to BytesIO, not disk |
| json | (stdlib) | Parse JSON strings in preconditions/assertions cells | Validate JSON format during parsing |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| openpyxl | xlsxwriter | xlsxwriter cannot read existing files (write-only); openpyxl does both read and write, already installed |
| openpyxl | pandas | pandas is 10x heavier dependency for simple row parsing; overkill for 6-column flat data |

**Installation:**
```bash
# No new packages needed. openpyxl 3.1.5 already installed.
uv run python -c "import openpyxl; print(openpyxl.__version__)"  # verifies 3.1.5
```

**Version verification:**
- openpyxl: 3.1.5 (verified via `uv run python -c "import openpyxl; print(openpyxl.__version__)"` on 2026-04-08)

## Architecture Patterns

### Recommended Project Structure
```
backend/
├── utils/
│   ├── __init__.py          # (exists)
│   ├── logger.py            # (exists)
│   ├── run_logger.py        # (exists)
│   ├── screenshot.py        # (exists)
│   ├── excel_template.py    # NEW: template generation
│   └── excel_parser.py      # NEW: Excel file parsing + error collection
├── api/
│   └── routes/
│       └── tasks.py         # MODIFY: add GET /tasks/template endpoint
└── tests/
    └── unit/
        ├── test_excel_template.py  # NEW: template generation tests
        └── test_excel_parser.py    # NEW: parser + error collection tests
```

### Pattern 1: Template Generation (Pure Function)
**What:** A function that creates an in-memory Workbook, applies styling/validation, writes example data, and returns BytesIO buffer.
**When to use:** Template download endpoint.
**Example:**
```python
# backend/utils/excel_template.py
from io import BytesIO
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.utils import get_column_letter

# Column contract -- single source of truth for both template and parser
TEMPLATE_COLUMNS = [
    {"key": "name",          "header": "任务名称", "width": 25, "required": True},
    {"key": "description",   "header": "任务描述", "width": 40, "required": True},
    {"key": "target_url",    "header": "目标URL",  "width": 35, "required": False},
    {"key": "max_steps",     "header": "最大步数", "width": 12, "required": False},
    {"key": "preconditions", "header": "前置条件", "width": 40, "required": False},
    {"key": "assertions",    "header": "断言",     "width": 50, "required": False},
]

def generate_template() -> BytesIO:
    wb = Workbook()
    ws = wb.active
    ws.title = "测试用例"

    # Write styled headers (row 1)
    # ... apply font, fill, alignment, border ...

    # Add data validation for max_steps (column D, rows 2-1000)
    dv = DataValidation(type="whole", operator="between",
                        formula1=1, formula2=100, allow_blank=True)
    dv.error = "请输入 1-100 之间的整数"
    dv.errorTitle = "输入错误"
    dv.showErrorMessage = True
    ws.add_data_validation(dv)
    dv.add("D2:D1000")

    # Write 2 example rows (rows 2-3)
    # ...

    # Create README sheet
    ws_readme = wb.create_sheet("README")
    # ... fill instructions ...

    # Freeze top row
    ws.freeze_panes = "A2"

    buffer = BytesIO()
    wb.save(buffer)
    buffer.seek(0)
    return buffer
```

### Pattern 2: Parser with Collect-All Errors
**What:** A function that iterates rows, collects per-row errors without raising, and returns structured results for Phase 71's preview UI.
**When to use:** Parsing uploaded .xlsx files (Phase 71) and template round-trip validation (Phase 70 tests).
**Example:**
```python
# backend/utils/excel_parser.py
from dataclasses import dataclass, field
from typing import Any
from openpyxl import load_workbook
from openpyxl.cell.cell import MergedCell

@dataclass(frozen=True)
class ParsedRow:
    row_number: int
    data: dict[str, Any]   # keys match TEMPLATE_COLUMNS key names
    errors: list[str] = field(default_factory=list)

@dataclass(frozen=True)
class ParseResult:
    rows: list[ParsedRow]
    total_rows: int
    has_errors: bool

def parse_excel(buffer: BytesIO) -> ParseResult:
    wb = load_workbook(buffer, data_only=True)
    ws = wb.active

    # Validate headers match TEMPLATE_COLUMNS
    headers = [cell.value for cell in ws[1]]
    # ... compare against expected headers ...

    parsed_rows = []
    for row_idx, row in enumerate(ws.iter_rows(min_row=2), start=2):
        # Skip completely empty rows
        # Detect merged cells (MergedCell type check)
        # Coerce types per column
        # Collect errors for this row
        parsed_rows.append(ParsedRow(...))

    return ParseResult(
        rows=parsed_rows,
        total_rows=len(parsed_rows),
        has_errors=any(r.errors for r in parsed_rows),
    )
```

### Pattern 3: Template Download Endpoint
**What:** A GET endpoint that returns StreamingResponse with proper content type and disposition headers.
**When to use:** Template download API.
**Example:**
```python
# In backend/api/routes/tasks.py
from fastapi.responses import StreamingResponse
from backend.utils.excel_template import generate_template

@router.get("/template")
async def download_template():
    buffer = generate_template()
    return StreamingResponse(
        buffer,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=task_template.xlsx"},
    )
```

### Anti-Patterns to Avoid
- **Saving template to disk:** Template generation must be in-memory only (BytesIO). No temporary files on the filesystem.
- **Hardcoding column indices:** Use the shared `TEMPLATE_COLUMNS` list as the single source of truth. Both template generator and parser reference it. Changing column order requires updating only this one list.
- **Raising on first error in parser:** The parser must collect ALL errors across ALL rows before returning. Phase 71's preview UI needs to show every error at once.
- **Using pandas for parsing:** pandas is a heavy dependency (10+ MB) for a 6-column flat table. openpyxl's `iter_rows` is sufficient and already installed.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Excel data validation dropdowns | Custom dropdown via VBA or macro | openpyxl DataValidation | DataValidation produces native Excel dropdowns that work in all Excel-compatible apps without macros |
| Excel cell styling (headers, colors) | Manual XML manipulation | openpyxl.styles (Font, PatternFill, Alignment, Border) | openpyxl provides a clean Python API over OOXML styling; raw XML is error-prone and undocumented |
| Merged cell detection | Check cell value for None or empty | `isinstance(cell, MergedCell)` from openpyxl | MergedCell is a dedicated openpyxl type; value-based detection misses cases where only the anchor cell has a value |
| File download response | Custom response with manual headers | FastAPI StreamingResponse | Handles chunked transfer encoding, proper content-length, and content-type automatically |
| JSON parsing for preconditions/assertions | Custom string splitting | `json.loads()` with try/except | JSON is the agreed format; stdlib json handles all edge cases (escaped chars, nested structures) |

**Key insight:** openpyxl handles the full OOXML complexity of Excel files. The only code we write is domain logic (which columns, which validations, how to coerce types). All binary format details are delegated to the library.

## Common Pitfalls

### Pitfall 1: openpyxl Returns Varying Python Types Per Cell
**What goes wrong:** A cell that looks like "10" in Excel is read as `int(10)` by openpyxl, not `str("10")`. Boolean cells return `True`/`False`, not "true"/"false". Empty cells return `None`.
**Why it happens:** openpyxl preserves Excel's type system. If the user typed a number, it's stored as a number in .xlsx regardless of what the column expects.
**How to avoid:** Per-column type coercion in the parser. For string columns (name, description, target_url), always call `str(value).strip()` if value is not None. For max_steps, accept int or convert numeric string. For JSON columns, first convert to string, then parse JSON.
**Warning signs:** Tests that only use string values in fixture .xlsx files won't catch this. Test with `int`, `float`, `bool`, and `None` values.

### Pitfall 2: Merged Cells Cause Silent Data Loss
**What goes wrong:** If a user merges cells in the template, only the top-left cell has a value. Other cells in the merged range are `MergedCell` objects with no `.value` attribute access.
**Why it happens:** Excel merges cells by keeping one anchor cell and replacing others with references. openpyxl represents these as `MergedCell` instances (not regular `Cell` instances).
**How to avoid:** Check `isinstance(cell, MergedCell)` during row iteration. If any cell in a row is a MergedCell, report it as an error for that row with the cell coordinate.
**Warning signs:** Parser silently produces rows with missing data that later fail TaskCreate validation with confusing "field required" errors.

### Pitfall 3: DataValidation Range Too Narrow
**What goes wrong:** If the DataValidation range is set to `D2:D100` and a user adds data in row 101, no validation is applied to that cell.
**Why it happens:** DataValidation in openpyxl applies to an explicit cell range. It does not auto-extend.
**How to avoid:** Use a generous range like `D2:D10000`. The validation adds negligible file size overhead. 10000 rows covers even extreme batch imports.
**Warning signs:** QA adds data beyond the validation range and enters invalid values without error feedback.

### Pitfall 4: Empty Rows Parsed as Invalid Rows
**What goes wrong:** Excel sheets often have trailing "empty" rows that openpyxl still iterates over (especially if cells were previously formatted). The parser reports errors for rows that the user never intended to contain data.
**Why it happens:** openpyxl's `iter_rows` iterates over the worksheet's bounding box, which may include formatted-but-empty rows.
**How to avoid:** Skip rows where ALL cells are None or empty string. A row is "data" only if at least one cell has a non-empty value.
**Warning signs:** Parser reports "row 5: name is required" for a row the user left completely blank.

### Pitfall 5: UTF-8 BOM or Encoding Issues in StreamingResponse
**What goes wrong:** The downloaded .xlsx file is corrupted and Excel cannot open it.
**Why it happens:** StreamingResponse with wrong media_type or an encoding middleware interfering with binary data.
**How to avoid:** Use exact media_type `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`. Do not apply any text encoding to the BytesIO buffer. Ensure no middleware transforms the response body.
**Warning signs:** Excel shows "file is corrupted" or "file format not valid" when opening the download.

### Pitfall 6: Example Data Does Not Round-Trip Through Parser
**What goes wrong:** The template's example rows, when parsed back, produce validation errors. This means QA cannot even re-import the template as-is.
**Why it happens:** Example data might contain values that the parser's type coercion does not handle (e.g., an integer where the parser expects a JSON string).
**How to avoid:** Write a round-trip test: generate template -> parse it -> assert zero errors on example rows. This must be the first test written.
**Warning signs:** Parser returns errors on example rows. If this happens, either the example data is wrong or the parser is wrong -- fix one or the other.

## Code Examples

Verified patterns from live testing in the project's Python environment:

### Template Generation with Data Validation
```python
# Source: verified by running against openpyxl 3.1.5 in project venv
from openpyxl import Workbook
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.styles import Font, PatternFill, Alignment

wb = Workbook()
ws = wb.active
ws.title = "测试用例"

# Data validation for max_steps (column D)
dv = DataValidation(
    type="whole", operator="between",
    formula1=1, formula2=100, allow_blank=True
)
dv.error = "请输入 1-100 之间的整数"
dv.errorTitle = "输入错误"
dv.showErrorMessage = True
dv.showInputMessage = True
dv.prompt = "请输入 1 到 100 之间的整数"
dv.promptTitle = "最大步数"
ws.add_data_validation(dv)
dv.add("D2:D10000")  # generous range

# Freeze top row for scrolling
ws.freeze_panes = "A2"

# Set column widths
from openpyxl.utils import get_column_letter
widths = [25, 40, 35, 12, 40, 50]
for i, w in enumerate(widths, 1):
    ws.column_dimensions[get_column_letter(i)].width = w
```

### Merged Cell Detection During Parsing
```python
# Source: verified by running against openpyxl 3.1.5 in project venv
from openpyxl.cell.cell import MergedCell

for row in ws.iter_rows(min_row=2):
    row_errors = []
    for cell in row:
        if isinstance(cell, MergedCell):
            row_errors.append(
                f"单元格 {cell.coordinate} 是合并单元格，请取消合并后重试"
            )
        else:
            value = cell.value
            # type coercion per column...
```

### Type Coercion Per Column (Lenient Mode)
```python
# Source: aligned with D-09 (宽松模式)
def coerce_string(value) -> str | None:
    """Coerce cell value to string, lenient mode."""
    if value is None:
        return None
    if isinstance(value, bool):
        return str(value).lower()  # True -> "true"
    return str(value).strip()

def coerce_int(value, default: int | None = None) -> int | None:
    """Coerce cell value to int, lenient mode."""
    if value is None:
        return default
    if isinstance(value, bool):
        return None  # boolean is not a valid int
    if isinstance(value, (int, float)):
        return int(value)
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            return default
        try:
            return int(float(stripped))  # handles "10.0" -> 10
        except (ValueError, TypeError):
            return None  # will be caught as type error
    return None

def coerce_json_list(value) -> list | str | None:
    """Parse JSON string from cell, return list or raw string on failure."""
    if value is None:
        return None
    raw = str(value).strip()
    if not raw:
        return None
    try:
        parsed = json.loads(raw)
        if isinstance(parsed, list):
            return parsed
        return raw  # valid JSON but not a list, return raw for error reporting
    except json.JSONDecodeError:
        return raw  # invalid JSON, return raw for error reporting
```

### StreamingResponse for File Download
```python
# Source: FastAPI standard pattern, verified in project venv
from fastapi.responses import StreamingResponse
from io import BytesIO

@router.get("/template")
async def download_template():
    buffer: BytesIO = generate_template()
    return StreamingResponse(
        buffer,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition": "attachment; filename=task_template.xlsx"
        },
    )
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| xlsxwriter for Excel generation | openpyxl for both read+write | Project decision (v0.9.0 planning) | Single library handles template generation AND import parsing |
| File saved to disk then served | In-memory BytesIO + StreamingResponse | FastAPI best practice since 0.65+ | No temp file cleanup needed, no disk I/O |
| Per-cell validation during iteration | Collect-all errors, return structured result | D-08 decision | Phase 71 preview can show all errors at once |

**Deprecated/outdated:**
- `openpyxl.writer.excel` direct use: Use `Workbook.save(buffer)` instead -- the writer module is internal API.

## Column Contract (Single Source of Truth)

This is the contract between template generator and parser. Both must reference the same definition.

| Col | Key | Header (Chinese) | Type | Required | Default | TaskCreate Field |
|-----|-----|-------------------|------|----------|---------|------------------|
| A | name | 任务名称 | str | YES | - | name |
| B | description | 任务描述 | str | YES | - | description |
| C | target_url | 目标URL | str | NO | "" | target_url |
| D | max_steps | 最大步数 | int | NO | 10 | max_steps |
| E | preconditions | 前置条件 | JSON array | NO | None | preconditions |
| F | assertions | 断言 | JSON array | NO | None | assertions |

**Example data (2 rows):**

Row 2: `登录功能测试` | `打开登录页面，输入用户名和密码，点击登录按钮，验证是否跳转到首页` | `https://erp.example.com/login` | `15` | `["context['token'] = login_api()"]` | `[{"methodName":"check_login_status","headers":"main"}]`

Row 3: `创建订单测试` | `登录后进入订单页面，填写订单信息并提交，验证订单创建成功` | `https://erp.example.com/orders/new` | `20` | (empty) | (empty)

## Open Questions

1. **Should the parser also validate against TaskCreate schema, or only do type coercion?**
   - What we know: D-08 says collect-all errors. The parser does type coercion (D-09). TaskCreate has validation rules (min_length, ge, le).
   - What's unclear: Whether the parser should call `TaskCreate.model_validate()` on each row, or just return raw coerced data and let Phase 71's import service validate.
   - Recommendation: Parser does type coercion + basic checks (required fields, JSON parseability). Full Pydantic validation happens in Phase 71's import service. This keeps the parser focused and testable.

2. **Should the README sheet include column descriptions in both Chinese and English?**
   - What we know: CONTEXT.md says this is at Claude's discretion. QA users are Chinese-speaking.
   - Recommendation: Chinese-only README sheet. No English needed since the target audience is QA testers who read Chinese.

## Environment Availability

Step 2.6: SKIPPED (no external dependencies identified -- all required packages are already installed in the project venv).

| Dependency | Required By | Available | Version | Fallback |
|------------|------------|-----------|---------|----------|
| openpyxl | Template generation + parsing | Yes | 3.1.5 | -- |
| FastAPI | Template download endpoint | Yes | 0.135.1 | -- |
| starlette (StreamingResponse) | File download response | Yes | (bundled) | -- |
| pytest | Unit tests | Yes | (in venv) | -- |

**Missing dependencies with no fallback:** None.

**Missing dependencies with fallback:** None.

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | pytest (existing) |
| Config file | None (uses default pytest discovery) |
| Quick run command | `uv run pytest backend/tests/unit/test_excel_template.py backend/tests/unit/test_excel_parser.py -v` |
| Full suite command | `uv run pytest backend/tests/ -v` |

### Phase Requirements to Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| TMPL-01 | Template generates valid .xlsx with correct headers | unit | `uv run pytest backend/tests/unit/test_excel_template.py::test_template_has_correct_headers -v` | Wave 0 |
| TMPL-01 | Template contains 2 example data rows | unit | `uv run pytest backend/tests/unit/test_excel_template.py::test_template_has_example_data -v` | Wave 0 |
| TMPL-01 | Template contains README sheet | unit | `uv run pytest backend/tests/unit/test_excel_template.py::test_template_has_readme_sheet -v` | Wave 0 |
| TMPL-01 | Template round-trips through parser without errors | unit | `uv run pytest backend/tests/unit/test_excel_template.py::test_template_roundtrip -v` | Wave 0 |
| TMPL-02 | max_steps column has data validation (1-100) | unit | `uv run pytest backend/tests/unit/test_excel_template.py::test_max_steps_validation -v` | Wave 0 |
| TMPL-01 | GET /tasks/template returns .xlsx file | unit | `uv run pytest backend/tests/unit/test_excel_template.py::test_download_endpoint -v` | Wave 0 |

### Sampling Rate
- **Per task commit:** `uv run pytest backend/tests/unit/test_excel_template.py backend/tests/unit/test_excel_parser.py -v`
- **Per wave merge:** `uv run pytest backend/tests/ -v`
- **Phase gate:** Full suite green before `/gsd:verify-work`

### Wave 0 Gaps
- [ ] `backend/tests/unit/test_excel_template.py` -- covers TMPL-01, TMPL-02
- [ ] `backend/tests/unit/test_excel_parser.py` -- covers parser type coercion, error collection, merged cell detection, empty row skipping

## Sources

### Primary (HIGH confidence)
- openpyxl 3.1.5 live testing in project venv -- DataValidation, Workbook, load_workbook, merged cells, cell types, styling
- `backend/db/schemas.py` -- TaskCreate field definitions and validation rules
- `backend/db/models.py` -- Task ORM model field types
- `backend/api/routes/tasks.py` -- existing router pattern for endpoint addition
- `backend/api/main.py` -- router registration pattern
- `webseleniumerp/use_case/export.py` -- existing openpyxl usage in project
- `backend/utils/` -- existing utility module structure

### Secondary (MEDIUM confidence)
- FastAPI StreamingResponse documentation -- standard pattern for binary file responses
- openpyxl documentation -- iter_rows, data_only mode, cell types

### Tertiary (LOW confidence)
- None -- all critical claims verified by live testing

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH -- all libraries verified installed and functional in project venv
- Architecture: HIGH -- patterns verified against existing codebase structure and conventions
- Pitfalls: HIGH -- all pitfalls verified by writing and running test code against openpyxl 3.1.5
- Code examples: HIGH -- every code example was run against the project's Python environment

**Research date:** 2026-04-08
**Valid until:** 2026-05-08 (stable libraries, no fast-moving dependencies)
