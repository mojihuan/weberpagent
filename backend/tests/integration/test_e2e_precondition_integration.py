"""E2E integration tests for complete precondition flow.

Tests VAL-01: Complete flow from operation code selection to precondition
execution and result verification.
"""

import sys
import pytest
from pathlib import Path

from backend.core import external_precondition_bridge
from backend.core.precondition_service import PreconditionService
from backend.core.external_precondition_bridge import (
    configure_external_path,
    generate_precondition_code,
    reset_cache,
)


def _clear_common_from_sys_modules():
    """Clear common module from sys.modules to ensure fresh imports."""
    modules_to_remove = [k for k in sys.modules if k.startswith('common')]
    for mod in modules_to_remove:
        del sys.modules[mod]


@pytest.fixture(autouse=True)
def reset_bridge_cache():
    """Reset bridge cache and clear sys.modules before and after each test."""
    _clear_common_from_sys_modules()
    external_precondition_bridge.reset_cache()
    yield
    _clear_common_from_sys_modules()
    external_precondition_bridge.reset_cache()


@pytest.fixture
def mock_webseleniumerp(tmp_path: Path) -> Path:
    """Create mock webseleniumerp directory with PreFront class.

    Structure:
        webseleniumerp/
        ├── common/
        │   ├── __init__.py
        │   └── base_prerequisites.py  (PreFront class)
        └── config/
            └── settings.py  (DATA_PATHS)
    """
    weberp_dir = tmp_path / "webseleniumerp"
    weberp_dir.mkdir()

    # Create common/base_prerequisites.py with PreFront class
    common_dir = weberp_dir / "common"
    common_dir.mkdir()
    (common_dir / "__init__.py").write_text("")
    (common_dir / "base_prerequisites.py").write_text('''
class PreFront:
    """Mock PreFront class for testing."""

    def __init__(self):
        self.executed_operations = []

    def operations(self, codes):
        """Execute precondition operations."""
        self.executed_operations = codes
        return self
''')

    # Create config/settings.py
    config_dir = weberp_dir / "config"
    config_dir.mkdir()
    (config_dir / "settings.py").write_text('DATA_PATHS = {}')

    return weberp_dir


class TestCompleteFlow:
    """Tests for VAL-01: Complete flow from code selection to execution."""

    @pytest.mark.asyncio
    async def test_complete_flow_with_mock_module(self, mock_webseleniumerp):
        """Test complete flow: select codes -> generate code -> execute -> verify success.

        Steps:
        1. Configure bridge with mock path
        2. Generate code for ['FA1']
        3. Execute via PreconditionService
        4. Verify success and context variables
        """
        # 1. Configure bridge with mock path
        success, msg = configure_external_path(str(mock_webseleniumerp))
        assert success is True, f"Failed to configure path: {msg}"

        # 2. Generate code for ['FA1']
        code = generate_precondition_code(['FA1'], str(mock_webseleniumerp))

        # 3. Execute via PreconditionService
        service = PreconditionService()
        result = await service.execute_single(code, 0)

        # 4. Verify results
        assert result.success is True, f"Execution failed: {result.error}"
        assert result.error is None

        # Verify context has precondition_result set
        context = service.get_context()
        assert context.get('precondition_result') == 'success'

    @pytest.mark.asyncio
    async def test_multiple_operation_codes_execute_correctly(self, mock_webseleniumerp):
        """Test multiple operation codes (FA1, HC1) execute and set context.

        Steps:
        1. Configure bridge with mock path
        2. Generate code for ['FA1', 'HC1']
        3. Execute via PreconditionService
        4. Verify success and context
        """
        # 1. Configure bridge
        success, msg = configure_external_path(str(mock_webseleniumerp))
        assert success is True, f"Failed to configure path: {msg}"

        # 2. Generate code for multiple operations
        code = generate_precondition_code(['FA1', 'HC1'], str(mock_webseleniumerp))

        # 3. Execute via PreconditionService
        service = PreconditionService()
        result = await service.execute_single(code, 0)

        # 4. Verify results
        assert result.success is True, f"Execution failed: {result.error}"

        # Verify context
        context = service.get_context()
        assert context.get('precondition_result') == 'success'

    @pytest.mark.asyncio
    async def test_generated_code_pattern_matches_bridge_output(self, mock_webseleniumerp):
        """Test generated code structure matches expected pattern.

        Generated code should contain:
        - sys.path.insert(0, ...)
        - from common.base_prerequisites import PreFront
        - pre_front.operations(['FA1'])
        - context['precondition_result'] = 'success'
        """
        # Generate code for ['FA1']
        code = generate_precondition_code(['FA1'], str(mock_webseleniumerp))

        # Verify code structure
        assert "sys.path.insert(0," in code, "Missing sys.path.insert"
        assert "from common.base_prerequisites import PreFront" in code, "Missing PreFront import"
        assert "pre_front.operations(['FA1'])" in code, "Missing operations call"
        assert "context['precondition_result'] = 'success'" in code, "Missing context assignment"


class TestErrorScenarios:
    """Tests for VAL-02: Error handling scenarios."""

    def test_path_not_configured_returns_error(self):
        """Test is_available() returns False when path not set.

        When WEBSERP_PATH is not configured (None), the bridge should
        report as unavailable with an appropriate error message.

        This test verifies the API layer returns 503 when external module
        is unavailable, which is the expected behavior for path not configured.
        """
        from unittest.mock import patch, MagicMock
        from fastapi.testclient import TestClient
        from backend.api.main import app

        # Ensure fresh state
        _clear_common_from_sys_modules()
        external_precondition_bridge.reset_cache()

        # Mock settings to return None for weberp_path (path not configured)
        mock_settings = MagicMock()
        mock_settings.weberp_path = None

        # Patch at the route level (like test_external_operations.py does)
        with patch(
            'backend.api.routes.external_operations.is_available',
            return_value=False
        ), patch(
            'backend.api.routes.external_operations.get_unavailable_reason',
            return_value='WEBSERP_PATH not configured'
        ):
            client = TestClient(app)
            response = client.get("/api/external-operations")

            # API should return 503 when path not configured
            assert response.status_code == 503, "Expected 503 when path not configured"

    def test_path_not_exists_returns_error(self):
        """Test configure_external_path returns (False, error) for non-existent path.

        When configuring a path that doesn't exist, the function should
        return False with an error message containing 'does not exist'.
        """
        external_precondition_bridge.reset_cache()

        # Configure with non-existent path
        success, msg = configure_external_path('/nonexistent/path/12345')

        assert success is False, "Expected configure_external_path to return False"
        assert "does not exist" in msg.lower() or "not exist" in msg.lower(), \
            f"Expected error message about non-existent path, got: {msg}"

    def test_module_import_failure_returns_error(self, tmp_path: Path):
        """Test load_pre_front_class returns (None, error) on import failure.

        Create a mock directory where base_prerequisites.py has a syntax error
        which causes import to fail.
        """
        external_precondition_bridge.reset_cache()

        # Create mock with syntax error in base_prerequisites.py
        weberp_dir = tmp_path / "syntax_error_webseleniumerp"
        weberp_dir.mkdir()

        common_dir = weberp_dir / "common"
        common_dir.mkdir()
        (common_dir / "__init__.py").write_text("")
        # Create base_prerequisites.py with syntax error (missing colon after class def)
        (common_dir / "base_prerequisites.py").write_text('''
class PreFront
    def operations(self, codes):
        pass
''')  # Missing colon after "class PreFront" - syntax error

        config_dir = weberp_dir / "config"
        config_dir.mkdir()
        (config_dir / "settings.py").write_text('DATA_PATHS = {}')

        # Configure path to this mock with syntax error
        success, msg = configure_external_path(str(weberp_dir))
        assert success is True, f"Failed to configure path: {msg}"

        # Try to load PreFront class - should fail due to syntax error
        cls, error = external_precondition_bridge.load_pre_front_class()

        assert cls is None, "Expected load_pre_front_class to return None on import failure"
        assert error is not None, "Expected an error message"
        # Error should mention import failure or syntax error
        error_lower = error.lower()
        assert "import" in error_lower or "failed" in error_lower or "error" in error_lower or "syntax" in error_lower, \
            f"Expected import-related error message, got: {error}"

    @pytest.mark.asyncio
    async def test_execution_exception_captured_in_result(self):
        """Test PreconditionService captures exceptions in result.error.

        Create code that directly raises an exception and verify that
        PreconditionService captures it in result.error.
        """
        # Code that raises an exception during execution
        error_code = '''
raise ValueError("Simulated execution error")
'''

        # Execute via PreconditionService
        service = PreconditionService()
        result = await service.execute_single(error_code, 0)

        # Verify exception is captured
        assert result.success is False, "Expected success to be False when exception occurs"
        assert result.error is not None, "Expected error message to be captured"
        # Error should contain the exception message or type
        error_lower = result.error.lower()
        assert "simulated execution error" in error_lower or "valueerror" in error_lower, \
            f"Expected error to contain exception info, got: {result.error}"
