# Feature Specification: Fix Gemini API Integration

## Overview
Resolve the 400 API key error when the Phase III backend attempts to call the Google Gemini API for AI responses. Currently, the system returns "Error code: 400 - API key not valid. Please pass a valid API key." despite having valid API keys in the .env file.

## Problem Statement
The Phase III backend fails to properly utilize the GEMINI_API_KEY when making requests to the Google Gemini API, resulting in authentication failures. The system should use the GEMINI_API_KEY specifically for Gemini API calls with the correct endpoint and authorization format.

Currently the system has:
- OPENAI_API_KEY in .env (for OpenAI services)
- GEMINI_API_KEY in .env (for Gemini services)
- But backend is either using the wrong key or calling the API incorrectly

The correct Gemini API call should be:
- Endpoint: POST https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-chat:generate
- Authorization: Authorization: Bearer <GEMINI_API_KEY>
- Content-Type: application/json

## User Scenarios & Testing
- **Scenario 1**: User sends a message in the chat interface
  - Expected: AI-generated response from Gemini without errors
  - Actual: 400 error with "API key not valid" message

- **Scenario 2**: User adds a task via natural language
  - Expected: Task processed and AI response provided
  - Actual: Fails with authentication error

- **Scenario 3**: User interacts with tool-calling features
  - Expected: AI uses tools and responds appropriately
  - Actual: Authentication failure prevents response

## Functional Requirements
1. **API Key Management** - The system must read and properly use the GEMINI_API_KEY from the .env file, stripping any whitespace, and use it exclusively for Gemini API calls.

2. **Correct API Endpoint** - The system must call the correct Gemini API endpoint: POST https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-chat:generate

3. **Proper Authorization** - Requests to Gemini API must use Authorization header in the format "Bearer <GEMINI_API_KEY>"

4. **Separation of Concerns** - The system must ensure OPENAI_API_KEY is used only for OpenAI services and GEMINI_API_KEY only for Gemini services.

5. **Maintain Existing Features** - All current functionality must be preserved:
   - JWT authentication from Phase II backend
   - Conversation ID handling
   - Tool calls and logging
   - All existing API contracts and interfaces

## Non-Functional Requirements
- The fix should not impact performance significantly
- Error handling should be improved to provide clearer messages
- Configuration should be flexible and environment-aware

## Success Criteria
- Users receive AI-generated responses without authentication errors
- 100% of Gemini API calls succeed with valid API key
- JWT authentication continues to work properly
- Tool calling functionality remains intact
- Conversation state management continues to work
- All existing features continue to function as before

## Key Entities
- API Configuration (holds API keys and endpoints)
- AI Service (handles API calls to Gemini)
- Authentication Layer (manages JWT tokens)
- Chat Processing (handles conversation flow)

## Dependencies
- Google Gemini API availability
- Valid GEMINI_API_KEY in environment variables
- Phase II backend for JWT authentication

## Assumptions
- GEMINI_API_KEY value in .env is valid and properly formatted
- Google Gemini API is accessible and operational
- Network connectivity to Google APIs is available

## Scope
### In Scope
- Fixing Gemini API key usage and authentication
- Updating configuration to properly read GEMINI_API_KEY
- Modifying AI service to use correct endpoint and headers
- Preserving all existing functionality
- Updating relevant backend files (config.py, AI service files)

### Out of Scope
- Changing JWT authentication flow
- Modifying frontend components
- Changing OpenAI API usage (if any)
- Altering database schemas or conversation models

## Constraints
- Must maintain backward compatibility with existing API contracts
- Should not disrupt current user sessions
- Changes must be minimal and targeted to the API key issue