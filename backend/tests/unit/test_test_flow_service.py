"""Unit tests for TestFlowService — login prefix injection and two-phase variable substitution.

Covers:
- build_login_prefix: 5-line login instruction generation
- _build_description: login prefix injection, {{cached:key}} regex replacement,
  {{variable}} Jinja2 replacement, step number shifting, missing cache key handling
"""

import pytest

from backend.core.test_flow_service import TestFlowService, build_login_prefix


# ---------------------------------------------------------------------------
# Test 1: build_login_prefix produces correct 5-line content
# ---------------------------------------------------------------------------
def test_build_login_prefix_content():
    result = build_login_prefix(
        "https://erp.example.com", "Y59800075", "Aa123456"
    )

    assert "https://erp.example.com" in result
    assert "Y59800075" in result
    assert "Aa123456" in result
    assert "登录按钮" in result
    assert "登录成功" in result


# ---------------------------------------------------------------------------
# Test 2: build_login_prefix format — starts with "1. " and has 5 lines
# ---------------------------------------------------------------------------
def test_build_login_prefix_format():
    result = build_login_prefix(
        "https://erp.example.com", "Y59800075", "Aa123456"
    )

    assert result.startswith("1. ")
    lines = [line for line in result.split("\n") if line.strip()]
    assert len(lines) == 5


# ---------------------------------------------------------------------------
# Test 3: _build_description injects login prefix before user steps
# ---------------------------------------------------------------------------
def test_build_description_injects_login():
    svc = TestFlowService()
    description = "步骤1：点击库存管理"
    result = svc._build_description(
        task_description=description,
        login_url="https://erp.example.com",
        account="Y59800075",
        password="Aa123456",
        context={},
        cache_values={},
    )

    # Login prefix content should appear before user content
    assert "https://erp.example.com" in result
    assert "Y59800075" in result
    assert "库存管理" in result
    # Login prefix comes first
    login_pos = result.index("https://erp.example.com")
    user_pos = result.index("库存管理")
    assert login_pos < user_pos


# ---------------------------------------------------------------------------
# Test 4: _build_description replaces {{cached:key}} with cache values
# ---------------------------------------------------------------------------
def test_build_description_replaces_cached_variables():
    svc = TestFlowService()
    description = "步骤1：输入物品编号{{cached:i}}"
    result = svc._build_description(
        task_description=description,
        login_url="https://erp.example.com",
        account="Y59800075",
        password="Aa123456",
        context={},
        cache_values={"i": "202421774363480066"},
    )

    assert "202421774363480066" in result
    assert "{{cached:i}}" not in result


# ---------------------------------------------------------------------------
# Test 5: _build_description replaces {{variable}} with context via Jinja2
# ---------------------------------------------------------------------------
def test_build_description_replaces_context_variables():
    svc = TestFlowService()
    description = "步骤1：输入单号{{sf_no}}"
    result = svc._build_description(
        task_description=description,
        login_url="https://erp.example.com",
        account="Y59800075",
        password="Aa123456",
        context={"sf_no": "SF987654"},
        cache_values={},
    )

    assert "SF987654" in result


# ---------------------------------------------------------------------------
# Test 6: _build_description shifts user step numbers by +5
# ---------------------------------------------------------------------------
def test_build_description_shifts_step_numbers():
    svc = TestFlowService()
    description = "步骤1：点击库存管理\n步骤2：点击出库"
    result = svc._build_description(
        task_description=description,
        login_url="https://erp.example.com",
        account="Y59800075",
        password="Aa123456",
        context={},
        cache_values={},
    )

    assert "步骤6：" in result
    assert "步骤7：" in result
    # Original step numbers should not remain
    assert "步骤1：" not in result
    assert "步骤2：" not in result


# ---------------------------------------------------------------------------
# Test 7: Missing cache key produces empty string (no crash, no KeyError)
# ---------------------------------------------------------------------------
def test_build_description_missing_cache_key_empty_string():
    svc = TestFlowService()
    description = "步骤5：输入物品编号{{cached:nonexistent}}"
    result = svc._build_description(
        task_description=description,
        login_url="https://erp.example.com",
        account="Y59800075",
        password="Aa123456",
        context={},
        cache_values={},
    )

    # No crash and no {{cached:nonexistent}} in output
    assert "{{cached:nonexistent}}" not in result
    # Should contain the text around the replaced placeholder
    assert "物品编号" in result


# ---------------------------------------------------------------------------
# Test 8: Mixed {{cached:key}} and {{variable}} in same description
# ---------------------------------------------------------------------------
def test_build_description_mixed_cached_and_context():
    svc = TestFlowService()
    description = "步骤1：输入物品{{cached:i}}\n步骤2：输入单号{{sf_no}}"
    result = svc._build_description(
        task_description=description,
        login_url="https://erp.example.com",
        account="Y59800075",
        password="Aa123456",
        context={"sf_no": "SF123"},
        cache_values={"i": "ITEM001"},
    )

    assert "ITEM001" in result
    assert "SF123" in result
    assert "{{cached:i}}" not in result
    assert "{{sf_no}}" not in result


# ---------------------------------------------------------------------------
# Test 9: No cache_values and no context variables — login prefix + renumbered
# ---------------------------------------------------------------------------
def test_build_description_no_variables():
    svc = TestFlowService()
    description = "步骤1：点击按钮"
    result = svc._build_description(
        task_description=description,
        login_url="https://erp.example.com",
        account="Y59800075",
        password="Aa123456",
        context={},
        cache_values={},
    )

    # Should contain login prefix
    assert "https://erp.example.com" in result
    # User step should be renumbered to 6
    assert "步骤6：" in result
    assert "步骤1：" not in result


# ---------------------------------------------------------------------------
# Test 10: Empty login_url still produces 5-step prefix
# ---------------------------------------------------------------------------
def test_build_description_empty_login_url():
    svc = TestFlowService()
    description = "步骤1：点击按钮"
    result = svc._build_description(
        task_description=description,
        login_url="",
        account="Y59800075",
        password="Aa123456",
        context={},
        cache_values={},
    )

    # Should still produce 5 login steps (with empty URL in step 1)
    lines = [line for line in result.split("\n") if line.strip()]
    # 5 login steps + at least 1 user step
    assert len(lines) >= 6
    assert "步骤6：" in result
