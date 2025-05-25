---
description: Foundational software engineering principles for code quality, robustness,
  testability, security, documentation, performance, and proactive assistance.
globs: null
alwaysApply: true
---
# General Coding Conventions

These foundational principles guide all code development for this project.

## 1. Code Quality and Maintainability

- **Clarity & Simplicity:** Readable, understandable, maintainable code. Avoid unnecessary complexity.
- **Consistency:** Adhere to project style guides. If undefined, match existing codebase.
- **DRY (Don't Repeat Yourself):** Maximize reusability.
- **Meaningful Naming:** Clear, descriptive names for identifiers.
- **Focused Components (SRP):** Functions/methods do one thing. Classes have single responsibility.

## 2. Robustness and Resilience

- **Input Validation:** Rigorously validate external inputs.
- **Error Handling:** Sensible error handling, logging, graceful failure.
- **Resource Management:** Proper management of file handles, connections, memory.
- **Edge Cases:** Consider and handle boundary conditions.

## 3. Testability

- Write testable code (unit, integration).
- Prefer pure functions.
- Use dependency injection where appropriate.

## 4. Security

- **Untrusted Input:** Treat external input as potentially malicious. Sanitize/validate.
- **Prevent Common Vulnerabilities:** Guard against injection, XSS, CSRF, etc.
- **Least Privilege:** Minimal necessary permissions.
- **Secret Management:** Securely manage secrets (env vars, secrets manager). Refer to [tech_context.md](memory-bank/project/tech_context.md).

## 5. Documentation

- **Code Comments:** Explain the "why" of non-obvious code.
- **API Documentation:** Document public APIs (parameters, returns, behavior).

## 6. Performance

- Avoid obvious inefficiencies. Prioritize correctness/clarity first. Optimize based on profiling and specific requirements.

## 7. Proactive Assistance & Pattern Spotting

- **Identify Improvement Opportunities:** If, while (`FOCUS = IMPLEMENTATION`, `PLANNING`, or `DEBUGGING`), you notice a clear, contained opportunity to apply a standard design pattern (e.g., Factory, Observer, Strategy) aligned with [system_patterns.md](memory-bank/project/system_patterns.md) that would improve the current code section, briefly mention it to the user. Example: "As I'm working on [feature], I notice this part managing [X] could potentially use a Strategy pattern. This might make adding new [Y] types easier later. Just a thought for your consideration."
- **Alignment Check:** Ensure suggestions are consistent with [architecture.md](memory-bank/project/architecture.md) and [tech_context.md)(memory-bank/project/tech_context.md).
- **Non-Intrusive:** Present as suggestions, not demands. Avoid derailing the primary task unless a critical issue is spotted.
