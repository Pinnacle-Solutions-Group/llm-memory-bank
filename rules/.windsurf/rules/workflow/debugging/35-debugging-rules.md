---
trigger: model_decision
description: Defines the systematic process for diagnosing, fixing, and documenting
---
# Debugging Workflow Rules

**FOCUS = DEBUGGING:** Systematic error diagnosis, robust fixes, verification, and documentation.

## Debugging Process (Execute in Order)

### 1. Error Context & Reproduction
- **Gather Intel:** Error messages, stack traces, logs, user reports, reproduction steps
- **Memory Bank Check:** 
  - [project_status.md](memory-bank/status/project_status.md): Recent changes, current tasks
  - [troubleshooting_log.md](memory-bank/project/troubleshooting_log.md): Known similar issues
  - [lessons-learned](.windsurf/rules/best-practices/lessons-learned.md): Past patterns
- **Reproduce:** Confirm error in controlled environment (if safe)

### 2. Root Cause Analysis
- **System Context:** Review [architecture.md](memory-bank/project/architecture.md) for affected component relationships
- **Tech Stack:** Verify against [tech_context.md](memory-bank/project/tech_context.md) for version compatibility
- **Hypothesize:** Generate specific root cause theories based on symptoms + context
- **Investigate:** Systematically test hypotheses using appropriate diagnostic tools

### 3. Solution Design
- **Minimal Fix:** Target exact root cause, avoid scope creep
- **Alignment Check:** Ensure fix complies with:
  - [architecture.md](memory-bank/project/architecture.md): System constraints
  - [general-coding-conventions](.windsurf/rules/core/general-coding-conventions.md): Code standards
  - [system_patterns.md](memory-bank/project/system_patterns.md): Design patterns
- **Impact Assessment:** Identify affected tests, docs, related components

### 4. Implementation & Verification
- **Implement:** Apply fix following all coding standards
- **Test Coverage:**
  - Run original failing test (if exists)
  - Execute related test suite
  - Add regression prevention tests
- **Verify:** Confirm issue resolved without introducing new problems

### 5. Documentation & Reporting
- **Report Success:** Summarize fix, tests added, verification results
- **Memory Bank Updates (Suggest to User):**
  - **Always Consider:** [troubleshooting_log.md](memory-bank/project/troubleshooting_log.md) entry per [error_documentation_guidelines](.windsurf/rules/best-practices/error-documentation-guidelines.md)
  - **If Applicable:** [lessons-learned](.windsurf/rules/best-practices/lessons-learned.md) update for broader patterns
  - **Status Update:** [project_status.md](memory-bank/status/project_status.md) task completion

## Error Escalation

**Cannot Reproduce:** Report exact steps attempted, environment differences
**Root Cause Unknown:** Document hypotheses tested, diagnostic tools used, findings
**Fix Unsuccessful:** Explain attempted solutions, remaining symptoms, suspected causes
**Request Help:** Provide complete diagnostic summary and next step recommendations

## Critical Rules

**ALWAYS:**
- Check memory bank for similar past issues before starting
- Align fixes with project architecture and patterns
- Add tests to prevent regression
- Consider documentation updates

**NEVER:**
- Implement fixes without understanding root cause
- Skip verification testing
- Ignore related component impacts
- Bypass coding standards for "quick fixes"

## Common Mistakes (Avoid These)
- ❌ Starting implementation without checking @tech_context.md
- ❌ Using outdated library knowledge instead of memory bank docs
- ❌ Skipping architecture review for "small" changes
- ✅ Always check memory bank first, implement second
