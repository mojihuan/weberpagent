# Phase 13: 配置基础 - Research

**Researched:** 2026-03-17
**Domain:** Environment Configuration / FastAPI Startup Validation / External Module Integration
**Confidence:** HIGH

## Summary

Phase 13 focuses on configuring the WEBSERP_PATH environment variable that points to the external webseleniumerp project, implementing startup validation to ensure the path is valid, and providing documentation for the external project's config/settings.py file (which is in .gitignore and must be created by users).

This phase is foundational for v0.3 milestone — without proper configuration, the ExternalPreconditionBridge module (Phase 14) cannot import from webseleniumerp. The recommended approach follows existing patterns: extend `backend/config/settings.py` with a new field, add validation in FastAPI lifespan, and update `.env.example` and `README.md` with documentation.

**Primary recommendation:** Add `weberp_path` to Settings class, implement fail-fast validation in FastAPI startup, provide clear error messages with remediation steps.

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

**验证时机**
- 系统启动时验证（fail-fast 策略）
- 在 FastAPI startup event 中执行验证
- 配置错误时直接阻止启动，确保问题在第一时间暴露

**验证内容**
启动时全面验证以下内容：
1. 路径存在 — WEBSERP_PATH 指向的目录存在
2. base_prerequisites.py 存在 — 核心前置条件文件存在
3. config/settings.py 存在 — webseleniumerp 配置文件存在（该文件在 .gitignore 中，需用户创建）
4. 可导入性 — 模块可以成功导入（浅尝验证，不执行代码）

**文档位置**
- 在 README.md 中添加"webseleniumerp 配置"章节
- 提供完整的 config/settings.py 模板
- 包含 DATA_PATHS 配置示例

**错误处理策略**
- 启动失败 + 明确错误信息
- 打印具体缺失项（哪个文件/目录不存在）
- 提供修复建议（如何创建 config/settings.py）
- 使用 exit code 1 退出进程

### Claude's Discretion
- 验证函数的具体实现位置（backend/config/ 或 backend/services/）
- 错误信息的具体格式和文案
- 是否需要 logging vs print

### Deferred Ideas (OUT OF SCOPE)
- ExternalPreconditionBridge 模块实现 — Phase 14
- 前端操作码选择器组件 — Phase 15
- 操作码执行和结果展示 — Phase 16
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| CONFIG-01 | 用户可以在 .env 中配置 WEBSERP_PATH 指向 webseleniumerp 项目路径 | Pydantic BaseSettings pattern (settings.py) |
| CONFIG-02 | 系统启动时验证 WEBSERP_PATH 路径有效性 | FastAPI lifespan validation pattern |
| CONFIG-03 | 提供 webseleniumerp 的 config/settings.py 模板文档 | README.md documentation pattern |
</phase_requirements>

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| pydantic-settings | 2.x | Configuration management | Existing pattern in settings.py |
| FastAPI | 0.135.1+ | Lifespan events for validation | Existing startup hook in main.py |
| Python pathlib | stdlib | Path validation | Cross-platform path handling |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| sys | stdlib | Module import testing | Validate external module can be imported |
| os | stdlib | Environment access | Reading WEBSERP_PATH from .env |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| FastAPI lifespan validation | Middleware validation | Lifespan is cleaner, runs once at startup |
| print() for errors | logging module | print() simpler for startup errors; logging better for runtime |

**Installation:**
No new packages required — all functionality uses standard library and existing pydantic-settings.

## Architecture Patterns

### Recommended Project Structure
```
backend/
├── config/
│   ├── settings.py          # Add weberp_path field
│   └── validators.py        # NEW: startup validation functions (Claude's discretion)
├── api/
│   └── main.py              # Add validation call in lifespan
└── tests/
    └── unit/
        └── test_config_validation.py  # NEW: unit tests for validation
```

### Pattern 1: Pydantic Settings Extension
**What:** Add `weberp_path` field to existing Settings class
**When to use:** All configuration through Settings singleton
**Example:**
```python
# Source: existing backend/config/settings.py pattern
class Settings(BaseSettings):
    # ... existing fields ...

    # External webseleniumerp project path
    # Used to import base_prerequisites.py for precondition operations
    weberp_path: str | None = None
```

### Pattern 2: FastAPI Lifespan Validation
**What:** Validate configuration during application startup
**When to use:** Fail-fast on invalid configuration
**Example:**
```python
# Source: existing backend/api/main.py lifespan pattern
@asynccontextmanager
async def lifespan(app: FastAPI):
    # ... existing startup code ...

    # Validate WEBSERP_PATH if configured
    settings = get_settings()
    if settings.weberp_path:
        validate_weberp_path(settings.weberp_path)

    yield
    # ... shutdown code ...
```

### Pattern 3: Validation Function with Clear Errors
**What:** Dedicated validation function with actionable error messages
**When to use:** Configuration validation that needs detailed error reporting
**Example:**
```python
# Source: recommended pattern for this phase
def validate_weberp_path(path: str) -> None:
    """Validate webseleniumerp project path.

    Raises:
        SystemExit: If validation fails, with clear error message
    """
    from pathlib import Path

    weberp_dir = Path(path)

    # Check 1: Directory exists
    if not weberp_dir.exists():
        print(f"\n[CONFIG ERROR] WEBSERP_PATH directory not found: {path}")
        print("  Solution: Verify the path in your .env file")
        sys.exit(1)

    # Check 2: base_prerequisites.py exists
    base_prereq = weberp_dir / "base_prerequisites.py"
    if not base_prereq.exists():
        print(f"\n[CONFIG ERROR] base_prerequisites.py not found at: {base_prereq}")
        print("  Solution: Ensure webseleniumerp project is correctly cloned")
        sys.exit(1)

    # Check 3: config/settings.py exists
    config_file = weberp_dir / "config" / "settings.py"
    if not config_file.exists():
        print(f"\n[CONFIG ERROR] config/settings.py not found at: {config_file}")
        print("  This file is in webseleniumerp's .gitignore and must be created manually.")
        print("  Create the file with the following content:")
        print("""
# webseleniumerp config/settings.py
DATA_PATHS = {
    'test_data': '/path/to/your/test/data',
    # Add other paths as needed
}
""")
        sys.exit(1)

    # Check 4: Module import test (shallow)
    try:
        sys.path.insert(0, str(weberp_dir))
        import importlib.util
        spec = importlib.util.spec_from_file_location("base_prerequisites", base_prereq)
        if spec is None:
            raise ImportError("Cannot load module spec")
    except Exception as e:
        print(f"\n[CONFIG ERROR] Cannot import base_prerequisites: {e}")
        sys.exit(1)
```

### Anti-Patterns to Avoid
- **Silent failure on missing config**: Don't start the server if WEBSERP_PATH is invalid
- **Hardcoded paths**: Never hardcode paths in code, always use environment variables
- **Partial validation**: Validate all requirements (path, files, importability) together
- **Executing external code during validation**: Only test import capability, don't run code

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Path validation | Custom string parsing | pathlib.Path | Cross-platform, handles edge cases |
| Config loading | Manual .env parsing | pydantic-settings | Existing pattern, type-safe |
| Module import test | exec() or eval() | importlib.util | Safer, doesn't execute code |

**Key insight:** The validation should be lightweight — test that imports work without executing any actual code from the external project.

## Common Pitfalls

### Pitfall 1: config/settings.py Missing in External Project
**What goes wrong:** webseleniumerp has config/settings.py in .gitignore, so cloning the repo doesn't include it
**Why it happens:** The file contains user-specific data paths, so it's intentionally excluded from version control
**How to avoid:** Document this clearly in README.md with a copy-paste template
**Warning signs:** ImportError when trying to use base_prerequisites

### Pitfall 2: Relative Path Confusion
**What goes wrong:** User provides relative path like `../webseleniumerp` which doesn't resolve correctly
**Why it happens:** Working directory varies (project root vs backend/ vs tests/)
**How to avoid:** Resolve to absolute path during validation, document requirement for absolute paths
**Warning signs:** Path.exists() returns False even when directory exists

### Pitfall 3: WEBSERP_PATH Optional but Validation Required
**What goes wrong:** WEBSERP_PATH is optional (can be None), but if set, must be valid
**Why it happens:** Not all users need external precondition support
**How to avoid:** Only validate when WEBSERP_PATH is set (not None/empty)
**Warning signs:** Server fails to start even though feature isn't being used

### Pitfall 4: Import Side Effects
**What goes wrong:** Importing base_prerequisites.py triggers code execution (e.g., database connections)
**Why it happens:** Python executes module-level code during import
**How to avoid:** Use importlib.util.spec_from_file_location for shallow import test
**Warning signs:** Validation hangs or fails due to missing runtime dependencies

## Code Examples

### Adding weberp_path to Settings
```python
# Source: backend/config/settings.py (extend existing class)
class Settings(BaseSettings):
    # ... existing fields ...

    # External webseleniumerp project path for precondition operations
    # Set this to enable importing base_prerequisites.py
    # Example: /Users/you/projects/webseleniumerp
    weberp_path: str | None = None
```

### Updating .env.example
```bash
# Source: .env.example pattern
# ============================================
# External Precondition Module Configuration
# ============================================
# Path to webseleniumerp project (optional)
# Required for using external precondition operations (FA1, HC1, etc.)
# WEBSERP_PATH=/path/to/webseleniumerp
```

### README.md Documentation Section
```markdown
## webseleniumerp Configuration

To use external precondition operations from the webseleniumerp project:

### 1. Configure Environment Variable

Add to your `.env` file:
\`\`\`env
WEBSERP_PATH=/path/to/your/webseleniumerp
\`\`\`

### 2. Create config/settings.py

The webseleniumerp project requires a `config/settings.py` file (in .gitignore).
Create it with the following content:

\`\`\`python
# webseleniumerp/config/settings.py

# Data paths for test data files
DATA_PATHS = {
    'test_data': '/path/to/your/test/data',
    # Add other paths as needed by your precondition operations
}
\`\`\`

### 3. Verify Configuration

Start the server. If configuration is invalid, you'll see an error message
with specific instructions for fixing the issue.
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Hardcoded module paths | Environment variable configuration | v0.3 | Flexible deployment |
| Runtime import errors | Startup validation | v0.3 | Fail-fast, clear errors |

**Deprecated/outdated:**
- Direct sys.path manipulation without validation: Now use validated configuration

## Open Questions

1. **Should validation be in backend/config/ or backend/services/?**
   - What we know: Both locations are valid; services/ is more business-logic focused
   - What's unclear: Which aligns better with project conventions
   - Recommendation: Create `backend/config/validators.py` since it's configuration validation

2. **Should we cache the validated path for later use by Phase 14?**
   - What we know: Phase 14 will need to use the validated path for imports
   - What's unclear: Whether to store in Settings singleton or separate module
   - Recommendation: Store in Settings, access via get_settings().get_weberp_path() helper

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | pytest |
| Config file | None — uses auto-discovery |
| Quick run command | `uv run pytest backend/tests/unit/test_config_validation.py -v` |
| Full suite command | `uv run pytest backend/tests/ -v` |

### Phase Requirements → Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| CONFIG-01 | weberp_path field in Settings | unit | `pytest backend/tests/unit/test_config_validation.py::test_settings_has_weberp_path -v` | ❌ Wave 0 |
| CONFIG-02 | Startup validation fails on invalid path | unit | `pytest backend/tests/unit/test_config_validation.py::test_validate_invalid_path -v` | ❌ Wave 0 |
| CONFIG-02 | Startup validation passes on valid path | unit | `pytest backend/tests/unit/test_config_validation.py::test_validate_valid_path -v` | ❌ Wave 0 |
| CONFIG-02 | Startup validation skips when path is None | unit | `pytest backend/tests/unit/test_config_validation.py::test_validate_none_path -v` | ❌ Wave 0 |
| CONFIG-03 | README contains config/settings.py template | manual | N/A | N/A |

### Sampling Rate
- **Per task commit:** `uv run pytest backend/tests/unit/test_config_validation.py -v`
- **Per wave merge:** `uv run pytest backend/tests/ -v`
- **Phase gate:** Full suite green before `/gsd:verify-work`

### Wave 0 Gaps
- [ ] `backend/tests/unit/test_config_validation.py` — covers CONFIG-01, CONFIG-02
- [ ] `backend/config/validators.py` — validation functions to be tested
- [ ] Framework config: None needed (pytest auto-discovery works)

## Sources

### Primary (HIGH confidence)
- `backend/config/settings.py` — Existing Pydantic Settings pattern
- `backend/api/main.py` — Existing FastAPI lifespan pattern
- `.env.example` — Existing environment variable template format

### Secondary (MEDIUM confidence)
- `.planning/research/SUMMARY.md` — v0.3 architecture research
- `.planning/phases/01-foundation-fixes/01-CONTEXT.md` — Phase 1 configuration decisions

### Tertiary (LOW confidence)
- None — all patterns derived from existing codebase

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — Uses existing patterns (Pydantic Settings, FastAPI lifespan)
- Architecture: HIGH — Follows established project conventions
- Pitfalls: HIGH — Based on direct codebase analysis and webseleniumerp structure

**Research date:** 2026-03-17
**Valid until:** 30 days — stable configuration patterns
