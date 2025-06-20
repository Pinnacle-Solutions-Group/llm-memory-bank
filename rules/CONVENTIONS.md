# Rule: 10-mandatory-code-review

## Define the reasoning for making code changes

## MANDATORY CODE REVIEW

Before making ANY significant code changes, conduct an internal round table discussion with David Thomas (The Pragmatic Programmer), Andrew Hunt (The Pragmatic Programmer), and Uncle Bob (Clean Code). If they would approve, proceed, if not, iterate until they would approve.

---

# Rule: 12-general-coding-conventions

## Foundational software engineering principles for code quality, robustness, testability, security, documentation, performance, and proactive assistance.

## General Coding Conventions

Foundational principles for all code development. These are ALWAYS ENFORCED.

### Code Quality (Non-Negotiable)

- **Clarity First:** Readable > Clever. Simple > Complex.
- **Consistency:** Follow project style guides. If undefined, match existing patterns.
- **DRY:** Eliminate duplication. Extract reusable components.
- **Naming:** Descriptive, searchable identifiers. No abbreviations.
- **Single Responsibility:** One function = one purpose. One class = one concept.

### Robustness (Required)

- **Validate All Inputs:** External data is untrusted. Sanitize and validate.
- **Error Handling:** Log errors. Fail gracefully. Provide meaningful messages.
- **Resource Management:** Close connections, free memory, handle cleanup.
- **Edge Cases:** Test boundaries, nulls, empty states, max limits.

### Security (Critical)

- **Input Sanitization:** Prevent injection, XSS, CSRF attacks.
- **Least Privilege:** Minimal permissions required.
- **Secrets:** Use environment variables or secrets manager per [tech_context.md](memory-bank/project/tech_context.md).
- **Audit Trail:** Log security-relevant actions.

### Testing & Documentation

- **Testable Code:** Write unit tests. Prefer pure functions. Use dependency injection.
- **Comments:** Explain "why", not "what". Document non-obvious decisions.
- **API Docs:** Document public interfaces (params, returns, side effects).

### Performance Guidelines

- **Correctness First:** Make it work, then make it fast.
- **Profile Before Optimizing:** Measure actual bottlenecks.
- **Avoid Obvious Waste:** O(n²) where O(n) works, unnecessary loops, memory leaks.

### LLM Assistance Rules

**When to Suggest Improvements (During ANY FOCUS):**
- Clear design pattern opportunity aligned with [system_patterns.md](memory-bank/project/system_patterns.md)
- Architecture violation detected per [architecture.md](memory-bank/project/architecture.md) 
- Security vulnerability spotted
- Performance issue with obvious fix

**How to Suggest:**
- Brief mention: "This could benefit from [pattern/fix] because [reason]"
- Non-intrusive: Don't derail primary task unless critical
- Align with [tech_context.md](memory-bank/project/tech_context.md) constraints

---

# Rule: 15-comprehensive-testing

## Ensure AI assistant creates proper unit tests rather than temporary test scripts in projects with existing test suites

## Unit Test Development Rule

When working on projects that have an established unit test suite (indicated by presence of `tests/` directory with existing test files), the AI assistant MUST follow these guidelines:

### Required Actions

**DO:**
- Add new test cases to existing test files when testing related functionality
- Create new properly named test files following the project's test naming conventions (e.g., `test_*.py`)
- Ensure all test cases are properly documented with descriptive names and docstrings
- Run the full test suite after making changes to verify nothing is broken
- Structure tests using the project's established testing patterns and frameworks

**DO NOT:**
- Create temporary test scripts that will be deleted after verification
- Write one-off validation scripts instead of proper unit tests
- Skip adding tests for new functionality or bug fixes
- Leave test code uncommented or poorly documented

### Test Development Priority

1. **Extend existing tests** - Add test cases to existing test classes when functionality is related
2. **Create new test modules** - When testing entirely new functionality, create appropriately named test files
3. **Maintain test coverage** - Ensure new code paths have corresponding test coverage
4. **Follow project patterns** - Use the same testing framework, assertion style, and organization as existing tests

### Rationale

Temporary test scripts provide short-term validation but offer no long-term value. Proper unit tests serve as:
- **Living documentation** of expected behavior
- **Regression prevention** for future changes
- **Code quality assurance** through continuous validation
- **Collaboration tools** for team development

Always prioritize building and maintaining a comprehensive, permanent test suite over quick, disposable validation scripts

---

# Rule: 15-llm-interaction-guidelines

## Foundational principles for AI assistant interaction, emphasizing clarity

## LLM Interaction Guidelines

Core protocols for helpful, rigorous, secure, efficient, and context-aware assistance.

### Interaction Principles (ALWAYS FOLLOW)

#### 1. Clarity First
- **Ambiguous Request:** Seek clarification immediately. State exactly what's unclear.
- **No Assumptions:** Don't guess user intent on critical decisions.

#### 2. Context Gathering (REQUIRED)
- **Before Major Work:** Consult relevant Memory Bank sections per **memory-bank-usage**
- **Key Documents:** [project_brief.md](memory-bank/project/project_brief.md), [architecture.md](memory-bank/project/architecture.md), [tech_context.md](memory-bank/project/tech_context.md), [system_patterns.md](memory-bank/project/system_patterns.md)
- **Tech Stack Compliance:** [tech_context.md](memory-bank/project/tech_context.md) specifies exact package versions. If lacking knowledge of specified version, check Memory Bank docs first, then **STOP and NOTIFY** if still insufficient.
- **Alignment Check:** All work MUST align with project context. Deviations require explanation and confirmation.

#### 3. Structured Response
- **Clear Organization:** Logical structure, concise explanations
- **Justify Decisions:** Explain reasoning for solutions/changes
- **Follow FOCUS:** Adhere to current workflow from **00-meta-rules**
- **Suggest Improvements:** Offer relevant optimizations

#### 4. Resource Priority
- **Priority Order:** Memory Bank > Codebase > Conversation > External sources
- **External Info:** Adapt to project standards per **memory-bank-usage**

### Communication Protocols (CRITICAL)

#### STOP and NOTIFY
**When:** Critical blockers, missing essential info, destructive commands
**Action:** Halt immediately. State problem clearly. Await guidance.
**Examples:** Missing [architecture.md](memory-bank/project/architecture.md), unparseable instructions, risky operations

#### WARN and SEEK CONFIRMATION
**When:** Conflicts with [architecture.md](memory-bank/project/architecture.md), **general-coding-conventions**, or best practices
**Action:** Explain conflict, describe risks, propose alternative, request decision
**Template:** "This conflicts with [rule] because [reason]. Risk: [consequence]. Alternative: [suggestion]. Proceed as requested or use alternative?"

#### ASK/REQUEST CLARIFICATION
**When:** Ambiguous requests, significant optional parameters, consent-required actions
**Action:** State what's unclear, explain why clarification needed, provide options
**Examples:** Unclear requirements, external content fetching, shared resource changes

---

# Rule: 25-error-documentation-guidelines

## Specifies how to document significant or recurring errors, their diagnosis, and resolutions. AI prompts for updates and creation.

## Error Documentation Guidelines

This document outlines best practices for documenting significant, recurring, or non-obvious errors encountered during development. The goal is to create a valuable knowledge base in [troubleshooting_log.md](memory-bank/project/troubleshooting_log.md) (or a similar designated file) to accelerate future debugging efforts.

### When to Document an Error

Document errors that are:

- **Non-obvious:** The cause and solution are not immediately apparent.
- **Recurring:** The same or similar errors have occurred multiple times.
- **Significant Impact:** The error caused considerable delay or system malfunction.
- **Complex Solution:** The steps to diagnose and resolve were involved.

### Standard Error Log Entry Format (to be used in [troubleshooting_log.md](memory-bank/project/troubleshooting_log.md))

Each entry should ideally include:

1. **Error Summary:** Date, Symptom(s), System/Module, Severity.
2. **Context & Environment:** Software versions, configuration, reproduction steps.
3. **Diagnosis Steps:** Investigation, tools used, key findings.
4. **Root Cause:** Fundamental reason.
5. **Resolution:** Steps taken, code/config changes (link to PRs if possible).
6. **Preventative Measures / Lessons Learned:** How to prevent; link to [lessons-learned](memory-bank/project/lessons_learned.md) if applicable.

### LLM Actions & Prompts

After successfully resolving an error when `FOCUS = DEBUGGING`, if the error meets the criteria outlined above, **YOU MUST** check if the designated troubleshooting log file (e.g., [troubleshooting_log.md](memory-bank/project/troubleshooting_log.md)) exists.

- **If the log file does NOT exist:** **YOU MUST** first prompt the user: "I'd like to suggest an entry for the troubleshooting log, but [troubleshooting_log.md](memory-bank/project/troubleshooting_log.md) doesn't seem to exist yet. Shall I create it using the standard format outlined in this **error-documentation-guidelines rule**?" If approved, create the file with a placeholder structure.
- **Once the log file exists (or was just created):** **YOU MUST** then prompt the user: "This seems like a good candidate for our troubleshooting log. Would you like me to help draft an entry for [troubleshooting_log.md](memory-bank/project/troubleshooting_log.md) based on our debugging session?"

---

# Rule: 25-lessons-learned

## A living document capturing key insights, patterns, and solutions from

## Lessons Learned

This document captures key lessons learned during the project. Reviewing these can help avoid repeating past mistakes, leverage successful patterns, and improve overall development efficiency. This is primarily maintained by the user but serves as important context for the AI, and the AI should prompt for updates.

### Guiding Principles from Past Experience (Examples to be replaced by actual project lessons)

- **Verify Assumptions:** Before complex operations, explicitly verify assumptions about file states, external services, or data.
- **Tool Specificity:** Understand and use the most appropriate tool for each specific task. Query if unsure.
- **Clear Task Definition:** Ensure tasks are well-defined and understood before implementation. Refer to [project_status.md](memory-bank/status/project_status.md) for current tasks.
- **Instruction Adherence:** Strictly follow provided instructions, rules, and workflow protocols. Clarify ambiguities.
- **Iterative Feedback:** For complex tasks, consider proposing a small part or asking for confirmation on approach before full implementation.

### LLM Proactive Prompts

After a complex `FOCUS = PLANNING` phase or a `FOCUS = DEBUGGING` session that yielded significant insights, YOU SHOULD prompt the user: "Were there any key takeaways or patterns from this [planning/debugging] session that should be captured in [lessons-learned](memory-bank/project/lessons_learned.md) for future reference?"