---
phase: 29-frontend-field-config-ui
plan: 01
subsystem: frontend
tags: [typescript, api-client, types, field-params]
requires: [28-02]
provides: [field-types, listFields-api]
affects: [AssertionConfig, externalAssertionsApi]
tech-stack:
  added: [AssertionFieldInfo, AssertionFieldGroup, AssertionFieldsResponse types]
  patterns: [API client pattern, optional field_params]
key-files:
  created: []
  modified:
    - frontend/src/types/index.ts
    - frontend/src/api/externalAssertions.ts
decisions:
  - field_params is optional for backward compatibility with existing assertions
  - Type structure mirrors backend Pydantic models exactly
metrics:
  duration: 2 min
  completed: "2026-03-22T03:31:00Z"
  tasks: 2
  files: 2
---

# Phase 29 Plan 01: Types and API Client Summary

Extended TypeScript types and API client to support field_params configuration for the three-layer assertion parameter structure.

## One-liner

Added field_params to AssertionConfig and created field discovery types with listFields() API method for accessing /external-assertions/fields endpoint.

## Changes Made

### Task 1: Extend AssertionConfig type and add field types

**File:** `frontend/src/types/index.ts`

- Added `field_params?: Record<string, string>` to AssertionConfig interface for field validation parameters (e.g., `{ saleTime: 'now', salesOrder: 'SA' }`)
- Added `AssertionFieldInfo` interface matching backend FieldInfo model
- Added `AssertionFieldGroup` interface matching backend FieldGroup model
- Added `AssertionFieldsResponse` interface matching backend AssertionFieldsResponse model

**Commit:** f375eda

### Task 2: Add listFields() API method

**File:** `frontend/src/api/externalAssertions.ts`

- Imported `AssertionFieldsResponse` type
- Added `listFields()` method to `externalAssertionsApi` object
- Method calls `/external-assertions/fields` endpoint and returns `Promise<AssertionFieldsResponse>`

**Commit:** a78f374

## Verification Results

- TypeScript compilation: PASSED (no errors)
- AssertionConfig.field_params exists: VERIFIED
- AssertionFieldInfo, AssertionFieldGroup, AssertionFieldsResponse types exist: VERIFIED
- listFields() method exists and returns correct type: VERIFIED

## Deviations from Plan

None - plan executed exactly as written.

## Key Decisions

1. **field_params is optional** - Maintains backward compatibility with existing assertions that don't use field validation
2. **Type names match backend** - AssertionFieldInfo, AssertionFieldGroup, AssertionFieldsResponse mirror backend Pydantic models

## Files Modified

| File | Changes |
|------|---------|
| frontend/src/types/index.ts | Added field_params to AssertionConfig, added 3 new field interfaces |
| frontend/src/api/externalAssertions.ts | Added listFields() method with proper typing |

## Dependencies

- Requires Phase 28 Plan 02 (fields API endpoint)
- Provides types and API for Phase 29 Plan 02 (FieldParamsEditor component)

---

## Self-Check: PASSED

- [x] frontend/src/types/index.ts contains field_params in AssertionConfig
- [x] frontend/src/types/index.ts contains AssertionFieldInfo, AssertionFieldGroup, AssertionFieldsResponse
- [x] frontend/src/api/externalAssertions.ts contains listFields method
- [x] Commits f375eda and a78f374 exist
