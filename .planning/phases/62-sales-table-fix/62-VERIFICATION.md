---
phase: 62-sales-table-fix
verified: 2026-04-04T12:00:00Z
status: human_needed
score: 3/4 must-haves verified (1 requires human)
re_verification: false
human_verification:
  - test: "E2E verification of sales outbound table filling"
    expected: "Agent locates td cell for sales amount, clicks to enter edit mode, fills 150, fills logistics, submits successfully"
    why_human: "E2E run aa7a4f49 reported success in commit 38b7e9d, but automated verifier cannot re-run browser-use agent against live ERP to independently confirm"
---

# Phase 62: Sales Outbound Table Fix Verification Report

**Phase Goal:** Fix the AI agent's inability to locate and fill the "sales amount" input field in the sales outbound page by extending DOM patch and adding prompt guidance.
**Verified:** 2026-04-04
**Status:** human_needed
**Re-verification:** No -- initial verification

## Goal Achievement

### Observable Truths

Truths derived from ROADMAP success_criteria, adjusted for the documented pivot from input placeholder detection to td text content detection.

| # | Truth | Status | Evidence |
|---|-------|--------|----------|
| 1 | `dom_patch.apply_dom_patch()` calls all 5 patch behaviors (is_interactive with ERP classes + td cells, paint_order, should_exclude_child, assign_interactive_indices) | VERIFIED | `apply_dom_patch()` at line 239-242 calls 4 patch functions; `_patch_is_interactive` handles 2 behaviors (ERP CSS classes + `_is_textual_td_cell` for td cells). Logger reports "successfully applied all 5 patches". |
| 2 | `<td>` cells with text content in sales outbound table get clickable indices in DOM snapshot | VERIFIED | `_is_textual_td_cell()` (line 37-81) checks td tag inside tr, calls `get_all_children_text()` for text content, returns True. Wired into `_patch_is_interactive` at line 206. All helper functions importable. 36 unit tests pass. |
| 3 | `ENHANCED_SYSTEM_MESSAGE` has Section 9 with click-to-edit workflow guidance | VERIFIED | `## 9. ERP` found in prompt string. Contains: click-to-edit workflow (CLICK td -> wait for input -> INPUT), placeholder matching, row targeting, field confusion warning ("do not confuse logistics fee and sales amount"), evaluate JS fallback. `CHINESE_ENHANCEMENT` alias intact. Total 9 `## ` sections. |
| 4 | Sales outbound E2E: sales amount correctly filled to 150 without field confusion | VERIFIED (commit evidence) | Commit 38b7e9d documents: "E2E result: run aa7a4f49 completed 26 steps successfully - item added, sales amount 150 filled via click+input, logistics filled, confirmed with success modal." Cannot independently re-run without live ERP. |

**Score:** 4/4 truths verified (truth 4 based on commit evidence, pending independent human confirmation)

### Required Artifacts

| Artifact | Expected | Status | Details |
|----------|----------|--------|---------|
| `backend/agent/dom_patch.py` | Extended DOM patch with `_is_textual_td_cell`, `_is_inside_table_cell`, `_is_erp_table_cell_input`, `_patch_assign_interactive_indices`; 5 total patch behaviors | VERIFIED | 329 lines. All 4 new helpers present and importable. `_is_textual_td_cell` wired into `_patch_is_interactive`. `_patch_assign_interactive_indices` wired into `apply_dom_patch`. |
| `backend/agent/prompts.py` | ENHANCED_SYSTEM_MESSAGE with Section 9 ERP table cell filling guidance | VERIFIED | 97 lines. Section 9 present with click-to-edit workflow, placeholder matching, row targeting, negative examples, JS fallback. `CHINESE_ENHANCEMENT` alias valid. |

### Key Link Verification

| From | To | Via | Status | Details |
|------|----|-----|--------|---------|
| `_is_textual_td_cell` | `_patch_is_interactive` | Called at line 206 inside patched `is_interactive` | WIRED | td cells with text content marked interactive when `is_interactive` is called |
| `_patch_is_interactive` | `apply_dom_patch` | Called at line 239 | WIRED | First patch applied in `apply_dom_patch()` |
| `_patch_assign_interactive_indices` | `apply_dom_patch` | Called at line 242 | WIRED | Fourth patch applied, forces interactive for ERP table cell inputs |
| `apply_dom_patch` | `browser_agent.py` | Imported and called at line 86 | WIRED | Called before Agent instantiation |
| `apply_dom_patch` | `proxy_agent.py` | Imported and called at line 110 | WIRED | Called before Agent instantiation |
| `apply_dom_patch` | `agent_service.py` | Imported and called at line 357 | WIRED | Called in agent creation flow |
| `ENHANCED_SYSTEM_MESSAGE` | `agent_service.py` | Imported at line 16, passed at line 375 | WIRED | Passed as `extend_system_message` to Agent constructor |
| `CHINESE_ENHANCEMENT` | `browser_agent.py` | Imported at line 15, passed at line 92 | WIRED | Alias works; same object as ENHANCED_SYSTEM_MESSAGE |
| `CHINESE_ENHANCEMENT` | `proxy_agent.py` | Imported at line 17, passed at line 116 | WIRED | Alias works |

### Data-Flow Trace (Level 4)

| Artifact | Data Variable | Source | Produces Real Data | Status |
|----------|---------------|--------|--------------------|--------|
| `dom_patch.py` | `_is_textual_td_cell` return value | `get_all_children_text()` on AccessibilityNode | Real -- recursively collects TEXT_NODE values from DOM | FLOWING |
| `dom_patch.py` | `_is_erp_table_cell_input` return value | Node attributes (placeholder) + parent chain | Real -- checks actual DOM node properties | FLOWING |
| `prompts.py` | `ENHANCED_SYSTEM_MESSAGE` string | Static string constant | Real -- 9 sections of guidance text | FLOWING |

### Behavioral Spot-Checks

| Behavior | Command | Result | Status |
|----------|---------|--------|--------|
| All dom_patch helpers importable | `uv run python -c "from backend.agent.dom_patch import ..."` | "All functions importable: OK" | PASS |
| Section 9 content present | `uv run python -c "assert '## 9.' in ENHANCED_SYSTEM_MESSAGE"` | "prompts.py Section 9: OK, Total ## sections: 9" | PASS |
| CHINESE_ENHANCEMENT alias valid | `uv run python -c "assert ENHANCED_SYSTEM_MESSAGE is CHINESE_ENHANCEMENT"` | "CHINESE_ENHANCEMENT alias: OK" | PASS |
| Unit tests pass | `uv run pytest backend/tests/unit/test_dom_patch.py backend/tests/unit/test_enhanced_prompt.py` | 36 passed, 6 warnings | PASS |

### Requirements Coverage

| Requirement | Source Plan | Description | Status | Evidence |
|-------------|------------|-------------|--------|----------|
| DOM-PATCH-01 | 62-01-PLAN | Extend DOM patch for ERP table cell input visibility | SATISFIED | `_is_textual_td_cell` + `_is_erp_table_cell_input` + `_patch_assign_interactive_indices` all present and wired |
| PROMPT-01 | 62-01-PLAN | Add Section 9 with ERP table cell filling guidance | SATISFIED | Section 9 present with click-to-edit workflow, field confusion warning, row targeting, JS fallback |
| E2E-01 | 62-01-PLAN | E2E verification of sales outbound table filling | SATISFIED (commit evidence) | Commit 38b7e9d documents successful E2E run aa7a4f49 with 26 steps, sales amount 150 filled |

**Note:** Requirements DOM-PATCH-01, PROMPT-01, E2E-01 appear in ROADMAP and PLAN but not in `REQUIREMENTS.md` (which covers v0.8.0 scope only). These are v0.8.1 requirements tracked in ROADMAP. No orphaned requirements found.

**Plan vs Implementation Pivot:**

The PLAN specified `_patch_assign_interactive_indices` as the primary fix targeting input placeholders. During implementation, this was found to be incorrect because Ant Design click-to-edit tables do not render `<input>` elements until the `<td>` cell is clicked. The correct fix was `_is_textual_td_cell()` inside `_patch_is_interactive`, which marks td cells with text content as interactive. Both approaches are implemented (the input placeholder patch is still present as a fallback for when inputs do exist after click), but the td cell detection is the primary mechanism. This pivot is documented in SUMMARY.md deviations and was the correct engineering decision.

### Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
|------|------|---------|----------|--------|
| (none) | - | - | - | No anti-patterns detected |

No TODO/FIXME/PLACEHOLDER comments found. No empty implementations. No console.log statements. No hardcoded empty data values in production code paths. The `_ERP_TABLE_CELL_PLACEHOLDERS` constant is intentionally hardcoded (ERP field names) and correctly implemented as a frozenset.

### Human Verification Required

### 1. E2E Sales Outbound Table Filling

**Test:** Create a sales outbound task in the platform UI with description targeting the sales amount field. Execute and observe the agent's behavior.
**Expected:**
- Agent adds product to table
- Agent clicks the correct td cell for sales amount (not logistics fee)
- Agent fills sales amount = 150
- Agent fills logistics number
- Submit succeeds with success modal
**Why human:** E2E run aa7a4f49 is documented in commit 38b7e9d as successful, but the automated verifier cannot re-run a browser-use agent against a live ERP system to independently confirm. The commit evidence is strong (26 steps, specific values mentioned), but independent re-confirmation would strengthen confidence.

### Gaps Summary

No code gaps found. Both artifacts are substantive, wired, and have flowing data. All 36 unit tests pass. The implementation correctly pivoted from the PLAN's input placeholder approach to td text content detection.

The only item flagged is the E2E verification (truth 4), which is documented as successful in the commit message but was performed by the implementing agent rather than independently verified. If the E2E evidence in the commit is trusted, all 4 truths are verified and the phase goal is achieved.

---

_Verified: 2026-04-04T12:00:00Z_
_Verifier: Claude (gsd-verifier)_
