# Data Model: Gemini API Integration

## Entity: APIConfiguration
- **Fields**:
  - openai_api_key: string (API key for OpenAI services)
  - gemini_api_key: string (API key for Gemini services)
  - openai_base_url: string (base URL for OpenAI-compatible services)
  - gemini_base_url: string (base URL for Gemini API)
  - gemini_model: string (model identifier for Gemini)
  - temperature: float (temperature setting for AI responses)
  - max_tokens: int (maximum tokens to generate)
  - timeout: int (request timeout in seconds)

- **Validation Rules**:
  - gemini_api_key must be provided when using Gemini API
  - gemini_api_key should be stripped of whitespace
  - openai_api_key should be available if OpenAI services are used

## Entity: GeminiAPIRequest
- **Fields**:
  - model: string (Gemini model to use)
  - contents: array (message contents in Gemini format)
  - generation_config: object (generation parameters like temperature)
  - tools: array (available tools/functions)
  - safety_settings: object (safety configuration)

- **Validation Rules**:
  - Contents must follow Gemini API format
  - Generation config should include temperature and max_tokens
  - Tools should follow Gemini API specification

## Entity: GeminiAPIResponse
- **Fields**:
  - candidates: array (AI response candidates)
  - usage_metadata: object (token usage information)
  - prompt_feedback: object (feedback about the input prompt)

- **Validation Rules**:
  - Candidates array must contain at least one candidate
  - Response should be transformable to OpenAI-compatible format

## Entity: ToolCall
- **Fields**:
  - name: string (function name)
  - arguments: string (function arguments as JSON string)
  - id: string (unique identifier for the tool call)

- **Validation Rules**:
  - Arguments must be valid JSON
  - Name must match an available tool
  - Tool call format must be compatible with Gemini API

## Entity: AIService
- **Fields**:
  - config: APIConfiguration (configuration instance)
  - http_client: HttpClient (client for making API requests)

- **Relationships**:
  - Uses APIConfiguration for connection details
  - Makes HTTP requests to Gemini API
  - Processes GeminiAPIResponse to OpenAI-compatible format

## Relationships
- APIConfiguration (1) → GeminiAPIRequest (N) : "configures"
- AIService (1) → GeminiAPIRequest (N) : "creates"
- GeminiAPIRequest (1) → GeminiAPIResponse (1) : "receives"
- AIService (1) → ToolCall (N) : "processes"