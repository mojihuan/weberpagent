"""Tests for STATE-01: external assertion state leak in context dict.

Verifies that _run_external_assertions does NOT pollute the context dict
with 'external_assertion_summary'. The summary is persisted to DB via
_publish_external_assertion_results and should NOT remain in the mutable
context dict that flows into _variable_map and downstream codegen.
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest


class TestStateLeak:
    """Unit tests ensuring external assertion summary does not leak into context."""

    @pytest.mark.asyncio
    async def test_context_no_assertion_summary_after_run(self) -> None:
        """After _run_external_assertions, context must NOT contain external_assertion_summary.

        The function should execute assertions, publish results, but leave the
        context dict untouched. STATE-01: the summary belongs in DB, not context.
        """
        from backend.api.routes.run_pipeline import _run_external_assertions

        context = {"precondition_var": "value123"}
        mock_summary = {
            "passed": 2,
            "failed": 0,
            "errors": 0,
            "total": 2,
            "results": [],
        }

        with (
            patch(
                "backend.api.routes.run_pipeline.execute_all_assertions",
                new_callable=AsyncMock,
                return_value=mock_summary,
            ),
            patch(
                "backend.api.routes.run_pipeline._publish_external_assertion_results",
                new_callable=AsyncMock,
                return_value=10,
            ),
        ):
            _, _ = await _run_external_assertions(
                run_id="test-run",
                external_assertions=[{"type": "url_contains", "name": "t1", "expected": "x"}],
                context=context,
                shared_cache=MagicMock(),
                run_repo=MagicMock(),
                event_manager_obj=MagicMock(),
                session=MagicMock(),
                global_seq=1,
            )

        assert "external_assertion_summary" not in context

    @pytest.mark.asyncio
    async def test_context_no_assertion_summary_with_failures(self) -> None:
        """Even when assertions produce failures, context must NOT be polluted.

        The summary with failures should be published to DB but not injected
        into the context dict. Failure status is returned via the function's
        return value, not via context mutation.
        """
        from backend.api.routes.run_pipeline import _run_external_assertions

        context = {"precondition_var": "value123"}
        mock_summary = {
            "passed": 1,
            "failed": 1,
            "errors": 1,
            "total": 3,
            "results": [],
        }

        with (
            patch(
                "backend.api.routes.run_pipeline.execute_all_assertions",
                new_callable=AsyncMock,
                return_value=mock_summary,
            ),
            patch(
                "backend.api.routes.run_pipeline._publish_external_assertion_results",
                new_callable=AsyncMock,
                return_value=15,
            ),
        ):
            status, _ = await _run_external_assertions(
                run_id="test-run",
                external_assertions=[
                    {"type": "url_contains", "name": "t1", "expected": "x"},
                ],
                context=context,
                shared_cache=MagicMock(),
                run_repo=MagicMock(),
                event_manager_obj=MagicMock(),
                session=MagicMock(),
                global_seq=5,
            )

        assert "external_assertion_summary" not in context
        assert status == "failed"

    @pytest.mark.asyncio
    async def test_variable_map_excludes_assertion_summary(self) -> None:
        """_variable_map construction from a post-assertion context must not contain external_assertion_summary.

        Simulates the _variable_map filtering logic (lines 543-548) to confirm
        that even if the key were present, the filter would exclude it. But more
        importantly, confirms the key is never there in the first place.
        """
        from backend.api.routes.run_pipeline import _run_external_assertions

        context = {"precondition_var": "value123"}
        mock_summary = {
            "passed": 2,
            "failed": 0,
            "errors": 0,
            "total": 2,
            "results": [],
        }

        with (
            patch(
                "backend.api.routes.run_pipeline.execute_all_assertions",
                new_callable=AsyncMock,
                return_value=mock_summary,
            ),
            patch(
                "backend.api.routes.run_pipeline._publish_external_assertion_results",
                new_callable=AsyncMock,
                return_value=10,
            ),
        ):
            _, _ = await _run_external_assertions(
                run_id="test-run",
                external_assertions=[{"type": "url_contains", "name": "t1", "expected": "x"}],
                context=context,
                shared_cache=MagicMock(),
                run_repo=MagicMock(),
                event_manager_obj=MagicMock(),
                session=MagicMock(),
                global_seq=1,
            )

        # Simulate _variable_map construction as in run_pipeline.py lines 543-548
        _variable_map = {
            k: str(v) for k, v in context.items()
            if isinstance(v, (str, int, float)) and not k.startswith("assertion")
        }

        assert "external_assertion_summary" not in _variable_map
        assert _variable_map == {"precondition_var": "value123"}
