"""Common utilities used by both cursor and windsurf modules."""

import re
import shutil
import subprocess

from rich.console import Console

console = Console()


def run_compare(file1, file2):
    """Run file comparison tool."""
    if shutil.which("bcompare"):
        subprocess.run(["bcompare", file1, file2])
    else:
        subprocess.run(["diff", file1, file2])
        # TODO: after showing diff, then what?


def extract_frontmatter(content):
    """Extract frontmatter from markdown content as a dictionary."""
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)", content, re.DOTALL)
    if match:
        frontmatter_text = match.group(1)
        body = match.group(2)

        # Parse frontmatter manually
        frontmatter = {}
        lines = frontmatter_text.split("\n")
        i = 0

        while i < len(lines):
            line = lines[i].strip()

            if ":" in line and not line.startswith("#"):
                key, value = line.split(":", 1)
                key = key.strip()
                value = value.strip()

                # Handle multi-line values (if line ends with incomplete value)
                if value and not value.endswith(",") and not value.endswith("|"):
                    # Single line value
                    if value.lower() == "true":
                        frontmatter[key] = True
                    elif value.lower() == "false":
                        frontmatter[key] = False
                    elif value.lower() == "null" or value == "":
                        frontmatter[key] = (
                            "null" if value.lower() == "null" else ""
                        )  # Preserve null as string, empty as empty
                    elif value.startswith('"') and value.endswith('"'):
                        frontmatter[key] = value[1:-1]  # Remove quotes
                    else:
                        frontmatter[key] = value
                elif value == "|":
                    # Multi-line literal block
                    multiline_value = []
                    i += 1
                    while i < len(lines) and (
                        lines[i].startswith("  ") or lines[i].strip() == ""
                    ):
                        if lines[i].strip():
                            multiline_value.append(
                                lines[i][2:]
                            )  # Remove 2-space indent
                        else:
                            multiline_value.append("")
                        i += 1
                    frontmatter[key] = "\n".join(multiline_value)
                    i -= 1  # Adjust for the outer loop increment
                else:
                    # Handle incomplete/continuing values or empty values
                    if value == "" or value.lower() == "null":
                        frontmatter[key] = "null" if value.lower() == "null" else ""
                    else:
                        # Handle incomplete/continuing values (like description ending with comma)
                        full_value = value
                        i += 1
                        # Look ahead for continuation lines (non-key lines)
                        while i < len(lines):
                            next_line = lines[i].strip()
                            if ":" in next_line and not next_line.startswith(" "):
                                # This is a new key, stop collecting
                                i -= 1
                                break
                            if next_line:
                                full_value += " " + next_line
                            i += 1

                        # Clean up the full value
                        full_value = full_value.strip().rstrip(",")
                        frontmatter[key] = full_value if full_value else None

            i += 1

        return frontmatter, body
    return {}, content


def derive_editor_fields(activation, globs=None, description=""):
    """Convert simple activation to editor-specific fields with validation."""

    if activation == "always":
        return {"alwaysApply": True, "globs": "", "trigger": "always"}

    elif activation == "glob":
        if not globs or not globs.strip():
            raise ValueError("activation: glob requires non-empty globs: field")
        return {
            "alwaysApply": False,  # Will be omitted in Cursor output
            "globs": globs.strip(),
            "trigger": "glob",
        }

    elif activation == "agent-requested":
        return {"alwaysApply": False, "globs": "", "trigger": "model"}

    elif activation == "manual":
        return {"alwaysApply": False, "globs": "", "trigger": "manual"}

    else:
        raise ValueError(
            f"Invalid activation type: {activation}. Must be one of: always, glob, agent-requested, manual"
        )


def validate_frontmatter(frontmatter_dict):
    """Validate frontmatter for the new activation-based system."""
    activation = frontmatter_dict.get("activation")

    if not activation:
        raise ValueError(
            "Missing required 'activation' field. Must be one of: always, glob, agent-requested, manual"
        )

    globs = frontmatter_dict.get("globs", "")

    # Validate activation/globs combinations
    if activation == "glob" and (not globs or not globs.strip()):
        raise ValueError("activation: glob requires non-empty globs: field")

    if (
        activation in ["always", "agent-requested", "manual"]
        and globs
        and globs.strip()
    ):
        raise ValueError(f"activation: {activation} should not have globs field")

    return True


def create_cursor_frontmatter(frontmatter_dict):
    """Create Cursor-style frontmatter from activation-based dictionary."""
    validate_frontmatter(frontmatter_dict)

    activation = frontmatter_dict["activation"]
    globs = frontmatter_dict.get("globs", "")
    description = frontmatter_dict.get("description", "")

    lines = ["---"]

    # Description (always include)
    if description.strip():
        # Always use unquoted single-line format
        lines.append(f"description: {description}")
    else:
        lines.append("description: ")

    # Handle each activation type
    if activation == "always":
        lines.append("globs: ")
        lines.append("alwaysApply: true")

    elif activation == "glob":
        lines.append(f"globs: {globs}")
        # Omit alwaysApply for Auto-Attached behavior

    elif activation in ["agent-requested", "manual"]:
        lines.append("globs: ")
        lines.append("alwaysApply: false")

    lines.append("---")
    lines.append("")  # First blank line after frontmatter
    lines.append("")  # Second blank line for Cursor
    return "\n".join(lines)


def create_windsurf_frontmatter(frontmatter_dict):
    """Create Windsurf-style frontmatter from activation-based dictionary."""
    validate_frontmatter(frontmatter_dict)

    activation = frontmatter_dict["activation"]
    globs = frontmatter_dict.get("globs", "")
    description = frontmatter_dict.get("description", "")

    editor_fields = derive_editor_fields(activation, globs, description)

    lines = ["---"]
    lines.append(f"trigger: {editor_fields['trigger']}")

    # Description
    if description.strip():
        # Always use unquoted single-line format
        lines.append(f"description: {description}")
    else:
        lines.append("description: ")

    # Globs
    if editor_fields["globs"]:
        lines.append(f"globs: {editor_fields['globs']}")
    else:
        lines.append("globs: ")

    lines.append("---")
    return "\n".join(lines)


def filecmp(f1, f2):
    """Compare two files for equality."""
    try:
        with open(f1, "rb") as a, open(f2, "rb") as b:
            return a.read() == b.read()
    except FileNotFoundError:
        # If either file doesn't exist, they're not equal
        return False
