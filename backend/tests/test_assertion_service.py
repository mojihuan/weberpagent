"""Tests for AssertionService.check_element_exists real DOM detection.

Tests ERR-03: check_element_exists must use page.evaluate() + querySelector
for real DOM detection instead of the previous hardcoded True stub.
"""

import json
from unittest.mock import AsyncMock, MagicMock

import pytest
from pydantic import ValidationError

from backend.api.schemas.index import Assertion


class TestCheckElementExists:
    """Unit tests for AssertionService.check_element_exists DOM detection."""

    @pytest.mark.asyncio
    async def test_element_found(self) -> None:
        """check_element_exists returns (True, "", selector) when element exists.

        Mocks page.evaluate to return a found result via JSON.stringify pattern.
        The real browser-use page.evaluate returns string from JSON.stringify.
        """
        from backend.core.assertion_service import AssertionService

        service = AssertionService(session=MagicMock())

        # Mock history with page that returns found element
        history = MagicMock()
        history.page.evaluate = AsyncMock(
            return_value='{"found": true, "tag": "DIV"}'
        )

        passed, message, actual = await service.check_element_exists(history, ".btn")

        assert passed is True
        assert message == ""
        assert actual == ".btn"

    @pytest.mark.asyncio
    async def test_element_not_found(self) -> None:
        """check_element_exists returns (False, message, "") when element not found.

        page.evaluate returns {"found": false} — element not in DOM.
        """
        from backend.core.assertion_service import AssertionService

        service = AssertionService(session=MagicMock())

        history = MagicMock()
        history.page.evaluate = AsyncMock(
            return_value='{"found": false}'
        )

        passed, message, actual = await service.check_element_exists(history, ".missing")

        assert passed is False
        assert ".missing" in message
        assert actual == ""

    @pytest.mark.asyncio
    async def test_page_unavailable(self) -> None:
        """check_element_exists returns (False, error, "") when page is not available.

        History object without page attribute — must not raise, must return failure tuple.
        """
        from backend.core.assertion_service import AssertionService

        service = AssertionService(session=MagicMock())

        # spec=object so hasattr(history, "page") returns False
        history = MagicMock(spec=object)

        passed, message, actual = await service.check_element_exists(history, ".btn")

        assert passed is False
        assert ".btn" in message
        assert actual == ""

    @pytest.mark.asyncio
    async def test_invalid_selector_raises_no_exception(self) -> None:
        """check_element_exists returns (False, error, "") on JS evaluation error.

        page.evaluate raises an exception (e.g. SyntaxError from bad selector).
        Must not propagate — must return a failure tuple.
        """
        from backend.core.assertion_service import AssertionService

        service = AssertionService(session=MagicMock())

        history = MagicMock()
        history.page.evaluate = AsyncMock(side_effect=Exception("SyntaxError"))

        passed, message, actual = await service.check_element_exists(
            history, "[[[invalid"
        )

        assert passed is False
        assert "SyntaxError" in message or "[[[invalid" in message
        assert actual == ""

    def test_schema_accepts_element_exists(self) -> None:
        """Assertion Pydantic schema must accept 'element_exists' as a valid type.

        ERR-03: element_exists must be a valid literal in the Assertion type field
        so that assertion pipelines can route to check_element_exists.
        """
        assertion = Assertion(type="element_exists", name="test", expected=".btn")
        assert assertion.type == "element_exists"
        assert assertion.expected == ".btn"

        # Also verify existing types still work
        old_assertion = Assertion(type="url_contains", name="test", expected="http://x")
        assert old_assertion.type == "url_contains"
