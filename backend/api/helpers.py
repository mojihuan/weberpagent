"""API route shared helpers."""

import json
import logging
from typing import Any

from fastapi import HTTPException

logger = logging.getLogger(__name__)


def _build_task_dict(task: Any) -> dict:
    """Build a standardized task response dict from a Task ORM object.

    Extracts 12 fields + computes has_code/latest_run_id from task.runs.
    Used by list_tasks and get_task to avoid duplicate dict construction.
    """
    task_dict = {
        'id': task.id,
        'name': task.name,
        'description': task.description,
        'target_url': task.target_url,
        'max_steps': task.max_steps,
        'status': task.status,
        'created_at': task.created_at,
        'updated_at': task.updated_at,
        'preconditions': task.preconditions,
        'assertions': task.external_assertions,
        'login_role': task.login_role,
        'has_code': False,
        'latest_run_id': None,
    }
    if task.runs:
        latest_run = max(task.runs, key=lambda r: r.created_at)
        task_dict['latest_run_id'] = latest_run.id
        task_dict['has_code'] = bool(latest_run.generated_code_path)
    return task_dict


def _parse_task_json_fields(task: Any) -> tuple[list | None, list | None]:
    """Parse preconditions and external_assertions JSON strings from a Task.

    Returns (preconditions, external_assertions) tuple.
    On parse failure, logs a warning and returns None for that field.
    """
    preconditions = None
    if task.preconditions:
        try:
            preconditions = json.loads(task.preconditions)
        except json.JSONDecodeError:
            logger.warning(f"Task {task.id} preconditions JSON parse failed")

    external_assertions = None
    if hasattr(task, 'external_assertions') and task.external_assertions:
        try:
            external_assertions = json.loads(task.external_assertions)
        except json.JSONDecodeError:
            logger.warning(f"Task {task.id} external_assertions JSON parse failed")

    return preconditions, external_assertions


def raise_not_found(entity_type: str, entity_id: str = "") -> None:
    """Raise HTTPException(404) with a standard 'X not found' message.

    Args:
        entity_type: Human-readable entity name (e.g. "Task", "Run", "Batch").
        entity_id: Optional entity identifier to include in the message.
    """
    detail = f"{entity_type} {entity_id} not found" if entity_id else f"{entity_type} not found"
    raise HTTPException(status_code=404, detail=detail)
