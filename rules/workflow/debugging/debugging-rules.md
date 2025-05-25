---
description: Defines the systematic process for diagnosing, fixing, and documenting
  issues when FOCUS = DEBUGGING.
globs: null
alwaysApply: false
---
# Debugging Workflow Rules

This document outlines the process to follow when **FOCUS = DEBUGGING**.
It assumes Core Rules (e.g., [core/00-meta-rules](rules/core/00-meta-rules.md), [core/llm-interaction-guidelines](rules/core/llm-interaction-guidelines.md)) and Best Practices (from [best-practices/lessons-learned](rules/best-practices/lessons-learned.md)) are understood and applied.

**Overall Goal:** Diagnose the root cause of an error or unexpected behavior, implement a robust fix aligned with project context, verify the fix, and document significant findings.

## Process

1. **Understand & Contextualize Error:**

   - **Gather Details:** Collect all available information: error messages, stack traces, logs, user reports, and precise reproduction steps.
   - **Consult Memory Bank:** Review relevant documents for context:
     - [memory-bank/status/project_status.md](memory-bank/status/project_status.md) (recent changes, current tasks).
     - [memory-bank/project/architecture.md](memory-bank/project/architecture.md) & [memory-bank/project/system_patterns.md](memory-bank/project/system_patterns.md) (system context of affected component).
     - [memory-bank/project/tech_context.md](memory-bank/project/tech_context.md) (technology-specifics).
     - [best-practices/lessons-learned](rules/best-practices/lessons-learned.md) (past similar issues).
     - [memory-bank/project/troubleshooting_log.md](memory-bank/project/troubleshooting_log.md) (documented errors).
   - **Reproduce:** If possible and safe, reproduce the error in a controlled environment.

2. **Analyze & Hypothesize Root Cause(s):**

   - Analyze symptoms against the project context (codebase, architecture, dependencies).
   - Formulate hypotheses about potential root causes. Consider recent code, data, or environmental changes.

3. **Investigate & Identify Cause:**

   - Systematically investigate hypotheses to pinpoint the exact root cause.
   - Use appropriate diagnostic tools and techniques.

4. **Plan Fix:**

   - Design the minimal, targeted fix to resolve the issue without regressions.
   - Ensure the fix aligns with:
     - Project architecture ([memory-bank/project/architecture.md](memory-bank/project/architecture.md)).
     - Coding standards ([core/general-coding-conventions](rules/core/general-coding-conventions.md)).
     - Tech context ([memory-bank/project/tech_context.md](memory-bank/project/tech_context.md)).
   - Identify any related documentation (code comments, technical docs) needing updates.

5. **Implement & Verify Fix:**

   - Implement the fix, adhering to all standards.
   - **Test Thoroughly:**
     - Run the specific test that initially failed (if any).
     - Execute related existing tests.
     - Add new tests to cover the fix and prevent regressions, following project testing standards.

6. **Report & Document:**
   - **Outcome:** Report if the fix was successful and the issue resolved. Provide the implemented fix and any new/updated tests.
   - **Memory Bank Updates (Propose to User):**
     - [memory-bank/status/project_status.md](memory-bank/status/project_status.md) (update task status).
     - Consider if a new entry in [memory-bank/project/troubleshooting_log.md](memory-bank/project/troubleshooting_log.md) is warranted, as per [best-practices/error-documentation-guidelines](rules/best-practices/error-documentation-guidelines.md).
     - [best-practices/lessons-learned](rules/best-practices/lessons-learned.md) if a broader lesson was identified.
     - Relevant technical documentation in [memory-bank/project/error_documentation.md](memory-bank/project/error_documentation.md) if the issue revealed important system insights.
   - **Stuck?** If unable to find the root cause or a fix after reasonable effort, clearly report findings, hypotheses, attempts, and request assistance.

<!-- End of Debugging Workflow -->
