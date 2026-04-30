"""Backward-compatible re-exports — use runs_routes or run_pipeline directly.

Split per D-06: HTTP endpoints in runs_routes.py, pipeline logic in run_pipeline.py.
"""

from backend.api.routes.runs_routes import router  # noqa: F401
from backend.api.routes.run_pipeline import run_agent_background  # noqa: F401
