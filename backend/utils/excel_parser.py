"""Excel file parser for test case import.

Parses .xlsx files into structured ParsedRow objects with collect-all error
handling. Uses TEMPLATE_COLUMNS from excel_template as column contract.
"""

from dataclasses import dataclass, field
from typing import Any

from io import BytesIO
import json

from openpyxl import load_workbook
from openpyxl.cell.cell import MergedCell

from backend.utils.excel_template import TEMPLATE_COLUMNS


@dataclass(frozen=True)
class ParsedRow:
    """A single parsed row with data and any errors."""

    row_number: int
    data: dict[str, Any]
    errors: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class ParseResult:
    """Result of parsing an Excel workbook."""

    rows: list[ParsedRow]
    total_rows: int
    has_errors: bool


def _coerce_string(value: Any) -> str | None:
    """Coerce cell value to string. Returns None for empty cells."""
    if value is None:
        return None
    if isinstance(value, bool):
        return str(value).lower()
    return str(value).strip()


def _coerce_int(value: Any, default: int | None = None) -> int | None:
    """Coerce cell value to int. Returns default for empty cells."""
    if value is None:
        return default
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return int(value)
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            return default
        try:
            return int(float(stripped))
        except (ValueError, TypeError):
            return None
    return None


def _coerce_json_list(value: Any) -> tuple[list | None, str | None]:
    """Parse JSON array from cell. Returns (parsed_list_or_None, error_or_None)."""
    if value is None:
        return None, None
    raw = str(value).strip()
    if not raw:
        return None, None
    try:
        parsed = json.loads(raw)
        if isinstance(parsed, list):
            return parsed, None
        return None, f"JSON 值不是数组: {raw[:50]}"
    except json.JSONDecodeError:
        return None, f"JSON 格式错误: {raw[:50]}"


def _is_empty_row(cells: tuple) -> bool:
    """Check if all cells in a row are None (never entered by user).

    Rows where the user typed something (even an empty string) are NOT
    considered empty -- they should be parsed so required-field validation
    can report errors.
    """
    for cell in cells:
        if cell is None:
            continue
        if isinstance(cell, MergedCell):
            # MergedCell means the row has content (user merged cells)
            return False
        if cell.value is not None:
            return False
    return True


def _has_merged_cells(cells: tuple) -> bool:
    """Check if any cell in the row is a MergedCell."""
    return any(isinstance(cell, MergedCell) for cell in cells)


def _validate_headers(ws) -> list[str] | None:
    """Validate that row 1 headers match TEMPLATE_COLUMNS.

    Returns list of error strings if mismatch, None if headers are valid.
    """
    expected_headers = [col["header"] for col in TEMPLATE_COLUMNS]
    errors = []

    for idx, expected in enumerate(expected_headers):
        actual = ws.cell(row=1, column=idx + 1).value
        if actual is None or str(actual).strip() != expected:
            errors.append(
                f"列 {idx + 1} 表头应为 '{expected}'，实际为 '{actual}'"
            )

    extra_cols = ws.max_column - len(expected_headers)
    if extra_cols > 0:
        errors.append(f"多余列: 发现 {ws.max_column} 列，预期 {len(expected_headers)} 列")

    return errors if errors else None


def parse_excel(buffer: BytesIO) -> ParseResult:
    """Parse an .xlsx workbook into structured row data.

    Uses collect-all strategy: collects all errors across all rows without
    raising on individual row errors. Only fatal errors (unopenable file)
    raise exceptions.

    Args:
        buffer: BytesIO containing .xlsx file data.

    Returns:
        ParseResult with all parsed rows, total count, and error flag.
    """
    wb = load_workbook(buffer, data_only=True)
    ws = wb.active

    # Validate headers
    header_errors = _validate_headers(ws)
    if header_errors is not None:
        return ParseResult(
            rows=[
                ParsedRow(
                    row_number=0,
                    data={},
                    errors=header_errors,
                )
            ],
            total_rows=1,
            has_errors=True,
        )

    parsed_rows: list[ParsedRow] = []

    for row_tuple in ws.iter_rows(min_row=2):
        # Skip completely empty rows
        if _is_empty_row(row_tuple):
            continue

        row_number = row_tuple[0].row if row_tuple else 0
        row_errors: list[str] = []

        # Check for merged cells
        if _has_merged_cells(row_tuple):
            row_errors.append("第 {} 行包含合并单元格，请取消合并后重新上传".format(row_number))

        # Build data dict from columns
        data: dict[str, Any] = {}

        for col_idx, col_def in enumerate(TEMPLATE_COLUMNS):
            key = col_def["key"]
            cell_value = None

            if col_idx < len(row_tuple):
                cell = row_tuple[col_idx]
                if not isinstance(cell, MergedCell):
                    cell_value = cell.value

            if key in ("name", "description", "target_url"):
                coerced = _coerce_string(cell_value)
                # target_url has empty string default, others None
                if key == "target_url" and coerced is None:
                    data[key] = col_def.get("default", "")
                else:
                    data[key] = coerced if coerced is not None else (col_def.get("default") or None)

            elif key == "max_steps":
                coerced = _coerce_int(cell_value, default=col_def.get("default", 10))
                if coerced is None and cell_value is not None and str(cell_value).strip() != "":
                    row_errors.append("最大步数必须为 1-100 之间的整数")
                    data[key] = col_def.get("default", 10)
                else:
                    data[key] = coerced

            elif key in ("preconditions", "assertions"):
                parsed_list, json_error = _coerce_json_list(cell_value)
                data[key] = parsed_list
                if json_error is not None:
                    col_header = col_def["header"]
                    row_errors.append(f"{col_header}: {json_error}")
                    # Store raw string for UI to display
                    data[key] = str(cell_value).strip() if cell_value is not None else None

        # Check required fields
        for col_def in TEMPLATE_COLUMNS:
            if col_def["required"]:
                key = col_def["key"]
                header = col_def["header"]
                val = data.get(key)
                if val is None or (isinstance(val, str) and val.strip() == ""):
                    row_errors.append(f"必填字段 '{header}' 不能为空")

        parsed_rows.append(
            ParsedRow(
                row_number=row_number,
                data=data,
                errors=row_errors,
            )
        )

    has_errors = any(row.errors for row in parsed_rows)
    return ParseResult(
        rows=parsed_rows,
        total_rows=len(parsed_rows),
        has_errors=has_errors,
    )
