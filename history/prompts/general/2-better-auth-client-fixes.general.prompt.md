---
id: 2
title: Better Auth Client Fixes for TypeScript Callable and Fetch Redirect Errors
stage: general
date_iso: 2026-01-08
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: 003-module-compatibility-fix
user: Fozia
command: manual
labels: ["auth", "typescript", "better-auth", "frontend"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml: |
  - C:\Users\Fozia\hackhton-spec\hackhton-II\src\lib\auth\client.ts
  - C:\Users\Fozia\hackhton-spec\hackhton-II\phaseII\frontend\src\lib\auth\client.ts
  - C:\Users\Fozia\hackhton-spec\hackhton-II\phaseII\frontend\src\components\auth\LoginForm.tsx
  - C:\Users\Fozia\hackhton-spec\hackhton-II\phaseII\frontend\src\components\auth\SignupForm.tsx
  - C:\Users\Fozia\hackhton-spec\hackhton-II\phaseII\frontend\src\hooks\useSignIn.ts
  - C:\Users\Fozia\hackhton-spec\hackhton-II\phaseII\frontend\src\hooks\useSignUp.ts
  - C:\Users\Fozia\hackhton-spec\hackhton-II\phaseII\frontend\src\hooks\useSignOut.ts
tests_yaml: |
  - Unit tests for auth client functionality
  - Integration tests for authentication flows
---

# Better Auth Client Fixes for TypeScript Callable and Fetch Redirect Errors

## Issue Description

This record documents the fixes for two critical authentication errors in the Better Auth integration:

1. **TypeScript Callable Error (TS2349)**: "This expression is not callable. Type '{ social: <...> }' has no call signatures."
2. **Fetch API Redirect Enum Error**: "The provided value 'false' is not a valid enum value of type RequestRedirect"

## Root Causes

### TypeScript Callable Error
- The original auth client implementation used destructuring: `export const { signIn, signUp, ... } = createAuthClient(...)`
- This approach causes TypeScript to lose proper call signature information for the individual functions
- TypeScript cannot properly infer that these are callable functions

### Fetch API Redirect Enum Error
- Better Auth was configured with `redirect: false` which is not a valid value for the fetch API's redirect property
- Valid redirect values are: `'follow'`, `'error'`, or `'manual'`

## Solutions Applied

### 1. Fixed Auth Client Export Pattern

Changed from destructuring export:
```typescript
// Before (problematic)
export const {
  signIn,
  signUp,
  signOut,
  useSession,
  // ... others
} = createAuthClient({ /* config */ });
```

To individual function exports:
```typescript
// After (fixed)
const authClient = createAuthClient({ /* config */ });

export const signIn = authClient.signIn;
export const signUp = authClient.signUp;
export const signOut = authClient.signOut;
export const useSession = authClient.useSession;
// ... others
```

### 2. Fixed Fetch API Configuration

Updated the auth client to use proper redirect values:
```typescript
const authClient = createAuthClient({
  fetchOptions: {
    baseURL: process.env.NEXT_PUBLIC_BASE_URL || 'http://localhost:3000',
    redirect: 'manual',  // Valid fetch API redirect value
  },
  plugins: [],
});
```

### 3. Removed Redundant Redirect Configurations

Since the redirect is now handled globally in the client, removed redundant `redirect: 'manual'` from individual API calls.

## Files Modified

1. `src/lib/auth/client.ts` - Fixed TypeScript callable error and redirect enum error
2. `phaseII/frontend/src/lib/auth/client.ts` - Updated with proper configuration
3. `phaseII/frontend/src/components/auth/LoginForm.tsx` - Removed redundant redirect config
4. `phaseII/frontend/src/components/auth/SignupForm.tsx` - Removed redundant redirect config
5. `phaseII/frontend/src/hooks/useSignIn.ts` - Fixed import and removed redundant redirect config
6. `phaseII/frontend/src/hooks/useSignUp.ts` - Removed redundant redirect config
7. `phaseII/frontend/src/hooks/useSignOut.ts` - Removed redundant redirect config

## Verification

- TypeScript callable errors should be resolved
- Fetch API redirect enum errors should be eliminated
- All authentication flows (sign in, sign up, sign out) should function correctly
- Components and hooks can import and use auth functions without TypeScript errors

## Result

The authentication client now works correctly with:
- Proper TypeScript typing for all auth functions
- Valid fetch API configuration
- No runtime errors related to redirect enum values
- Clean integration with Next.js and Better Auth

These changes ensure stable authentication functionality without build warnings or runtime errors.