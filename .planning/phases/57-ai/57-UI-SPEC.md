---
phase: 57
slug: ai-reasoning-format
status: draft
shadcn_initialized: false
preset: none
created: 2026-04-02
---

# Phase 57 — UI Design Contract

> Visual and interaction contract for AI reasoning text formatting. Replaces pipe-delimited single-line text with labeled, color-coded badge rows. Covers ReasoningLog (execution monitor) and StepItem (report detail) components.

---

## Design System

| Property | Value |
|----------|-------|
| Tool | none (raw Tailwind CSS v4) |
| Preset | not applicable |
| Component library | none |
| Icon library | Lucide React (not used in this phase) |
| Font | system default (sans-serif) |

---

## Spacing Scale

Declared values (must be multiples of 4):

| Token | Value | Usage |
|-------|-------|-------|
| xs | 4px (`gap-1`) | Badge-to-content inline gap |
| sm | 8px (`gap-2`, `p-2`) | Badge row internal gap, segment padding |
| md | 16px (`space-y-4`, `p-4`) | Step-level spacing, container padding |
| lg | 24px | Not used in this phase |
| xl | 32px | Not used in this phase |
| 2xl | 48px | Not used in this phase |
| 3xl | 64px | Not used in this phase |

Exceptions: none

---

## Typography

| Role | Size | Weight | Line Height |
|------|------|--------|-------------|
| Badge label | 12px (`text-xs`) | 500 (`font-medium`) | default (1.33) |
| Reasoning body | 14px (`text-sm`) | 400 (normal) | default (1.5) |
| Section heading | 14px (`text-sm`, `font-medium`) | 500 (`font-medium`) | default (1.5) |
| Empty state | 14px (`text-sm`) | 400 (normal, italic) | default (1.5) |

Notes:
- Badge labels use `text-xs font-medium` matching the existing Action/Error badge pattern from `ReasoningLog.tsx` lines 33-35 and `StatusBadge.tsx`.
- Reasoning body text uses `text-sm` matching the existing `step.reasoning` rendering in both `ReasoningLog.tsx` and `StepItem.tsx`.

---

## Color

### Surface Colors (existing, unchanged)

| Role | Value | Usage |
|------|-------|-------|
| Dominant (60%) | `bg-white` / `bg-gray-50` | Page background, card backgrounds |
| Secondary (30%) | `bg-gray-100` | Section dividers, inactive badge backgrounds |
| Destructive | `bg-red-100 text-red-700` | Error badge (existing, unchanged) |

### Reasoning Label Badge Colors (new for this phase)

| Label | Background | Text | Hex Reference |
|-------|-----------|------|---------------|
| Eval | `bg-purple-100` | `text-purple-700` | badge bg #F3E8FF / text #7E22CE |
| Verdict | `bg-green-100` | `text-green-700` | badge bg #DCFCE7 / text #15803D |
| Memory | `bg-orange-100` | `text-orange-700` | badge bg #FFEDD5 / text #C2410C |
| Goal | `bg-blue-100` | `text-blue-700` | badge bg #DBEAFE / text #1D4ED8 |
| Unlabeled | `bg-gray-100` | `text-gray-600` | fallback for non-standard text |

Accent reserved for: Goal badge (`bg-blue-100 text-blue-700`) and existing Action badge. These are the primary navigational/decision labels in the reasoning display.

Color source: CONTEXT.md D-05 (locked), mapped to Tailwind utility classes.

---

## Component Inventory

### New Files

| File | Type | Purpose |
|------|------|---------|
| `frontend/src/utils/reasoningParser.ts` | Utility (pure function) | Parse pipe-delimited reasoning text into structured segments |
| `frontend/src/components/shared/ReasoningText.tsx` | Component | Render parsed reasoning segments as badge + text rows |

### Modified Files

| File | Change | Lines Affected |
|------|--------|----------------|
| `frontend/src/components/RunMonitor/ReasoningLog.tsx` | Replace reasoning render block (lines 40-47) with `<ReasoningText>` | 40-47 |
| `frontend/src/components/Report/StepItem.tsx` | Replace reasoning render block (lines 112-117) with `<ReasoningText>` | 112-117 |
| `frontend/src/components/shared/index.ts` | Add `ReasoningText` export | 1 line addition |

### Shared Exports

Add to `frontend/src/components/shared/index.ts`:
```
export { ReasoningText } from './ReasoningText'
```

---

## Visual Specification

### Reasoning Segment Row

Each parsed segment renders as a horizontal row:

```
+--------+---------------------------------------------+
| [Eval] | Agent initialized, no previous action to...  |
+--------+---------------------------------------------+
| [Vrdt] | N/A                                         |
+--------+---------------------------------------------+
| [Mem]  | Starting the ERP test task...               |
+--------+---------------------------------------------+
| [Goal] | Navigate to the target URL...               |
+--------+---------------------------------------------+
```

- Badge: `inline-flex items-center px-2 py-0.5 rounded text-xs font-medium shrink-0 {badge-color-class}`
- Content: `text-sm text-gray-600`
- Row layout: `flex items-start gap-2`
- Rows container: `space-y-1`

### Badge Label Text

| Label | Badge Display Text |
|-------|--------------------|
| Eval | `Eval` |
| Verdict | `Verdict` |
| Memory | `Memory` |
| Goal | `Goal` |
| (unlabeled) | no badge, plain text only |

### Integration Point 1: ReasoningLog.tsx

**Before** (current, lines 40-47):
```tsx
{step.reasoning && (
  <div className="flex items-start gap-2">
    <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-gray-100 text-gray-600 shrink-0">
      Reasoning
    </span>
    <span className="text-sm text-gray-600">{step.reasoning}</span>
  </div>
)}
```

**After**:
```tsx
{step.reasoning && (
  <ReasoningText text={step.reasoning} />
)}
```

The wrapper `<div className="flex items-start gap-2">` is removed because `ReasoningText` handles its own layout internally with `space-y-1` containing individual `flex items-start gap-2` rows.

### Integration Point 2: StepItem.tsx

**Before** (current, lines 112-117):
```tsx
{step.reasoning ? (
  <p className="text-sm text-gray-600 whitespace-pre-wrap">{step.reasoning}</p>
) : (
  <p className="text-sm text-gray-400 italic">暂无推理记录</p>
)}
```

**After**:
```tsx
{step.reasoning ? (
  <ReasoningText text={step.reasoning} />
) : (
  <p className="text-sm text-gray-400 italic">暂无推理记录</p>
)}
```

### Fallback Behavior

| Input | Behavior |
|-------|----------|
| `null` / `undefined` reasoning | Show "暂无推理记录" in italic gray (existing, unchanged at component level) |
| Empty string `""` | Parser returns empty array; `ReasoningText` renders `<span className="text-sm text-gray-600">{text}</span>` (the empty string) — but the parent components already gate on `step.reasoning` truthiness, so this path is not reachable |
| Non-matching text (no labels) | Each segment gets `label: ""`, rendered as plain `<span className="text-sm text-gray-600">{content}</span>` without a badge |
| Partial labels (e.g. only Eval + Goal) | Only matching segments get badges; missing segments simply do not appear |

---

## Copywriting Contract

| Element | Copy |
|---------|------|
| Primary CTA | Not applicable — this phase has no buttons or CTAs |
| Empty state heading | "暂无推理记录" (existing, D-08 locked) |
| Empty state body | Not applicable — single-line italic fallback only |
| Error state | Not applicable — no error states introduced in this phase |
| Destructive confirmation | Not applicable — no destructive actions in this phase |

Badge labels are technical terms (Eval, Verdict, Memory, Goal) that match the backend field names. No localization or alternative labels needed.

---

## Parsing Logic Contract

### Input Format (from backend, READ ONLY)

```python
# agent_service.py:252-262
parts = []
if evaluation_previous_goal:
    parts.append(f"Eval: {evaluation_previous_goal}")
if memory:
    parts.append(f"Memory: {memory}")
if next_goal:
    parts.append(f"Goal: {next_goal}")
reasoning = " | ".join(parts)
```

Verdict is embedded by the LLM inside the Eval value text:
```
Eval: [some text] Verdict: [verdict value] | Memory: [text] | Goal: [text]
```

### Parser Specification

```
Function: parseReasoning(text: string) => ReasoningSegment[]

ReasoningSegment = { label: string, content: string }

Algorithm:
1. If text is falsy or whitespace-only, return []
2. Split text by " | " (pipe with spaces) into parts
3. For each part:
   a. Match /^(Eval|Memory|Goal)\s*:\s*(.*)/i (case-insensitive)
   b. If match found:
      - If label is "Eval":
        * Check value for embedded Verdict: /Verdict\s*:\s*(.*)/i
        * If Verdict found: split Eval content at Verdict position
        * Push { label: "Eval", content: evalPartBeforeVerdict } (if non-empty)
        * Push { label: "Verdict", content: verdictValue }
      - Else: push { label: matchedLabel, content: value }
   c. If no match and part is non-empty: push { label: "", content: part.trim() }
4. Return segments array
```

---

## Registry Safety

| Registry | Blocks Used | Safety Gate |
|----------|-------------|-------------|
| none | not applicable | shadcn not initialized; no third-party registries |

---

## Checker Sign-Off

- [ ] Dimension 1 Copywriting: PASS
- [ ] Dimension 2 Visuals: PASS
- [ ] Dimension 3 Color: PASS
- [ ] Dimension 4 Typography: PASS
- [ ] Dimension 5 Spacing: PASS
- [ ] Dimension 6 Registry Safety: PASS

**Approval:** pending
