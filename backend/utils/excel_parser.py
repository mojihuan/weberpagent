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


# Stub: parse_excel not yet implemented (TDD RED phase)
def parse_excel(buffer: BytesIO) -> ParseResult:
    raise NotImplementedError("parse_excel not yet implemented")
