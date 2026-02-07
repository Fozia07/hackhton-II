# Architectural Decision Record: Multi-Provider AI Service with MCP Tools Integration

## Context
The Todo AI Chatbot needs to support both OpenAI and Google Gemini providers for AI agent functionality. The system must be flexible enough to work with either provider while maintaining MCP tools integration for task management operations.

## Decision
We implemented a multi-provider AI service that:

1. **Prioritizes Google Gemini**: Uses GEMINI_API_KEY environment variable when available, falling back to OpenAI
2. **Leverages OpenAI-compatible endpoint**: Uses Google's OpenAI-compatible endpoint (`https://generativelanguage.googleapis.com/v1beta/openai/`) with AsyncOpenAI client
3. **Maintains MCP tools integration**: Preserves all 5 MCP tools (add_task, list_tasks, complete_task, delete_task, update_task) regardless of provider
4. **Provides graceful fallback**: Automatically falls back to OpenAI when Gemini is not configured

## Alternatives Considered

### Separate Client Implementations
- **Pros**: Provider-specific optimizations, cleaner separation
- **Cons**: Code duplication, maintenance overhead, harder to maintain consistency

### Provider Abstraction Layer
- **Pros**: Clean interface, easy to add new providers
- **Cons**: Additional complexity, potential performance overhead

### Single Provider Approach
- **Pros**: Simpler implementation
- **Cons**: Vendor lock-in, limited flexibility, missed cost/performance optimization opportunities

## Consequences

### Positive
- Reduced vendor lock-in
- Ability to leverage competitive pricing/performance between providers
- Consistent functionality across providers
- Easy to switch or A/B test providers

### Negative
- Slight complexity in configuration management
- Potential differences in response quality/format between providers
- Need to ensure compatibility with both provider APIs

## Status
Implemented and validated.

## Notes
- Provider selection happens at runtime based on environment variables
- Both providers support the same function calling interface
- Error handling is consistent across providers