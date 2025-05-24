---
description: Defines the process for executing approved plans, writing code, and ensuring alignment with project standards when FOCUS = IMPLEMENTATION.
globs: 
alwaysApply: false
---

# Implementation Workflow Rules

This document outlines the process to follow when **FOCUS = IMPLEMENTATION**.
It assumes Core Rules (e.g., [core/general-coding-conventions](rules/core/general-coding-conventions.md)) and Best Practices (from [best-practices/lessons-learned](rules/best-practices/lessons-learned.md)) are understood. **Crucially, it presumes an approved plan (typically from a `FOCUS = PLANNING` phase or a clear, actionable user request) exists.**

**Overall Goal:** Accurately execute the approved plan, ensuring all generated code and modifications align with project context, standards, and requirements.

## Process

1. **Understand Plan & Context:**

   - **Confirm Plan:** Ensure a clear understanding of the approved implementation plan and the specific task(s). If no explicit plan exists, clarify the requirements thoroughly.
   - **Review Context:** Consult relevant documents:
     - [memory-bank/project/architecture.md](memory-bank/project/architecture.md) & [memory-bank/project/system_patterns.md](memory-bank/project/system_patterns.md)
     - [memory-bank/project/tech_context.md](memory-bank/project/tech_context.md)
     - [memory-bank/status/project_status.md](memory-bank/status/project_status.md) (overall state, related tasks)
     - Specific technical documents or API roadmaps ([memory-bank/project/error_documentation.md](memory-bank/project/error_documentation.md)) related to the task.
   - **Validate Alignment:** Verify the plan is consistent with the current project context. If discrepancies arise (e.g., recent changes invalidate parts of the plan), **STOP**, report to the user, and seek clarification before proceeding.

2. **Implement & Iterate:**

   - Execute the plan's steps methodically.
   - Consistently apply [core/general-coding-conventions](rules/core/general-coding-conventions.md) and [best-practices/lessons-learned](rules/best-practices/lessons-learned.md) (quality, security, documentation, architectural style).
   - **Issue Handling:** If significant issues or errors arise that are not straightforward to fix, notify the user and explicitly state: "Encountered [issue description]. Switching to FOCUS = DEBUGGING to resolve this." Then, follow [workflow/debugging/debugging-rules](rules/workflow/debugging/debugging-rules.md).

3. **Test & Document (as per plan or standards):**

   - Implement unit tests, integration tests, etc., as specified or as per good practice ([core/general-coding-conventions](rules/core/general-coding-conventions.md)).
   - Run all relevant tests.
   - **Test Failures:** If tests fail, notify the user: "Tests failed for [feature/task]. Switching to FOCUS = DEBUGGING." Follow [workflow/debugging/debugging-rules](rules/workflow/debugging/debugging-rules.md).
   - Add/update code comments, API documentation, and other necessary documentation.

4. **Report Completion & Propose Updates:**
   - Once implementation and successful testing are complete (including any debugging cycles), report task completion.
   - **Propose Memory Bank Updates (to user):**
     - [memory-bank/status/project_status.md](memory-bank/status/project_status.md) (task completion, progress).
     - Relevant technical documentation in [memory-bank/project/error_documentation.md](memory-bank/project/error_documentation.md) if new patterns emerged or key discoveries were made.
     - Potentially [memory-bank/project/architecture.md](memory-bank/project/architecture.md) or [memory-bank/project/tech_context.md](memory-bank/project/tech_context.md) files if architectural details were refined.

**(End of Implementation Workflow)**
