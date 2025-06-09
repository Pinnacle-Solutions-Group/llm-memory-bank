import re
import subprocess
from pathlib import Path

import click
from rich.console import Console

from lib import cursor, windsurf
from lib.commands import project_to_rules_impl, rules_to_project_impl
from lib.single_file import transform_to_project_single_file

console = Console()


@click.group()
def cli():
    pass


@cli.command()
@click.argument("project_folder", type=click.Path(exists=True, file_okay=False))
@click.option("--force", is_flag=True, help="Overwrite existing files")
@click.option("--compare", is_flag=True, help="Compare files before overwriting")
@click.option(
    "--editor",
    required=True,
    type=click.Choice(["cursor", "windsurf", "claude-code", "aider-chat"]),
    help="Specify the editor to use",
)
def rules_to_project(project_folder, force, compare, editor):
    """Copy rules to project/.cursor/rules with path/content transform."""
    if editor == "claude-code" or editor == "aider-chat":
        if editor == "claude-code":
            dst_file = "CLAUDE.md"
        elif editor == "aider-chat":
            dst_file = "CONVENTIONS.md"
        transform_to_project_single_file(project_folder, dst_file)
        return
    elif editor == "cursor":
        editor_module = cursor
    elif editor == "windsurf":
        editor_module = windsurf
    else:
        raise ValueError(f"Unsupported editor: {editor}")

    rules_to_project_impl(project_folder, force, compare, editor_module, editor)


@cli.command()
@click.argument("project_folder", type=click.Path(exists=True, file_okay=False))
@click.option("--force", is_flag=True, help="Overwrite existing files")
@click.option("--compare", is_flag=True, help="Compare files before overwriting")
@click.option(
    "--editor",
    required=True,
    type=click.Choice(["cursor", "windsurf"]),
    help="Specify the editor to use",
)
def project_to_rules(project_folder, force, compare, editor):
    """Compare .cursor/rules/*.mdc to rules/*.md after reverse transform."""
    if editor == "cursor":
        editor_module = cursor
    elif editor == "windsurf":
        editor_module = windsurf
    else:
        raise ValueError(f"Unsupported editor: {editor}")

    project_to_rules_impl(project_folder, force, compare, editor_module, editor)

    # Run markdownlint after successful completion
    console.print("[blue]Running markdownlint...")
    try:
        result = subprocess.run(
            [
                "npx",
                "markdownlint",
                "**/*.md",
                "--fix",
                "--ignore",
                "node_modules/",
                "--config",
                ".markdownlint.json",
            ],
            cwd=Path(__file__).parent,
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode == 0:
            console.print("[green]Markdownlint completed successfully.")
        else:
            console.print(f"[yellow]Markdownlint finished with warnings:")
            if result.stdout:
                console.print(result.stdout)
            if result.stderr:
                console.print(result.stderr)
    except FileNotFoundError:
        console.print(
            "[red]Error: npx command not found. Please install Node.js and npm."
        )
    except Exception as e:
        console.print(f"[red]Error running markdownlint: {e}")


@cli.command()
def lint():
    """Lint all markdown links in the project and warn if any are broken."""
    project_root = Path(__file__).parent.resolve()
    md_files = list(project_root.glob("rules/**/*.md")) + list(
        project_root.glob("memory-bank/**/*.md")
    )
    broken = 0
    for md_file in md_files:
        with open(md_file, "r") as f:
            content = f.read()
        for match in re.finditer(r"(?<!\!)\[[^\]]+\]\(([^)\s]+)\)", content):
            link = match.group(1)
            target = (project_root / link).resolve()
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
