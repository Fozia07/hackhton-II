# Research Findings: Fix Gemini API Integration

## Task 0.1: Google Gemini API Native Endpoint Patterns

### Decision: Use Google's native Gemini API with proper HTTP requests
### Rationale:
The native Google Gemini API requires direct HTTP requests with proper authorization headers rather than an OpenAI-compatible wrapper. This approach gives us more control and eliminates potential compatibility issues.

### Details:
- Endpoint: POST https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent
- Authorization: Authorization: Bearer <GEMINI_API_KEY>
- Content-Type: application/json
- Request body format is slightly different from OpenAI format but manageable

### Alternatives Considered:
1. Continue using OpenAI-compatible interface with correct key
   - Still has potential compatibility issues
2. Use Google's native SDK
   - Would require adding new dependencies
3. Direct HTTP calls to native API (chosen)
   - Most straightforward with existing architecture

## Task 0.2: API Key Separation Best Practices

### Decision: Maintain separate configuration values for OpenAI and Gemini keys
### Rationale:
Keeping the API keys separate ensures that each service uses the appropriate key. This approach maintains clarity and prevents cross-contamination of services.

### Details:
- GEMINI_API_KEY should be used exclusively for Gemini API calls
- OPENAI_API_KEY should be reserved for actual OpenAI services (if any)
- Configuration should validate that the correct key is available for each service
- Environment variable reading should strip whitespace as specified

### Alternatives Considered:
1. Single API key field that adapts based on usage
   - Less clear and more error-prone
2. Separate configuration classes for each service
   - Over-engineering for this use case
3. Maintain separate fields as decided
   - Clear, explicit, and maintainable approach

## Task 0.3: Google Gemini vs OpenAI-Compatible API Differences

### Decision: Implement mapping layer between OpenAI-style interface and Gemini API
### Rationale:
The existing codebase is designed around the OpenAI interface, so maintaining compatibility while switching to the native Gemini API provides the smoothest transition with minimal disruption.

### Details:
- Gemini API expects a different request format than OpenAI
- Response format also differs but can be mapped
- Tool calling is possible with Gemini API but uses different structure
- Error responses follow different patterns

### Mapping Requirements:
- Convert OpenAI-style messages to Gemini format
- Map Gemini response back to OpenAI-style response
- Handle tool/function calling according to Gemini API specifications

## Implementation Recommendation

Based on research, the best approach is to implement a direct HTTP client that calls the native Google Gemini API while maintaining the existing interface contracts. This allows the rest of the system to continue operating as before while fixing the core API key and endpoint issues.