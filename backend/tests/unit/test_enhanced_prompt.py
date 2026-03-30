"""Unit tests for ENHANCED_SYSTEM_MESSAGE prompt constant.

Tests verify structure and key content presence using keyword-based
assertions (not exact string matching per D-09). Covers PRM-01~05.
"""

import pytest

from backend.agent.prompts import ENHANCED_SYSTEM_MESSAGE


class TestEnhancedPrompt:
    """Tests for ENHANCED_SYSTEM_MESSAGE structure and content."""

    def test_is_non_empty_string(self):
        """ENHANCED_SYSTEM_MESSAGE must be a non-empty string."""
        assert isinstance(ENHANCED_SYSTEM_MESSAGE, str)
        assert len(ENHANCED_SYSTEM_MESSAGE.strip()) > 0

    def test_contains_click_to_edit_keywords(self):
        """PRM-01: Must contain click-to-edit guidance with key terms."""
        lower = ENHANCED_SYSTEM_MESSAGE.lower()
        assert "click" in lower
        assert "td" in lower
        assert "input" in lower
        assert "edit" in lower

    def test_contains_failure_recovery_keywords(self):
        """PRM-02: Must contain failure recovery rule with key terms."""
        lower = ENHANCED_SYSTEM_MESSAGE.lower()
        assert "fail" in lower or "失败" in ENHANCED_SYSTEM_MESSAGE
        assert "evaluate" in lower
        assert "find_elements" in lower
        assert "skip" in lower or "跳过" in ENHANCED_SYSTEM_MESSAGE

    def test_contains_post_fill_verification_keywords(self):
        """PRM-03: Must contain post-fill verification guidance."""
        lower = ENHANCED_SYSTEM_MESSAGE.lower()
        assert "verify" in lower or "确认" in ENHANCED_SYSTEM_MESSAGE
        assert "confirm" in lower or "校验" in ENHANCED_SYSTEM_MESSAGE
        assert "value" in lower or "值" in ENHANCED_SYSTEM_MESSAGE

    def test_contains_pre_submit_validation_keywords(self):
        """PRM-04: Must contain pre-submit validation rule."""
        lower = ENHANCED_SYSTEM_MESSAGE.lower()
        assert "submit" in lower or "提交" in ENHANCED_SYSTEM_MESSAGE
        assert "confirm" in lower or "校验" in ENHANCED_SYSTEM_MESSAGE
        assert "validate" in lower or "检查" in ENHANCED_SYSTEM_MESSAGE
        assert "check" in lower or "核实" in ENHANCED_SYSTEM_MESSAGE

    def test_line_count_under_60(self):
        """D-01: ENHANCED_SYSTEM_MESSAGE must be under 60 lines."""
        lines = ENHANCED_SYSTEM_MESSAGE.strip().splitlines()
        assert len(lines) <= 60

    def test_contains_chinese_form_field_mapping(self):
        """PRM-05: Must merge Chinese form field mapping from CHINESE_ENHANCEMENT."""
        lower = ENHANCED_SYSTEM_MESSAGE.lower()
        assert "login" in lower or "登录" in ENHANCED_SYSTEM_MESSAGE
        assert "search" in lower or "搜索" in ENHANCED_SYSTEM_MESSAGE
        assert "cancel" in lower or "取消" in ENHANCED_SYSTEM_MESSAGE

    def test_does_not_contain_json_output_template(self):
        """Must NOT contain redundant JSON action output format template."""
        assert '"action":' not in ENHANCED_SYSTEM_MESSAGE
        assert '"selector":' not in ENHANCED_SYSTEM_MESSAGE

    def test_contains_keyboard_operation_keywords(self):
        """KB-01~03: Must contain keyboard operation guidance with key terms."""
        lower = ENHANCED_SYSTEM_MESSAGE.lower()
        assert "send_keys" in lower
        assert "enter" in lower
        assert "escape" in lower
        assert "control" in lower
        assert "键盘操作" in ENHANCED_SYSTEM_MESSAGE

    def test_no_ctrl_v_guidance(self):
        """D-06: Must NOT contain Ctrl+V paste guidance."""
        lower = ENHANCED_SYSTEM_MESSAGE.lower()
        assert "control+v" not in lower
        assert "ctrl+v" not in lower

    def test_keyboard_section_line_count(self):
        """D-04: Keyboard operation section must not exceed 10 lines."""
        lines = ENHANCED_SYSTEM_MESSAGE.splitlines()
        section_start = None
        section_end = None
        for i, line in enumerate(lines):
            if line.strip().startswith("## 6."):
                section_start = i
            elif section_start is not None and line.strip().startswith("## "):
                section_end = i
                break
        assert section_start is not None, "Section '## 6.' not found"
        end = section_end if section_end is not None else len(lines)
        section_lines = [l for l in lines[section_start:end] if l.strip()]
        assert len(section_lines) <= 10
