"""Unit tests for CacheService in-memory key-value cache.

Tests cover all 6 methods (cache, cached, has, all, clear, delete),
bidirectional deepcopy guarantees, and D-05/D-06 edge cases.
"""

import copy

import pytest

from backend.core.cache_service import CacheService


def test_cache_stores_and_cached_retrieves():
    """CacheService().cache() stores a value, cached() retrieves it."""
    svc = CacheService()
    svc.cache("order_no", "SO-2026-001")
    assert svc.cached("order_no") == "SO-2026-001"


def test_cached_returns_deepcopy():
    """Retrieved values are deep copies; mutating them does not affect internal state."""
    svc = CacheService()
    original = {"items": [1, 2, 3]}
    svc.cache("data", original)

    retrieved = svc.cached("data")
    assert retrieved == {"items": [1, 2, 3]}

    # Mutate the retrieved copy
    retrieved["items"].append(4)

    # Internal state should be unchanged
    assert svc.cached("data") == {"items": [1, 2, 3]}


def test_cache_deep_copies_on_store():
    """Mutating the original object after caching does not affect stored value."""
    svc = CacheService()
    original = {"key": "value"}
    svc.cache("data", original)

    original["key"] = "mutated"

    assert svc.cached("data") == {"key": "value"}


def test_cache_returns_original_value():
    """cache(key, value) returns the original value reference, not a deepcopy."""
    svc = CacheService()
    obj = {"a": 1}
    result = svc.cache("k", obj)
    assert result is obj


def test_has_key():
    """has() distinguishes between cached None value and missing key (D-06)."""
    svc = CacheService()
    svc.cache("x", None)
    assert svc.has("x") is True
    assert svc.has("not_here") is False


def test_cached_missing_key_returns_none():
    """cached(missing_key) returns None, never raises exception (D-05)."""
    svc = CacheService()
    assert svc.cached("nonexistent") is None


def test_clear_removes_all():
    """clear() removes all cached data from the instance."""
    svc = CacheService()
    svc.cache("a", 1)
    svc.cache("b", 2)
    svc.clear()
    assert svc.has("a") is False
    assert svc.has("b") is False
    assert svc.cached("a") is None


def test_delete_removes_key():
    """delete() removes a single key while leaving others intact."""
    svc = CacheService()
    svc.cache("a", 1)
    svc.cache("b", 2)
    svc.delete("a")
    assert svc.has("a") is False
    assert svc.cached("b") == 2


def test_all_returns_deepcopy():
    """all() returns a deep copy; mutating it does not affect internal state."""
    svc = CacheService()
    svc.cache("data", {"nested": [1, 2]})
    all_data = svc.all()
    all_data["data"]["nested"].append(3)
    assert svc.cached("data") == {"nested": [1, 2]}


def test_overwrite_existing_key():
    """Caching an existing key overwrites the previous value."""
    svc = CacheService()
    svc.cache("k", "old")
    svc.cache("k", "new")
    assert svc.cached("k") == "new"
