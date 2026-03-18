# Deferred Items

## Pre-existing Issues (Out of Scope)

### Test Failure: test_is_available_returns_false_when_not_configured

**Location:** backend/tests/unit/test_external_bridge.py::TestExternalPreconditionBridgeBasics::test_is_available_returns_false_when_not_configured

**Issue:** Test expects `is_available()` to return `False` when WEBSERP_PATH is not configured. However, the test environment has WEBSERP_PATH configured, causing `is_available()` to return `True`.

**Why deferred:** This is a pre-existing test failure, Not introduced by Phase 17-01 changes. The test environment configuration differs from the test's assumptions.

**Recommendation:** Either:
1. Mock the settings in this test to ensure WEBSERP_PATH is not set
2. Or update the test to handle both configured and unconfigured scenarios
