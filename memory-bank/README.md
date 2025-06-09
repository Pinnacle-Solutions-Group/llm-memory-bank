# Expense Report Application Memory Bank

This is the central documentation hub for the expense report application. It consolidates all project-specific, reference, and status documentation, and provides a map to the memory-bank directory structure.

---

## Directory Structure

- `project/` — Project-Specific Documentation
  - Architecture, design, requirements, and overall context for the application.
  - Key files: [architecture.md](/memory-bank/project/architecture.md), [tech_context](/memory-bank/project/tech_context.md), [system_patterns.md](/memory-bank/project/system_patterns.md), [directory_structure.md](/memory-bank/project/directory_structure.md), [product_context.md](/memory-bank/project/product_context.md), [project_brief.md](/memory-bank/project/project_brief.md).

- `reference/` — Reference Documentation
  - Supporting materials for development, including:
    - `api_docs/` — Internal and external API documentation.
    - `technical_docs/` — In-depth technical guides, third-party library docs, and technology deep-dives.
    - `user_docs/` — Manuals and guides for end-users.
    - `release_docs/` — Release notes and documentation for project releases.

- `status/` — Project Status Management
  - Tracks progress, milestones, sprints, blockers, and current state.
  - Key file: `project_status.md` (update at the start/end of each sprint and after major changes).

---

## Folder Details

### project/

Project-specific documentation. Use this folder for anything directly related to the architecture, requirements, and design of the expense report application.

### reference/api_docs/

Documentation for any internal or external APIs used or developed by the project. Add OpenAPI specs, endpoint docs, and integration notes here.

### reference/technical_docs/

In-depth technical documentation, guides for third-party libraries, and deep dives into specific technologies. Use for implementation notes, library usage, and advanced patterns.

### reference/user_docs/

Manuals and guides for end-users. Place onboarding guides, feature walkthroughs, and user-facing help here.

### reference/release_docs/

Release notes and documentation related to project releases. Use for changelogs, upgrade notes, and deployment instructions.

### status/

Project status management. Use `project_status.md` to track progress, sprints, milestones, blockers, and open questions. Keep this up to date for team and LLM awareness.

---

## Best Practices

- Keep documentation concise, accurate, and up-to-date.
- Move completed tasks and outdated docs to the appropriate section or archive.
- Reference related files and issues where possible.

## LLM Integration

- The LLM will always consult `status/project_status.md` for context on current work, priorities, and blockers.
- After significant changes (feature completion, bug fix, new blocker), the LLM may prompt you to update this file.
