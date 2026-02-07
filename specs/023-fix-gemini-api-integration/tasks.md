# Implementation Tasks: Fix Gemini API Integration

## Feature Overview
Resolve the 400 API key error when the Phase III backend attempts to call the Google Gemini API for AI responses. The backend currently uses the wrong API key (OPENAI_API_KEY instead of GEMINI_API_KEY) and incorrect endpoint format. This fix will update the configuration and AI service to properly use the GEMINI_API_KEY with the native Gemini API endpoint, following OpenAI Agent SDK and MCP server best practices.

## Implementation Strategy
This implementation follows an incremental approach to fix the Gemini API integration. The core issue is that the backend is using the OPENAI_API_KEY for Gemini API calls and using an OpenAI-compatible endpoint instead of the native Gemini API. The solution involves researching OpenAI Agent SDK and MCP server documentation for Gemini integration patterns, updating the configuration to read GEMINI_API_KEY, implementing proper API calls following SDK best practices, and maintaining all existing functionality including tool calling.

## Phase 1: Setup and Research
Initialize the project environment, verify existing codebase, and research proper integration patterns.

- [x] T001 Review OpenAI Agent SDK Python documentation for Gemini API integration patterns
- [x] T002 Review MCP server documentation for Gemini API key configuration
- [x] T003 Research how OpenAI SDK handles alternative API providers like Gemini
- [x] T004 Verify current backend configuration in phaseIII/backend/app/core/config.py
- [x] T005 Examine current AI service implementation in phaseIII/backend/app/services/ai_agent.py
- [x] T006 Review .env file to confirm GEMINI_API_KEY is present
- [x] T007 Check if httpx or aiohttp is available for HTTP client needs

## Phase 2: Foundational
Implement foundational changes required for all user stories based on research findings.

- [x] T008 Add GEMINI_API_KEY field to AIConfig class in phaseIII/backend/app/core/config.py
- [x] T009 Add gemini_base_url field to AIConfig class in phaseIII/backend/app/core/config.py
- [x] T010 Update config validation to check for GEMINI_API_KEY in phaseIII/backend/app/core/config.py
- [x] T011 Add property methods for gemini_api_key and gemini_base_url in AppConfig class

## Phase 3: [US1] API Key Management and Configuration
Update configuration to properly read and use GEMINI_API_KEY for Gemini API calls following SDK patterns.

- [x] T012 [US1] Update AIConfig to read GEMINI_API_KEY from environment in phaseIII/backend/app/core/config.py
- [x] T013 [P] [US1] Strip whitespace from GEMINI_API_KEY value in phaseIII/backend/app/core/config.py
- [x] T014 [US1] Set gemini_base_url to https://generativelanguage.googleapis.com/v1beta in phaseIII/backend/app/core/config.py
- [x] T015 [US1] Update validation logic to ensure GEMINI_API_KEY is not empty in phaseIII/backend/app/core/config.py
- [x] T016 [US1] Add logging to track which API key is being used in phaseIII/backend/app/core/config.py

## Phase 4: [US2] Gemini API Integration Following SDK Best Practices
Implement Gemini API integration using patterns from OpenAI Agent SDK and MCP documentation.

- [x] T017 [US2] Update AsyncOpenAI client to use Gemini base URL and API key in phaseIII/backend/app/services/ai_agent.py
- [x] T018 [P] [US2] Configure client with correct Gemini endpoint format in phaseIII/backend/app/services/ai_agent.py
- [x] T019 [US2] Test if OpenAI SDK can directly call Gemini with base_url override in phaseIII/backend/app/services/ai_agent.py
- [x] T020 [US2] If SDK doesn't support Gemini, implement direct HTTP client approach in phaseIII/backend/app/services/ai_agent.py
- [x] T021 [US2] Create helper method to format messages for Gemini API format in phaseIII/backend/app/services/ai_agent.py
- [x] T022 [US2] Create helper method to format tools for Gemini API format in phaseIII/backend/app/services/ai_agent.py
- [x] T023 [US2] Implement _call_gemini_api method with proper Authorization header in phaseIII/backend/app/services/ai_agent.py
- [x] T024 [US2] Parse Gemini API response and extract AI text from candidates array in phaseIII/backend/app/services/ai_agent.py

## Phase 5: [US3] MCP Server Integration and Tool Calling
Preserve MCP server integration and tool calling functionality with Gemini API.

- [x] T025 [US3] Update process_conversation method to use Gemini API integration in phaseIII/backend/app/services/ai_agent.py
- [x] T026 [P] [US3] Implement tool call detection from Gemini response format in phaseIII/backend/app/services/ai_agent.py
- [x] T027 [US3] Map Gemini functionCall format to MCP tool execution in phaseIII/backend/app/services/ai_agent.py
- [x] T028 [US3] Update tool response handling to work with Gemini API format in phaseIII/backend/app/services/ai_agent.py
- [x] T029 [US3] Implement second API call after tool execution to get final response in phaseIII/backend/app/services/ai_agent.py
- [x] T030 [US3] Preserve existing error handling patterns in phaseIII/backend/app/services/ai_agent.py
- [x] T031 [US3] Ensure conversation history retrieval continues to work in phaseIII/backend/app/services/ai_agent.py
- [x] T032 [US3] Verify MCP client integration remains functional in phaseIII/backend/app/services/ai_agent.py

## Phase 6: Testing and Validation
Test the implementation to ensure the fix works correctly and all features are preserved.

- [x] T033 Test basic API connectivity with Gemini API using valid GEMINI_API_KEY
- [x] T034 [P] Test chat message without tool calls to verify AI response generation
- [x] T035 Test MCP tool calling functionality with add_task command
- [x] T036 Test MCP tool calling functionality with list_tasks command
- [x] T037 Verify JWT authentication continues to work properly
- [x] T038 Test conversation history persistence and retrieval
- [x] T039 Verify 400 API key error is eliminated
- [x] T040 Test that OpenAI SDK integration (if used) works correctly with Gemini

## Phase 7: Polish & Cross-Cutting Concerns
Finalize the implementation with error handling, documentation, and edge case management.

- [x] T041 Add comprehensive error handling for Gemini API failures in phaseIII/backend/app/services/ai_agent.py
- [x] T042 Add logging for Gemini API requests and responses in phaseIII/backend/app/services/ai_agent.py
- [x] T043 Update comments to explain Gemini API integration approach in phaseIII/backend/app/services/ai_agent.py
- [x] T044 Document which approach was used (SDK vs direct HTTP) in phaseIII/backend/app/services/ai_agent.py
- [x] T045 Verify all error messages are user-friendly and informative
- [x] T046 Test with various edge cases (empty responses, rate limits, etc.)
- [x] T047 Clean up any unused imports or code

## Dependencies

### Story Completion Order
- US2 (API Integration) depends on US1 (Configuration) - API calls need correct configuration
- US3 (MCP Tool Calling) depends on US2 (API Integration) - Tool calling needs working API integration

### Parallel Execution Examples
- Tasks T001, T002, T003 in Setup can run in parallel (different documentation sources)
- Tasks T013 and T014 in US1 can run in parallel (different configuration aspects)
- Tasks T018 and T021 in US2 can run in parallel (different implementation aspects)
- Tasks T026 and T027 in US3 can run in parallel (different tool handling aspects)
- Tasks T034, T035, T036 in Testing can run in parallel (different test scenarios)

## Independent Test Criteria

### US1 Test Criteria
- Configuration properly reads GEMINI_API_KEY from environment
- GEMINI_API_KEY value is stripped of whitespace
- Configuration validation ensures GEMINI_API_KEY is not empty
- Correct Gemini base URL is configured

### US2 Test Criteria
- API integration follows OpenAI Agent SDK best practices
- HTTP requests are made to correct Gemini API endpoint
- Authorization header uses proper format with GEMINI_API_KEY
- Request body follows Gemini API specification
- Response is properly parsed and AI text is extracted

### US3 Test Criteria
- MCP server integration continues to work properly
- Tool calling functionality works with new Gemini API format
- Conversation history continues to be retrieved and used
- Error handling provides clear messages for API failures
- All existing features continue to function as before