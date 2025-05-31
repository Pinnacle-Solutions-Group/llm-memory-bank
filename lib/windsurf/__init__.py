"""Windsurf editor specific transformations."""

import re

from ..common import create_windsurf_frontmatter, extract_frontmatter


def transform_to_project(src_path, dst_path):
    """Transform from template format to windsurf project files (.windsurf/rules/)."""
    with open(src_path, "r") as f:
        content = f.read()

    frontmatter, body = extract_frontmatter(content)

    # Transform links in body
    body = re.sub(r"\(rules/([^)]+)\.md\)", r"(.windsurf/rules/\1.md)", body)
    body = re.sub(r"\(memory-bank/", r"(.windsurf/memory-bank/", body)

    # Replace placeholders with final paths
    body = body.replace("WINDSURF_RULE_PLACEHOLDER_", ".windsurf/rules/")

    # Apply Windsurf-specific frontmatter formatting (customized below)
    windsurf_frontmatter = create_windsurf_frontmatter(frontmatter)

    with open(dst_path, "w") as f:
        f.write(windsurf_frontmatter + "\n" + body)


def transform_from_project(
    src_path, dst_path, project_basename=None, master_description=None
):
    """Transform (.windsurf/rules/...) to activation-based template format."""
    with open(src_path, "r") as f:
        content = f.read()

    frontmatter, body = extract_frontmatter(content)

    # Transform links in body
    body = re.sub(
        r"\(.windsurf/rules/([^)]+)\.md\)", lambda m: f"(rules/{m.group(1)}.md)", body
    )

    # Transform memory-bank links back to template format
    body = re.sub(r"\(\.windsurf/memory-bank/", r"(memory-bank/", body)

    # Prepare frontmatter for template format
    description = frontmatter.get("description", "")
    # Also rewrite .windsurf/rules/... links in the description
    if ".windsurf/rules/" in description:
        description = description.replace(".windsurf/rules/", "rules/")
    if (not description) and master_description:
        description = master_description

    # Convert windsurf frontmatter to activation-based format
    trigger = frontmatter.get("trigger", "model")
    globs = frontmatter.get("globs", None)

    # Map windsurf trigger to activation
    if trigger == "always_on":
        activation = "always"
    elif trigger == "glob":
        activation = "glob"
    elif trigger == "model_decision":
        activation = "agent-requested"
    elif trigger == "manual":
        activation = "manual"
    else:
        activation = "manual"  # Default fallback

    # Build new frontmatter
    new_frontmatter = {"description": description, "activation": activation}

    if activation == "glob" and globs:
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


def create_windsurf_frontmatter(frontmatter_dict):
    """Create Windsurf-style frontmatter with new trigger values and globs omission."""
    activation = frontmatter_dict.get("activation", "manual")
    globs = frontmatter_dict.get("globs", None)
    description = frontmatter_dict.get("description", "")

    # Map activation to trigger
    if activation == "always":
        trigger = "always_on"
    elif activation == "glob":
        trigger = "glob"
    elif activation == "agent-requested":
        trigger = "model_decision"
    elif activation == "manual":
        trigger = "manual"
    else:
        trigger = activation  # fallback

    lines = ["---"]
    lines.append(f"trigger: {trigger}")

    # Description
    if description.strip():
        lines.append(f"description: {description}")
    else:
        lines.append("description: ")

    # Globs (only if present and non-empty, and only for glob activation)
    if activation == "glob" and globs:
        lines.append(f"globs: {globs}")

    lines.append("---")
    return "\n".join(lines)
