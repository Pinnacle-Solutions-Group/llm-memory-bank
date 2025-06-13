import re
import subprocess
from pathlib import Path

import click
from rich.console import Console

from lib import cursor, windsurf
from lib.commands import rules_to_project_impl
from lib.single_file import transform_to_project_single_file

console = Console()


@click.group()
def cli():
    pass


@cli.command()
@click.option(
    "--all", is_flag=True, default=True, help="Generate rules for all supported editors"
)
def generate(all):
    """Generate editor-specific rules in the output directory for all supported editors."""
    output_folder = str(Path(__file__).parent.parent)  # Root directory as str

    # Generate for single-file editors
    transform_to_project_single_file(output_folder, "CLAUDE.md")
    transform_to_project_single_file(output_folder, "CONVENTIONS.md")

    # Generate for multi-file editors
    for editor, editor_module in [
        ("cursor", cursor),
        ("windsurf", windsurf),
    ]:
        rules_to_project_impl(
            output_folder,
            force=False,
            compare=False,
            editor_module=editor_module,
            editor_name=editor,
        )


@cli.command()
def lint():
    """Lint all markdown links in the project and warn if any are broken."""
    src_root = Path(__file__).parent.resolve()
    root_dir = src_root.parent
    md_files = list(src_root.glob("rules/**/*.md")) + list(
        root_dir.glob("memory-bank/**/*.md")
    )
    broken = 0
    for md_file in md_files:
        with open(md_file, "r") as f:
            content = f.read()
        for match in re.finditer(r"(?<!\!)\[[^\]]+\]\(([^)\s]+)\)", content):
            link = match.group(1)
            # Determine the base path depending on which directory the file is in
            if "rules" in str(md_file):
                base_path = src_root
            else:
                base_path = root_dir
            target = (base_path / link).resolve()
            if not target.exists():
                # Calculate line number (1-based)
                line_number = content.count("\n", 0, match.start()) + 1
                col_number = match.start() - content.rfind("\n", 0, match.start())
                print(
                    f"{md_file}:{line_number}:{col_number}: Broken link: {link} -> {target}"
                )
                broken += 1
    if broken == 0:
        console.print("[green]All markdown links are valid!")
    else:
        console.print(f"[red]{broken} broken links found.")


if __name__ == "__main__":
    cli()
