"""Run-scoped in-memory cache service.

Replaces the JSON file-based caching in webseleniumerp.
Lifecycle is tied to a single Run execution.
"""

import copy
from typing import Any


class CacheService:
    """In-memory key-value cache scoped to a single Run.

    All stored and retrieved values are deep-copied to guarantee
    immutability: external mutations never affect the cache's internal
    state, and cache mutations never affect returned references.
    """

    def __init__(self) -> None:
        self._store: dict[str, Any] = {}

    def cache(self, key: str, value: Any) -> Any:
        """Store a value and return the original for chaining.

        The value is deep-copied before storage to isolate the cache
        from external mutations.
        """
        self._store = {**self._store, key: copy.deepcopy(value)}
        return value

    def cached(self, key: str) -> Any:
        """Retrieve a cached value. Returns None if key does not exist (D-05).

        Returns a deep copy to prevent external code from mutating
        the cache's internal state.
        """
        if key not in self._store:
            return None
        return copy.deepcopy(self._store[key])

    def has(self, key: str) -> bool:
        """Check whether a key exists in the cache (D-06)."""
        return key in self._store

    def all(self) -> dict[str, Any]:
        """Return a deep copy of all cached data."""
        return copy.deepcopy(self._store)

    def clear(self) -> None:
        """Remove all cached data."""
        self._store = {}

    def delete(self, key: str) -> None:
        """Remove a single cached item by key (D-04)."""
        if key in self._store:
            self._store = {k: v for k, v in self._store.items() if k != key}
