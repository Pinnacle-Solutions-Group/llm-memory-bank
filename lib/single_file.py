"""Module for transforming rules into a single output file."""

import glob
import os
import re
from pathlib import Path
from typing import Dict, List

from .common import extract_frontmatter, validate_frontmatter


def transform_to_project_single_file(project_folder: str, dst_file: str) -> None:
    """Transform rules into a single file, sorting by priority."""
    # Get all .md files recursively from the rules directory in the current package
    template_folder = Path(__file__).parent.parent
    rules_dir = template_folder / "rules"
    rule_files = glob.glob(os.path.join(rules_dir, "**/*.md"), recursive=True)

    # Filter and sort rules with activation: always
    always_rules: List[Dict] = []
    for file in rule_files:
        with open(file, "r") as f:
            content = f.read()
            frontmatter, body = extract_frontmatter(content)
            if frontmatter.get("single_file") == "skip":
                continue
            if frontmatter.get("activation") == "always":
                # Validate frontmatter first
                validate_frontmatter(frontmatter)
                priority = int(frontmatter.get("priority", 999))
                # replace all markdown links to rules/ with just an emphasized subject
                body = re.sub(
                    r"\[([^\]]+)\]\(rules\/([^\)]+)\)",
                    r"**\1**",
                    body,
                )
                always_rules.append(
                    {
                        "name": os.path.basename(file).replace(".md", ""),
                        "priority": priority,
                        "description": frontmatter.get("description", ""),
                        "body": body,
                    }
                )

    # Sort rules by priority
    always_rules.sort(key=lambda x: x["priority"])

    output_path = os.path.join(project_folder, dst_file)

    with open(output_path, "w") as f:
        for i, rule in enumerate(always_rules):
            if i > 0:
                f.write("\n\n---\n\n")  # Extra newline before separator
            f.write(
                f"# Rule: {rule['name']}\n\n## {rule['description']}\n\n{rule['body'].strip()}"
            )
