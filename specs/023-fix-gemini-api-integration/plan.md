# Implementation Plan: Fix Gemini API Integration

## Technical Context

The Phase III backend currently uses an OpenAI-compatible interface to call Google's Gemini API, but it's using the wrong API key. The system should use the GEMINI_API_KEY specifically for Gemini API calls instead of the OPENAI_API_KEY. The configuration needs to be updated to use the correct endpoint and authorization format.

Current issues:
- Using OPENAI_API_KEY for Gemini API calls
- Incorrect endpoint configuration (using OpenAI-compatible endpoint instead of native Gemini)
- Wrong authorization header format

Required changes:
- Update configuration to read and use GEMINI_API_KEY for Gemini calls
- Change endpoint to the native Gemini API: https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-chat:generate
- Use proper authorization: "Authorization: Bearer <GEMINI_API_KEY>"

## Constitution Check

### Compliance Assessment
- **Spec-Driven Development**: ✓ Plan follows spec requirements
- **Incremental Evolution**: ✓ Fix builds on existing Phase III functionality
- **Code Quality and Documentation**: ✓ Solution will be well-documented
- **Architecture-First Approach**: ✓ Maintains current architecture while fixing issue

### Gate Evaluations
- [ ] No speculative development beyond spec requirements
- [ ] No bypassing established architecture patterns
- [ ] No introducing unapproved technology stacks

### Remediation Plan (if needed)
If any gates fail, implementation will pause for approval.

## Phase 0: Research & Unknown Resolution

### Research Tasks

#### Task 0.1: Google Gemini API Native Endpoint Patterns
**Objective**: Research the correct format for calling Google's native Gemini API with proper authentication

**Expected Outcomes**:
- Understanding of correct endpoint URL structure
- Proper authorization header format
- Required request body format
- Response format expectations

#### Task 0.2: API Key Separation Best Practices
**Objective**: Research how to properly separate OpenAI and Google Gemini API keys in the configuration

**Expected Outcomes**:
- Understanding of when to use each API key
- Best practices for environment variable management
- Secure handling of API keys in configuration

#### Task 0.3: Google Gemini vs OpenAI-Compatible API Differences
**Objective**: Research differences between Google's native Gemini API and OpenAI-compatible endpoint

**Expected Outcomes**:
- Understanding of parameter differences
- Differences in response structures
- Impact on existing tool calling functionality

## Phase 1: System Design & API Contracts

### Component 1.1: API Configuration Enhancement
**Purpose**: Enhance configuration to properly manage separate API keys for different services

**Requirements**:
- Add separate configuration for Gemini API key
- Maintain backward compatibility with existing config structure
- Properly validate both API keys are available

### Component 1.2: AI Service Modification
**Purpose**: Modify AI service to use native Gemini API with correct endpoint and authentication

**Requirements**:
- Switch from OpenAI-compatible interface to native Google API
- Use correct authorization header format
- Maintain existing tool calling functionality
- Preserve existing response handling

### Component 1.3: HTTP Client Implementation
**Purpose**: Implement proper HTTP client to call Gemini native API

**Requirements**:
- Construct proper HTTP requests to Gemini API
- Handle authentication with Gemini API key
- Manage request/response format conversion
- Preserve existing error handling patterns

## Phase 2: Implementation Approach

### Approach 2.1: Configuration Update
**Method**: Update configuration to use GEMINI_API_KEY for Gemini-specific calls

**Implementation Steps**:
1. Add GEMINI_API_KEY to AI configuration class
2. Update environment variable reading to handle Gemini key properly
3. Ensure proper validation of Gemini API key

### Approach 2.2: Direct HTTP Implementation
**Method**: Replace OpenAI client with direct HTTP calls to Gemini API

**Implementation Steps**:
1. Replace AsyncOpenAI client with direct HTTP client (aiohttp or httpx)
2. Format requests to match Gemini native API specification
3. Handle responses from Gemini API properly
4. Maintain tool calling functionality

### Approach 2.3: Service Layer Update
**Method**: Update service layer to adapt to new API implementation

**Implementation Steps**:
1. Update process_conversation method to work with new API response format
2. Adapt tool calling mechanism to new API format
3. Maintain existing interfaces and contracts

## Phase 3: Development Tasks

### Task 3.1: Configuration Updates
- [ ] Add GEMINI_API_KEY support to config.py
- [ ] Update AIConfig class to include Gemini-specific settings
- [ ] Validate that both API keys are properly configured

### Task 3.2: AI Service Implementation
- [ ] Replace OpenAI client with native Gemini API calls
- [ ] Implement proper request formatting for Gemini API
- [ ] Update response handling to match Gemini API format
- [ ] Preserve tool calling functionality

### Task 3.3: Testing and Validation
- [ ] Test basic API connectivity with Gemini API
- [ ] Test tool calling functionality with new implementation
- [ ] Verify JWT authentication continues to work
- [ ] Ensure all existing features continue to function

## Risk Assessment

### Risk 1: Breaking Existing Tool Calling
- **Impact**: High - Tool calling is core functionality
- **Mitigation**: Carefully map tool calling to new API format
- **Contingency**: Preserve existing interfaces while changing implementation

### Risk 2: Authentication Issues
- **Impact**: Medium - Could affect user sessions
- **Mitigation**: Test with existing JWT authentication flow
- **Contingency**: Preserve existing authentication mechanisms

## Success Criteria

- [ ] 400 API key errors eliminated during AI interactions
- [ ] Gemini API calls use correct GEMINI_API_KEY
- [ ] Native Gemini API endpoint is used correctly
- [ ] Tool calling functionality preserved
- [ ] JWT authentication continues to work properly
- [ ] All existing functionality remains intact