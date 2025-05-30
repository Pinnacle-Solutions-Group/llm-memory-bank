# Rules for LLM-Assisted Development

This directory contains rules and guidelines to help the LLM (you) effectively assist in the development of the expense report application.

## Categories

- **`core/`**: Fundamental rules that should generally always be active. These cover basic interaction, how to use the memory bank, and core project tenets.
- **`best-practices/`**: Guidelines derived from experience and common pitfalls. These help in producing higher quality code and avoiding rework.
- **`workflow/`**: Rules tailored to specific phases of development:
  - `planning/`: For when we are defining scope, features, and architecture.
  - `implementation/`: For when we are actively writing code.
  - `debugging/`: For when we are identifying and fixing issues.

Consult the `README.md` within each subdirectory for a description of the rules it contains.

## Frontmatter Specification

All rule files use unified YAML frontmatter that supports both Cursor and Windsurf editors. The transformation system converts this to editor-specific formats during deployment.

### Unified Frontmatter Format

```yaml
---
description: Human-friendly description of what this rule does
globs: "**/*.ts,**/*.tsx,**/*.js,**/*.jsx"  # File patterns (optional)
alwaysApply: true                            # Boolean: always active (optional, default: false)
trigger: "always"                           # Windsurf trigger mode (optional, derived from alwaysApply)
---
```

### Field Definitions

#### Required Fields
- **`description`**: Human-readable summary of the rule's purpose
  - Used by both editors for rule documentation
  - Used by Windsurf AI for "model decision" mode relevance

#### Optional Fields
- **`globs`**: File pattern matching
  - **Format**: Comma-separated glob patterns as string
  - **Example**: `"**/*.ts,**/*.tsx,**/*.js,**/*.jsx"`
  - **Both editors**: Use comma-separated string format
  - **Default**: `null` (no file restrictions)

- **`alwaysApply`**: Cursor-style always-on flag
  - **Type**: Boolean
  - **Purpose**: When `true`, rule applies to all contexts
  - **Default**: `false`

- **`trigger`**: Windsurf-style activation mode
  - **Values**: `"always"`, `"glob"`, `"model"`, `"manual"`
  - **Auto-derived**: If not specified, derived from `alwaysApply` and `globs`
  - **Override**: Can be explicitly set to override derivation

### Trigger Derivation Logic

When `trigger` is not explicitly set, it's derived as follows:

1. **`alwaysApply: true`** → `trigger: "always"`
2. **`globs` present** → `trigger: "glob"`
3. **Neither condition** → `trigger: "model"` (AI decides based on description)

### Editor-Specific Transformations

#### Cursor (.mdc files)
```yaml
---
description: Human-friendly description
globs: "**/*.ts,**/*.tsx"       # Comma-separated format
alwaysApply: true               # Boolean preserved
---
```

#### Windsurf (.md files)
```yaml
---
trigger: always                               # String format
description: Human-friendly description      # String preserved
globs: "**/*.ts,**/*.tsx"                     # Comma-separated format
---
```

### Examples

#### Always-Active Core Rule
```yaml
---
description: Defines core AI operational guidelines and FOCUS determination
alwaysApply: true
# trigger automatically becomes "always"
---
```

#### File-Pattern Specific Rule
```yaml
---
description: TypeScript and React component development standards
globs: "**/*.ts,**/*.tsx,**/*.js,**/*.jsx"
# trigger automatically becomes "glob"
---
```

#### Model-Decision Rule
```yaml
---
description: Advanced debugging techniques for complex system issues
# No alwaysApply or globs - trigger becomes "model"
---
```

#### Manual-Invocation Rule
```yaml
---
description: Generate comprehensive API documentation
trigger: "manual"
# Explicitly set to manual override
---
```

### Maintainer Notes

- **Source of Truth**: Rules in `rules/` directory use unified frontmatter
- **Transformation**: `lib/cursor/` and `lib/windsurf/` modules handle editor-specific conversion
- **Validation**: CLI lint command checks frontmatter consistency
- **Editor Testing**: Test transformations in real projects before committing changes
