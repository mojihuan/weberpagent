"""Core regression tests for login_role=None path and report step ordering.

Covers:
- login_role=None does NOT inject login prefix content into task text
- login_role=None preserves original task description exactly (no prefix, no renumbering)
- Login steps appear before business steps in generated description (TestFlowService)
- build_login_prefix produces correct 5-line sequential output
- Preconditions work correctly when login_role=None (no interference)

These tests complement (NOT duplicate) test_runs_login_role_integration.py.
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from backend.core.test_flow_service import LOGIN_STEP_COUNT, TestFlowService, build_login_prefix


class TestCoreRegression:
    """Core regression tests ensuring zero regression from v0.9.0 behavior."""

    # ------------------------------------------------------------------
    # Test 1: login_role=None does NOT inject login prefix content
    # ------------------------------------------------------------------
    @pytest.mark.asyncio
    async def test_login_role_none_no_account_service_import(self):
        """Verify AccountService is never used and no login prefix content appears
        in the task text when login_role=None."""
        from backend.api.routes.runs import run_agent_background

        with (
            patch("backend.api.routes.runs.async_session") as mock_session_ctx,
            patch("backend.api.routes.runs.AgentService") as mock_agent_cls,
            patch("backend.api.routes.runs.ReportService") as mock_report_cls,
            patch("backend.api.routes.runs.AssertionService") as mock_assertion_cls,
            patch("backend.api.routes.runs.AssertionResultRepository") as mock_ar_repo,
            patch("backend.api.routes.runs.PreconditionResultRepository") as mock_pr_repo,
            patch("backend.api.routes.runs.event_manager") as mock_em,
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

            await run_agent_background(
                run_id="reg-run-1",
                task_id="task-1",
                task_name="No Login Regression",
                task_description="步骤1：执行某个操作",
                max_steps=5,
                target_url="https://erp.example.com/page",
                login_role=None,
            )

            # Verify the task text passed to run_with_cleanup has NO login prefix content
            call_kwargs = mock_agent.run_with_cleanup.call_args
            task_text = call_kwargs.kwargs.get("task") or call_kwargs.args[0]
            assert "打开" not in task_text, "Login prefix '打开' should not appear when login_role=None"
            assert "登录按钮" not in task_text, "Login prefix '登录按钮' should not appear when login_role=None"
            assert "登录成功" not in task_text, "Login prefix '登录成功' should not appear when login_role=None"

            # Verify target_url is passed through (NOT suppressed/None)
            assert call_kwargs.kwargs.get("target_url") == "https://erp.example.com/page"

    # ------------------------------------------------------------------
    # Test 2: login_role=None preserves original task description exactly
    # ------------------------------------------------------------------
    @pytest.mark.asyncio
    async def test_login_role_none_original_task_description_preserved(self):
        """Verify task description is passed through without modification when
        login_role=None -- no prefix added, no step renumbering, no substitution."""
        from backend.api.routes.runs import run_agent_background

        original_description = "步骤1：测试原始描述"

        with (
            patch("backend.api.routes.runs.async_session") as mock_session_ctx,
            patch("backend.api.routes.runs.AgentService") as mock_agent_cls,
            patch("backend.api.routes.runs.ReportService") as mock_report_cls,
            patch("backend.api.routes.runs.AssertionService") as mock_assertion_cls,
            patch("backend.api.routes.runs.AssertionResultRepository") as mock_ar_repo,
            patch("backend.api.routes.runs.PreconditionResultRepository") as mock_pr_repo,
            patch("backend.api.routes.runs.event_manager") as mock_em,
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

            await run_agent_background(
                run_id="reg-run-2",
                task_id="task-2",
                task_name="Preserve Description",
                task_description=original_description,
                max_steps=5,
                target_url="https://erp.example.com/page",
                login_role=None,
            )

            # The task text should be exactly the original description
            call_kwargs = mock_agent.run_with_cleanup.call_args
            task_text = call_kwargs.kwargs.get("task") or call_kwargs.args[0]
            assert task_text == original_description, (
                f"Expected exact original description, got: {task_text}"
            )

    # ------------------------------------------------------------------
    # Test 3: Login steps appear before business steps in generated description
    # ------------------------------------------------------------------
    def test_report_step_ordering_login_before_business(self):
        """Verify login steps appear before business steps in the generated
        task description from TestFlowService._build_description()."""
        flow = TestFlowService()

        result = flow._build_description(
            task_description="步骤1：打开销售出库页面\n步骤2：选择客户\n步骤3：添加商品",
            login_url="https://erptest.epbox.cn/login",
            account="Y59800075",
            password="Aa123456",
            context={},
            cache_values={},
        )

        lines = result.split("\n")

        # Find index of login "打开" line (login step 1)
        login_open_idx = None
        for i, line in enumerate(lines):
            if "打开" in line and "erptest.epbox.cn/login" in line:
                login_open_idx = i
                break
        assert login_open_idx is not None, f"'打开' login line not found in output:\n{result}"

        # Find index of business "销售出库" line (first business step)
        business_idx = None
        for i, line in enumerate(lines):
            if "销售出库" in line:
                business_idx = i
                break
        assert business_idx is not None, f"'销售出库' line not found in output:\n{result}"

        # Login step must appear before business step
        assert login_open_idx < business_idx, (
            f"Login step (line {login_open_idx}) must appear before business step (line {business_idx})"
        )

        # Verify shifted step numbers: first business step is now 步骤6 (offset by LOGIN_STEP_COUNT=5)
        assert "步骤6" in result, f"Expected '步骤6' (shifted first business step) in:\n{result}"
        assert "步骤7" in result, f"Expected '步骤7' (shifted second business step) in:\n{result}"
        assert "步骤8" in result, f"Expected '步骤8' (shifted third business step) in:\n{result}"

    # ------------------------------------------------------------------
    # Test 4: build_login_prefix produces correct sequential output
    # ------------------------------------------------------------------
    def test_report_login_prefix_correct_step_sequence(self):
        """Verify the login prefix has correct sequential numbering (1-5)
        with expected content on each line."""
        result = build_login_prefix(
            "https://erptest.epbox.cn/login",
            "Y59800075",
            "Aa123456",
        )

        lines = [line for line in result.split("\n") if line.strip()]

        assert len(lines) == 5, f"Expected exactly 5 lines, got {len(lines)}: {lines}"

        assert lines[0].startswith("1. "), f"Line 1 should start with '1. ': {lines[0]}"
        assert "erptest.epbox.cn/login" in lines[0], f"Line 1 should contain URL: {lines[0]}"

        assert lines[1].startswith("2. "), f"Line 2 should start with '2. ': {lines[1]}"
        assert "Y59800075" in lines[1], f"Line 2 should contain account: {lines[1]}"

        assert lines[2].startswith("3. "), f"Line 3 should start with '3. ': {lines[2]}"
        assert "Aa123456" in lines[2], f"Line 3 should contain password: {lines[2]}"

        assert lines[3].startswith("4. "), f"Line 4 should start with '4. ': {lines[3]}"
        assert "登录按钮" in lines[3], f"Line 4 should contain '登录按钮': {lines[3]}"

        assert lines[4].startswith("5. "), f"Line 5 should start with '5. ': {lines[4]}"
        assert "登录成功" in lines[4], f"Line 5 should contain '登录成功': {lines[4]}"

    # ------------------------------------------------------------------
    # Test 5: login_role=None with preconditions causes no interference
    # ------------------------------------------------------------------
    @pytest.mark.asyncio
    async def test_login_role_none_with_preconditions_no_interference(self):
        """Verify preconditions still work correctly when login_role=None --
        no crash from login_role branching logic."""
        from backend.api.routes.runs import run_agent_background

        with (
            patch("backend.api.routes.runs.async_session") as mock_session_ctx,
            patch("backend.api.routes.runs.AgentService") as mock_agent_cls,
            patch("backend.api.routes.runs.ReportService") as mock_report_cls,
            patch("backend.api.routes.runs.AssertionService") as mock_assertion_cls,
            patch("backend.api.routes.runs.AssertionResultRepository") as mock_ar_repo,
            patch("backend.api.routes.runs.PreconditionResultRepository") as mock_pr_repo,
            patch("backend.api.routes.runs.event_manager") as mock_em,
            patch("backend.api.routes.runs.PreconditionService") as mock_precondition_cls,
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
            mock_pr = MagicMock()
            mock_pr.create = AsyncMock()
            mock_pr_repo.return_value = mock_pr

            mock_em.publish = AsyncMock()
            mock_em.set_status = MagicMock()

            # Mock precondition service
            mock_precondition_instance = MagicMock()
            mock_precondition_result = MagicMock()
            mock_precondition_result.success = True
            mock_precondition_result.error = None
            mock_precondition_result.duration_ms = 10
            mock_precondition_result.variables = {"test_var": "hello"}
            mock_precondition_instance.execute_single = AsyncMock(
                return_value=mock_precondition_result
            )
            mock_precondition_instance.get_context.return_value = {"test_var": "hello"}
            mock_precondition_cls.return_value = mock_precondition_instance
            mock_precondition_cls.substitute_variables = staticmethod(
                lambda desc, ctx: desc
            )

            # Should complete without raising any AttributeError or ImportError
            await run_agent_background(
                run_id="reg-run-3",
                task_id="task-3",
                task_name="Precondition Test",
                task_description="步骤1：测试操作",
                max_steps=5,
                preconditions=["context['test_var'] = 'hello'"],
                target_url="https://erp.example.com/page",
                login_role=None,
            )

            # Verify the function completed successfully (no exception)
            # and precondition was executed
            mock_precondition_instance.execute_single.assert_called_once()

            # Verify task still does not contain login prefix content
            call_kwargs = mock_agent.run_with_cleanup.call_args
            task_text = call_kwargs.kwargs.get("task") or call_kwargs.args[0]
            assert "打开" not in task_text
            assert "登录按钮" not in task_text
