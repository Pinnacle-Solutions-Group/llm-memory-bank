---
description: Defines the core logic for the AI to determine its operational FOCUS
  (Planning, Implementation, Debugging) and how to apply other rule sets. This is
  the foundational rule.
globs: null
alwaysApply: true
---
# Meta-Rules for AI Assistant Interaction

<!-- BEGIN: Main Content -->

You will be guided by a set of rule files. Process them according to this meta-rule.

**Rule Categories & Purpose:**

- **This File ([00-meta-rules](rules/core/00-meta-rules.md)):** Governs overall system behavior and FOCUS determination.
- **Memory Bank ([memory-bank/](memory-bank/)):** Project-specific context, architecture, tech stack, status. Example: [architecture.md](memory-bank/project/architecture.md). Consult as directed by other rules and for situational awareness.
- **Core Rules (in [core/](rules/core)):** Essential operational guidelines. Example: [llm-interaction-guidelines](rules/core/llm-interaction-guidelines.md).
- **Best Practices (in [best-practices/](rules/best-practices)):** Project-wide best practices. Example: [lessons-learned](rules/best-practices/lessons-learned.md). **ALWAYS FOLLOW.**
- **Workflow Rules (in [workflow/](rules/workflow)):** Specific instructions for your current **FOCUS**: PLANNING, IMPLEMENTATION, or DEBUGGING. Example: [planning-rules](rules/workflow/planning/planning-rules.md).

**Determining Your Operational FOCUS and Applicable Rules:**

Your primary goal is to identify the correct FOCUS and apply the corresponding rules. Use this hierarchy:

1. **Explicit User Command (Overrides All):**

   - **Check:** Does the user's LATEST request contain `FOCUS = PLANNING`, `FOCUS = IMPLEMENTATION`, or `FOCUS = DEBUGGING`?
   - **Action:** If YES, adopt that FOCUS. Apply its specific workflow rules from [workflow/[FOCUS]/](rules/workflow/) along with Core Rules and Best Practices.

2. **Infer Task Intent (Primary Method if No Explicit Command):**

   - **Analyze User's Current Request:**
     - High-level design, analysis, planning, solution exploration? -> **FOCUS = PLANNING** (Use rules from [workflow/planning/ folder](rules/workflow/planning))
     - Writing code, direct modifications, implementing known steps? -> **FOCUS = IMPLEMENTATION** (Use rules from [workflow/implementation/ folder](rules/workflow/implementation))
     - Fixing errors, diagnosing issues, analyzing failures? -> **FOCUS = DEBUGGING** (Use rules from [workflow/debugging/ folder](rules/workflow/debugging))
   - **Uncertainty:** If intent is unclear, ASK the user to specify the FOCUS.

3. **Assistant's Internal State (Context/Cross-Check - If Applicable):**
   - (This section applies if you have persistent internal modes like 'Act', 'Debug', 'Architect'.)
   - **Cross-check:** Does your internal mode conflict with the FOCUS from Step 2?
     - _Conflict Example:_ Internal Mode = 'Debug', but request implies `FOCUS = PLANNING`.
   - **Action on Conflict:** Notify the user: "My current internal mode is [Your Mode]. Your request suggests [FOCUS from Step 2]. I will proceed with FOCUS = [FOCUS from Step 2]. Is this correct, or should I stay in [Your Mode]?" _Prioritize FOCUS from Step 2 after notifying._
   - **Ambiguity:** If your mode covers multiple FOCUS types, rely on FOCUS from Step 2 for rule selection.

**Applying Rules:**

- **Always Apply:**
  - Relevant Core Rules (e.g., [memory-bank-usage](rules/core/memory-bank-usage.md), [general-coding-conventions](rules/core/general-coding-conventions.md)).
  - All rules in [best-practices/](rules/best-practices).
- **Apply One Workflow Set:** The single, most relevant workflow rule set from [workflow/[FOCUS]/](rules/workflow/) based on the determined FOCUS.
- **Consult Memory Bank:** Actively use files in [memory-bank/](memory-bank/) for context, validation, and to inform your actions, as guided by [llm-memory-interaction](rules/core/llm-memory-interaction.md) and the current workflow.

<!-- END: Main Content -->

## Rules Directory Structure

```text
rules/
├── best-practices/
│   ├── error_documentation_guidelines.md
│   ├── lessons-learned.md
│   └── README.md
├── core/
│   ├── 00-meta-rules.md
│   ├── general-coding-conventions.md
│   ├── llm-interaction-guidelines.md
│   ├── llm-memory-interaction.md
│   ├── memory-bank-usage.md
│   └── README.md
├── project/
│   └── README.md
└── workflow/
    ├── debugging/
    │   ├── debugging_rules.md
    │   └── README.md
    ├── implementation/
    │   ├── implementation_rules.md
    │   └── README.md
    ├── planning/
    │   ├── planning-rules.md
    │   └── README.md
    └── README.md
```
