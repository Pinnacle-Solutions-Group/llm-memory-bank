# Required Setup for the LLM Memory Bank

## 🧠 Memory Bank: What to Update First

Update these files to reflect your project:

- [ ] `memory-bank/project/project_brief.md` — Project overview, objectives, users, timeline, metrics
- [ ] `memory-bank/project/product_context.md` — Problem, solution, value, market, competitive advantage
- [ ] `memory-bank/project/architecture.md` — System architecture (add if missing)
- [ ] `memory-bank/project/system_patterns.md` — Design patterns, data flow, security (add if missing)
- [ ] `memory-bank/project/tech_context.md` — Tech stack, integrations, deployment (add if missing)
- [ ] `memory-bank/project/directory_structure.md` — Source code layout
- [ ] `memory-bank/status/project_status.md` — Current progress, tasks, milestones, blockers
- [ ] `memory-bank/reference/troubleshooting_log.md` — Error log (add if missing)
- [ ] `memory-bank/reference/user_docs/` — End-user guides (optional)
- [ ] `memory-bank/reference/release_docs/` — Release notes (optional)

## NOTE: Utilize the LLM to assist with this

Here is a real-world example of starting the architecture:

> My plan for this is to use @tech_context.md and build the @project_brief.md
> Users will be able to take photos of receipts from their phone, and their receipts should be uploaded to:
> [bucket]/receipts/[user-email]/[yyyy-mm-dd]/[guid].png
> using amplify.  It will then be submitted to OpenAI for recognition and categorization and entered into the DynamoDB database
> Then, when complete, the user can flag the expense report to be approved and download an excel copy
