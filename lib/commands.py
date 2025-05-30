"""Generic command implementations that work with both editors."""

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from rich.console import Console
from rich.prompt import Prompt

from .common import extract_frontmatter, filecmp, run_compare

console = Console()


def rules_to_project_impl(project_folder, force, compare, editor_module, editor_name):
    """Implementation of rules-to-project command."""
    template_folder = Path(__file__).parent.parent
    rules_dir = template_folder / "rules"
    rules_files = list(rules_dir.glob("**/*.md"))

    if editor_name == "cursor":
        target_dir = Path(project_folder) / ".cursor" / "rules"
    elif editor_name == "windsurf":
        target_dir = Path(project_folder) / ".windsurf" / "rules"
    else:
        raise ValueError(f"Unsupported editor: {editor_name}")

    target_dir.mkdir(parents=True, exist_ok=True)

    for src in rules_files:
        if src.name == "README.md":
            continue
        rel = Path(src).relative_to(rules_dir)
        dst = target_dir / rel
        if editor_name == "cursor" and rel.suffix == ".md":
            dst = dst.with_suffix(".mdc")
        dst.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile("w+", delete=False) as tf:
            editor_module.transform_to_project(src, tf.name)
            tf.flush()
            if dst.exists():
                if filecmp(tf.name, dst):
                    console.print(f"[green]Identical, skipping {dst}")
                elif force:
                    shutil.copy(tf.name, dst)
                    console.print(f"[yellow]Overwriting {dst}")
                elif compare:
                    console.print(f"[red]Diff for {dst}")
                    run_compare(tf.name, dst)
                else:
                    console.print(f"[cyan]Skipping {dst} (use --force or --compare)")
            else:
                shutil.copy(tf.name, dst)
        os.unlink(tf.name)

    # README files
    for src in rules_files:
        if src.name != "README.md":
            continue
        rel = Path(src).relative_to(rules_dir)
        dst = target_dir / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        if not dst.exists() or force:
            shutil.copy(src, dst)

    # memory-bank
    mb_src = template_folder / "memory-bank"
    mb_dst = Path(project_folder) / "memory-bank"
    if mb_src.exists():
        if not mb_dst.exists():
            shutil.copytree(mb_src, mb_dst)
            console.print(f"[green]Copied memory-bank to {mb_dst}")
        else:
            for src_dir, _, files in os.walk(mb_src):
                rel_dir = Path(src_dir).relative_to(mb_src)
                dst_dir = mb_dst / rel_dir
                dst_dir.mkdir(parents=True, exist_ok=True)
                for file in files:
                    src_file = Path(src_dir) / file
                    dst_file = dst_dir / file
                    if not dst_file.exists():
                        resp = Prompt.ask(
                            f"[yellow]Copy missing file {dst_file}? (y/n)",
                            choices=["y", "n"],
                            default="n",
                        )
                        if resp == "y":
                            shutil.copy(src_file, dst_file)
                            console.print(f"[green]Copied {src_file} to {dst_file}")

    src = template_folder / "LLM-README.md"
    dst = Path(project_folder) / "LLM-README.md"
    if filecmp(src, dst):
        console.print(f"[green]Identical, skipping {dst}")
    elif force:
        shutil.copy(src, dst)
        console.print(f"[yellow]Overwriting {dst}")
    elif compare:
        console.print(f"[red]Diff for {dst}")
        run_compare(src, dst)
    else:
        console.print(f"[cyan]Skipping {dst} (use --force or --compare)")


def project_to_rules_impl(project_folder, force, compare, editor_module, editor_name):
    """Implementation of project-to-rules command."""
    template_folder = Path(__file__).parent.parent

    # Check if git repo is clean
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=template_folder,
            capture_output=True,
            text=True,
            check=True,
        )
        if result.stdout.strip():
            console.print(
                "[red]Git repository is not clean. Please commit or stash changes before proceeding."
            )
            sys.exit(1)
    except subprocess.CalledProcessError:
        console.print("[yellow]Warning: Not in a git repository or git command failed.")
    except FileNotFoundError:
        console.print("[yellow]Warning: git command not found.")

    rules_dir = template_folder / "rules"
    if editor_name == "cursor":
        editor_dir = Path(project_folder) / ".cursor"
        file_extension = ".mdc"
    elif editor_name == "windsurf":
        editor_dir = Path(project_folder) / ".windsurf"
        file_extension = ".md"
    else:
        raise ValueError(f"Unsupported editor: {editor_name}")

    project_basename = Path(project_folder).name
    rules_files = list(rules_dir.glob("**/*.md"))

    # 1) Gather all files to process as source: dest dict
    files_to_process = {}
    for src in rules_files:
        if src.name == "README.md":
            continue
        rel = Path(src).relative_to(rules_dir)
        if editor_name == "cursor":
            source_file = editor_dir / ("rules" / rel).with_suffix(rel.suffix + "c")
        else:  # windsurf
            source_file = editor_dir / ("rules" / rel)

        if source_file.exists():
            files_to_process[source_file] = src
        else:
            console.print(f"[red]Missing {source_file}")

    # 2) Loop through and process using the separate functions
    for source_file, dest_file in files_to_process.items():
        # Load master description
        with open(dest_file, "r") as f:
            master_content = f.read()
        master_frontmatter, _ = extract_frontmatter(master_content)
        master_description = master_frontmatter.get("description")

        with tempfile.NamedTemporaryFile("w+", delete=False) as tf:
            editor_module.transform_from_project(
                source_file,
                tf.name,
                project_basename=project_basename,
                master_description=master_description,
            )
            tf.flush()
            if filecmp(tf.name, dest_file):
                console.print(f"[green]Identical, skipping {dest_file}")
            elif force:
                shutil.copy(tf.name, dest_file)
                console.print(f"[yellow]Updated {dest_file}")
            elif compare:
                console.print(f"[red]Diff for {dest_file}")
                run_compare(tf.name, dest_file)
            else:
                console.print(f"[cyan]Skipping {dest_file} (use --force or --compare)")
        os.unlink(tf.name)

    # Then check for new files in editor_dir
    if editor_name == "cursor":
        editor_files = [
            f
            for f in list(editor_dir.glob("rules/**/*.mdc"))
            if str(f).find("/project/") == -1
        ]
    else:  # windsurf
        editor_files = [
            f
            for f in list(editor_dir.glob("rules/**/*.md"))
            if str(f).find("/project/") == -1
        ]

    for editor_file in editor_files:
        if editor_file.name == "README.md":
            continue
        rel = Path(editor_file).relative_to(editor_dir / "rules")
        if editor_name == "cursor":
            target_md = rules_dir / rel.with_suffix(".md")
        else:  # windsurf
            target_md = rules_dir / rel

        if not target_md.exists():
            console.print(f"[yellow]Found new file: {editor_file}")
            if force:
                with tempfile.NamedTemporaryFile("w+", delete=False) as tf:
                    editor_module.transform_from_project(
                        editor_file,
                        tf.name,
                        project_basename=project_basename,
                    )
                    target_md.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy(tf.name, target_md)
                    console.print(f"[green]Copied new file to {target_md}")
                os.unlink(tf.name)
            else:
                console.print(
                    f"[cyan]Skipping new file {target_md} (use --force to create)"
                )

    # Handle LLM-README.md
    src = template_folder / "LLM-README.md"
    dst = editor_dir / "LLM-README.md"
    if dst.exists():
        if filecmp(src, dst):
            console.print(f"[green]Identical, skipping {src}")
        elif force:
            shutil.copy(dst, src)
            console.print(f"[yellow]Updated {src}")
        elif compare:
            console.print(f"[red]Diff for {src}")
            run_compare(dst, src)
        else:
            console.print(f"[cyan]Skipping {src} (use --force or --compare)")

    console.print(f"[bold green]Done.")
