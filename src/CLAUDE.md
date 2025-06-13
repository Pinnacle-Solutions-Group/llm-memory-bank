# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Core Commands

### Development Commands
```bash
# Run tests (from src/ directory)
cd src && python -m pytest

# Lint/format code (from src/ directory)  
cd src && ruff format **/*.py
cd src && ruff check **/*.py

# Format markdown (from root)
npx markdownlint '**/*.md' --fix --ignore node_modules/ --config .markdownlint.json

# Run using mise (if available)
mise run format        # Format both Python and Markdown
mise run test          # Run tests
mise run generate-all  # Generate all output formats
mise run info          # Show environment info
```

### Main CLI Commands
```bash
# Generate editor-specific rules in output/ directory (run from src/)
cd src && python main.py generate --editor cursor --force
cd src && python main.py generate --editor windsurf --force
cd src && python main.py generate --editor claude-code --force  
cd src && python main.py generate --editor aider-chat --force

# Validate markdown links (run from src/)
cd src && python main.py lint

# Or use mise tasks (from root):
mise run generate-cursor
mise run generate-windsurf  
mise run generate-all
mise run lint
```

## Architecture Overview

This is a **transformation engine** that generates editor-specific LLM prompt rules and memory banks at the repository root.

### Project Structure
```
llm-memory-bank/
├── .cursor/              # Generated Cursor rules (ready to copy!)
├── .windsurf/            # Generated Windsurf rules (ready to copy!)
├── CLAUDE.md             # Generated Claude file (ready to copy!)
├── memory-bank/          # Project memory bank (ready to copy!)
├── src/                  # All source code and documentation
│   ├── main.py           # CLI entry point  
│   ├── lib/              # Core transformation logic
│   ├── rules/            # Template rules (.md files)
│   ├── tests/            # Test suite
│   ├── docs/             # Documentation
│   └── all config files  # README, LICENSE, .mise.toml, etc.
└── .gitignore            # Excludes generated folders
```

### Core Components

**`src/main.py`** - CLI entry point with Click commands
- `generate` command creates outputs at repository root
- Supports cursor, windsurf, claude-code, aider-chat editors
- `lint` command validates markdown links

**`src/lib/commands.py`** - Editor-agnostic command implementations  
- `rules_to_project_impl()` - Transform template rules to editor format
- Handles file comparison and diff tools integration

**`src/lib/common.py`** - Shared utilities
- Frontmatter parsing and manipulation
- File comparison with `filecmp()`  
- Diff tools integration (bcompare support)

**Editor Modules** - Transform content between template and editor formats:
- **`src/lib/cursor/`** - `.md` ↔ `.mdc` transformations, `mdc:` link prefixes
- **`src/lib/windsurf/`** - Path rewriting transformations
- **`src/lib/single_file.py`** - Generate single files (CLAUDE.md, CONVENTIONS.md)

### Key Transformations

**Link Rewriting:**
- Template: `[text](rules/file.md)` 
- Cursor: `[text](mdc:.cursor/rules/file.mdc)`
- Windsurf: `[text](.windsurf/rules/file.md)`

**File Extensions:**
- Template: `rules/*.md`
- Cursor: `.cursor/rules/*.mdc` 
- Windsurf: `.windsurf/rules/*.md`

**Frontmatter Management:**
- Unified template format with cross-editor field derivation
- Cursor `alwaysApply` ↔ Windsurf `trigger` field conversion
- Project-specific descriptions injected during transformation

### Safety Features

- Git status checking before `project-to-rules` operations
- File comparison with skip/force/compare options
- Automatic markdownlint execution after project-to-rules
- Temporary file handling with cleanup

## Testing

Run tests with: `cd src && python -m pytest` or `mise run test`

Test files are in `src/tests/` directory:
- `test_frontmatter.py` - Frontmatter parsing and manipulation
- `test_single_file.py` - Single file generation  
- `test_transformations.py` - Editor transformation logic

## Usage for End Users

1. **Download this repository** 
2. **Generate outputs**: `cd src && python main.py generate --editor cursor --force`
3. **Copy to your project**: Copy `.cursor/` and `memory-bank/` from root to your project
4. **Enjoy**: LLM rules and memory bank are now active in your project