# 005 - Frontend Authentication API Alignment - Implementation Plan

## Architecture Decision

### API Alignment Approach
The team decided to align the frontend authentication implementation with the actual Better Auth client API. This approach ensures that all authentication calls use methods that actually exist in the Better Auth API, resolving TypeScript compilation errors.

### Type Safety Strategy
The implementation will prioritize type safety by using only documented and available methods from the Better Auth client, ensuring the codebase remains reliable and maintainable.

## Decisions

### Decision 1: Removal of signIn.credentials() and signUp.email() methods
**Rationale**: These methods do not exist in the Better Auth client API. TypeScript reports that `signIn` and `signUp` are objects with a `social` property but no credentials-based methods.
**Action**: Replace with direct method calls using the correct Better Auth patterns.
**Impact**: Resolves TypeScript compilation errors and aligns with actual API surface.

### Decision 2: Use of direct signIn and signUp function calls
**Rationale**: The Better Auth client exports signIn and signUp as functions that can be called directly with the appropriate parameters.
**Action**: Call `signIn('credentials', {email, password})` and `signUp('email', {email, password, name})` directly instead of using sub-methods.
**Impact**: Maintains authentication functionality while using supported API methods.

### Decision 3: Client-level redirect configuration
**Rationale**: Rather than passing redirect options to each authentication call (which was causing fetch API redirect enum errors), configure redirect behavior at the client level.
**Action**: Set `fetchOptions: { redirect: 'manual' }` in the auth client configuration.
**Impact**: Eliminates fetch API redirect enum errors while maintaining proper redirect handling.

### Decision 4: Authentication strategy alignment
**Rationale**: The authentication strategy strings ('credentials' for login, 'email' for signup) must match the strategy defined in the Better Auth server configuration.
**Action**: Use 'credentials' strategy for signIn and 'email' strategy for signUp as these are standard Better Auth strategies.
**Impact**: Ensures frontend calls align with backend configuration without requiring backend changes.

## Implementation Strategy

### Phase 1: Code Correction
1. Update LoginForm to use `signIn('credentials', {email, password})` directly
2. Update SignupForm to use `signUp('email', {email, password, name})` directly
3. Update authentication hooks to use correct direct method calls
4. Remove any usage of non-existent sub-methods like `signIn.credentials` or `signUp.email`

### Phase 2: Redirect Handling Implementation
1. Configure `fetchOptions: { redirect: 'manual' }` in the auth client
2. Ensure all authentication flows properly handle redirects manually
3. Update redirect handling in success callbacks for login, signup, and logout
4. Test redirect behavior in all authentication flows

### Phase 3: Testing and Validation
1. Test email/password login functionality
2. Test email/password signup functionality
3. Verify TypeScript compiles without authentication-related errors
4. Ensure all authentication flows work as expected with proper redirect handling

## Technical Components

### Authentication Components
- LoginForm: Updated to use direct signIn method
- SignupForm: Updated to use direct signUp method
- Authentication hooks: Updated to use correct API methods
- Auth client: Properly configured Better Auth client with fetchOptions

### Redirect Handling
- Client-level redirect configuration using `fetchOptions: { redirect: 'manual' }`
- Manual redirect handling in authentication success callbacks
- Proper navigation after authentication using Next.js router

## Quality Assurance
- All authentication methods use only available Better Auth API functions
- TypeScript compiles successfully without authentication errors
- Email/password authentication flows work correctly
- Redirect handling works properly with manual redirect configuration
- Code aligns with Better Auth documentation
- No backend authentication logic is modified