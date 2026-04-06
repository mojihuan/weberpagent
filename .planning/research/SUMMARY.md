# Project Research Summary

**Project:** aiDriveUITest -- v0.8.4 DOM Patch Optimization
**Domain:** AI-driven UI automation testing -- ERP table interaction reliability
**Researched:** 2026-04-06
**Confidence:** HIGH

## Executive Summary

This is an internal optimization milestone for an existing AI-driven UI test platform. The product uses browser-use (v0.12.2) to drive a browser agent that fills ERP (Ant Design) table cells. The agent currently fails in loops because it cannot distinguish table rows, has no memory of past failures, and cannot adapt its interaction strategy. The four optimizations (OPTIMIZE-01 through OPTIMIZE-04) -- row identity injection, failure tracking with dynamic annotation, strategy prioritization, and failure recovery -- are entirely implemented within the existing monkey-patch architecture across four files. No new dependencies or modules are needed.

The recommended approach follows a strict dependency chain: row identity detection first, then failure tracking state, then strategy levels, then recovery logic. All new code is additive to existing files (`dom_patch.py`, `stall_detector.py`, `agent_service.py`, `prompts.py`). State flows through module-level dicts (matching the existing `_PATCHED` pattern), and annotations are injected into the DOM dump as HTML comments that the LLM agent reads. Total estimated change: 270-410 lines.

The key risks are: (1) module-level failure tracker state leaking across test runs due to the idempotent `apply_dom_patch()` guard, (2) interactive index instability across re-serializations causing annotations to appear on wrong elements, and (3) strategy annotations biasing the LLM toward using `evaluate` JS (strategy 3) when simpler `input()` actions would work. Each has clear prevention strategies documented below.

## Key Findings

### Recommended Stack

No new external dependencies are required. The entire v0.8.4 milestone is built on Python stdlib and browser-use internal APIs that are already monkey-patched by the existing codebase.

**Core technologies:**
- **browser-use 0.12.2 internal APIs** (`DOMTreeSerializer`, `SimplifiedNode`, `EnhancedDOMTreeNode`) -- all verified against installed source; the patch targets are stable static/instance methods
- **Python `re` (stdlib)** -- `I\d{15}` pattern for IMEI-based row identity detection
- **Python `dataclasses` (frozen=True)** -- immutable result types following existing `StallResult` pattern
- **Python `hashlib` (stdlib)** -- DOM fingerprinting for click-no-effect detection; already used in `agent_service.py`

### Expected Features

**Must have (table stakes):**
- Row identity via IMEI detection -- Agent cannot target the correct row without it; placeholder text is duplicated across rows
- Failure tracker state -- Without memory, the Agent retries the same failing action indefinitely
- Dynamic annotation in DOM dump -- Agent needs per-element failure hints embedded directly in what it reads
- Strategy level annotation (3 tiers) -- Agent must know whether to use native `input()`, click-to-edit then `input()`, or `evaluate` JS
- Failure recovery for click-no-effect -- The most common failure mode in ERP tables
- Prompt Section 9 updates -- Agent needs explicit rules for reading new annotations

**Should have (differentiators):**
- Automatic strategy downgrade -- After 2 failures, change annotation so Agent naturally switches approach without explicit messages
- Edit-state misjudgment recovery -- Guide Agent through correct click-then-wait-then-input workflow

**Defer:**
- Wrong-column detection -- Lower frequency failure mode; cross-references two subsystems; can be added incrementally
- Persistent failure tracker across runs -- Explicitly rejected; clean slate per run
- ML-based failure classification -- Over-engineered for 3 known modes
- Visual/screenshot-based column identification -- Unreliable for text-heavy ERP tables

### Architecture Approach

All changes fit into the existing layered architecture: `agent_service.py` orchestrates, `dom_patch.py` monkey-patches browser-use internals, `stall_detector.py` detects anomalies, `monitored_agent.py` bridges detectors to the agent loop, and `prompts.py` extends the system message. No new modules are created. New patches follow the save-original-wrap-replace pattern. State uses module-level dicts keyed by `backend_node_id`. Annotations are injected during DOM serialization and consumed by the LLM in the next step.

**Major components:**
1. **Patch 4 enhancement** (`dom_patch.py`) -- Extends `_assign_interactive_indices` wrapper with row identity detection and strategy level determination
2. **Patch 6 (new)** (`dom_patch.py`) -- Row identity comment injection via `serialize_tree` wrapping
3. **Patch 7 (new)** (`dom_patch.py`) -- Dynamic failure annotation injection, reads `_failure_tracker` during serialization
4. **Failure tracker state** (`dom_patch.py`) -- Module-level `dict[int, FailureRecord]` with `update_failure_tracker()` and `reset_failure_tracker()`
5. **StallDetector extension** (`stall_detector.py`) -- New `detect_failure_mode()` method returning `FailureDetectionResult`
6. **step_callback wiring** (`agent_service.py`) -- Call `update_failure_tracker()` and `detect_failure_mode()` in existing try/except block
7. **Section 9 prompt additions** (`prompts.py`) -- Four append-only rule blocks for row identity, anti-repeat, strategy, recovery

### Critical Pitfalls

1. **Failure tracker state leaking across runs** -- The `_PATCHED` guard in `apply_dom_patch()` prevents reset code from running after the first call. Use a separate `reset_failure_tracker()` function called per-run, not inside the idempotent patch registration.
2. **Interactive index mismatch across re-serializations** -- DOM indices change every step. Do NOT use index as the key for `_failure_tracker`; use `backend_node_id` (Chromium's stable node ID) instead.
3. **Strategy annotations biasing Agent toward evaluate JS** -- Only annotate strategy 3 when strategies 1 and 2 have actually failed. Do not annotate all elements with all strategy options. No annotation means "use normal input()".
4. **Multiple patches on `_assign_interactive_indices` creating wrapping chains** -- Merge row identity and strategy logic into the existing Patch 4 wrapper; do not create separate patch functions that stack.
5. **DOM hash unchanged false positives** -- Do not trigger "click no effect" from DOM hash alone; require both hash match AND failure keyword in evaluation. Consider threshold of 2 instead of 1.

## Implications for Roadmap

Based on research, suggested phase structure follows the dependency chain:

### Phase 1: Foundation (Row Identity + Failure State)
**Rationale:** These are leaf dependencies. Row identity detection (T01) and failure tracker state (T07-T08) have no dependencies on each other or on later features. They must be correct before anything is built on top.
**Delivers:** `_detect_row_identity()` helper, `_failure_tracker` state management, `update_failure_tracker()` function, `reset_failure_tracker()` function, StallDetector `detect_failure_mode()` method (T11)
**Addresses:** OPTIMIZE-01 core, OPTIMIZE-02 state layer
**Avoids:** Pitfall 1 (state leaking) via separate reset function; Pitfall 11 (index mismatch) via `backend_node_id` keying
**Estimated LOC:** ~120 lines across 2 files

### Phase 2: DOM Patch Enhancements (Annotation Injection)
**Rationale:** Builds on Phase 1's helpers and state. All annotation injection into the DOM dump happens here. This is the highest technical risk phase because it touches the serialization pipeline.
**Delivers:** Patch 4 enhancement with row identity + strategy (T04-T06), Patch 6 row identity injection (T02-T03), Patch 7 dynamic annotation (T09-T10)
**Addresses:** OPTIMIZE-01 injection, OPTIMIZE-02 annotation, OPTIMIZE-03 strategy levels
**Avoids:** Pitfall 2 (parser breaking) via module-level dict storage and proper serialize_tree wrapping; Pitfall 6 (patch ordering) by merging into single Patch 4 wrapper; Pitfall 3 (strategy bias) by only annotating failed strategies
**Estimated LOC:** ~180 lines in dom_patch.py

### Phase 3: Service Wiring + Prompts (Integration)
**Rationale:** Connects the monitoring layer to DOM patch state, then adds the prompt rules the Agent needs. Prompts reference actual annotation formats from Phase 2.
**Delivers:** step_callback integration (T12), state reset per-run, Section 9 prompt additions (T13-T16)
**Addresses:** OPTIMIZE-02 wiring, OPTIMIZE-04 failure recovery
**Avoids:** Pitfall 8 (prompt bloat) by capping each rule block at 3-5 lines; Pitfall 9 (intervention flooding) by capping messages per step
**Estimated LOC:** ~55 lines across 2 files

### Phase 4: E2E Validation + Tuning
**Rationale:** The system must be validated end-to-end with the full sales outbound scenario. Threshold tuning (failure counts, strategy downgrade triggers) requires real execution data.
**Delivers:** Validated E2E test, tuned thresholds, documented baseline improvement
**Avoids:** Pitfall 7 (DOM hash false positives) by calibrating threshold against real data; Pitfall 10 (snapshot_node unreliability) by testing strategy stability across steps; Pitfall 15 (React state not updated) by verifying evaluate JS includes event dispatch
**Estimated LOC:** ~20 lines of threshold constants + test code

### Phase Ordering Rationale

- Phase 1 before Phase 2 because row identity and failure tracker are data dependencies for annotation injection
- Phase 2 before Phase 3 because prompts must reference the actual annotation formats that the patches produce
- Phase 4 after all implementation because thresholds can only be tuned with real execution data
- Patch 4 enhancements (row identity + strategy) are merged into a single wrapper to avoid multi-layer wrapping chains

### Research Flags

Phases likely needing deeper research during planning:
- **Phase 2:** The `serialize_tree()` wrapping approach for annotation injection needs validation against actual browser-use output format. The ARCHITECTURE research identified two approaches (text post-processing vs node-level data storage); the choice should be confirmed with a small prototype.
- **Phase 4:** Qwen 3.5 Plus instruction-following behavior with strategy annotations is not empirically verified. The PITFALLS research flagged strategy bias risk based on general LLM behavior patterns, not Qwen-specific testing.

Phases with standard patterns (skip research-phase):
- **Phase 1:** All patterns are well-established in the existing codebase. `_detect_row_identity()` is a DOM traversal helper matching `_is_textual_td_cell()`. Failure tracker is a module-level dict matching `_PATCHED`.
- **Phase 3:** step_callback wiring follows the exact pattern of existing detector calls. Prompt additions are append-only text.

## Confidence Assessment

| Area | Confidence | Notes |
|------|------------|-------|
| Stack | HIGH | All internal APIs verified against installed browser-use 0.12.2 source code. No new dependencies. |
| Features | HIGH | Feature set derived from direct analysis of existing codebase failure modes and the Phase 66 design document. |
| Architecture | HIGH | All integration points verified by reading source code. Serialization pipeline order confirmed. Module-level state pattern is established. |
| Pitfalls | HIGH | All critical pitfalls identified from direct code analysis of `apply_dom_patch()`, step_callback, serialization pipeline. |

**Overall confidence:** HIGH

### Gaps to Address

- **`backend_node_id` stability:** Research assumes Chromium `backend_node_id` is stable across steps within the same page load. This needs validation during Phase 1 implementation. If unstable, fall back to `(tag_name, placeholder, row_identity)` composite key.
- **`snapshot_node` reliability for strategy detection:** The ARCHITECTURE research recommends combining `snapshot_node` with `is_visible` and bounding box checks, but the exact composite logic needs tuning against real ERP DOM. Flag for Phase 4.
- **Qwen 3.5 Plus annotation interpretation:** The LLM's actual behavior when reading HTML comment annotations in DOM dumps is not tested. Phase 4 E2E validation should specifically track strategy selection accuracy.
- **Evaluate JS event dispatch:** The prompt must include React `dispatchEvent` patterns for strategy 3. The exact event sequence (`input` + `change` + potentially `blur`) needs verification against Ant Design's Input component behavior.

## Sources

### Primary (HIGH confidence)
- `backend/agent/dom_patch.py` -- 5 existing patches, monkey-patch patterns, `_PATCHED` state management (329 lines)
- `backend/agent/stall_detector.py` -- `StallDetector.check()`, `StallResult(frozen=True)` (138 lines)
- `backend/agent/monitored_agent.py` -- `_pending_interventions` injection, step_callback structure (239 lines)
- `backend/core/agent_service.py` -- step_callback detector calls (lines 302-337), `apply_dom_patch()` call (line 357) (447 lines)
- `backend/agent/prompts.py` -- ENHANCED_SYSTEM_MESSAGE Section 9 (lines 52-83) (97 lines)
- `.venv/.../browser_use/dom/serializer/serializer.py` -- DOMTreeSerializer pipeline, `serialize_tree()` method (1276 lines)
- `.venv/.../browser_use/dom/views.py` -- `SimplifiedNode` (slots=True), `EnhancedDOMTreeNode`, `SerializedDOMState`
- `.planning/milestones/v0.8.3-phases/66-优化方案设计/66-OPTIMIZE-DESIGN.md` -- Design document with 16 tasks (T01-T16) (540 lines)

### Secondary (MEDIUM confidence)
- LLM instruction-following behavior for strategy annotation bias (general LLM patterns, not Qwen-specific)
- React synthetic event behavior for evaluate JS workaround (well-established React behavior)
- Playwright DOM serialization and element visibility detection (from training data)

---
*Research completed: 2026-04-06*
*Ready for roadmap: yes*
