---
description: Defines the process for understanding requirements, designing solutions,
  and creating detailed implementation plans when FOCUS = PLANNING.
globs: null
alwaysApply: false
---
# Planning Workflow Rules

This document outlines the process to follow when **FOCUS = PLANNING**.
It assumes Core Rules and Best Practices are understood.

**Overall Goal:** Develop a well-reasoned, actionable implementation plan that aligns with project goals, architecture, and best practices, then present it for approval.

## Process

1. **Clarify Requirements & Gather Context:**

   - **Understand Task:** Ensure full clarity on the problem to be solved or the feature to be developed. Ask clarifying questions if any ambiguity exists.
   - **Consult Memory Bank:** Thoroughly review relevant documents:
     - [memory-bank/project/project_brief.md](memory-bank/project/project_brief.md) & [memory-bank/project/product_context.md](memory-bank/project/product_context.md) (goals, user needs).
     - [memory-bank/project/architecture.md](memory-bank/project/architecture.md) & [memory-bank/project/system_patterns.md](memory-bank/project/system_patterns.md) (architectural constraints & patterns).
     - [memory-bank/project/tech_context.md](memory-bank/project/tech_context.md) (approved technologies, versions).
     - [memory-bank/status/project_status.md](memory-bank/status/project_status.md) (related ongoing work, priorities).
     - [best-practices/lessons-learned](rules/best-practices/lessons-learned.md) (relevant past experiences).
   - Review existing codebase sections related to the task.
   - **State Constraints & Assumptions:** Clearly list key constraints (e.g., performance targets, deadlines if known) and any assumptions made.

2. **Explore Solutions & Design:**

   - **Brainstorm Options:** Identify potential solutions that align with the project's architecture, tech stack, and established patterns.
   - **Evaluate Trade-offs:** For each viable option, consider:
     - Maintainability, Scalability, Performance, Security
     - Complexity (development effort, cognitive load)
     - Alignment with overall project goals and [core/general-coding-conventions](rules/core/general-coding-conventions.md).
   - **Select Optimal Solution:** Choose the best approach and provide a clear, concise justification, referencing Memory Bank documents or established principles.

3. **Detail Implementation Plan:**

   - **Step-by-Step Breakdown:** Create a logical sequence of implementation steps.
   - **Code Changes:** Identify key new modules, classes, functions, or modifications to existing code. Ensure these respect the architecture in [memory-bank/project/architecture.md](memory-bank/project/architecture.md).
   - **Testing Strategy:** Outline necessary tests (unit, integration, E2E if applicable).
   - **Documentation:** List new documentation or updates required (code comments, API docs, [memory-bank/project/error_documentation.md](memory-bank/project/error_documentation.md)).
   - **Dependencies:** Identify any new libraries, other tasks, or external system dependencies.
   - **Rollback/Contingency (if applicable):** For critical changes, briefly note any rollback considerations.

4. **Assess Plan Impact & Request Approval:**
   - **Memory Bank Impact:** Note if the plan requires updates to [memory-bank/project/architecture.md](memory-bank/project/architecture.md), [memory-bank/project/tech_context.md](memory-bank/project/tech_context.md), etc.
   - **Present Plan:** Clearly present the proposed solution, justification, and detailed steps.
   - **Seek Approval:** **Crucially, request explicit user review and approval of the plan _before_ transitioning to `FOCUS = IMPLEMENTATION`.** State: "Please review the proposed plan. Upon approval, I will switch to FOCUS = IMPLEMENTATION."

<!-- End of Planning Workflow -->
