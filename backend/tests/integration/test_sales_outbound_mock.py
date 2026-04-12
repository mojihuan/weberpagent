"""Mock integration tests for complete sales outbound flow.

Validates the full integration chain from Phases 74-77 works end-to-end
by mocking external dependencies (AgentService/LLM) while verifying
internal flow orchestration correctness (per D-02).

Covers:
- login_role="main" -> AccountService resolution -> login prefix injection
- {{cached:key}} variable replacement with cache values
- Step number offset (+5) with login prefix
- Shared CacheService bridges precondition and assertion phases
- Mixed cached and context variable two-phase substitution
- Missing cache key graceful degradation (no crash)
"""

import re
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from backend.core.account_service import AccountInfo
from backend.core.cache_service import CacheService
from backend.core.precondition_service import ContextWrapper
from backend.core.test_flow_service import TestFlowService


class TestSalesOutboundMock:
    """Mock integration tests covering complete sales outbound data flow."""

    # ------------------------------------------------------------------
    # Test 1: Master flow — login_role="main" end-to-end
    # ------------------------------------------------------------------
    @pytest.mark.asyncio
    async def test_complete_flow_login_role_main(self):
        """Full flow: login_role=main resolves account and injects login prefix."""
        from backend.api.routes.runs import run_agent_background

        mock_account_info = AccountInfo(
            account="Y59800075", password="Aa123456", role="main"
        )

        with (
            patch("backend.api.routes.runs.async_session") as mock_session_ctx,
            patch("backend.api.routes.runs.AgentService") as mock_agent_cls,
            patch("backend.api.routes.runs.ReportService") as mock_report_cls,
            patch("backend.api.routes.runs.AssertionService") as mock_assertion_cls,
            patch("backend.api.routes.runs.AssertionResultRepository") as mock_ar_repo,
            patch("backend.api.routes.runs.PreconditionResultRepository") as mock_pr_repo,
            patch("backend.api.routes.runs.event_manager") as mock_em,
            patch("backend.core.account_service.account_service.resolve") as mock_resolve,
            patch("backend.core.account_service.account_service.get_login_url") as mock_url,
        ):
            mock_session = AsyncMock()
            mock_session_ctx.return_value.__aenter__ = AsyncMock(return_value=mock_session)
            mock_session_ctx.return_value.__aexit__ = AsyncMock(return_value=False)

            mock_agent = MagicMock()
            mock_result = MagicMock()
            mock_result.is_successful.return_value = True
            mock_agent.run_with_cleanup = AsyncMock(return_value=mock_result)
            mock_agent_cls.return_value = mock_agent

            mock_report = MagicMock()
            mock_report.generate_report = AsyncMock()
            mock_report_cls.return_value = mock_report

            mock_assertion_cls.return_value = MagicMock()
            mock_ar_repo.return_value = MagicMock()
            mock_pr_repo.return_value = MagicMock()

            mock_em.publish = AsyncMock()
            mock_em.set_status = MagicMock()

            mock_resolve.return_value = mock_account_info
            mock_url.return_value = "https://erptest.epbox.cn/login"

            await run_agent_background(
                run_id="run-sales-1",
                task_id="task-sales-1",
                task_name="Sales Outbound",
                task_description="步骤1：点击库存管理\n步骤2：点击销售出库",
                max_steps=15,
                target_url="https://erptest.epbox.cn/inventory",
                login_role="main",
            )

            # Verify AccountService.resolve was called with "main"
            mock_resolve.assert_called_once_with("main")

            # Capture the task argument passed to agent_service.run_with_cleanup()
            call_kwargs = mock_agent.run_with_cleanup.call_args
            task_text = call_kwargs.kwargs.get("task", "")

            # Assert login prefix content is present
            assert "打开 https://erptest.epbox.cn/login" in task_text
            assert "Y59800075" in task_text
            assert "Aa123456" in task_text
            assert "登录按钮" in task_text

            # Assert target_url is suppressed to None when login_role is set
            assert call_kwargs.kwargs.get("target_url") is None

            # Assert no error: run_with_cleanup was called (flow completed)
            mock_agent.run_with_cleanup.assert_called_once()

    # ------------------------------------------------------------------
    # Test 2: {{cached:key}} replacement in agent task
    # ------------------------------------------------------------------
    def test_cached_variable_replacement_in_agent_task(self):
        """Validates {{cached:key}} substituted with cache values before agent."""
        shared_cache = CacheService()
        shared_cache.cache("order_no", "SO-2026-001")
        shared_cache.cache("imei", "I012345678901234")

        flow = TestFlowService()
        result = flow._build_description(
            task_description="步骤1：输入订单号{{cached:order_no}}\n步骤2：扫描IMEI{{cached:imei}}",
            login_url="https://erptest.epbox.cn/login",
            account="Y59800075",
            password="Aa123456",
            context={},
            cache_values=shared_cache.all(),
        )

        # Cache values substituted correctly
        assert "SO-2026-001" in result
        assert "I012345678901234" in result

        # No remaining {{cached:...}} patterns
        assert "{{cached:order_no}}" not in result
        assert "{{cached:imei}}" not in result

        # Login prefix appears before user content (position check)
        login_pos = result.find("打开")
        order_pos = result.find("SO-2026-001")
        assert login_pos < order_pos, "Login prefix must appear before user content"

    # ------------------------------------------------------------------
    # Test 3: Step number offset with login prefix (+5)
    # ------------------------------------------------------------------
    def test_step_number_offset_with_login_prefix(self):
        """Validates step numbers shifted by +5 when login prefix injected."""
        flow = TestFlowService()
        result = flow._build_description(
            task_description="步骤1：点击库存管理\n步骤2：点击销售出库\n步骤3：输入物品编号",
            login_url="https://erptest.epbox.cn/login",
            account="Y59800075",
            password="Aa123456",
            context={},
            cache_values={},
        )

        # Steps shifted by +5
        assert "步骤6：" in result
        assert "步骤7：" in result
        assert "步骤8：" in result

        # Original step numbers removed (regex check for unshifted numbers)
        original_steps = re.findall(r"步骤([123])：", result)
        assert original_steps == [], f"Found unshifted step numbers: {original_steps}"

    # ------------------------------------------------------------------
    # Test 4: Shared CacheService bridges precondition to assertion
    # ------------------------------------------------------------------
    def test_shared_cache_bridges_precondition_to_assertion(self):
        """Validates shared CacheService lifecycle across precondition/assertion phases."""
        shared_cache = CacheService()
        shared_cache.cache("product_name", "测试商品A")
        shared_cache.cache("quantity", 100)

        # Precondition phase uses ContextWrapper with shared cache
        context_wrapper = ContextWrapper(cache=shared_cache)

        # Assertion phase reads from same shared cache via ContextWrapper
        assert context_wrapper.cached("product_name") == "测试商品A"
        assert context_wrapper.cached("quantity") == 100

        # Missing key returns None gracefully
        assert context_wrapper.cached("nonexistent") is None

    # ------------------------------------------------------------------
    # Test 5: Mixed cached and context variable two-phase substitution
    # ------------------------------------------------------------------
    def test_mixed_cached_and_context_variables(self):
        """Validates two-phase substitution: regex cached, then Jinja2 context."""
        flow = TestFlowService()
        result = flow._build_description(
            task_description="步骤1：输入物品{{cached:item_code}}\n步骤2：输入备注{{remark}}",
            login_url="https://erptest.epbox.cn/login",
            account="Y59800075",
            password="Aa123456",
            context={"remark": "测试备注"},
            cache_values={"item_code": "SKU-001"},
        )

        # Both phases substituted
        assert "SKU-001" in result
        assert "测试备注" in result

        # No remaining {{...}} patterns
        assert "{{" not in result
        assert "}}" not in result

    # ------------------------------------------------------------------
    # Test 6: Missing cache key graceful degradation
    # ------------------------------------------------------------------
    def test_missing_cache_key_graceful_degradation(self):
        """Validates no crash on missing cache keys; empty string replacement."""
        flow = TestFlowService()

        # Should not raise any exception
        result = flow._build_description(
            task_description="步骤1：输入{{cached:nonexistent_key}}继续操作",
            login_url="https://erptest.epbox.cn/login",
            account="Y59800075",
            password="Aa123456",
            context={},
            cache_values={},
        )

        # No exception raised (test reaching this point proves it)
        assert "继续操作" in result

        # The {{cached:...}} pattern was replaced (with empty string)
        assert "{{cached:nonexistent_key}}" not in result
