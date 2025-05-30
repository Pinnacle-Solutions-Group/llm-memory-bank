
## 🛠️ CLI Usage: main.py

You can use the provided CLI tool to manage rules and lint documentation links. Run:

```text
Usage: main.py [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  lint              Lint all markdown links in the project and warn if links are broken
  project-to-rules  <project-dir> Compare .cursor/rules/*.mdc to rules/*.md after reversing the mdc: links
  rules-to-project  <project-dir> Copy rules to project/.cursor/rules with path/content, 
                                  renaming to .mdc and changing markdown links to mdc:
```

- **lint**: Lint all markdown links in the project and warn if any are broken or malformed.
- **project-to-rules**: Compare `.cursor/rules/*.mdc` to `rules/*.md` after project changes and sync as needed.
- **rules-to-project**: Copy rules to `project/.cursor/rules` with correct path/content for project use.

---
