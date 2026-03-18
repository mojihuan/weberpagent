"""E2E integration tests for complete precondition flow.

Tests VAL-01: Complete flow from operation code selection to precondition
execution and result verification.
"""

import pytest
from pathlib import Path

from backend.core import external_precondition_bridge
from backend.core.precondition_service import PreconditionService
from backend.core.external_precondition_bridge import (
    configure_external_path,
    generate_precondition_code,
    reset_cache,
)


@pytest.fixture(autouse=True)
def reset_bridge_cache():
    """Reset bridge cache before and after each test."""
    external_precondition_bridge.reset_cache()
    yield
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
