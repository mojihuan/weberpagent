# Deferred Items

## Pre-existing TypeScript Errors (Out of Scope)

These errors existed before Phase 15-02 execution and are not related to the OperationCodeSelector component:

### 1. ApiAssertionResults.tsx - Unused Import
- **File:** `frontend/src/components/Report/ApiAssertionResults.tsx`
- **Line:** 1
- **Error:** TS6133: 'Clock' is declared but its value is never read
- **Impact:** Build fails with `npm run build` (tsc -b step)
- **Deferred:** Pre-existing issue, not caused by Phase 15 work

### 2. RunList.tsx - Type Mismatch
- **File:** `frontend/src/pages/RunList.tsx`
- **Line:** 122
- **Error:** TS2345: Argument of type 'string | undefined' is not assignable to parameter of type 'string | null'
- **Impact:** Build fails with `npm run build` (tsc -b step)
- **Deferred:** Pre-existing issue, not caused by Phase 15 work

## Note

The OperationCodeSelector component itself compiles and builds correctly with Vite.
The build failures are from unrelated pre-existing TypeScript issues.
