"""Module for transforming rules into a single output file."""

import glob
import os
import re
from pathlib import Path
from typing import Dict, List

from .common import extract_frontmatter, validate_frontmatter


def extract_priority_from_filename(filename: str) -> int:
    """Extract priority from filename in format ##-RuleName.md.
    
    Args:
        filename: Base filename (not full path)
        
    Returns:
        Priority as integer, or 999 if no priority prefix found
    """
    # Extract just the filename without directory
    basename = os.path.basename(filename)
    
    # Check if filename starts with ##- pattern
    match = re.match(r'^(\d{1,2})-', basename)
    if match:
        return int(match.group(1))
    
    # Default priority for files without numeric prefix
    return 999


def transform_to_project_single_file(project_folder: str, dst_file: str) -> None:
    """Transform rules into a single file, sorting by priority."""
    # Get all .md files recursively from the rules directory in the current package
    template_folder = Path(__file__).parent.parent
    rules_dir = template_folder / "rules"
    rule_files = glob.glob(os.path.join(rules_dir, "**/*.md"), recursive=True)

    # Group rules by target location
    main_rules: List[Dict] = []  # For CLAUDE.md (single_file: true)
    section_rules: Dict[str, List[Dict]] = {}  # For memory-bank sections

    for file in rule_files:
        with open(file, "r") as f:
            content = f.read()
            frontmatter, body = extract_frontmatter(content)
            single_file_value = frontmatter.get("single_file", False)

            # Skip if single_file is false or "skip" (backward compatibility)
            if single_file_value in [False, "false", "skip"]:
                continue

            if frontmatter.get("activation") == "always":
                # Validate frontmatter first
                validate_frontmatter(frontmatter)
                # Extract priority from filename instead of frontmatter
                priority = extract_priority_from_filename(file)
                # replace all markdown links to rules/ with just an emphasized subject
                body = re.sub(
                    r"\[([^\]]+)\]\(rules\/([^\)]+)\)",
                    r"**\1**",
                    body,
                )
                rule_data = {
                    "name": os.path.basename(file).replace(".md", ""),
                    "priority": priority,
                    "description": frontmatter.get("description", ""),
                    "body": body,
                }

                # Determine target location
                if single_file_value == True or single_file_value == "true":
                    main_rules.append(rule_data)
                elif isinstance(
                    single_file_value, str
                ) and single_file_value.startswith("section:"):
                    section_path = single_file_value[8:]  # Remove "section:" prefix
                    if section_path not in section_rules:
                        section_rules[section_path] = []
                    section_rules[section_path].append(rule_data)

    # Sort rules by priority
    main_rules.sort(key=lambda x: x["priority"])

    # Write main CLAUDE.md
    output_path = os.path.join(project_folder, dst_file)
    with open(output_path, "w") as f:
        # Add header if it's CLAUDE.md
        if dst_file == "CLAUDE.md":
            f.write("# CLAUDE.md\n\n")
            f.write(
                "This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.\n\n"
            )

            # Add conditional loading instructions if there are section rules
            if section_rules:
                f.write("## Conditional Instructions\n\n")
                for section_path in sorted(section_rules.keys()):
                    f.write(f"- When working with {section_path.replace('/', ' ')}, ")
                    f.write(
                        f"consult `/{section_path}/CLAUDE.md` for additional instructions.\n"
                    )
                f.write("\n")

            if main_rules:
                f.write("## Core Rules\n\n")

        # Write main rules
        for i, rule in enumerate(main_rules):
            if i > 0:
                f.write("\n\n---\n\n")  # Extra newline before separator
            f.write(
                f"# Rule: {rule['name']}\n\n## {rule['description']}\n\n{prefix_headers(rule['body'].strip())}"
            )

    # Write section-specific files
    for section_path, rules in section_rules.items():
        rules.sort(key=lambda x: x["priority"])
        section_output_path = os.path.join(project_folder, section_path, "CLAUDE.md")

        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(section_output_path), exist_ok=True)

        with open(section_output_path, "w") as f:
            # Add header for section-specific CLAUDE.md
            f.write(
                f"# {section_path.split('/')[-1].title()} Instructions for Claude Code\n\n"
            )
            f.write(
                f"These instructions apply when working with {section_path.replace('/', ' ')}.\n\n"
            )

            for i, rule in enumerate(rules):
                if i > 0:
                    f.write("\n\n---\n\n")
                f.write(
                    f"# Rule: {rule['name']}\n\n## {rule['description']}\n\n{prefix_headers(rule['body'].strip())}"
                )


def prefix_headers(markdown: str) -> str:
    """Add an additional '#' before each Markdown header line."""
    lines = markdown.splitlines()
    new_lines = []
    for line in lines:
        if line.lstrip().startswith("#"):
            # Add one more '#' before the first sequence of #'s
            idx = 0
            while idx < len(line) and line[idx] == "#":
                idx += 1
            new_lines.append("#" + line)
        else:
            new_lines.append(line)
    return "\n".join(new_lines)
