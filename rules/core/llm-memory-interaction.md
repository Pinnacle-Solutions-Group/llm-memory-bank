---
description: Guides AI interaction with the project's Memory Bank, focusing on documentation, tech stack, and architectural consistency.
globs: 
alwaysApply: false
---

# LLM Guidelines for Memory Bank Usage

## Core Principles

1. **Memory Bank is Primary:** The Memory Bank (files within `memory-bank/project/` and `memory-bank/reference/`) is your primary source of truth for project context, code generation, and decision-making.
2. **Maintain Consistency:** Strictly adhere to the defined architecture (ref: [architecture.md](memory-bank/project/architecture.md), [system_patterns.md)(memory-bank/project/system_patterns.md)) and coding standards.
3. **Development Context:** Always consider the current development FOCUS (see [00-meta-rules](rules/core/00-meta-rules.md)) and project status (ref: [project_status.md)(memory-bank/status/project_status.md)) in your actions.

## Technology Stack Adherence & Documentation Protocol

The authoritative source for the technology stack is [tech_context.md](memory-bank/project/tech_context.md). You MUST use the specified versions.

**Documentation Workflow for Libraries in `tech_context.md`:**

For any library `[LIBRARY_NAME]` with major version `[MAJOR_VERSION]` from `tech_context.md`:

1. **Check Local Roadmap:**

   - **Path:** `../../memory-bank/reference/api_docs/[LIBRARY_NAME]/[MAJOR_VERSION]/llms.txt`
   - This file acts as a curated table of contents for the library's documentation.

2. **Roadmap Missing - Create It:**

   - **Action:** If `llms.txt` is missing, inform the user:
     > "To ensure correct usage of `[LIBRARY_NAME] v[MAJOR_VERSION]` (as per [tech_context.md](memory-bank/project/tech_context.md)), I need its documentation. No local roadmap found at `../../memory-bank/reference/api_docs/[LIBRARY_NAME]/[MAJOR_VERSION]/llms.txt`.
     > Please provide the primary documentation URL for `[LIBRARY_NAME] v[MAJOR_VERSION]` using the `@web` command so I can create this roadmap."
   - **On User URL via `@web`:**
     1. Fetch the main page and identify key navigation links/sections.
     2. **Propose an initial structure for `llms.txt`** including Markdown links to these key sections.
     3. You MAY also offer to summarize the primary landing page or top 2-3 most critical linked pages from the documentation site if they seem foundational. If approved, save these as `../../memory-bank/reference/api_docs/[LIBRARY_NAME]/[MAJOR_VERSION]/llms-[feature_slug].txt`, and update the proposed `llms.txt` to point to these local summaries.
     4. Upon approval of the `llms.txt` structure (and any summaries), save the file(s).
     5. Notify: "Documentation roadmap (and any initial summaries) for `[LIBRARY_NAME] v[MAJOR_VERSION]` created at `../../memory-bank/reference/api_docs/[LIBRARY_NAME]/[MAJOR_VERSION]/`. I will now use this as my guide."

3. **Using Local Documentation & Deep Dives:**
   - **Consult Roadmap First:** Always start by checking `llms.txt` and any `llms-[feature].txt` files for `[LIBRARY_NAME]`.
   - **Need More Detail (External Link in Roadmap):** If `llms.txt` links to an external URL for a feature and you need more detail:
     1. **ASK/REQUEST PERMISSION** (as per [llm-interaction-guidelines](rules/core/llm-interaction-guidelines.md)):
        > "For task '[current task summary]' using `[LIBRARY_NAME] v[MAJOR_VERSION]`, I need to understand its '[feature_name]' capabilities better. The roadmap points to [URL]. May I fetch this page, summarize it locally as `../../memory-bank/reference/api_docs/[LIBRARY_NAME]/[MAJOR_VERSION]/llms-[feature_name_slug].txt`, and update the roadmap?"
     2. **On User Approval:**
        a. Fetch the URL via `@web`.
        b. Create a concise summary and save to the specified path.
        c. Update `llms.txt` to point to the new local file.
        d. Notify: "Detailed summary for '[feature_name]' created, and roadmap updated. Proceeding with task."

## Architectural Document Processing

When referencing architecture documents (e.g., [architecture.md](memory-bank/project/architecture.md), [system_patterns.md)(memory-bank/project/system_patterns.md)):

1. **Parse & Understand:** Load diagrams, extract boundaries, flows, dependencies.
2. **Validate Changes:** Ensure alignment with architectural constraints.
3. **Maintain Patterns:** Uphold separation of concerns and defined patterns.

**Error Handling (Architecture):**

- **Missing/Unreadable Doc:** **STOP and NOTIFY** user.
- **Diagram Parse Failure:** **REQUEST CLARIFICATION** or a corrected diagram.
- **Architectural Violation:** **WARN and SEEK CONFIRMATION** from user.

## Status Updates

If your actions lead to significant changes, advise the user that [project_status.md](memory-bank/status/project_status.md) and related documents in `memory-bank/project/` might need updating.
