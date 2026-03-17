"""Configuration validation functions."""
import ast
import sys
import importlib.util
from pathlib import Path


def validate_weberp_path(path: str) -> None:
    """Validate webseleniumerp project path.

    Performs the following checks:
    1. Directory exists
    2. base_prerequisites.py exists
    3. config/settings.py exists (user-created file)
    4. base_prerequisites.py is importable

    Args:
        path: Path to webseleniumerp project directory.

    Raises:
        SystemExit: If validation fails, with clear error message.
    """
    weberp_dir = Path(path)

    # Check 1: Directory exists
    if not weberp_dir.exists():
        print(f"\n[CONFIG ERROR] WEBSERP_PATH directory not found: {path}")
        print("  Solution: Verify the path in your .env file")
        print("  Example: WEBSERP_PATH=/Users/you/projects/webseleniumerp")
        sys.exit(1)

    # Check 2: base_prerequisites.py exists
    base_prereq = weberp_dir / "base_prerequisites.py"
    if not base_prereq.exists():
        print(f"\n[CONFIG ERROR] base_prerequisites.py not found at: {base_prereq}")
        print("  Solution: Ensure webseleniumerp project is correctly cloned")
        print("  The project should contain base_prerequisites.py at its root")
        sys.exit(1)

    # Check 3: config/settings.py exists
    config_file = weberp_dir / "config" / "settings.py"
    if not config_file.exists():
        print(f"\n[CONFIG ERROR] config/settings.py not found at: {config_file}")
        print("  This file is in webseleniumerp's .gitignore and must be created manually.")
        print("  Create the file with the following content:")
        print("""
# webseleniumerp/config/settings.py

# Data paths for test data files
DATA_PATHS = {
    'test_data': '/path/to/your/test/data',
    # Add other paths as needed by your precondition operations
}
""")
        sys.exit(1)

    # Check 4: Module import test (shallow - validates syntax without executing code)
    try:
        source_code = base_prereq.read_text(encoding="utf-8")
        ast.parse(source_code)
    except SyntaxError as e:
        print(f"\n[CONFIG ERROR] Cannot import base_prerequisites: SyntaxError at line {e.lineno}")
        print(f"  {e.msg}")
        print("  Solution: Check that base_prerequisites.py contains valid Python syntax")
        sys.exit(1)
    except Exception as e:
        print(f"\n[CONFIG ERROR] Cannot import base_prerequisites: {e}")
        print("  Solution: Check that base_prerequisites.py contains valid Python syntax")
        sys.exit(1)
