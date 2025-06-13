# LLM Memory Bank

A tool for managing and synchronizing LLM prompt rules and memory files between template repositories and editor-specific project directories (Cursor `.cursor/` and Windsurf `.windsurf/`).

##  Documentation

Detailed documentation is available in [the docs/ folder](docs/index.md)

## 🎯 Purpose

This project solves the challenge of maintaining consistent LLM prompts and rules across different AI-powered editors while allowing for project-specific customizations. It handles:

- **File format transformations** (`.md` ↔ `.mdc` for Cursor)
- **Link rewriting** (`rules/file.md` ↔ `mdc:.cursor/rules/file.mdc`)
- **Frontmatter management** with project-specific descriptions
- **Bidirectional synchronization** between templates and projects
- **Link validation** and broken link detection

## 🎯 Team Collaboration & Governance

This project includes a sophisticated rule system that transforms how teams collaborate with AI assistants. However, setup and configuration is required before teams can realize these benefits.

**📖 [Complete Setup and Usage Guide](docs/setup-and-usage.md)**

### Key Benefits (After Proper Setup)

#### **Team Efficiency**
- **Consistent AI assistance** regardless of experience level
- **Institutional knowledge capture** prevents repeated debugging  
- **Faster onboarding** through inherited AI knowledge

#### **Quality Assurance**
- **Built-in quality gates** prevent rushed implementations
- **Architecture compliance** automatically enforced
- **Technical debt prevention** through required planning

#### **LLM Accuracy**
- **Current documentation** used instead of outdated training data
- **Project-specific context** guides all AI responses
- **Systematic problem-solving** through FOCUS workflow

### ⚠️ Investment Required

- **Initial Setup**
- **Ongoing Maintenance**
- **Team Training**: FOCUS workflow and memory bank usage

**This is a framework, not plug-and-play.** See the [Setup Guide](docs/setup-and-usage.md) for detailed requirements.

## 🚀 Quick Start (Installation Only)

You have two main ways to set up the project: using [mise](https://mise.jdx.dev/) (recommended for automatic tool and environment management) or using `pip` with a Python virtual environment.

### Option 1: Using mise (Recommended)

```bash
# Clone the repository
git clone <repository-url>
cd llm-memory-bank

# Use mise for tool and environment management
mise trust
mise run setup
```

This will automatically:
- Install the correct Python version (Python 3.12 by default, as specified in `.mise.toml`).
- Set up the virtual environment using `uv` (a fast Python package installer and resolver, often used with `mise`).
- Install all required dependencies.

`mise` helps manage project-specific tool versions (like Python, Node.js) and environment variables, ensuring consistency across different setups. `uv` is a very fast alternative to `pip` and `venv`, significantly speeding up dependency installation and resolution.

### Option 2: Using pip and venv

If you prefer not to use `mise`, you can set up the project manually using `pip` and Python's built-in `venv` module.

1.  **Ensure Python is installed:** You'll need Python 3.12 or newer. You can check your Python version with `python --version`.
2.  **Clone the repository:**
    ```bash
    git clone <repository-url> # Replace <repository-url> with the actual URL
    cd llm-memory-bank
    ```
3.  **Create and activate a virtual environment:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows, use: .venv\Scripts\activate
    ```
4.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

This will install all necessary Python packages into your virtual environment. You will also need to ensure Node.js and npm/npx are installed and available in your PATH if you plan to use the `project-to-rules` command, as it relies on `markdownlint` which is typically installed via npx.

### Basic Usage

```bash
# Generate editor-specific rules at repository root
cd src && python main.py generate --editor cursor --force
cd src && python main.py generate --editor windsurf --force
cd src && python main.py generate --editor claude-code --force

# Or use mise to generate all formats
mise run generate-all

# Then copy the generated folders to your project:
# - Copy .cursor/ to your project root for Cursor
# - Copy .windsurf/ to your project root for Windsurf  
# - Copy CLAUDE.md to your project root for Claude Code
# - Copy memory-bank/ to your project root (for all editors)
```

**⚠️ IMPORTANT**: After installation, see [Setup and Usage Guide](docs/setup-and-usage.md) and your project's `LLM-README.md` for complete configuration instructions.

**📚 [Complete Documentation](docs/index.md)**

## 🛠️ CLI Reference

### Commands

#### `generate`
Generate editor-specific rules and configurations at the repository root.

```bash
cd src && python main.py generate --editor <cursor|windsurf|claude-code|aider-chat> [OPTIONS]
```

**Options:**
- `--force`: Overwrite existing files without prompting
- `--compare`: Show diffs before overwriting files
- `--editor`: Target editor [required]

**What it does:**
- For Cursor: Creates `.cursor/rules/*.mdc` with transformed links
- For Windsurf: Creates `.windsurf/rules/*.md` with path rewrites
- For Claude Code: Creates `CLAUDE.md` single file
- For Aider: Creates `CONVENTIONS.md` single file
- Copies `memory-bank/` to root (shared by all editors)

#### `lint`
Validate all markdown links in the project.

```bash
python main.py lint
```

**What it does:**
- Scans `rules/**/*.md` and `memory-bank/**/*.md`
- Reports broken links with file:line:column positions
- Validates link targets exist

## 📁 Project Structure

```text
llm-memory-bank/
├── .cursor/               # Generated Cursor rules (ready to copy!)
├── .windsurf/             # Generated Windsurf rules (ready to copy!)
├── CLAUDE.md              # Generated Claude file (ready to copy!)
├── memory-bank/           # Generated memory bank (ready to copy!)
├── src/                   # All source code
│   ├── main.py           # CLI entry point
│   ├── lib/              # Core library modules
│   │   ├── __init__.py
│   │   ├── common.py     # Shared utilities (frontmatter, file comparison)
│   │   ├── commands.py   # Generic command implementations
│   │   ├── cursor/       # Cursor-specific transformations
│   │   └── windsurf/     # Windsurf-specific transformations
│   ├── rules/            # Template rule files (.md)
│   ├── tests/            # Test suite
│   ├── docs/             # Documentation
│   └── config files      # README, LICENSE, .mise.toml, etc.
└── .gitignore            # Excludes generated folders
```

### Architecture

The codebase is organized into modular components:

- **`src/lib/common.py`**: Shared utilities like frontmatter parsing, file comparison, and diff tools
- **`src/lib/commands.py`**: Editor-agnostic command implementations that delegate to editor modules
- **`src/lib/cursor/`**: Cursor-specific transformations (`.md` ↔ `.mdc`, `mdc:` links)
- **`src/lib/windsurf/`**: Windsurf-specific transformations (path rewriting only)
- **`src/main.py`**: Lightweight CLI that imports and delegates to library modules

Each editor module implements the same interface:
- `transform_to_project(src, dst)` - Template → Project

## 🔄 Transformation Examples

### Cursor Transformations

**Template → Project:**
```markdown
<!-- rules/coding-style.md -->
See [best practices](rules/best-practices.md) for details.

<!-- → .cursor/rules/coding-style.mdc -->
See [best practices](mdc:.cursor/rules/best-practices.mdc) for details.
```

**Project → Template:**
```markdown
<!-- .cursor/rules/coding-style.mdc -->
See [best practices](mdc:.cursor/rules/best-practices.mdc) for details.

<!-- → rules/coding-style.md -->
See [best practices](rules/best-practices.md) for details.
```

### Windsurf Transformations

**Template → Project:**
```markdown
<!-- rules/coding-style.md -->
See [best practices](rules/best-practices.md) for details.

<!-- → .windsurf/rules/coding-style.md -->
See [best practices](.windsurf/rules/best-practices.md) for details.
```

### Frontmatter Management

The tool automatically manages YAML frontmatter, converting between unified template format and editor-specific formats:

- **Template format**: Unified structure in `rules/*.md` files
- **Cursor format**: All fields always present in `.cursor/rules/*.mdc` files  
- **Windsurf format**: Trigger-based activation in `.windsurf/rules/*.md` files

**📋 [Complete Frontmatter Documentation](docs/frontmatter-structure.md)**

## 🤝 Contributing

### Adding Support for New Editors

1. Create a new module: `lib/new_editor/__init__.py`
2. Implement the required interface:
   ```python
   def transform_to_project(src_path, dst_path):
       """Transform template file to project format."""
       pass
   
   def transform_from_project(src_path, dst_path, project_basename=None, master_description=None):
       """Transform project file back to template format."""
       pass
   ```
3. Update `main.py` to include the new editor in click choices and import the module
4. Update `lib/commands.py` if editor-specific directory logic is needed

### Development Guidelines

- **Modularity**: Keep editor-specific logic in respective modules
- **Consistency**: New editors should follow the same interface pattern
- **Safety**: Always validate file operations and provide clear error messages
- **Testing**: Test transformations with real project files
- **Documentation**: Update README and inline docs for new features

### Common Tasks

**Testing transformations:**
```bash
# Create a test project
mkdir test-project
python main.py rules-to-project test-project --editor cursor --force
# Modify files in test-project/.cursor/rules/
python main.py project-to-rules test-project --editor cursor
```

**Debugging link issues:**
```bash
python main.py lint  # Check for broken links
```

## 📋 Requirements

**For `mise` users:**
- [mise](https://mise.jdx.dev/) for tool and environment management.
- Dependencies (Python, Node.js, `uv`, Python packages) are managed automatically by `mise` as configured in `.mise.toml` and `pyproject.toml`.

**For `pip` users:**
- Python 3.12 or newer.
- `pip` and `venv` (usually included with Python).
- Dependencies are listed in `requirements.txt`.
- Node.js and npm/npx: Required for the `project-to-rules` command's automatic `markdownlint` execution. You'll need to install these separately.

**Optional:**
- `bcompare` for visual file comparison

## 🐛 Troubleshooting

**"Git repository not clean" error:**
- Commit or stash changes before running `project-to-rules`
- This prevents accidental loss of template changes

**Import errors:**
- Ensure you're running from the project root directory
- Check that all dependencies are installed

**File not found errors:**
- Verify project structure matches expected editor layout
- Use `--force` flag cautiously to overwrite existing files

## 📄 License

Copyright 2024 Mike Crowe <drmikecrowe@gmail.com> and Pinnacle Solutions Group <mike.crowe@pinnsg.com>

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

See [LICENSE](LICENSE) for the full license text.

---

*This tool enables seamless collaboration between AI-powered editors while maintaining a single source of truth for LLM prompts and rules.*
