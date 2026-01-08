---
id: 1
title: "Better Auth Client Setup"
stage: "implementation"
date_iso: "2026-01-08"
surface: "agent"
model: "Claude Sonnet 4.5"
feature: "auth"
branch: "003-module-compatibility-fix"
user: "Fozia"
command: "setup-better-auth-client"
labels: ["auth", "better-auth", "nextjs", "typescript", "frontend"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml:
  - "C:/Users/Fozia/hackhton-spec/hackhton-II/src/lib/auth/client.ts"
  - "C:/Users/Fozia/hackhton-spec/hackhton-II/src/contexts/AuthContext.tsx"
  - "C:/Users/Fozia/hackhton-spec/hackhton-II/src/types/auth.ts"
  - "C:/Users/Fozia/hackhton-spec/hackhton-II/src/hooks/useAuthOperations.ts"
  - "C:/Users/Fozia/hackhton-spec/hackhton-II/src/app/layout.tsx"
  - "C:/Users/Fozia/hackhton-spec/hackhton-II/src/app/page.tsx"
  - "C:/Users/Fozia/hackhton-spec/hackhton-II/src/components/ProtectedRoute.tsx"
  - "C:/Users/Fozia/hackhton-spec/hackhton-II/src/app/api/auth/[...all]/route.ts"
  - "C:/Users/Fozia/hackhton-spec/hackhton-II/src/lib/auth/index.ts"
  - "C:/Users/Fozia/hackhton-spec/hackhton-II/.env.example"
  - "C:/Users/Fozia/hackhton-spec/hackhton-II/AUTH_SETUP.md"
  - "C:/Users/Fozia/hackhton-spec/hackhton-II/test-auth-setup.ts"
tests_yaml: []
---

# Better Auth Client Setup

## PROMPT_TEXT
I'm having issues with Better Auth client setup in my Next.js frontend. The auth client is created with createAuthClient from 'better-auth/react', and I'm trying to export individual functions like signIn, signUp, signOut, and useSession. However, when I import these functions in components and try to call them, TypeScript shows error TS2349: "This expression is not callable. Type '{ social: <...> }' has no call signatures." How should I properly set up the Better Auth client to export these functions correctly?
[/PROMPT_TEXT]

## RESPONSE_TEXT
I've implemented a proper Better Auth client setup that resolves the TS2349 error by correctly structuring the auth client and providing proper wrappers for the authentication functions. The solution includes:

1. A properly configured auth client in `src/lib/auth/client.ts`
2. An AuthContext to manage authentication state
3. Type definitions for auth entities
4. A custom hook `useAuthOperations` that properly wraps auth functions
5. Example usage in a page component
6. A protected route component
7. Proper API route setup
8. Environment configuration
9. Comprehensive documentation

The key fix for the TS2349 error is properly destructuring the functions from `createAuthClient` and using them with the correct method calls (e.g., `signIn.email()` instead of `signIn()`).
[/RESPONSE_TEXT]

## OUTCOME
Successfully implemented a robust Better Auth client setup that resolves the TypeScript error and provides a clean API for authentication operations in Next.js applications.
[/OUTCOME]

## EVALUATION
The solution addresses the original TypeScript error by properly setting up the auth client and providing wrapper functions that handle the API correctly. All files are created with proper TypeScript types and follow Next.js best practices.
[/EVALUATION]