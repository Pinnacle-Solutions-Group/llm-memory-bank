# Frontmatter Structure

The LLM Memory Bank tool manages YAML frontmatter automatically, converting between a unified template format and editor-specific formats. This document explains the structure and requirements for each format.

## Template Format (rules/*.md)

All rule files in the template use a unified frontmatter structure with all fields always present:

```yaml
---
description: "Rule description here"
globs: "**/*.ts,**/*.tsx"
alwaysApply: false
trigger: "manual"  # Optional, only when explicitly set
---
```

**Template format rules:**
- ✅ **All fields always present**: `description`, `globs`, `alwaysApply` appear in every file
- ✅ **Empty fields show blank**: `globs:` instead of `globs: null` 
- ✅ **Quoted values**: String values are quoted in template format
- ✅ **Trigger preservation**: Windsurf-specific trigger field preserved when present
- ✅ **Cross-editor compatibility**: Contains fields for both Cursor and Windsurf

**Fields:**
- `description`: Rule description (required, always present)
- `globs`: File patterns as comma-separated string (always present, empty if not applicable)
- `alwaysApply`: Boolean flag (required, always present)
- `trigger`: Windsurf-specific trigger type (optional, preserved if present)

**Template examples:**

*Rule with globs:*
```yaml
---
description: "TypeScript coding standards"
globs: "**/*.ts,**/*.tsx"
alwaysApply: false
---
```

*Rule without globs:*
```yaml
---
description: "Core meta rules for AI behavior"
globs: 
alwaysApply: true
---
```

## Cross-Editor Field Derivation

When transforming between editor formats via the template, the tool intelligently derives missing cross-editor fields:

### Cursor → Template → Windsurf

When importing from Cursor, the tool derives Windsurf's `trigger` field:

1. **Preservation First**: If the template file already exists and has a `trigger` field, it's preserved
2. **Derivation Logic**: If no existing trigger, derives from Cursor fields:
   - `alwaysApply: true` → `trigger: "always"`
   - Globs present + `alwaysApply` omitted → `trigger: "glob"` (Auto-Attached)
   - `alwaysApply: false` + empty globs + has description → `trigger: "model"` (Agent-Requested)
   - `alwaysApply: false` + empty globs + minimal description → `trigger: "manual"`

### Windsurf → Template → Cursor

When importing from Windsurf, the tool derives Cursor's `alwaysApply` field:

1. **Preservation First**: If the template file already exists and has an `alwaysApply` field, it's preserved
2. **Derivation Logic**: If no existing alwaysApply, derives from Windsurf trigger:
   - `trigger: "always"` → `alwaysApply: true`
   - All other triggers → `alwaysApply: false`

**Example transformation sequence:**
```yaml
# 1. Cursor source (.cursor/rules/typescript.mdc)
---
description: TypeScript rules
globs: **/*.ts
---

# 2. Template (rules/typescript.md) - adds derived trigger
---
description: "TypeScript rules"  
globs: "**/*.ts"
alwaysApply: false
trigger: "glob"  # ← Derived from globs presence + alwaysApply omission
---

# 3. Windsurf output (.windsurf/rules/typescript.md)
---
trigger: glob
description: TypeScript rules
globs: **/*.ts
---
```

## Cursor Format (.cursor/rules/*.mdc)

Cursor requires specific fields to be present for different rule activation types:

```yaml
---
description: TypeScript coding standards
globs: **/*.ts,**/*.tsx
---

```

### Cursor-Specific Rules

- ✅ **Field presence depends on rule type**: Different rule types require different fields
- ✅ **Auto-Attached behavior**: Omitting `alwaysApply` when globs are present triggers auto-attachment
- ✅ **Empty fields show blank**: `globs:` instead of omitting the field entirely  
- ✅ **No quotes on values**: Clean format without unnecessary quotation marks
- ✅ **Double newline after frontmatter**: Two blank lines before content begins
- ❌ **No trigger field**: Cursor doesn't use trigger-based activation

### Cursor Rule Types & Field Requirements

**Always Rules** (`alwaysApply: true`):
```yaml
---
description: Core meta rules for AI behavior  
globs: 
alwaysApply: true
---
```

**Auto-Attached Rules** (globs present, `alwaysApply` omitted):
```yaml
---
description: TypeScript coding standards
globs: **/*.ts,**/*.tsx
---
```

**Agent-Requested Rules** (`alwaysApply: false` + empty globs):
```yaml
---
description: Advanced debugging techniques
globs: 
alwaysApply: false
---
```

**Manual Rules** (`alwaysApply: false` + minimal fields):
```yaml
---
description: 
globs: 
alwaysApply: false
---
```

### Key Insight: Auto-Attached Behavior

⚠️ **Critical Field Requirements by Rule Type**:

- **Always Rules**: Must include `alwaysApply: true`
- **Auto-Attached Rules**: Must **omit** `alwaysApply` entirely when globs are present
- **Agent-Requested Rules**: Must include `alwaysApply: false` with empty globs  
- **Manual Rules**: Must include `alwaysApply: false` with minimal fields

**Auto-Attached Rule Behavior**: When globs are present and `alwaysApply` is missing, Cursor automatically attaches the rule when working with matching files. Including `alwaysApply: false` would disable this auto-attachment behavior.

### Cursor Examples

*Always rule (alwaysApply: true):*
```yaml
---
description: Core meta rules for AI behavior
globs: 
alwaysApply: true
---
```

*Auto-Attached rule (globs present, alwaysApply omitted):*
```yaml
---
description: TypeScript coding standards and best practices
globs: **/*.ts,**/*.tsx,**/*.js,**/*.jsx
---
```

*Agent-Requested rule (alwaysApply: false + empty globs):*
```yaml
---
description: Advanced debugging techniques for complex issues
globs: 
alwaysApply: false
---
```

*Manual rule (alwaysApply: false + minimal fields):*
```yaml
---
description: 
globs: 
alwaysApply: false
---
```

## Windsurf Format (.windsurf/rules/*.md)

Windsurf also requires all fields present, with trigger-based activation:

```yaml
---
trigger: glob
description: TypeScript coding standards
globs: **/*.ts,**/*.tsx
---
```

### Windsurf-Specific Rules

- ✅ **All fields always present**: `trigger`, `description`, `globs` appear in every file
- ✅ **Empty fields show blank**: `globs:` instead of omitting the field entirely
- ✅ **No quotes on values**: Clean format without unnecessary quotation marks
- ✅ **Single newline after frontmatter**: One blank line before content begins
- ✅ **Automatic trigger derivation**: Derived from `alwaysApply` and `globs` if not explicit

### Trigger Derivation Logic

- `alwaysApply: true` → `trigger: always`
