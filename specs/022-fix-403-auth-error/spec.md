# Feature Specification: Fix 403 Authentication Error in Todo AI Chatbot

## Overview
Resolve the 403 Forbidden error that occurs when users sign in and attempt to add tasks through the chat interface. The error occurs due to a mismatch between the user ID in the API URL path and the username contained in the JWT token.

## Problem Statement
When users sign in and attempt to interact with the chat interface (specifically when adding tasks), they encounter a 403 Forbidden error. The backend logs reveal that the token payload contains the correct username ('hamzah12'), but the API request is made with an encoded email address ('hamzah12%40gmail.com') in the URL path, causing an authentication mismatch.

## User Scenarios & Testing
- **Scenario 1**: User logs in with email address, attempts to add a task via chat
  - Expected: Task is successfully added without authentication errors
  - Actual: 403 Forbidden error occurs

- **Scenario 2**: User logs in with username, attempts to add a task via chat
  - Expected: Task is successfully added without authentication errors
  - Actual: May still fail if email was stored in localStorage

- **Scenario 3**: User logs in with either email or username, interacts with chat
  - Expected: All chat interactions work seamlessly with proper authentication

## Functional Requirements
1. **Authentication Consistency** - The system must ensure that the user identifier used in API calls matches the username stored in the JWT token, regardless of what the user enters during login (email vs username).

2. **Token-Path Alignment** - The API path parameter must align with the username contained in the authentication token to prevent 403 errors.

3. **Storage Correction** - The system must store the correct username (from the token or API response) in localStorage rather than relying on user input which may be an email address.

4. **Error Prevention** - The system must prevent 403 Forbidden errors by ensuring authentication token and API path parameters are consistent.

5. **Seamless User Experience** - Users should be able to log in with either their email or username without experiencing authentication errors during subsequent chat interactions.

## Non-Functional Requirements
- The solution must maintain backward compatibility with existing user accounts
- The fix should not require users to change their login credentials
- Performance should not be impacted by the authentication fix

## Success Criteria
- Users can successfully add tasks through the chat interface without encountering 403 errors
- 99% of chat interactions complete with successful 200 responses
- Authentication process works consistently regardless of whether users log in with email or username
- System maintains security standards while fixing the authentication mismatch

## Key Entities
- JWT Token (contains username)
- API URL path parameter (currently mismatched)
- localStorage (stores username for subsequent API calls)
- User authentication credentials (may be email or username)

## Dependencies
- Phase II authentication backend must return consistent username in token/response
- Frontend must properly extract and store correct username from authentication response

## Assumptions
- The Phase II backend API can return the canonical username in the response
- The existing authentication token format will remain unchanged
- Users may continue to log in with either email addresses or usernames

## Scope
### In Scope
- Fixing the 403 authentication error in the chat interface
- Ensuring consistent user identification between token and API calls
- Updating localStorage with correct username after authentication
- Supporting both email and username login methods

### Out of Scope
- Changing the underlying authentication system
- Modifying how Phase II backend generates JWT tokens
- Major UI redesign of the login interface
- Migration of existing user data formats

## Constraints
- Solution must be compatible with existing JWT token format
- Must not break existing user sessions
- Changes should be minimal and focused on the authentication mismatch