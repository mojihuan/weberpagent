"""代码审查 Agent - 审查生成的代码"""

import ast
import json
import logging
import re
from backend.agent_simple.types import InteractiveElement
from backend.agent_simple.form_filler.types import ReviewResult, ReviewIssue
from backend.llm.base import BaseLLM
from backend.agent_simple.form_filler.prompts import build_code_reviewer_prompt

logger = logging.getLogger(__name__)

# 危险模块和函数
DANGEROUS_IMPORTS = {
    "os", "subprocess", "sys", "shutil", "socket",
    "pickle", "marshal", "eval", "exec", "compile",
    "__import__", "importlib",
}

DANGEROUS_CALLS = {
    "os.system", "os.popen", "subprocess.run", "subprocess.call",
    "subprocess.Popen", "eval", "exec", "compile",
}


class CodeReviewer:
    """代码审查 Agent - 审查生成的代码是否安全、有效、完整"""

    def __init__(self, llm: BaseLLM | None = None):
        """初始化代码审查器

        Args:
            llm: 可选的 LLM 实例，用于语义审查
        """
        self._llm = llm

    async def review(self, code: str, elements: list[InteractiveElement]) -> ReviewResult:
        """审查代码

        Args:
            code: 待审查的代码
            elements: 页面可交互元素列表

        Returns:
            ReviewResult 包含审查结果
        """
        issues: list[ReviewIssue] = []
        suggestions: list[str] = []

        # 1. 安全性检查
        issues.extend(self._check_security(code))

        # 2. 语法检查
        issues.extend(self._check_syntax(code))

        # 3. 选择器有效性检查
        selector_issues, selector_suggestions = self._check_selectors(code, elements)
        issues.extend(selector_issues)
        suggestions.extend(selector_suggestions)

        # 4. 逻辑完整性检查
        coverage_issues, coverage_suggestions = self._check_coverage(code, elements)
        issues.extend(coverage_issues)
        suggestions.extend(coverage_suggestions)

        # 5. LLM 语义审查（可选）
        if self._llm is not None:
            llm_issues, llm_suggestions = await self._llm_review(code, elements)
            issues.extend(llm_issues)
            suggestions.extend(llm_suggestions)

        # 确定是否通过
        has_critical = any(i.severity == "CRITICAL" for i in issues)
        has_high = any(i.severity == "HIGH" for i in issues)
        approved = not has_critical and not has_high

        return ReviewResult(approved=approved, issues=issues, suggestions=suggestions)

    def _check_security(self, code: str) -> list[ReviewIssue]:
        """检查代码安全性"""
        issues = []
        for dangerous in DANGEROUS_IMPORTS:
            pattern = rf"^\s*(import\s+{dangerous}|from\s+{dangerous}\s+import)"
            if re.search(pattern, code, re.MULTILINE):
                issues.append(ReviewIssue(
                    severity="CRITICAL",
                    line=None,
                    message=f"检测到危险导入: {dangerous}",
                ))
        for dangerous in DANGEROUS_CALLS:
            if dangerous in code:
                issues.append(ReviewIssue(
                    severity="CRITICAL",
                    line=None,
                    message=f"检测到危险调用: {dangerous}",
                ))
        return issues

    def _check_syntax(self, code: str) -> list[ReviewIssue]:
        """检查语法正确性"""
        issues = []
        try:
            ast.parse(code)
        except SyntaxError as e:
            issues.append(ReviewIssue(
                severity="HIGH",
                line=e.lineno,
                message=f"语法错误: {e.msg}",
            ))
        return issues

    def _check_selectors(self, code: str, elements: list[InteractiveElement]) -> tuple[list[ReviewIssue], list[str]]:
        """检查选择器有效性"""
        issues = []
        suggestions = []

        # 收集有效属性
        valid_placeholders = {el.placeholder for el in elements if el.placeholder}
        valid_texts = {el.text for el in elements if el.text}

        # 检查 placeholder 选择器
        placeholder_pattern = r'get_by_placeholder\(["\']([^"\']+)["\']\)'
        for match in re.finditer(placeholder_pattern, code):
            value = match.group(1)
            if value not in valid_placeholders:
                suggestions.append(f"placeholder '{value}' 未在元素列表中找到")

        return issues, suggestions

    def _check_coverage(self, code: str, elements: list[InteractiveElement]) -> tuple[list[ReviewIssue], list[str]]:
        """检查字段覆盖完整性"""
        issues = []
        suggestions = []

        input_elements = [el for el in elements if el.tag in ("INPUT", "SELECT", "TEXTAREA")]
        if not input_elements:
            return issues, suggestions

        filled_count = 0
        for el in input_elements:
            identifier = el.placeholder or el.name or el.id or el.aria_label
            if identifier and identifier in code:
                filled_count += 1

        coverage = filled_count / len(input_elements) if input_elements else 1.0
        if coverage < 0.5:
            issues.append(ReviewIssue(
                severity="MEDIUM",
                line=None,
                message=f"字段覆盖率较低: {coverage:.0%}",
            ))

        return issues, suggestions

    async def _llm_review(
        self, code: str, elements: list[InteractiveElement]
    ) -> tuple[list[ReviewIssue], list[str]]:
        """使用 LLM 进行语义审查

        Args:
            code: 待审查的代码
            elements: 页面可交互元素列表

        Returns:
            tuple[list[ReviewIssue], list[str]]: LLM 发现的问题和建议
        """
        issues: list[ReviewIssue] = []
        suggestions: list[str] = []

        if self._llm is None:
            return issues, suggestions

        try:
            messages = build_code_reviewer_prompt(code, elements)
            response = await self._llm.chat_with_vision(messages, images=[])
            llm_issues, llm_suggestions = self._parse_llm_response(response.content)
            issues.extend(llm_issues)
            suggestions.extend(llm_suggestions)
        except Exception as e:
            logger.warning(f"LLM 审查失败，跳过: {e}")

        return issues, suggestions

    def _parse_llm_response(self, response: str) -> tuple[list[ReviewIssue], list[str]]:
        """解析 LLM 响应，提取问题和建议

        Args:
            response: LLM 的原始响应文本

        Returns:
            tuple[list[ReviewIssue], list[str]]: 解析出的问题和建议
        """
        issues: list[ReviewIssue] = []
        suggestions: list[str] = []

        try:
            # 尝试提取 JSON 内容
            json_str = response.strip()

            # 处理可能的 markdown 代码块包装
            if "```json" in json_str:
                start = json_str.find("```json") + 7
                end = json_str.find("```", start)
                json_str = json_str[start:end].strip()
            elif "```" in json_str:
                start = json_str.find("```") + 3
                end = json_str.find("```", start)
                json_str = json_str[start:end].strip()

            data = json.loads(json_str)

            # 解析 issues
            for issue_data in data.get("issues", []):
                issues.append(ReviewIssue(
                    severity=issue_data.get("severity", "MEDIUM"),
                    line=issue_data.get("line"),
                    message=issue_data.get("message", ""),
                ))

            # 解析 suggestions
            suggestions.extend(data.get("suggestions", []))

        except json.JSONDecodeError as e:
            logger.warning(f"解析 LLM 响应失败: {e}")
        except Exception as e:
            logger.warning(f"处理 LLM 响应时出错: {e}")

        return issues, suggestions