---
description: Explains the structure and purpose of the Project Memory Bank, guiding the AI on where to find specific types of information.
globs: 
alwaysApply: false
---

# Guidelines for Using the Project Memory Bank

## Purpose of Memory Bank

The Memory Bank contains structured documentation for the application. It's your reference for project context, requirements, and technical implementation. This rule guides you on _what_ information resides where. For _how_ to interact with it (e.g., creating documentation roadmaps), see [llm-memory-interaction](rules/core/llm-memory-interaction.md).

## How to Navigate and Use This Memory Bank

- **Project Goals, Scope, Product Vision:**

  - [project_brief.md](memory-bank/project/project_brief.md): High-level overview, objectives.
  - [product_context.md](memory-bank/project/product_context.md): Problem, solution, value, target users.

- **Technical Design and Architecture:**

  - [architecture.md](memory-bank/project/architecture.md): Overall system architecture.
  - [system_patterns.md](memory-bank/project/system_patterns.md): Design patterns, data flow, security.
  - [tech_context.md](memory-bank/project/tech_context.md): Tech stack, integrations, environment, deployment.
  - [directory_structure.md](memory-bank/project/directory_structure.md): Source code organization.

- **Current Project Status and Progress:**

  - [project_status.md](memory-bank/status/project_status.md): Development focus, sprint goals, milestones, tasks, issues.

- **Specific Technical Documentation, API Info, Guides:**

  - `memory-bank/reference/api_docs/`: Curated roadmaps (`llms.txt`) and detailed summaries (`llms-[feature].txt`) for key libraries (see [llm-memory-interaction](rules/core/llm-memory-interaction.md)).
  - `memory-bank/reference/technical_docs/`: In-depth technical guides, third-party library info.
  - `memory-bank/reference/user_docs/`: End-user guides.
  - `memory-bank/reference/release_docs/`: Release notes.
  - [troubleshooting_log.md](memory-bank/project/troubleshooting_log.md): Log of significant/recurring errors and their solutions (see [error_documentation_guidelines](rules/best-practices/error-documentation-guidelines.md)).

- **Core Principle:**
  - **Align Changes:** Before significant modifications, ensure alignment with the Memory Bank. Document necessary deviations.

## Maintaining This Memory Bank

While users are primarily responsible for updates, be aware of its structure:

- It should be regularly updated as the project evolves.
- Architectural changes should be reflected in [architecture.md](memory-bank/project/architecture.md), [system_patterns.md)(memory-bank/project/system_patterns.md), etc.
- You will assist in creating/maintaining API documentation roadmaps as per [llm-memory-interaction](rules/core/llm-memory-interaction.md).
- You may assist in drafting entries for [troubleshooting_log.md](memory-bank/project/troubleshooting_log.md) as per [error_documentation_guidelines](rules/best-practices/error-documentation-guidelines.md).
