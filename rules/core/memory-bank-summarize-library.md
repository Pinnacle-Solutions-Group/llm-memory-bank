---
description: null
globs: null
alwaysApply: false
---
# LLMs Update Library Rule

## Purpose

Defines the workflow for creating and maintaining `llms.txt` (the documentation roadmap/index) for libraries listed in [tech_context](memory-bank/project/tech_context.md).

## Workflow

1. **Check for Roadmap:**
   - For any `[LIBRARY_NAME]` and `[MAJOR_VERSION]` in `tech_context.md`, check for `memory-bank/reference/api_docs/[LIBRARY_NAME]/[MAJOR_VERSION]/llms.txt`.
   - If present, use as the authoritative roadmap for documentation lookup.

2. **If Roadmap Missing:**
   - Notify user: "To ensure correct usage of `[LIBRARY_NAME] v[MAJOR_VERSION]`, I need its documentation. No local roadmap found at [memory-bank/reference/api_docs](memory-bank/reference/api_docs) in sub-folder `[LIBRARY_NAME]/[MAJOR_VERSION]/llms.txt`. Please provide the primary documentation URL for `[LIBRARY_NAME] v[MAJOR_VERSION]` using the `@web` command so I can create this roadmap."
   - On user-provided URL:
     1. Fetch the main page and identify key navigation links/sections.
     2. Propose an initial structure for `llms.txt` with Markdown links to these key sections.
     3. Optionally offer to summarize the landing page or top 2-3 most critical linked pages if foundational. If approved, save as `llms-[feature_slug].txt` and update `llms.txt` to link to these.
     4. Upon approval, save the file(s) and notify user of completion and location.

3. **Using the Roadmap:**
   - Always consult `llms.txt` and any `llms-[feature].txt` files for the library before external lookups.
   - If more detail is needed and the roadmap links externally, request permission to fetch, summarize, and update the roadmap as needed.

## Notes
- The roadmap should be a comprehensive, link-rich, index-style dump of the docs, with all major sections and links, minimal/no commentary.
- Do not summarize or paraphrase unless explicitly requested.
