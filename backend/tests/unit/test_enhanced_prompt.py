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

    def test_line_count_under_80(self):
        """D-01: ENHANCED_SYSTEM_MESSAGE must be under 80 lines."""
        lines = ENHANCED_SYSTEM_MESSAGE.strip().splitlines()
        assert len(lines) <= 80

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

    def test_contains_table_interaction_keywords(self):
        """TBL-01~04: Must contain table interaction guidance with key terms."""
        lower = ENHANCED_SYSTEM_MESSAGE.lower()
        assert "checkbox" in lower
        assert "el-checkbox" in lower
        assert "evaluate" in lower
        assert "queryselector" in lower
        assert "fallback" in lower
        assert "表格交互" in ENHANCED_SYSTEM_MESSAGE

    def test_table_section_line_count(self):
        """D-03: Table interaction section must not exceed 10 lines."""
        lines = ENHANCED_SYSTEM_MESSAGE.splitlines()
        section_start = None
        section_end = None
        for i, line in enumerate(lines):
            if line.strip().startswith("## 7."):
                section_start = i
            elif section_start is not None and line.strip().startswith("## "):
                section_end = i
                break
        assert section_start is not None, "Section '## 7.' not found"
        end = section_end if section_end is not None else len(lines)
        section_lines = [l for l in lines[section_start:end] if l.strip()]
        assert len(section_lines) <= 10

    def test_contains_file_upload_keywords(self):
        """IMP-01/02: Must contain file upload guidance with key terms."""
        lower = ENHANCED_SYSTEM_MESSAGE.lower()
        assert "upload_file" in lower
        assert "file input" in lower or "文件上传" in ENHANCED_SYSTEM_MESSAGE
        assert "文件上传" in ENHANCED_SYSTEM_MESSAGE
        assert "available_file_paths" in lower

    def test_file_upload_section_line_count(self):
        """D-06: File upload section must not exceed 10 lines."""
        lines = ENHANCED_SYSTEM_MESSAGE.splitlines()
        section_start = None
        section_end = None
        for i, line in enumerate(lines):
            if line.strip().startswith("## 8."):
                section_start = i
            elif section_start is not None and line.strip().startswith("## "):
                section_end = i
                break
        assert section_start is not None, "Section '## 8.' not found"
        end = section_end if section_end is not None else len(lines)
        section_lines = [l for l in lines[section_start:end] if l.strip()]
        assert len(section_lines) <= 10


class TestSection9Phase69:
    """Tests for Phase 69 Section 9 prompt rule additions (PROMPT-01/02/03, RECOV-03)."""

    def test_contains_row_identity_rules(self):
        """PROMPT-01: Section 9 must contain row identity usage rules."""
        assert "行标识" in ENHANCED_SYSTEM_MESSAGE or "行定位" in ENHANCED_SYSTEM_MESSAGE
        assert "行:" in ENHANCED_SYSTEM_MESSAGE

    def test_contains_anti_repeat_rules(self):
        """PROMPT-02: Section 9 must contain anti-repeat rules."""
        assert (
            "已尝试" in ENHANCED_SYSTEM_MESSAGE
            or "反重复" in ENHANCED_SYSTEM_MESSAGE
            or "不要重复" in ENHANCED_SYSTEM_MESSAGE
        )

    def test_contains_strategy_priority_rules(self):
        """PROMPT-03: Section 9 must contain strategy priority rules."""
        assert "策略" in ENHANCED_SYSTEM_MESSAGE
        assert (
            "1-原生 input" in ENHANCED_SYSTEM_MESSAGE
            or "2-需先 click" in ENHANCED_SYSTEM_MESSAGE
            or "3-evaluate JS" in ENHANCED_SYSTEM_MESSAGE
        )

    def test_contains_failure_recovery_rules(self):
        """RECOV-03: Section 9 must contain failure recovery rules for all three modes."""
        assert (
            "click_no_effect" in ENHANCED_SYSTEM_MESSAGE
            or (
                "click" in ENHANCED_SYSTEM_MESSAGE
                and (
                    "无变化" in ENHANCED_SYSTEM_MESSAGE
                    or "无响应" in ENHANCED_SYSTEM_MESSAGE
                )
            )
        )
        assert (
            "wrong_column" in ENHANCED_SYSTEM_MESSAGE
            or "错误列" in ENHANCED_SYSTEM_MESSAGE
            or "误点" in ENHANCED_SYSTEM_MESSAGE
        )
        assert (
            "edit_not_active" in ENHANCED_SYSTEM_MESSAGE
            or "未激活" in ENHANCED_SYSTEM_MESSAGE
        )

    def test_total_line_count_under_80(self):
        """D-05/RESEARCH Pitfall 4: Total ENHANCED_SYSTEM_MESSAGE must stay under 80 lines."""
        lines = ENHANCED_SYSTEM_MESSAGE.strip().splitlines()
        assert len(lines) <= 80

    def test_existing_section9_content_unchanged(self):
        """DEPTH-04: Section 9 rewritten with column annotation cross-positioning."""
        assert "列:" in ENHANCED_SYSTEM_MESSAGE
        assert "定位" in ENHANCED_SYSTEM_MESSAGE
        assert "操作" in ENHANCED_SYSTEM_MESSAGE

    def test_contains_column_annotation_rules(self):
        """DEPTH-04: Section 9 must contain column annotation cross-positioning rules."""
        assert "列:" in ENHANCED_SYSTEM_MESSAGE
        assert "交叉" in ENHANCED_SYSTEM_MESSAGE or "定位" in ENHANCED_SYSTEM_MESSAGE
