# Technical Specification Writer

## Expertise
Expert skill for generating high-quality, implementation-ready technical specifications for software systems, APIs, agents, and backend services. Converts ideas, user stories, or feature requests into formal, testable specifications that engineering teams can implement directly.

## Purpose
This skill enforces spec-driven development standards by creating comprehensive technical specifications that:
- Are testable and unambiguous
- Map cleanly to engineering tasks
- Provide clear acceptance criteria
- Define data models and API contracts precisely
- Identify edge cases and error scenarios
- Establish clear boundaries (in-scope vs out-of-scope)

## When to Use
Use this skill when you need to:
- Convert user stories or feature requests into formal specifications
- Document API designs and contracts
- Define database schemas and data models
- Specify agent or service architectures
- Create implementation-ready technical documentation
- Ensure specifications meet quality standards
- Generate testable acceptance criteria

## Mandatory Specification Sections

Every specification MUST include these 11 sections:

### 1. Title
Clear, descriptive name for the feature/system being specified.

### 2. Overview
High-level summary of what is being built and why. Should answer:
- What problem does this solve?
- Who are the users/consumers?
- What is the business value?

### 3. Goals
Specific, measurable objectives this spec aims to achieve. Use SMART criteria:
- Specific: Clearly defined outcomes
- Measurable: Quantifiable success metrics
- Achievable: Realistic within constraints
- Relevant: Aligned with business objectives
- Time-bound: Clear timeline expectations

### 4. Functional Requirements
Detailed list of what the system must do. Each requirement should be:
- Atomic (single responsibility)
- Testable (can be verified)
- Unambiguous (clear interpretation)
- Numbered for reference (FR-001, FR-002, etc.)

### 5. Non-Functional Requirements
Performance, security, scalability, reliability, and operational requirements:
- **Performance**: Response times, throughput, resource limits
- **Security**: Authentication, authorization, data protection, compliance
- **Scalability**: Load handling, growth projections
- **Reliability**: Uptime targets, error rates, recovery time
- **Maintainability**: Code quality, documentation, monitoring
- **Usability**: User experience, accessibility

### 6. Data Models
Schema definitions, relationships, validation rules (if applicable):
- Entity definitions with fields and types
- Relationships and cardinality
- Constraints and validation rules
- Indexes and performance considerations
- Migration strategy

### 7. API / Interface Definitions
Endpoints, methods, request/response formats (if applicable):
- HTTP methods and paths
- Request parameters and body schemas
- Response formats and status codes
- Authentication and authorization
- Rate limiting and quotas
- Versioning strategy

### 8. Error Handling & Edge Cases
All failure scenarios and how to handle them:
- Error taxonomy with codes and messages
- Retry and timeout strategies
- Degradation and fallback behavior
- Validation errors
- System failures
- Edge cases and boundary conditions

### 9. Assumptions & Constraints
Dependencies, limitations, prerequisites:
- External dependencies (services, libraries, APIs)
- Technical constraints (platform, language, infrastructure)
- Business constraints (budget, timeline, resources)
- Assumptions about user behavior or system state
- Known limitations

### 10. Out of Scope
Explicitly state what is NOT included:
- Features deferred to future releases
- Related but separate concerns
- Alternative approaches not pursued
- Clarify boundaries to prevent scope creep

### 11. Acceptance Criteria
Testable conditions that define "done":
- Given-When-Then scenarios
- Test cases with expected outcomes
- Performance benchmarks
- Security validation steps
- User acceptance criteria

## Specification Quality Standards

### Language and Clarity
- Use clear, unambiguous language
- Define all technical terms and acronyms
- Use consistent terminology throughout
- Avoid implementation details unless necessary
- Focus on WHAT, not HOW (unless architecture decisions are needed)

### Structure and Format
- Use consistent formatting and structure
- Number requirements for easy reference
- Use tables for structured data
- Include diagrams for complex relationships
- Use code blocks for examples

### Completeness
- All mandatory sections present
- No undefined terms or references
- All dependencies identified
- All error cases covered
- All assumptions documented

### Testability
- Every requirement is verifiable
- Acceptance criteria are measurable
- Test cases can be derived directly
- Success metrics are quantifiable

## Best Practices

### Converting User Stories to Specifications
1. Extract the Goal: Identify the core functionality needed
2. Define Acceptance Criteria: Convert "so that" into testable conditions
3. Identify Data Requirements: What data is needed to support this?
4. Define API/Interface: How will users interact with this feature?
5. Consider Edge Cases: What could go wrong? What are the boundaries?
6. Specify Non-Functional Requirements: Performance, security, etc.

### Common Pitfalls to Avoid
1. Vague Requirements: "The system should be fast" → Specify: "API response time p95 < 200ms"
2. Implementation Details in Specs: Focus on WHAT, not HOW
3. Missing Error Cases: Always specify what happens when things go wrong
4. Untestable Criteria: Specify measurable metrics
5. Scope Creep: Use "Out of Scope" section aggressively
6. Ambiguous Language: Use "must", "will", "shall" instead of "should", "might", "could"
7. Missing Dependencies: Document all external systems or services required
8. No Success Metrics: Define how you'll measure if the feature achieves its goals

## Summary

This skill provides a comprehensive framework for creating production-ready technical specifications that:
- Follow spec-driven development principles
- Are immediately implementable by engineering teams
- Include all necessary sections and details
- Provide clear acceptance criteria
- Map directly to tasks and tests
- Serve as authoritative documentation

Use this skill whenever you need to convert ideas into formal, testable specifications that engineering teams can implement with confidence.
