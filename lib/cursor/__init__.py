"""Cursor editor specific transformations."""

import re

from ..common import create_cursor_frontmatter, extract_frontmatter


def transform_to_project(src_path, dst_path):
    """Transform from template format to cursor project files (.cursor/rules/)."""
    with open(src_path, "r") as f:
        content = f.read()

    frontmatter, body = extract_frontmatter(content)

    # Convert old-style frontmatter to new activation-based format if needed
    if frontmatter and "activation" not in frontmatter:
        frontmatter = convert_legacy_to_activation(frontmatter)

    # Transform links in body
    body = re.sub(
        r"\(rules/([^)]+)\.md\)",
        lambda m: f"(mdc:.cursor/rules/{m.group(1)}.mdc)",
        body,
    )
    body = re.sub(r"\(memory-bank/", r"(mdc:memory-bank/", body)

    # Replace placeholders with final paths
    body = body.replace("CURSOR_RULE_PLACEHOLDER_", "mdc:.cursor/rules/")

    # Apply Cursor-specific frontmatter formatting
    cursor_frontmatter = create_cursor_frontmatter(frontmatter)

    with open(dst_path, "w") as f:
        f.write(cursor_frontmatter + body)


def convert_legacy_to_activation(frontmatter):
    """Convert legacy frontmatter (alwaysApply/globs/trigger) to activation-based format."""
    new_frontmatter = {}

    # Preserve description
    if "description" in frontmatter:
        new_frontmatter["description"] = frontmatter["description"]

    # Determine activation from legacy fields
    always_apply = frontmatter.get("alwaysApply", False)
    globs = frontmatter.get("globs", "")
    trigger = frontmatter.get("trigger", "")

    if always_apply is True:
        new_frontmatter["activation"] = "always"
    elif globs and globs.strip() and globs not in ["null"]:
        new_frontmatter["activation"] = "glob"
        new_frontmatter["globs"] = globs
    elif trigger == "manual":
        new_frontmatter["activation"] = "manual"
    else:
        new_frontmatter["activation"] = "agent-requested"

    return new_frontmatter


def transform_from_project(
    src_path, dst_path, project_basename=None, master_description=None
):
    """Transform from cursor project files back to activation-based template format."""
    with open(src_path, "r") as f:
        content = f.read()
    frontmatter, body = extract_frontmatter(content)

    def repl(match):
        inner = match.group(1)
        inner = inner.replace("mdc:", "")
        inner = inner.replace(".cursor/rules", "rules")
        inner = inner.replace(".mdc", ".md")
        if project_basename:
            inner = re.sub(rf"^{re.escape(project_basename)}/", "", inner)
        return f"({inner})"

    body = re.sub(r"\(mdc:[^)]*(rules/|memory-bank/)", r"(\1", body)
    body = body.replace(".mdc)", ".md)")
    body = re.sub(r"\((mdc:)?\.cursor/rules/[^)]+\.mdc\)", repl, body)

    if not body:
        from ..common import console

        console.print(f"[red]Warning: {src_path} is empty")
        return

    # Prepare frontmatter for template format
    description = frontmatter.get("description", "")
    if (not description) and master_description:
        description = master_description

    # Convert cursor frontmatter to activation-based format
    globs = frontmatter.get("globs", "")
    always_apply = frontmatter.get("alwaysApply")

    # Determine activation based on Cursor rule type patterns
    if always_apply is True:
        activation = "always"
    elif globs and globs.strip() and globs not in ["null"]:
        activation = "glob"
    elif always_apply is False and (
        not globs or not globs.strip() or globs in ["null"]
    ):
        activation = "manual"
    else:
        activation = "agent-requested"

    # Build new frontmatter
    new_frontmatter = {"description": description, "activation": activation}

    if activation == "glob":
        new_frontmatter["globs"] = globs

    with open(dst_path, "w") as f:
        f.write(dump_frontmatter(new_frontmatter, body))


def dump_frontmatter(frontmatter, body):
    """Dump frontmatter in new activation-based template format."""
    if not frontmatter:
        return body

    lines = ["---"]

    # Description (always include)
    desc = frontmatter.get("description", "")
    if desc:
        # Always use unquoted single-line format
        lines.append(f"description: {desc}")
    else:
        lines.append("description: ")

    # Activation (always include)
    activation = frontmatter.get("activation", "manual")
    lines.append(f"activation: {activation}")

    # Globs (only for glob activation)
    if activation == "glob":
        globs_value = frontmatter.get("globs", "")
        if globs_value:
            lines.append(f'globs: "{globs_value}"')
        else:
            lines.append("globs: ")

    lines.append("---")

    return "\n".join(lines) + "\n" + body
