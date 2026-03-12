"""表单填写子模块 - 多 Agent 协作模式"""

from backend.agent_simple.form_filler.types import (
    GeneratedCode,
    ReviewIssue,
    ReviewResult,
    FillResult,
)
from backend.agent_simple.form_filler.code_reviewer import CodeReviewer
from backend.agent_simple.form_filler.prompts import (
    FIELD_GENERATION_RULES,
    build_code_generator_prompt,
    build_code_reviewer_prompt,
    build_code_optimizer_prompt,
    generate_field_value,
)

from backend.agent_simple.form_filler.orchestrator import FormFiller

__all__ = [
    "FormFiller",
    # Types
    "GeneratedCode",
    "ReviewIssue",
    "ReviewResult",
    "FillResult",
    # Agents
    "CodeReviewer",
    # Prompts
    "FIELD_GENERATION_RULES",
    "build_code_generator_prompt",
    "build_code_reviewer_prompt",
    "build_code_optimizer_prompt",
    "generate_field_value",
]