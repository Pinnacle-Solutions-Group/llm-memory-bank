# Single File Generation (CLAUDE.md, CONVENTIONS.md)

This document explains how the `single_file` frontmatter field controls which rules are included in generated single files like `CLAUDE.md` and `CONVENTIONS.md`.

## Frontmatter Field: `single_file`

The `single_file` field in rule frontmatter determines where (if anywhere) a rule should be included in single-file outputs.

### Possible Values

1. **`false`** (default) - The rule is not included in any single file output
   ```yaml
   single_file: false
   ```

2. **`true`** - The rule is included in the main output file (`CLAUDE.md` or `CONVENTIONS.md`)
   ```yaml
   single_file: true
   ```

3. **`section:<path>`** - The rule is placed in a section-specific file
   ```yaml
   single_file: section:memory-bank
   ```
   This creates `/memory-bank/CLAUDE.md` with rules specific to that section.

### Backward Compatibility

For backward compatibility, `single_file: skip` is treated the same as `single_file: false`.

## How It Works

When generating single files (for claude-code or aider-chat):

1. **Main File Generation**
   - Only rules with `activation: always` AND `single_file: true` are included
   - Rules are sorted by priority (lower numbers first)
   - The main file includes conditional loading instructions for section files

2. **Section File Generation**
   - Rules with `single_file: section:<path>` are grouped by path
   - Each section gets its own `CLAUDE.md` file at `/<path>/CLAUDE.md`
   - Rules within each section are sorted by priority

3. **Conditional Loading**
   - The main `CLAUDE.md` includes instructions like:
     ```markdown
     ## Conditional Instructions
     
     - When working with memory-bank, consult `/memory-bank/CLAUDE.md` for additional instructions.
     ```

## Example Usage

### Core Rule (Always Active)
```yaml
---
description: Core coding standards
activation: always
priority: 10
single_file: true
---
```

### Memory Bank Specific Rule
```yaml
---
description: Memory bank usage guidelines
activation: always
priority: 20
single_file: section:memory-bank
---
```

### Editor-Only Rule (Not in Single Files)
```yaml
---
description: Cursor-specific formatting
activation: always
priority: 30
single_file: false
---
```

## Benefits

1. **Cleaner Main File** - Only essential rules in the root `CLAUDE.md`
2. **Context-Specific Loading** - Rules load only when relevant
3. **Better Organization** - Related rules stay together
4. **Reduced Context** - AI doesn't process irrelevant instructions

## Implementation Notes

- Section directories are created automatically if they don't exist
- Each section file includes a header explaining when it applies
- The main file always includes the conditional loading instructions when section files exist