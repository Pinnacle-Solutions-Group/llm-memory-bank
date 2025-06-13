# LLM Memory Bank: Setup and Usage Guide

## Overview

The LLM Memory Bank transforms AI-assisted development through structured rules and project-specific knowledge. **Setup and configuration is required before teams realize benefits.**

## 🚨 Reality Check: Investment Required

- **Initial Setup**
- **Ongoing Maintenance**
- **Team Training**: Understanding FOCUS workflow and memory bank patterns
- **Documentation Discipline**: Continuous memory bank maintenance

**This is a framework, not plug-and-play.** Teams must invest in setup and maintenance to realize benefits.

## 📋 Setup Requirements Checklist

### Phase 1: Essential Project Documentation (8-12 hours)

#### Core Project Files
- [ ] **`memory-bank/project/project_brief.md`** — Project overview, objectives, timeline
- [ ] **`memory-bank/project/product_context.md`** — Problem, solution, market context
- [ ] **`memory-bank/project/tech_context.md`** — **CRITICAL** - Exact tech stack versions
- [ ] **`memory-bank/project/directory_structure.md`** — Code organization patterns

#### Architecture Documentation
- [ ] **`memory-bank/project/architecture.md`** — System architecture, constraints
- [ ] **`memory-bank/project/system_patterns.md`** — Design patterns, data flow

#### Status Tracking
- [ ] **`memory-bank/status/project_status.md`** — Current progress, tasks, blockers

### Phase 2: Library Documentation (4-8 hours)

For each major library in `tech_context.md`:
- [ ] **Generate roadmap**: `memory-bank/reference/api_docs/[LIBRARY]/[VERSION]/llms.md`
- [ ] **Document key sections**: Create summaries for frequently used features
- [ ] **Establish update process**: Who maintains, when to update

### Phase 3: Process & Training (4-6 hours)

#### Documentation Processes
- [ ] **Troubleshooting log**: Set up `memory-bank/reference/troubleshooting_log.md`
- [ ] **Update responsibilities**: Assign memory bank maintenance ownership
- [ ] **Quality standards**: Define what constitutes complete documentation

#### Team Training
- [ ] **FOCUS workflow**: Planning → Implementation → Debugging
- [ ] **Memory bank usage**: When to consult, when to update
- [ ] **Rule customization**: Project-specific adaptations

## 🔄 Daily Usage Patterns

### FOCUS Workflow System

**🎯 PLANNING**: Requirements analysis, architecture design
- AI gathers context from memory bank
- Explores multiple solution approaches
- Requires explicit approval before implementation

**⚙️ IMPLEMENTATION**: Code writing, testing, standards application
- Validates against architecture documentation
- Uses current library documentation
- Enforces coding standards automatically

**🐛 DEBUGGING**: Error diagnosis, issue resolution
- References troubleshooting log for similar issues
- Documents solutions for future reference
- Updates memory bank with findings

### Setting FOCUS

**Explicit**: `"FOCUS = PLANNING: Design user authentication system"`
**Automatic**: AI infers from context
- "Design a new feature" → PLANNING
- "Implement the approved design" → IMPLEMENTATION
- "Fix the API error" → DEBUGGING

### Library Documentation Generation

**Create library roadmap**:
```text
"Generate documentation roadmap for React v18.2.0 from @web https://react.dev"
```

**Summarize specific sections**:
```text
"Summarize React Hooks from @web https://react.dev/learn/hooks"
```

## 🎯 Benefits Realized (After Setup)

### Team Efficiency
- **Consistent AI assistance** regardless of experience level
- **Institutional knowledge capture** prevents repeated debugging
- **Faster onboarding** through inherited AI knowledge

### Quality Assurance
- **Built-in quality gates** prevent rushed implementations
- **Architecture compliance** automatically enforced
- **Technical debt prevention** through required planning

### LLM Accuracy
- **Current documentation** used instead of outdated training data
- **Project-specific context** guides all AI responses
- **Systematic problem-solving** through FOCUS workflow

## 🔧 Memory Bank File Details

### Project Context Files

**`project_brief.md`**: Project name, objectives, users, milestones, team structure

**`product_context.md`**: Problem statement, solution approach, market analysis, competitive advantage

**`tech_context.md`**: Exact library versions, databases, integrations, deployment environments
- **CRITICAL**: Referenced by ALL rules - accuracy essential

**`directory_structure.md`**: File organization, naming conventions, configuration locations

### Architecture Files

**`architecture.md`**: System diagrams, component boundaries, data flow, constraints, dependencies

**`system_patterns.md`**: Design patterns, state management, error handling, testing strategies

### Status Files

**`project_status.md`**: Development phase, active tasks, milestones, blockers, recent decisions

### Reference Files

**`troubleshooting_log.md`**: Documented errors, root causes, solutions, recurring patterns

**`api_docs/[LIBRARY]/[VERSION]/llms.md`**: Library navigation roadmaps

**`api_docs/[LIBRARY]/[VERSION]/llms-[section].md`**: Detailed section summaries

## 🔄 Rule Application Flow

```text
User Request → AI Determines FOCUS → Apply Workflow Rules → 
Check Core Standards → Consult Memory Bank → Generate Response → 
Update Memory Bank if Needed
```

## 🚀 Getting Started

1. **Install** using instructions in main README
2. **Complete Phase 1** documentation (essential files)
3. **Set up one library** documentation as proof of concept
4. **Train team** on FOCUS workflow
5. **Establish maintenance** processes
6. **Scale** to additional libraries and advanced patterns

## 🎯 Success Indicators

You'll know the system is working when:
- AI responses reference your project's architecture consistently
- Team members get consistent answers regardless of who asks
- Error solutions are captured and reused effectively
- New team members can be productive immediately
- Technical debt stops accumulating due to rushed decisions

## ⚠️ Common Setup Mistakes

- **Incomplete tech context**: Leads to outdated library usage
- **Missing architecture docs**: AI can't enforce compliance
- **No maintenance process**: Documentation becomes stale
- **Skipping team training**: FOCUS workflow not adopted
- **Rushing setup**: Incomplete memory bank reduces effectiveness

## 📚 Additional Resources

- [Rules Documentation](rules-overview.md) - Complete rule system details
- Main README - Installation and CLI reference
- `LLM-README.md` in your project - Team usage guide 
