# LLM Memory Bank Rules Overview

This document provides a comprehensive overview of the rule system that governs LLM interactions within projects using this memory bank system.

## Rule System Architecture

The rules are organized into a hierarchical system with four main categories:

### 1. Core Rules (`rules/core/`) - ALWAYS APPLY
Essential operational guidelines that form the foundation of all AI assistant interactions.

### 2. Best Practices (`rules/best-practices/`) - ALWAYS APPLY  
Project-wide standards that ensure consistency and quality across all work.

### 3. Workflow Rules (`rules/workflow/`) - APPLY ONE SET
FOCUS-specific instructions that change based on the current task type (Planning, Implementation, or Debugging).

### 4. Memory Bank (`memory-bank/`) - CONSULT AS NEEDED
Project context and documentation that provides the knowledge base for decisions.

## Core Rules

### Meta-Rules (`00-meta-rules.md`)
**Purpose**: The foundational rule that defines how the AI determines its operational FOCUS and applies other rule sets.

**Key Functions**:
- Establishes priority system for rule application
- Defines FOCUS determination logic (Planning → Implementation → Debugging)
- Provides escalation guidelines when the AI encounters uncertainty
- Acts as the "operating system" for all other rules

**Team Impact**: Ensures consistent AI behavior across all team members and projects.

### General Coding Conventions (`general-coding-conventions.md`)
**Purpose**: Establishes non-negotiable software engineering principles for all code development.

**Key Standards**:
- Code quality (clarity, consistency, DRY principles)
- Robustness (input validation, error handling, resource management)
- Security (input sanitization, least privilege, secrets management)
- Testing and documentation requirements

**Team Impact**: Maintains consistent code quality regardless of which team member is working with the AI.

### LLM Interaction Guidelines (`llm-interaction-guidelines.md`)
**Purpose**: Defines how the AI should communicate and interact with users.

**Key Functions**:
- Communication style and tone guidelines
- When to ask clarifying questions vs. making assumptions
- How to present options and trade-offs
- Escalation procedures for complex scenarios

**Team Impact**: Ensures productive and efficient human-AI collaboration.

### Memory Bank Usage (`memory-bank-usage.md`)
**Purpose**: The critical rule that ensures the AI always uses project-specific, up-to-date documentation rather than general knowledge.

**Key Functions**:
- Mandates checking tech context before any library work
- Provides templates for requesting documentation updates
- Establishes validation processes for technical decisions
- Prevents outdated knowledge from causing issues

**Team Impact**: **CRITICAL** - This rule is what makes the memory bank system effective by ensuring the AI always works with current, project-specific information.

### Memory Bank Library Overview (`memory-bank-library-overview.md`)
**Purpose**: Defines the process for creating comprehensive library documentation roadmaps.

**Team Impact**: Ensures consistent, navigable documentation for all project dependencies.

### Memory Bank Section Summarize (`memory-bank-section-summarize.md`)
**Purpose**: Defines the process for creating detailed documentation for specific library sections.

**Team Impact**: Provides deep, actionable documentation for complex technical implementations.

## Best Practices Rules

### Error Documentation Guidelines (`error-documentation-guidelines.md`)
**Purpose**: Standardizes how significant errors are documented to build institutional knowledge.

**Key Functions**:
- Defines criteria for which errors should be documented
- Provides standard format for troubleshooting entries
- Automates the documentation process through AI prompts

**Team Impact**: Builds a searchable knowledge base that prevents repeated debugging of the same issues.

### Lessons Learned (`lessons-learned.md`)
**Purpose**: Captures and applies broader patterns and insights from project experience.

**Team Impact**: Prevents repeated architectural and design mistakes across projects.

## Workflow Rules

### Planning Rules (`workflow/planning/planning-rules.md`)
**Purpose**: Governs the requirements analysis and solution design phase.

**Key Process**:
1. **Requirements Analysis**: Comprehensive context gathering and ambiguity resolution
2. **Solution Design**: Multiple option evaluation with trade-off analysis
3. **Implementation Planning**: Detailed step sequencing and risk assessment
4. **Plan Review**: Impact assessment and explicit approval requests

**Team Impact**: Ensures thorough upfront planning that prevents costly rework and technical debt.

### Implementation Rules (`workflow/implementation/implementation-rules.md`)
**Purpose**: Governs the code execution phase with precision and quality focus.

**Key Process**:
1. **Plan Validation**: Ensures alignment with approved plans and current context
2. **Code Implementation**: Methodical execution following all standards
3. **Testing & Verification**: Comprehensive test coverage and validation
4. **Completion & Documentation**: Results reporting and memory bank updates

**Team Impact**: Ensures high-quality, well-tested implementations that align with project architecture.

### Debugging Rules (`workflow/debugging/debugging-rules.md`)
**Purpose**: Provides systematic approach to error diagnosis and resolution.

**Key Process**:
1. **Error Context**: Comprehensive information gathering and reproduction
2. **Root Cause Analysis**: Systematic hypothesis testing using project context
3. **Solution Design**: Minimal, targeted fixes aligned with architecture
4. **Implementation & Verification**: Robust testing and regression prevention
5. **Documentation**: Knowledge capture for future reference

**Team Impact**: Reduces debugging time and prevents regression through systematic approaches.

## Project Rules (`rules/project/`)
**Purpose**: Placeholder for project-specific customizations and overrides.

**Team Impact**: Allows projects to customize the rule system while maintaining the core framework.

## Rule Interaction Patterns

### Rule Priority System
1. **Core Rules**: Always enforced, cannot be overridden
2. **Best Practices**: Always applied, can be extended by project rules
3. **Workflow Rules**: Applied based on current FOCUS
4. **Project Rules**: Can customize and extend other rules

### FOCUS Transitions
The system supports dynamic transitions between workflow modes:
- **Planning → Implementation**: After explicit plan approval
- **Implementation → Debugging**: When errors or test failures occur
- **Debugging → Implementation**: After successful issue resolution
- **Any → Planning**: When requirements become unclear

### Memory Bank Integration
All rules are designed to work with the memory bank system:
- Rules reference specific memory bank files for context
- Rules mandate documentation updates for significant changes
- Rules prevent the use of outdated general knowledge
- Rules provide templates for requesting missing documentation

## Benefits Summary

### For Individual Developers
- **Consistency**: Same high-quality AI assistance regardless of experience level
- **Efficiency**: Reduced context switching and rework through systematic approaches
- **Learning**: Built-in best practices and institutional knowledge transfer

### for Teams
- **Standardization**: Consistent code quality and documentation across all team members
- **Knowledge Retention**: Systematic capture of lessons learned and troubleshooting solutions
- **Onboarding**: New team members inherit the same AI assistance patterns immediately

### For Projects
- **Technical Debt Prevention**: Systematic architecture compliance and planning requirements
- **Risk Mitigation**: Comprehensive testing and validation requirements
- **Maintainability**: Consistent documentation and error handling standards

### For Organizations
- **Scalability**: Rule system can be replicated across multiple projects and teams
- **Quality Assurance**: Built-in quality gates and review processes
- **Knowledge Management**: Systematic capture and reuse of technical knowledge 
