# LLM Memory Bank Documentation

Welcome to the LLM Memory Bank documentation. This tool enables seamless collaboration between AI-powered editors while maintaining a single source of truth for LLM prompts and rules.

## 📚 Documentation Overview

### Getting Started

- **[Setup and Usage Guide](setup-and-usage.md)** - Complete setup instructions, team collaboration guidelines, and usage patterns
  - Initial project setup and configuration
  - Team collaboration workflows
  - FOCUS methodology explanation
  - Memory bank organization

### Technical Reference

- **[Frontmatter Structure](frontmatter-structure.md)** - Detailed YAML frontmatter format specifications
  - Template format (unified)
  - Cursor format (.mdc files)
  - Windsurf format (.md files)
  - Transformation rules and validation
  - Common issues and troubleshooting

- **[Rules Overview](rules-overview.md)** - Comprehensive guide to the rule system
  - Rule categories and organization
  - Core meta-rules and FOCUS workflow
  - Project-specific rule patterns
  - Best practices for rule creation

## 🎯 Quick Navigation

### For New Users
1. Start with [Setup and Usage Guide](setup-and-usage.md) to understand the system
2. Review [Rules Overview](rules-overview.md) to understand the rule structure
3. Reference [Frontmatter Structure](frontmatter-structure.md) when creating new rules

### For Developers
1. Check [Frontmatter Structure](frontmatter-structure.md) for technical implementation details
2. Review transformation rules and validation requirements
3. See the main README for architecture and contributing guidelines

### For Team Leads
1. Read [Setup and Usage Guide](setup-and-usage.md) for governance and team workflows
2. Understand the investment required and team training needs
3. Plan for ongoing maintenance and rule evolution

## 🛠️ Tool Reference

## 📋 Key Concepts

### Frontmatter Requirements
- **All fields always present**: Never omit fields, show empty as `field:`
- **Editor-specific formats**: Each editor has different required fields
- **Automatic transformations**: Tool handles conversions between formats

### Rule Categories
- **Core Meta Rules**: AI behavior and FOCUS workflow
- **Workflow Rules**: Planning, implementation, debugging processes  
- **Best Practices**: Coding standards and quality guidelines
- **Project-Specific**: Customized rules for specific codebases

### Transformation Process
1. **Template → Editor**: Converts unified format to editor-specific format
2. **Link Rewriting**: Updates internal links for each editor
3. **Field Mapping**: Ensures all required fields are present
4. **Validation**: Checks format compliance and data integrity

## 🤝 Contributing

When contributing to documentation:

1. **Keep it current**: Update docs when implementing new features
2. **Be specific**: Include exact code examples and error messages
3. **Test examples**: Verify all code snippets work as documented
4. **Cross-reference**: Link between related documentation sections

## 🛠️ For Developers & Maintainers

**Implementation Details:**
- [Frontmatter Structure](frontmatter-structure.md) - Complete YAML frontmatter specifications
- Cross-editor field derivation and preservation logic
- **Automated Quality Assurance**: markdownlint runs automatically after `project-to-rules`
- Comprehensive test suite (38 tests) covering all transformations

**Development Workflow:**
1. Make changes in editor-specific project files
2. Run `project-to-rules` to sync back to template
3. Automatic markdownlint fixes formatting issues
4. Commit unified template changes
5. Use `rules-to-project` to deploy to other projects
