"""ExcelParser unit tests.

Tests parse_excel() with type coercion, error collection, empty row skipping,
merged cell detection, required field validation, and template round-trip.
"""

import json
from io import BytesIO

import pytest
from openpyxl import Workbook

from backend.utils.excel_template import TEMPLATE_COLUMNS, generate_template
from backend.utils.excel_parser import ParsedRow, ParseResult, parse_excel


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_workbook(
    headers: list[str] | None = None,
    rows: list[list] | None = None,
) -> BytesIO:
    """Build a minimal .xlsx workbook for testing."""
    wb = Workbook()
    ws = wb.active
    ws.title = "测试用例"
    if headers is None:
        headers = [col["header"] for col in TEMPLATE_COLUMNS]
    ws.append(headers)
    if rows:
        for row in rows:
            ws.append(row)
    buf = BytesIO()
    wb.save(buf)
    buf.seek(0)
    return buf


def _default_headers() -> list[str]:
    return [col["header"] for col in TEMPLATE_COLUMNS]


# ---------------------------------------------------------------------------
# Task 1 core tests (TDD RED phase)
# ---------------------------------------------------------------------------


class TestParseExcelBasic:
    """Basic parsing: valid data rows, column keys, skip empty rows."""

    def test_valid_two_rows_returns_two_parsed_rows(self):
        buf = _make_workbook(rows=[
            ["Task A", "Description A", "https://a.com", 10, None, None],
            ["Task B", "Description B", "https://b.com", 20, None, None],
        ])
        result = parse_excel(buf)
        assert len(result.rows) == 2
        assert result.has_errors is False

    def test_parsed_row_data_keys_match_template_columns(self):
        buf = _make_workbook(rows=[
            ["Task A", "Description A", "", 10, None, None],
        ])
        result = parse_excel(buf)
        row = result.rows[0]
        expected_keys = {col["key"] for col in TEMPLATE_COLUMNS}
        assert set(row.data.keys()) == expected_keys

    def test_empty_rows_skipped(self):
        buf = _make_workbook(rows=[
            ["Task A", "Description A", "", 10, None, None],
            [None, None, None, None, None, None],  # completely empty
            ["Task C", "Description C", "", 15, None, None],
        ])
        result = parse_excel(buf)
        assert len(result.rows) == 2
        assert result.rows[0].data["name"] == "Task A"
        assert result.rows[1].data["name"] == "Task C"


class TestTypeCoercion:
    """Type coercion: strings, ints, defaults, floats."""

    def test_string_columns_coerced_from_number(self):
        """String columns (name, description, target_url) return strings."""
        buf = _make_workbook(rows=[
            [12345, "Description", "https://a.com", 10, None, None],
        ])
        result = parse_excel(buf)
        assert result.rows[0].data["name"] == "12345"
        assert isinstance(result.rows[0].data["name"], str)

    def test_max_steps_integer_cell_returns_int(self):
        buf = _make_workbook(rows=[
            ["Task", "Desc", "", 15, None, None],
        ])
        result = parse_excel(buf)
        assert result.rows[0].data["max_steps"] == 15
        assert isinstance(result.rows[0].data["max_steps"], int)

    def test_max_steps_empty_returns_default_10(self):
        buf = _make_workbook(rows=[
            ["Task", "Desc", "", None, None, None],
        ])
        result = parse_excel(buf)
        assert result.rows[0].data["max_steps"] == 10

    def test_max_steps_float_returns_int(self):
        buf = _make_workbook(rows=[
            ["Task", "Desc", "", 10.0, None, None],
        ])
        result = parse_excel(buf)
        assert result.rows[0].data["max_steps"] == 10
        assert isinstance(result.rows[0].data["max_steps"], int)


class TestJsonParsing:
    """JSON column parsing: preconditions and assertions."""

    def test_preconditions_valid_json_array(self):
        buf = _make_workbook(rows=[
            ["Task", "Desc", "", 10, '["code1", "code2"]', None],
        ])
        result = parse_excel(buf)
        assert result.rows[0].data["preconditions"] == ["code1", "code2"]
        assert result.rows[0].errors == []

    def test_preconditions_empty_returns_none(self):
        buf = _make_workbook(rows=[
            ["Task", "Desc", "", 10, None, None],
        ])
        result = parse_excel(buf)
        assert result.rows[0].data["preconditions"] is None
        assert result.rows[0].errors == []

    def test_preconditions_invalid_json_reports_error(self):
        buf = _make_workbook(rows=[
            ["Task", "Desc", "", 10, "not json at all", None],
        ])
        result = parse_excel(buf)
        assert len(result.rows[0].errors) == 1
        assert "JSON" in result.rows[0].errors[0]

    def test_assertions_valid_json_array(self):
        buf = _make_workbook(rows=[
            ["Task", "Desc", "", 10, None, '[{"methodName":"xxx","headers":"main"}]'],
        ])
        result = parse_excel(buf)
        assert result.rows[0].data["assertions"] == [{"methodName": "xxx", "headers": "main"}]
        assert result.rows[0].errors == []

    def test_assertions_non_array_json_reports_error(self):
        buf = _make_workbook(rows=[
            ["Task", "Desc", "", 10, None, '{"key": "val"}'],
        ])
        result = parse_excel(buf)
        assert len(result.rows[0].errors) == 1
        assert "数组" in result.rows[0].errors[0]


class TestErrorCollection:
    """Error collection: required fields, merged cells, collect-all."""

    def test_merged_cell_detected(self):
        wb = Workbook()
        ws = wb.active
        ws.title = "测试用例"
        ws.append(_default_headers())
        ws.append(["Task", "Desc", "", 10, None, None])
        # Row 3 has a merged cell
        ws.merge_cells("A3:B3")
        ws["A3"] = "Merged task"
        ws["C3"] = ""
        ws["D3"] = 10
        ws["E3"] = None
        ws["F3"] = None
        buf = BytesIO()
        wb.save(buf)
        buf.seek(0)
        result = parse_excel(buf)
        assert len(result.rows) == 2
        merged_row = result.rows[1]
        assert any("合并单元格" in err for err in merged_row.errors)

    def test_missing_required_field_reports_error(self):
        buf = _make_workbook(rows=[
            ["", "Description", "", 10, None, None],  # name empty
        ])
        result = parse_excel(buf)
        assert len(result.rows[0].errors) >= 1
        assert any("任务名称" in err for err in result.rows[0].errors)

    def test_multiple_errors_collected_per_row(self):
        buf = _make_workbook(rows=[
            ["", "", "", None, None, None],  # name and description empty
        ])
        result = parse_excel(buf)
        errors = result.rows[0].errors
        assert len(errors) >= 2
        assert any("任务名称" in err for err in errors)
        assert any("任务描述" in err for err in errors)


class TestRoundTrip:
    """Template round-trip: generate_template -> parse_excel -> zero errors."""

    def test_roundtrip_template_zero_errors(self):
        buf = generate_template()
        result = parse_excel(buf)
        assert len(result.rows) == 2
        assert result.has_errors is False
        for row in result.rows:
            assert row.errors == []
