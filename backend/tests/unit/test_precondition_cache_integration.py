"""Integration tests for ContextWrapper cache/cached delegation to CacheService.

Verifies CACHE-03: ContextWrapper delegates cache() and cached() calls
to an injected (or default-created) CacheService instance.
"""

from backend.core.cache_service import CacheService
from backend.core.precondition_service import ContextWrapper


def test_context_cache_delegates():
    """ctx.cache() stores value and ctx.cached() retrieves it via CacheService delegation."""
    cache_svc = CacheService()
    ctx = ContextWrapper(cache=cache_svc)
    result = ctx.cache("order_no", "SO-2026-001")
    assert result == "SO-2026-001"
    assert ctx.cached("order_no") == "SO-2026-001"


def test_context_cached_delegates():
    """Cache via ContextWrapper is readable from the shared CacheService instance."""
    cache_svc = CacheService()
    ctx = ContextWrapper(cache=cache_svc)
    ctx.cache("i", "123")
    assert cache_svc.cached("i") == "123"


def test_contextwrapper_no_cache_param_works():
    """ContextWrapper() with no arguments creates its own internal CacheService."""
    ctx = ContextWrapper()
    ctx.cache("key", "value")
    assert ctx.cached("key") == "value"


def test_contextwrapper_cached_returns_none_for_missing():
    """D-05: cached() returns None for missing keys, not KeyError."""
    ctx = ContextWrapper()
    assert ctx.cached("nonexistent") is None


def test_existing_context_interface_unchanged():
    """All existing ContextWrapper interfaces work after adding cache integration."""
    ctx = ContextWrapper()
    ctx["order_id"] = "ORD-123"
    assert ctx["order_id"] == "ORD-123"
    assert "order_id" in ctx
    assert ctx.get("order_id") == "ORD-123"
    assert ctx.to_dict()["order_id"] == "ORD-123"
    assert list(ctx.keys()) == ["order_id"]
