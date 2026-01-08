# 005 - Frontend Authentication API Alignment - Tasks

## Constraints:
- No backend authentication logic changes
- No undocumented Better Auth APIs
- No use of `any` or `@ts-ignore`
- No inline fetch redirect configuration

## Task 1: Update LoginForm to use correct API methods
- [ ] Replace `signIn.credentials({email, password})` with `signIn(AUTH_STRATEGY, {email, password})` using the configured auth strategy
- [ ] Verify TypeScript compiles without errors for LoginForm
- [ ] Test email/password login functionality
- [ ] Ensure proper error handling is maintained

## Task 2: Update SignupForm to use correct API methods
- [ ] Replace `signUp.email({email, password, name})` with `signUp(AUTH_STRATEGY, {email, password, name})` using the configured auth strategy
- [ ] Verify TypeScript compiles without errors for SignupForm
- [ ] Test email/password signup functionality
- [ ] Ensure proper error handling is maintained

## Task 3: Update authentication hooks to use correct methods
- [ ] Update useSignIn hook to use direct `signIn(AUTH_STRATEGY, {...})` call using the configured auth strategy
- [ ] Update useSignUp hook to use direct `signUp(AUTH_STRATEGY, {...})` call using the configured auth strategy
- [ ] Update useSignOut hook if needed
- [ ] Verify all hooks compile without TypeScript errors

## Task 4: Configure client-level redirect handling
- [ ] Add `fetchOptions: { redirect: 'manual' }` to auth client configuration
- [ ] Remove any inline redirect options from authentication calls
- [ ] Ensure proper redirect handling in success callbacks
- [ ] Test redirect behavior after authentication

## Task 5: Test authentication flows
- [ ] Test login functionality with valid credentials
- [ ] Test login functionality with invalid credentials
- [ ] Test signup functionality with valid information
- [ ] Test signup functionality with invalid information
- [ ] Verify proper error messages are displayed

## Task 6: Verify TypeScript compilation
- [ ] Run TypeScript compiler to ensure no authentication-related errors
- [ ] Fix any remaining type issues
- [ ] Verify all authentication responses are properly typed
- [ ] Ensure type safety is maintained throughout

## Task 7: Documentation and handoff
- [ ] Document the correct Better Auth API usage patterns
- [ ] Update any relevant README files
- [ ] Prepare handoff documentation for team
- [ ] Verify all changes are properly committed