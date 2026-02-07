# Research Findings: Fix 403 Authentication Error

## Task 0.1: User Identity Management Patterns

### Decision: Use API Response as Canonical Username Source
### Rationale:
The Phase II backend login API should return the canonical username in its response, which the frontend can then store in localStorage. This ensures consistency between what's stored client-side and what's in the JWT token.

### Details:
- When a user logs in, the API response should include the actual username
- Frontend should prioritize the username from the API response over what the user entered
- This approach maintains consistency between token claims and API path parameters

### Alternatives Considered:
1. Decoding JWT tokens client-side to extract username
   - Rejected due to potential security concerns
2. Making additional API call to fetch user details
   - Adds extra latency but provides reliable username
3. Using backend middleware to normalize identifiers
   - Would require backend changes

## Task 0.2: JWT Token Inspection Methodology

### Decision: Do not decode JWT tokens client-side for username extraction
### Rationale:
While JWT tokens can be decoded client-side to extract the username claim, this approach introduces potential security concerns and complexity. It's better to rely on the API response to provide the canonical username.

### Details:
- JWT decoding client-side exposes token structure to client
- Server could potentially change token format breaking client-side parsing
- API response approach is more reliable and secure

### Alternatives Considered:
1. Decode JWT and use "username" claim
   - Rejected due to security implications
2. Decode JWT and use "sub" claim
   - Same security concerns as above
3. Use API response as source of truth
   - Chosen as the most secure and maintainable approach

## Task 0.3: API Path Parameter Authentication Best Practices

### Decision: Ensure API path parameter matches token username
### Rationale:
The backend authentication logic correctly compares the user_id in the path parameter with the username in the JWT token. The frontend should ensure these match by using the canonical username from the API response or token.

### Details:
- API call format: `/api/{username}/chat`
- Username parameter must match the "username" claim in JWT
- Client should store and use consistent identifier format

### Alternatives Considered:
1. Change backend to accept email in path parameter
   - Rejected as it requires backend changes
2. Normalize emails to usernames in middleware
   - Rejected as it adds complexity
3. Ensure frontend sends correct username
   - Chosen as the most straightforward approach

## Implementation Recommendation

Based on research, the most effective approach is to update the login flow to capture the canonical username from the API response and store that in localStorage. This ensures consistency between:
1. What's stored in localStorage (for subsequent API calls)
2. What's sent in API path parameters
3. What's in the JWT token (for backend validation)

This solution requires minimal changes to the existing architecture while directly addressing the root cause of the 403 error.