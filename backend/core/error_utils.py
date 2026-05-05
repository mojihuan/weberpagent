"""Shared exception handling utilities.

Unifies repeated try-except patterns across the codebase per FUNC-04.
Per D-09: simple functions, no decorators or context managers.
Per D-10: no custom exception hierarchy.
"""

import logging
from typing import Any, Awaitable, Callable, TypeVar

logger = logging.getLogger(__name__)

T = TypeVar("T")


async def non_blocking_execute(
    fn: Callable[..., Awaitable[T]],
    *args: Any,
    error_msg: str = "Non-blocking operation failed",
    **kwargs: Any,
) -> T | None:
    """Execute async function, log errors, never raise.

    Use for: optional operations where failure should not interrupt flow.
    Returns None on failure, result on success.
    """
    try:
        return await fn(*args, **kwargs)
    except Exception as e:
        logger.error(f"{error_msg}: {e}")
        return None


def silent_execute(
    fn: Callable[..., T],
    *args: Any,
    **kwargs: Any,
) -> T | None:
    """Execute function, silently swallow exceptions.

    Use for: cleanup, optional side-effects where errors are truly irrelevant.
    Returns None on failure, result on success.
    """
    try:
        return fn(*args, **kwargs)
    except Exception:
        return None
