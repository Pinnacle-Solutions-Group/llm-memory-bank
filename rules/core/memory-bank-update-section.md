---
description: null
globs: null
alwaysApply: false
---
# LLMs Update Summary Rule

## Purpose

Defines the workflow for creating and maintaining `llms-[section].txt` summary/overview files for specific library features or documentation sections.

If the user requests a documentation roadmap or summary for a library, always create or update the corresponding file in the memory bank, unless the user says otherwise.

## Workflow

1. **When a summary or technical overview is requested:**
   - When asked to create or update an llms.txt for a library, you MUST write the file to `memory-bank/reference/api_docs/[LIBRARY_NAME]/[MAJOR_VERSION]/llms.txt`, not just output the content in chat. If the directory does not exist, create it.
   - Crawl ONLY the specified page/section.
   - Produce a detailed, LLM-friendly, prose-style technical overview of the content, suitable for direct use in code or as developer reference.
   - Save the output to `memory-bank/reference/api_docs/[LIBRARY_NAME]/[MAJOR_VERSION]/llms-[section].txt` (e.g., llms-authentication.txt).
   - Update the main `llms.txt` reference index to include a link to this new file, e.g.:
     - `[Authentication](memory-bank/reference/api_docs/aws-amplify/6/llms-authentication.txt)`
   - Do NOT summarize or crawl other sections unless explicitly requested.
   - The summary should be thorough, accurate, and LLM-optimized (clear, structured, with code/examples if relevant).

2. **Default Behavior:**
   - If the user does NOT request a summary/overview, default to the reference/index dump behavior as defined in `llms-update-library.mdc`.

## Notes
- Summaries must be explicitly requested ("summary", "detailed summary", "technical overview", or "LLM-friendly documentation").
- Do not add commentary, prose, or explanations unless explicitly requested.
