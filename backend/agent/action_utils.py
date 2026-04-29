"""Shared utilities for extracting action info from browser-use AgentOutput."""
from __future__ import annotations

from typing import Any


def extract_action_info(agent_output: Any) -> tuple[str, dict]:
    """Extract action name and params from browser-use AgentOutput.

    AgentOutput.action is a list of ActionModel. Each ActionModel has one
    non-None field whose key is the action name and value is the params.

    Returns:
        (action_name, action_params) -- ("unknown", {}) if extraction fails.
    """
    if not agent_output:
        return "unknown", {}

    if not hasattr(agent_output, "action") or not agent_output.action:
        return "unknown", {}

    first_action = agent_output.action[0]
    action_dict = first_action.model_dump(exclude_none=True, mode="json")

    if not action_dict:
        return "unknown", {}

    action_name = list(action_dict.keys())[0]
    action_params = action_dict[action_name]

    return action_name, action_params if isinstance(action_params, dict) else {}
