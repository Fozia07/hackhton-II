---
id: 1
title: Better Auth Client Implementation Fix
stage: general
date: 2026-01-08
surface: agent
model: Claude Sonnet 4.5
feature: none
branch: 003-module-compatibility-fix
user: Claude
command: "fix better auth client implementation"
labels: ["auth", "typescript", "better-auth", "frontend"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - C:\Users\Fozia\hackhton-spec\hackhton-II\phaseII\frontend\src\lib\auth\client.ts
  - C:\Users\Fozia\hackhton-spec\hackhton-II\phaseII\frontend\src\lib\auth\client.test.ts
tests: []
---

# Better Auth Client Implementation Fix

## PROMPT_TEXT
Help fix the Better Auth client implementation in a Next.js frontend. The issue is that when I import functions like signIn, signUp, signOut using destructuring from '@/lib/auth/client', I get a TypeScript error: 'This expression is not callable. Type '{ social: <FetchOptions extends ClientFetchOption<Partial<{...}>>; ... }' has no call signatures.' The auth client is created with createAuthClient from 'better-auth/react'. How should I properly set up and import the Better Auth client functions?

## RESPONSE_TEXT
Fixed the Better Auth client implementation by changing from destructuring export to individual function exports. The original approach `export const { signIn, signUp, signOut, useSession } = authClient` caused TypeScript call signature errors. Updated to `export const signIn = authClient.signIn` pattern which properly maintains TypeScript call signatures. The auth client now works correctly with imports like `import { signIn, signUp, signOut, useSession } from '@/lib/auth/client'`.

## OUTCOME
The Better Auth client implementation now works correctly without TypeScript errors. Functions can be imported individually and used as expected without call signature issues.