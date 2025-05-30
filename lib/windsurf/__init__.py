"""Windsurf editor specific transformations."""

import re

from ..common import create_windsurf_frontmatter, extract_frontmatter


def transform_to_project(src_path, dst_path):
    """Transform from template format to windsurf project files (.windsurf/rules/)."""
    with open(src_path, "r") as f:
        content = f.read()

    frontmatter, body = extract_frontmatter(content)

    # Convert old-style frontmatter to new activation-based format if needed
    if frontmatter and "activation" not in frontmatter:
        frontmatter = convert_legacy_to_activation(frontmatter)

    # Transform links in body
    body = re.sub(r"\(rules/([^)]+)\.md\)", r"(.windsurf/rules/\1.md)", body)
    body = re.sub(r"\(memory-bank/", r"(.windsurf/memory-bank/", body)

    # Replace placeholders with final paths
    body = body.replace("WINDSURF_RULE_PLACEHOLDER_", ".windsurf/rules/")

    # Apply Windsurf-specific frontmatter formatting
    windsurf_frontmatter = create_windsurf_frontmatter(frontmatter)

    with open(dst_path, "w") as f:
        f.write(windsurf_frontmatter + "\n" + body)


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
    """Transform (.windsurf/rules/...) to activation-based template format."""
    with open(src_path, "r") as f:
        content = f.read()

    frontmatter, body = extract_frontmatter(content)

    # Transform links in body
    def repl(match):
        inner = match.group(1)
        inner = inner.replace(".windsurf/rules/", "rules/")
        return f"({inner})"

    body = re.sub(r"\((.windsurf/rules/[^)]+)\)", repl, body)

    # Transform memory-bank links back to template format
    body = re.sub(r"\(\.windsurf/memory-bank/", r"(memory-bank/", body)

    # Prepare frontmatter for template format
    description = frontmatter.get("description", "")
    if (not description) and master_description:
        description = master_description

    # Convert windsurf frontmatter to activation-based format
    trigger = frontmatter.get("trigger", "model")
    globs = frontmatter.get("globs", "")

    # Map windsurf trigger to activation
    if trigger == "always":
        activation = "always"
    elif trigger == "glob":
        activation = "glob"
    elif trigger == "model":
        activation = "agent-requested"
    elif trigger == "manual":
        activation = "manual"
    else:
        activation = "manual"  # Default fallback

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
