# Excel 模版动态数据填充 Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 在前置条件阶段支持从 ERP API 获取数据并填充 Excel 模版，生成文件路径供 agent 上传。

**Architecture:** 在 `ContextWrapper` 中新增 `fill_excel()` 和 `get_excel_path()` 两个方法。前置条件代码调用 `context.get_data()` 获取数据，调用 `context.fill_excel()` 写入模版副本的指定单元格，调用 `context.get_excel_path()` 获取填充后文件路径存入变量。pipeline 通过 `run_id` 传入 `ContextWrapper`，用于隔离不同 run 的填充文件。

**Tech Stack:** Python, openpyxl, Pydantic, FastAPI, Jinja2

---

### Task 1: Settings 新增模版目录配置 + .gitignore 更新

**Files:**
- Modify: `backend/config/settings.py:59` (在 database_url 后添加)
- Modify: `.gitignore:278` (在 outputs/ 后添加)

**Step 1: 在 settings.py 添加 templates_dir 配置**

在 `database_url` 字段之后添加：

```python
    # Excel template directory for dynamic data filling
    templates_dir: str = "data/templates"
    # Filled Excel output directory (runtime, per-run subdirs)
    filled_dir: str = "data/filled"
```

**Step 2: 在 .gitignore 中添加 data/filled/ 忽略**

在 `outputs/` 行之后添加：

```
data/filled/
```

**Step 3: 创建 data/templates 目录并放入 .gitkeep**

```bash
mkdir -p data/templates data/filled
touch data/templates/.gitkeep
```

**Step 4: Commit**

```bash
git add backend/config/settings.py .gitignore data/templates/.gitkeep
git commit -m "feat: add templates_dir and filled_dir config for Excel template filling"
```

---

### Task 2: ExcelFillService 核心模块

**Files:**
- Create: `backend/core/excel_fill_service.py`
- Test: `backend/tests/test_excel_fill_service.py`

**Step 1: 写测试文件**

```python
"""Tests for ExcelFillService."""
import pytest
from pathlib import Path
from openpyxl import Workbook

from backend.core.excel_fill_service import ExcelFillService


@pytest.fixture
def template_dir(tmp_path):
    """Create a template directory with a sample Excel file."""
    templates = tmp_path / "templates"
    templates.mkdir()
    wb = Workbook()
    ws = wb.active
    ws.title = "Sheet1"
    ws.cell(row=1, column=1, value="IMEI")
    ws.cell(row=1, column=2, value="物品编号")
    wb.save(templates / "test_template.xlsx")
    return templates


@pytest.fixture
def output_dir(tmp_path):
    """Create an output directory for filled files."""
    out = tmp_path / "filled"
    out.mkdir()
    return out


@pytest.fixture
def service(template_dir, output_dir):
    return ExcelFillService(
        templates_dir=str(template_dir),
        filled_dir=str(output_dir),
        run_id="test_run_001",
    )


class TestFillExcel:
    def test_fill_single_cell(self, service, template_dir, output_dir):
        """Fill a single cell and verify the output file."""
        result = service.fill_excel("test_template", row=2, col=1, value="IMEI123456")
        assert result is service  # returns self for chaining

        path = service.get_excel_path("test_template")
        assert path.exists()

        from openpyxl import load_workbook
        wb = load_workbook(path)
        ws = wb["Sheet1"]
        assert ws.cell(row=2, column=1).value == "IMEI123456"
        # Original template should be unchanged
        orig = load_workbook(template_dir / "test_template.xlsx")
        assert orig["Sheet1"].cell(row=2, column=1).value is None

    def test_fill_multiple_cells_same_template(self, service):
        """Multiple fill calls on same template operate on the same copy."""
        service.fill_excel("test_template", row=2, col=1, value="AAA")
        service.fill_excel("test_template", row=2, col=2, value="BBB")

        from openpyxl import load_workbook
        wb = load_workbook(service.get_excel_path("test_template"))
        ws = wb["Sheet1"]
        assert ws.cell(row=2, column=1).value == "AAA"
        assert ws.cell(row=2, column=2).value == "BBB"

    def test_fill_nonexistent_template_raises(self, service):
        """Raises FileNotFoundError when template doesn't exist."""
        with pytest.raises(FileNotFoundError, match="not_found"):
            service.fill_excel("not_found", row=1, col=1, value="x")

    def test_get_path_before_fill_returns_original(self, service, template_dir):
        """get_excel_path before any fill returns the original template."""
        path = service.get_excel_path("test_template")
        assert path == template_dir / "test_template.xlsx"

    def test_fill_creates_run_subdirectory(self, service, output_dir):
        """Filled file goes into {filled_dir}/{run_id}/ subdirectory."""
        service.fill_excel("test_template", row=1, col=1, value="x")
        expected_dir = output_dir / "test_run_001"
        assert expected_dir.exists()
        assert (expected_dir / "test_template.xlsx").exists()

    def test_fill_with_sheet_name(self, service, template_dir):
        """Can target a specific sheet."""
        from openpyxl import Workbook, load_workbook
        wb = load_workbook(template_dir / "test_template.xlsx")
        wb.create_sheet("CustomSheet")
        wb.save(template_dir / "test_template.xlsx")

        service.fill_excel("test_template", sheet="CustomSheet", row=1, col=1, value="v")
        wb2 = load_workbook(service.get_excel_path("test_template"))
        assert wb2["CustomSheet"].cell(row=1, column=1).value == "v"

    def test_different_runs_isolated(self, template_dir, output_dir):
        """Two runs with different run_ids get independent copies."""
        svc1 = ExcelFillService(str(template_dir), str(output_dir), "run_A")
        svc2 = ExcelFillService(str(template_dir), str(output_dir), "run_B")

        svc1.fill_excel("test_template", row=2, col=1, value="RUN_A")
        svc2.fill_excel("test_template", row=2, col=1, value="RUN_B")

        from openpyxl import load_workbook
        wb1 = load_workbook(svc1.get_excel_path("test_template"))
        wb2 = load_workbook(svc2.get_excel_path("test_template"))
        assert wb1["Sheet1"].cell(row=2, column=1).value == "RUN_A"
        assert wb2["Sheet1"].cell(row=2, column=1).value == "RUN_B"
```

**Step 2: 运行测试确认失败**

```bash
uv run pytest backend/tests/test_excel_fill_service.py -v
```

预期: FAIL — `ModuleNotFoundError: No module named 'backend.core.excel_fill_service'`

**Step 3: 实现 ExcelFillService**

创建 `backend/core/excel_fill_service.py`:

```python
"""Excel template filling service for precondition data injection."""

import logging
import shutil
from pathlib import Path

from openpyxl import load_workbook

logger = logging.getLogger(__name__)


class ExcelFillService:
    """Manages Excel template copying and cell filling for a single run.

    Each run gets its own subdirectory under filled_dir.
    Templates are copied on first fill and reused for subsequent fills.
    """

    def __init__(self, templates_dir: str, filled_dir: str, run_id: str):
        self._templates_dir = Path(templates_dir)
        self._filled_dir = Path(filled_dir)
        self._run_id = run_id
        self._run_dir = self._filled_dir / run_id
        # Track which templates have been copied to avoid re-copying
        self._copied: set[str] = set()

    def _template_path(self, template_name: str) -> Path:
        """Resolve the full path to a template .xlsx file."""
        return self._templates_dir / f"{template_name}.xlsx"

    def _filled_path(self, template_name: str) -> Path:
        """Resolve the full path to the filled copy."""
        return self._run_dir / f"{template_name}.xlsx"

    def _ensure_copy(self, template_name: str) -> Path:
        """Copy template to run dir if not already done. Returns filled path."""
        if template_name not in self._copied:
            src = self._template_path(template_name)
            if not src.exists():
                raise FileNotFoundError(
                    f"Excel template not found: {src}"
                )
            self._run_dir.mkdir(parents=True, exist_ok=True)
            dst = self._filled_path(template_name)
            shutil.copy2(src, dst)
            self._copied.add(template_name)
            logger.info(f"Copied template '{template_name}' to {dst}")
        return self._filled_path(template_name)

    def fill_excel(
        self,
        template_name: str,
        sheet: str = "Sheet1",
        row: int = 2,
        col: int = 1,
        value: str | int | float | None = None,
    ) -> "ExcelFillService":
        """Fill a cell in an Excel template copy.

        Args:
            template_name: Template filename without .xlsx extension.
            sheet: Sheet name (default 'Sheet1').
            row: Row number (1-based).
            col: Column number (1-based).
            value: Value to write.

        Returns:
            self for chaining.

        Raises:
            FileNotFoundError: If template doesn't exist.
        """
        path = self._ensure_copy(template_name)
        wb = load_workbook(path)
        ws = wb[sheet]
        ws.cell(row=row, column=col, value=value)
        wb.save(path)
        logger.info(f"Filled {template_name} [{sheet}] ({row},{col}) = {value}")
        return self

    def get_excel_path(self, template_name: str) -> Path:
        """Get the absolute path to a filled Excel file.

        If fill_excel hasn't been called yet, returns the original template path.
        """
        if template_name in self._copied:
            return self._filled_path(template_name).resolve()
        return self._template_path(template_name).resolve()
```

**Step 4: 运行测试确认通过**

```bash
uv run pytest backend/tests/test_excel_fill_service.py -v
```

预期: 全部 PASS

**Step 5: Commit**

```bash
git add backend/core/excel_fill_service.py backend/tests/test_excel_fill_service.py
git commit -m "feat: add ExcelFillService for template copying and cell filling"
```

---

### Task 3: 将 ExcelFillService 集成到 ContextWrapper

**Files:**
- Modify: `backend/core/precondition_service.py:63-140` (ContextWrapper 类)
- Test: `backend/tests/test_excel_fill_service.py` (追加集成测试)

**Step 1: 修改 ContextWrapper.__init__ 接受 run_id**

`precondition_service.py` 第 71 行，修改 `__init__`:

```python
    def __init__(self, *, cache: CacheService | None = None, run_id: str | None = None):
        self._data: dict[str, Any] = {}
        self._cache = cache or CacheService()
        self._run_id = run_id
        self._excel_service: ExcelFillService | None = None
        self._assertion_count = 0
        self._assertion_summary = {
            "total": 0,
            "passed": 0,
            "failed": 0,
            "errors": 0
        }
```

**Step 2: 添加 import 和新方法**

在文件顶部 import 区添加：

```python
from backend.core.excel_fill_service import ExcelFillService
```

在 `ContextWrapper` 类中，`get_data` 方法之后（约第 119 行后）添加：

```python
    def _get_excel_service(self) -> ExcelFillService:
        """Lazily create ExcelFillService on first use."""
        if self._excel_service is None:
            if not self._run_id:
                raise RuntimeError(
                    "Excel filling requires a run_id. "
                    "Ensure the pipeline passes run_id to ContextWrapper."
                )
            from backend.config.settings import get_settings
            settings = get_settings()
            self._excel_service = ExcelFillService(
                templates_dir=settings.templates_dir,
                filled_dir=settings.filled_dir,
                run_id=self._run_id,
            )
        return self._excel_service

    def fill_excel(
        self,
        template_name: str,
        sheet: str = "Sheet1",
        row: int = 2,
        col: int = 1,
        value: str | int | float | None = None,
    ) -> "ContextWrapper":
        """Fill a cell in an Excel template copy.

        Copies the template to a run-specific directory on first call,
        then writes value to the specified cell.

        Args:
            template_name: Template filename without .xlsx extension.
            sheet: Sheet name (default 'Sheet1').
            row: Row number (1-based).
            col: Column number (1-based).
            value: Value to write.

        Returns:
            self for chaining.
        """
        svc = self._get_excel_service()
        svc.fill_excel(template_name, sheet, row, col, value)
        return self

    def get_excel_path(self, template_name: str) -> str:
        """Get the absolute path to a filled Excel file as string.

        If fill_excel hasn't been called for this template yet,
        returns the original template path.

        Args:
            template_name: Template filename without .xlsx extension.

        Returns:
            Absolute file path as string.
        """
        svc = self._get_excel_service()
        return str(svc.get_excel_path(template_name))
```

**Step 3: 运行测试确认通过**

```bash
uv run pytest backend/tests/test_excel_fill_service.py -v
```

**Step 4: Commit**

```bash
git add backend/core/precondition_service.py
git commit -m "feat: integrate ExcelFillService into ContextWrapper"
```

---

### Task 4: Pipeline 传入 run_id 到 ContextWrapper

**Files:**
- Modify: `backend/api/routes/run_pipeline.py:91` (PreconditionService 构造)
- Modify: `backend/core/precondition_service.py:212-220` (PreconditionService.__init__)

**Step 1: 修改 PreconditionService.__init__ 接受 run_id**

`precondition_service.py` 第 212 行，修改为：

```python
    def __init__(
        self,
        external_module_path: str | None = None,
        *,
        cache: CacheService | None = None,
        run_id: str | None = None,
    ):
        self.external_module_path = external_module_path
        self.context: ContextWrapper = ContextWrapper(cache=cache, run_id=run_id)
```

**Step 2: 在 pipeline 中传入 run_id**

`run_pipeline.py` 第 91 行，修改为：

```python
    precondition_service = PreconditionService(
        external_module_path=external_module_path, cache=shared_cache, run_id=run_id
    )
```

**Step 3: 运行全部后端测试确认无回归**

```bash
uv run pytest backend/tests/ -v
```

**Step 4: Commit**

```bash
git add backend/core/precondition_service.py backend/api/routes/run_pipeline.py
git commit -m "feat: pass run_id through pipeline to ContextWrapper for Excel isolation"
```

---

### Task 5: 端到端集成测试

**Files:**
- Create: `backend/tests/test_excel_fill_e2e.py`

**Step 1: 写端到端测试**

模拟完整的 pipeline 场景：前置条件获取数据 → 填充模版 → 变量替换 → 验证文件存在。

```python
"""End-to-end tests for Excel template filling in precondition pipeline."""

import pytest
from pathlib import Path
from openpyxl import Workbook

from backend.core.precondition_service import PreconditionService


@pytest.fixture
def template_dir(tmp_path):
    """Create template directory with sample files."""
    td = tmp_path / "templates"
    td.mkdir()
    for name in ["purchase_order", "inventory_transfer"]:
        wb = Workbook()
        ws = wb.active
        ws.title = "Sheet1"
        ws.cell(row=1, column=1, value="IMEI")
        ws.cell(row=1, column=2, value="物品编号")
        wb.save(td / f"{name}.xlsx")
    return td


@pytest.fixture
def filled_dir(tmp_path):
    fd = tmp_path / "filled"
    fd.mkdir()
    return fd


@pytest.fixture
def env_vars(template_dir, filled_dir, monkeypatch):
    """Set environment variables for settings."""
    monkeypatch.setenv("TEMPLATES_DIR", str(template_dir))
    monkeypatch.setenv("FILLED_DIR", str(filled_dir))


class TestPreconditionExcelFill:
    def test_fill_and_get_path(self, env_vars, monkeypatch):
        """Precondition fills Excel and stores path in context."""
        monkeypatch.setenv("TEMPLATES_DIR", str(Path(__file__).parent.parent.parent / "data" / "templates"))
        monkeypatch.setenv("FILLED_DIR", str(Path(__file__).parent / "tmp_filled"))

        svc = PreconditionService(run_id="e2e_test_001")

        code = """
context['test_value'] = 'IMEI999'
context.fill_excel('purchase_order', row=2, col=1, value='IMEI999')
context['excel_file'] = context.get_excel_path('purchase_order')
"""
        import asyncio
        result = asyncio.run(svc.execute_single(code, 0))
        assert result.success, f"Precondition failed: {result.error}"

        ctx = svc.get_context()
        assert ctx['test_value'] == 'IMEI999'
        assert 'excel_file' in ctx
        assert 'purchase_order.xlsx' in ctx['excel_file']

        # Verify the file exists and has correct content
        from openpyxl import load_workbook
        wb = load_workbook(ctx['excel_file'])
        assert wb["Sheet1"].cell(row=2, column=1).value == 'IMEI999'

    def test_variable_substitution_with_excel_path(self, env_vars):
        """Task description {{excel_file}} gets replaced with actual path."""
        svc = PreconditionService(run_id="e2e_test_002")

        code = """
context.fill_excel('purchase_order', row=2, col=1, value='ABC123')
context['excel_file'] = context.get_excel_path('purchase_order')
"""
        import asyncio
        result = asyncio.run(svc.execute_single(code, 0))
        assert result.success

        ctx = svc.get_context()
        description = "请上传文件 {{excel_file}} 到采购入库页面"
        substituted = PreconditionService.substitute_variables(description, ctx)

        assert "{{excel_file}}" not in substituted
        assert ctx['excel_file'] in substituted
        assert substituted.startswith("请上传文件 ")

    def test_multiple_templates_in_one_task(self, env_vars):
        """One task uses multiple Excel templates."""
        svc = PreconditionService(run_id="e2e_test_003")

        code = """
context.fill_excel('purchase_order', row=2, col=1, value='A')
context['file_a'] = context.get_excel_path('purchase_order')
context.fill_excel('inventory_transfer', row=2, col=1, value='B')
context['file_b'] = context.get_excel_path('inventory_transfer')
"""
        import asyncio
        result = asyncio.run(svc.execute_single(code, 0))
        assert result.success

        ctx = svc.get_context()
        assert 'file_a' in ctx
        assert 'file_b' in ctx
        assert ctx['file_a'] != ctx['file_b']
        assert 'purchase_order' in ctx['file_a']
        assert 'inventory_transfer' in ctx['file_b']
```

**Step 2: 运行测试**

```bash
uv run pytest backend/tests/test_excel_fill_e2e.py -v
```

**Step 3: 运行全部后端测试确认无回归**

```bash
uv run pytest backend/tests/ -v
```

**Step 4: Commit**

```bash
git add backend/tests/test_excel_fill_e2e.py
git commit -m "test: add end-to-end tests for Excel template filling in preconditions"
```

---

### Task 6: 添加示例模版文件

**Files:**
- Create: `data/templates/new_purchase_order.xlsx`

**Step 1: 创建示例模版**

参考 `webseleniumerp` 的实际模版结构，创建 `new_purchase_order.xlsx`：
- Sheet1 表头: A1="IMEI", B1="物品编号", C1="备注"
- 第 2 行留空（由前置条件填充）

用 Python 脚本生成：

```bash
uv run python -c "
from openpyxl import Workbook
wb = Workbook()
ws = wb.active
ws['A1'] = 'IMEI'
ws['B1'] = '物品编号'
ws['C1'] = '备注'
wb.save('data/templates/new_purchase_order.xlsx')
print('Created data/templates/new_purchase_order.xlsx')
"
```

**Step 2: Commit**

```bash
git add data/templates/new_purchase_order.xlsx
git commit -m "feat: add sample Excel template for purchase order"
```

---

### Task 7: 清理临时测试文件并验证完整流程

**Step 1: 确认 .gitignore 生效**

```bash
git status
```

确认 `data/filled/` 不会出现在 untracked 中。

**Step 2: 运行全部测试**

```bash
uv run pytest backend/tests/ -v
```

**Step 3: 手动验证（可选）**

启动后端，在前端界面创建一个测试任务，前置条件写：

```python
items = context.get_data('PcImport', '库存管理|库存列表', i=2, j=13)
context.fill_excel('new_purchase_order', row=2, col=1, value=items[0]['imei'])
context['excel_file'] = context.get_excel_path('new_purchase_order')
```

任务描述写：

```
请上传文件 {{excel_file}} 到采购入库页面
```

验证 agent 能正确获取到文件路径并执行上传。
