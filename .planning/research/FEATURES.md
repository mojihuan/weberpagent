# Feature Landscape: Table Interaction Optimization (v0.8.4)

**Domain:** AI-driven UI automation testing -- table row identity, failure tracking, strategy prioritization, failure recovery
**Researched:** 2026-04-06
**Scope:** Features for OPTIMIZE-01 through OPTIMIZE-04 only; existing features documented in earlier FEATURES.md

## Table Stakes

Features required for the Agent to reliably fill ERP table cells. Without these, the Agent gets stuck in loops or fills wrong cells.

| Feature | Why Expected | Complexity | Depends On | Notes |
|---------|--------------|------------|------------|-------|
| **Row identity via IMEI detection** | Agent cannot distinguish which row to operate on when multiple rows share the same column placeholder (e.g., `placeholder="销售金额"` appears N times for N products) | Medium | Existing `_is_textual_td_cell()` traversal pattern | Detect IMEI pattern `I\d{15}` in `<td>` child text, inject as HTML comment before the `<tr>` in DOM dump. Straightforward regex + DOM traversal. |
| **Failure tracker state** | Without failure memory, the Agent sees the same DOM dump every step and retries the same failing action indefinitely | Low | Module-level dict pattern (same as existing `_PATCHED`) | `dict[int, dict]` at module scope: `{index: {"count": int, "last_error": str, "mode": str}}`. Simple data structure, well-understood pattern in this codebase. |
| **Dynamic annotation in DOM dump** | Agent needs per-element contextual hints (failure count, strategy suggestion) embedded directly in the DOM dump it reads | Medium | Failure tracker state + serialization pipeline | Must hook into browser-use's DOM text output stage. The monkey-patch pattern is already established (5 patches in dom_patch.py), so the integration surface is known. |
| **Strategy level annotation (3 tiers)** | Agent must know whether to use native `input()`, click-to-edit then `input()`, or `evaluate` JS -- picking wrong strategy wastes steps and causes loops | Medium | Row identity + snapshot_node visibility detection | Strategy 1 (visible input) vs Strategy 2 (hidden/click-to-edit) is determined by `snapshot_node` presence -- a property already used in Patch 4. Strategy 3 is fallback triggered by failure tracker. |
| **Failure recovery for click-no-effect** | Agent clicks a `<td>` but DOM hash does not change -- the most common failure mode in ERP tables | Low | DOM hash comparison in step_callback | step_callback already computes `dom_hash` (agent_service.py line 196). Comparing before/after hashes is a trivial extension of the existing StallDetector pattern. |
| **Prompt Section 9 updates** | Agent needs explicit rules telling it how to read and use the new DOM annotations | Low | All DOM Patch features complete | Append-only to existing Section 9 (prompts.py line 52-83). Low risk, immediate effect on Agent behavior. |

## Differentiators

Features that go beyond basic table filling reliability. These are not strictly required but significantly improve Agent success rate.

| Feature | Value Proposition | Complexity | Depends On | Notes |
|---------|-------------------|------------|------------|-------|
| **Wrong-column detection and correction** | When Agent clicks "total cost" instead of "sales amount", annotate the mistake and highlight the correct column -- preventing repeated mis-targeting | Medium | Row identity (OPTIMIZE-01) + evaluation keyword matching | Requires matching evaluation keywords like "wrong column"/"误点" in StallDetector, then using row identity to locate the correct column. Cross-references two subsystems. |
| **Edit-state misjudgment recovery** | When Agent assumes a `<td>` has entered edit mode (input visible) but it has not, guide the Agent through the correct click-then-wait-then-input workflow | Low | Strategy level annotation | Essentially a special case of strategy downgrade: if Strategy 2 fails because the click did not activate the input, annotate and re-guide. The click-then-wait pattern already exists in Section 9 prompts. |
| **Automatic strategy downgrade** | After 2 failures on same index, automatically change the strategy annotation from Strategy 1 -> 2 or 2 -> 3 in the DOM dump, so the Agent naturally picks the next approach without explicit intervention messages | Medium | Failure tracker + strategy annotation | This is the most impactful differentiator: it makes strategy switching invisible to the Agent. The Agent just sees different annotations in the DOM dump and acts accordingly. Requires careful state management to avoid premature downgrade. |

## Anti-Features

Features to explicitly NOT build for this milestone.

| Anti-Feature | Why Avoid | What to Do Instead |
|--------------|-----------|-------------------|
| **Row identity via custom `data-*` attribute injection** | Requires modifying the ERP application's DOM (writing `data-row-identity` onto `<tr>` elements), which is fragile and assumes write access to the page | Detect IMEI from existing `<td>` text content (read-only approach). Inject as HTML comment in the DOM dump (not the actual DOM). |
| **Persistent failure tracker across runs** | Failure state from one test run poisoning the next; increases complexity for reset logic | Module-level dict reset in `apply_dom_patch()` at run start (matches existing `_PATCHED` pattern). Clean slate every run. |
| **ML-based failure mode classification** | Over-engineering for 3 known failure modes; training data not available; latency concerns | Hardcoded keyword matching in StallDetector (already established pattern with `FAILURE_KEYWORDS` regex). 3 modes, 3 regex sets. |
| **Visual/screenshot-based column identification** | Requires vision model processing per step; latency; unreliable for text-heavy ERP tables | Use DOM text content and placeholder attributes (already available through DOM Patch). Text-based matching is deterministic and fast. |
| **Generic framework for arbitrary table types** | Only ERP Ant Design tables are in scope; generic abstraction adds complexity without benefit | Hardcode ERP-specific patterns (IMEI regex, placeholder list, click-to-edit detection). Optimize for the known use case. |
| **MutationObserver-based real-time DOM tracking** | Requires injecting JS into the page; browser-use sandboxing may block; adds async complexity | Stick with per-step DOM dump snapshot approach (already established). The snapshot-before-action model is sufficient for failure detection. |
| **Rewriting existing patches** | 5 existing patches work; replacing them risks regression | Extend and enhance existing patches (especially Patch 4). Add new patches alongside. Preserve existing behavior. |

## Feature Dependencies

```
OPTIMIZE-01: Row Identity
    _detect_row_identity(tr_node)           -- no deps
    _patch_add_row_identity()               -- depends on _detect_row_identity
    Patch 4 enhancement (row attribution)   -- depends on _patch_add_row_identity
    Section 9 prompt update (row hints)     -- depends on _patch_add_row_identity
    |
    v
OPTIMIZE-02: Failure Tracker
    _failure_tracker dict (module-level)    -- no deps
    update_failure_tracker(index, eval, hash)  -- depends on _failure_tracker
    _patch_dynamic_annotation()             -- depends on _failure_tracker
    Section 9 prompt update (anti-repeat)   -- depends on _patch_dynamic_annotation
    |
    v
OPTIMIZE-03: Strategy Levels
    Strategy level detection in Patch 4     -- depends on Patch 4 enhancement (OPTIMIZE-01)
    _inject_strategy_annotation()           -- depends on strategy detection
    Strategy downgrade via _failure_tracker -- depends on OPTIMIZE-02
    Section 9 prompt update (strategy)      -- depends on _inject_strategy_annotation
    |
    v
OPTIMIZE-04: Failure Recovery
    click-no-effect detection               -- depends on _failure_tracker (OPTIMIZE-02)
    wrong-column detection                  -- depends on row identity (OPTIMIZE-01)
    edit-state misjudgment detection        -- depends on strategy levels (OPTIMIZE-03)
    StallDetector extension (3 modes)       -- depends on all above
    step_callback integration               -- depends on StallDetector extension
    Section 9 prompt update (recovery)      -- depends on all detection logic
```

**Dependency chain:** OPTIMIZE-01 is the foundation. OPTIMIZE-02 builds on the patch infrastructure. OPTIMIZE-03 requires both row identity and failure tracking. OPTIMIZE-04 requires all three. This ordering is enforced by the Phase 66 design document (T01-T16 task numbering).

## Existing Infrastructure These Features Depend On

| Existing Component | How It's Used | File | Risk |
|--------------------|---------------|------|------|
| `_is_textual_td_cell()` | Reuse DOM traversal pattern for row identity detection | dom_patch.py:37-81 | Low -- well-tested pattern |
| `_patch_assign_interactive_indices()` | Enhance with row attribution and strategy level | dom_patch.py:289-328 | Medium -- core patch, must not break existing behavior |
| `apply_dom_patch()` | Register new patches; reset `_failure_tracker` per run | dom_patch.py:214-247 | Low -- additive change |
| `StallDetector.check()` | Extend with 3 failure mode detections | stall_detector.py:53-78 | Medium -- adding new detection alongside existing consecutive-failure and stagnant-DOM checks |
| `step_callback` in agent_service.py | Call `update_failure_tracker()` in detector calls section (line 302-337) | agent_service.py:302-337 | Low -- adding one more call in existing try/except block |
| `_pending_interventions` list | Store failure recovery messages for Agent injection | monitored_agent.py:53 | Low -- same pattern as stall messages |
| Section 9 prompt | Append-only additions for row identity, anti-repeat, strategy, recovery rules | prompts.py:52-83 | Low -- append-only, no modification of existing content |

## MVP Recommendation

**Must-have for v0.8.4:**
1. Row identity (OPTIMIZE-01) -- without this, Agent cannot target the correct row
2. Failure tracker + dynamic annotation (OPTIMIZE-02) -- without this, Agent loops on failures
3. Strategy level annotation (OPTIMIZE-03 core) -- without this, Agent picks wrong strategy

**Should-have (same milestone, second priority):**
4. Click-no-effect recovery (OPTIMIZE-04 partial) -- most common failure mode
5. Edit-state misjudgment recovery (OPTIMIZE-04 partial) -- second most common

**Defer:**
6. Wrong-column detection (OPTIMIZE-04 partial) -- lower frequency failure mode; requires cross-referencing row identity and evaluation keywords; can be added incrementally after core works

## Complexity Assessment

| Feature | Code Changes (estimated LOC) | Files Modified | Testing Difficulty |
|---------|------------------------------|----------------|--------------------|
| Row identity detection | 40-60 lines | dom_patch.py | Medium -- need mock tr/td tree with IMEI text |
| Row identity DOM dump injection | 30-50 lines | dom_patch.py | High -- must hook into browser-use serialization output |
| Failure tracker state | 15-20 lines | dom_patch.py | Low -- pure data structure |
| update_failure_tracker() | 25-35 lines | dom_patch.py | Medium -- keyword matching + hash comparison logic |
| Dynamic annotation patch | 40-60 lines | dom_patch.py | High -- must inject comments into serialized DOM text |
| Strategy level detection | 20-30 lines | dom_patch.py | Medium -- snapshot_node presence check |
| Strategy annotation injection | 30-40 lines | dom_patch.py | High -- same serialization hook as dynamic annotation |
| StallDetector 3-mode extension | 30-50 lines | stall_detector.py | Medium -- extend existing check pattern |
| step_callback integration | 10-15 lines | agent_service.py | Low -- one function call in existing try/except |
| Section 9 prompt additions | 30-50 lines | prompts.py | Low -- text-only, verified by E2E testing |

**Total estimated LOC:** 270-410 lines across 4 files (dom_patch.py bears ~80% of the load).

## Sources

- Phase 66 design document: `.planning/milestones/v0.8.3-phases/66-优化方案设计/66-OPTIMIZE-DESIGN.md`
- Existing DOM Patch implementation: `backend/agent/dom_patch.py` (329 lines, 5 patches)
- StallDetector: `backend/agent/stall_detector.py` (138 lines)
- step_callback integration: `backend/core/agent_service.py` lines 302-337
- MonitoredAgent lifecycle: `backend/agent/monitored_agent.py` (239 lines)
- Phase 65 analysis conclusions (headless not sole root cause, DOM patches browser-mode independent)
- Playwright documentation on DOM serialization and element visibility detection (training data, MEDIUM confidence)
- Browser-use DOM serializer architecture: `ClickableElementDetector`, `PaintOrderRemover`, `DOMTreeSerializer` classes (verified from import paths in dom_patch.py)
