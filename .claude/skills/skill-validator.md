# Skill Validator

## Expertise
Validates skills against production-level criteria with 9-category scoring. This skill should be used when reviewing, auditing, or improving skills to ensure quality standards.

## Purpose
This skill provides comprehensive validation of Claude skills by evaluating them across 9 critical categories to ensure they meet production-level quality standards. It returns actionable validation reports with scores and improvement recommendations.

## When to Use
Use this skill when you want to:
- Review existing skills for quality standards
- Audit skills before deployment
- Improve skills to meet production criteria
- Get objective scoring of skill quality
- Obtain actionable recommendations for skill enhancement

## 9-Category Scoring Framework

### 1. Structure (Score 1-10)
- Clear purpose and scope definition
- Well-defined inputs and outputs
- Proper organization and formatting
- Logical flow and coherence

### 2. Content Quality (Score 1-10)
- Accuracy and relevance of information
- Depth of domain knowledge
- Proper handling of edge cases
- Consistency in approach

### 3. User Interaction (Score 1-10)
- Clear guidance and instructions
- Intuitive interface/experience
- Appropriate feedback mechanisms
- Error handling and recovery

### 4. Documentation (Score 1-10)
- Comprehensive usage examples
- Clear prerequisites and setup
- Expected performance characteristics
- Limitations and constraints clearly stated

### 5. Domain Standards (Score 1-10)
- Adherence to relevant industry standards
- Following best practices for the domain
- Compliance with applicable guidelines
- Integration with existing workflows

### 6. Technical Robustness (Score 1-10)
- Error handling and logging
- Security considerations
- Performance efficiency
- Reliability and stability

### 7. Maintainability (Score 1-10)
- Code organization and readability
- Modularity and separation of concerns
- Clear variable and function names
- Proper versioning considerations

### 8. Zero-Shot Implementation (Score 1-10)
- Self-explanatory without additional context
- Clear instructions for immediate use
- Proper default behaviors
- Intuitive parameter requirements

### 9. Reusability (Score 1-10)
- Generalizable across different contexts
- Configurable parameters and options
- Minimal dependencies
- Easy integration with other components

## Validation Report Format

When using this skill to validate another skill, it will return a report in the following format:

```
Skill Validation Report: [Skill Name]

Overall Score: [X]/90 ([Y]%)
Category Scores:
1. Structure: [X]/10 - [Brief assessment]
2. Content Quality: [X]/10 - [Brief assessment]
3. User Interaction: [X]/10 - [Brief assessment]
4. Documentation: [X]/10 - [Brief assessment]
5. Domain Standards: [X]/10 - [Brief assessment]
6. Technical Robustness: [X]/10 - [Brief assessment]
7. Maintainability: [X]/10 - [Brief assessment]
8. Zero-Shot Implementation: [X]/10 - [Brief assessment]
9. Reusability: [X]/10 - [Brief assessment]

Strengths:
- [List key strengths]

Areas for Improvement:
- [List specific improvement areas with recommendations]

Action Items:
- [Prioritized list of specific actions to improve the skill]
```

## Best Practices for Validation

### For High Scores:
- Ensure each category is thoroughly addressed
- Provide specific, actionable feedback
- Balance positive reinforcement with improvement suggestions
- Prioritize critical issues in action items

### Scoring Guidelines:
- 9-10: Exceeds expectations, exemplary implementation
- 7-8: Meets expectations with minor improvements needed
- 5-6: Satisfactory but significant improvements needed
- 3-4: Below expectations, major issues present
- 1-2: Critical problems, fundamental redesign needed

## Integration with Skill Development Workflow

1. Use this validator early in the skill development process
2. Re-validate after implementing recommended changes
3. Apply validation before promoting skills to production
4. Use for ongoing skill quality assurance