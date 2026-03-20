"""Tests for ContextWrapper assertion result storage."""

import pytest
from backend.core.precondition_service import ContextWrapper


class TestContextWrapperAssertionStorage:
    """Tests for ContextWrapper assertion result storage."""

    def test_store_assertion_result_stores_at_indexed_key(self):
        """store_assertion_result stores result at assertion_result_N key."""
        context = ContextWrapper()
        result = {
            "success": True,
            "passed": True,
            "method": "test_assert",
            "class_name": "PcAssert",
            "field_results": [],
            "duration": 0.5,
            "error": None
        }

        context.store_assertion_result(0, result)

        assert context["assertion_result_0"] == result

    def test_get_assertion_results_summary_returns_correct_counts(self):
        """get_assertion_results_summary returns correct summary."""
        context = ContextWrapper()

        # Store passed assertion
        context.store_assertion_result(0, {
            "passed": True,
            "success": True,
            "method": "test1",
            "class_name": "PcAssert",
            "field_results": [],
            "duration": 0.1
        })

        # Store failed assertion
        context.store_assertion_result(1, {
            "passed": False,
            "success": True,
            "method": "test2",
            "class_name": "PcAssert",
            "field_results": [{"field": "x", "expected": "a", "actual": "b"}],
            "duration": 0.2
        })

        # Store error assertion
        context.store_assertion_result(2, {
            "passed": False,
            "success": False,
            "error_type": "TimeoutError",
            "method": "test3",
            "class_name": "PcAssert",
            "field_results": [],
            "duration": 30.0
        })

        summary = context.get_assertion_results_summary()

        assert summary["total"] == 3
        assert summary["passed"] == 1
        assert summary["failed"] == 1
        assert summary["errors"] == 1

    def test_multiple_stores_update_summary_progressively(self):
        """Multiple store_assertion_result calls update summary progressively."""
        context = ContextWrapper()

        context.store_assertion_result(0, {"passed": True, "success": True, "method": "t1", "class_name": "P", "field_results": [], "duration": 0.1})
        assert context["assertion_results"]["total"] == 1

        context.store_assertion_result(1, {"passed": False, "success": True, "method": "t2", "class_name": "P", "field_results": [], "duration": 0.1})
        assert context["assertion_results"]["total"] == 2

    def test_stored_results_accessible_via_dict_syntax(self):
        """Stored results are accessible via context['assertion_result_0'] syntax."""
        context = ContextWrapper()
        result = {"passed": True, "success": True, "method": "test", "class_name": "PcAssert", "field_results": [], "duration": 0.1}

        context.store_assertion_result(0, result)

        # Access via dict syntax
        assert context["assertion_result_0"]["passed"] is True

    def test_reset_assertion_tracking_clears_all(self):
        """reset_assertion_tracking clears all assertion data."""
        context = ContextWrapper()

        context.store_assertion_result(0, {"passed": True, "success": True, "method": "t1", "class_name": "P", "field_results": [], "duration": 0.1})
        context.store_assertion_result(1, {"passed": False, "success": True, "method": "t2", "class_name": "P", "field_results": [], "duration": 0.1})

        context.reset_assertion_tracking()

        assert context.get_assertion_results_summary()["total"] == 0
        assert "assertion_result_0" not in context._data
        assert "assertion_results" not in context._data
