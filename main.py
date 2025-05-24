import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import click
import yaml
from rich.console import Console
from rich.prompt import Prompt

console = Console()


def find_files(pattern, root, exclude=None):
    """Find files matching pattern under root, optionally excluding some."""
    try:
        # Try fd-find
        result = subprocess.run(
            ["fd", pattern, str(root)], capture_output=True, text=True, check=True
        )
        files = result.stdout.strip().split("\n")
        if exclude:
            files = [f for f in files if exclude not in f]
        return files
    except Exception:
        # Fallback to os.walk
        matches = []
        for dirpath, _, filenames in os.walk(root):
            for filename in filenames:
                if Path(filename).match(pattern):
                    full = str(Path(dirpath) / filename)
                    if not exclude or exclude not in full:
                        matches.append(full)
        return matches


def run_compare(file1, file2):
    if shutil.which("bcompare"):
        subprocess.run(["bcompare", file1, file2])
    else:
        subprocess.run(["diff", file1, file2])


def transform_to_project(src_path, dst_path):
    """Transform (rules/...) to (mdc:.cursor/rules/...) and .md to .mdc in links."""
    with open(src_path, "r") as f:
        content = f.read()

    # Only replace inside markdown links
    def repl(match):
        inner = match.group(1)
        inner = inner.replace("rules/", "mdc:.cursor/rules/")
        inner = inner.replace(".md", ".mdc")
        return f"({inner})"

    content = re.sub(r"\((rules/[^)]+\.md)\)", repl, content)
    with open(dst_path, "w") as f:
        f.write(content)


def extract_frontmatter(content):
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)", content, re.DOTALL)
    if match:
        frontmatter = yaml.safe_load(match.group(1))
        body = match.group(2)
        return frontmatter, body
    return {"description": None}, content


def dump_frontmatter(frontmatter, body):
    return f"---\n{yaml.safe_dump(frontmatter, sort_keys=False)}---\n{body}"


approved_links = set()


def transform_to_rules(
    src_path, dst_path, final_dest, project_basename=None, master_description=None
):
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
    # No more interactive link validation or stub creation
    if not body:
        console.print(f"[red]Warning: {src_path} is empty")
        return
    if (not frontmatter.get("description")) and master_description:
        frontmatter["description"] = master_description
    with open(dst_path, "w") as f:
        f.write(dump_frontmatter(frontmatter, body))


@click.group()
def cli():
    pass


@cli.command()
@click.argument("project_folder", type=click.Path(exists=True, file_okay=False))
@click.option("--force", is_flag=True, help="Overwrite existing files")
@click.option("--compare", is_flag=True, help="Compare files before overwriting")
def rules_to_project(project_folder, force, compare):
    """Copy rules to project/.cursor/rules with path/content transform."""
    template_folder = Path(__file__).parent
    rules_dir = template_folder / "rules"
    target_dir = Path(project_folder) / ".cursor" / "rules"
    target_dir.mkdir(parents=True, exist_ok=True)
    console.print(f"[bold green]Copying rules from {rules_dir} to {target_dir}")
    for src in find_files("*.md", rules_dir, exclude="README"):
        rel = Path(src).relative_to(rules_dir)
        dst = target_dir / (rel.name + "c")
        with tempfile.NamedTemporaryFile("w+", delete=False) as tf:
            transform_to_project(src, tf.name)
            tf.flush()
            if dst.exists():
                if force:
                    shutil.copy(tf.name, dst)
                    console.print(f"[yellow]Overwriting {dst}")
                elif compare:
                    if filecmp(tf.name, dst):
                        console.print(f"[green]Identical, skipping {dst}")
                    else:
                        console.print(f"[red]Diff for {dst}")
                        run_compare(tf.name, dst)
                else:
                    console.print(f"[cyan]Skipping {dst} (use --force or --compare)")
            else:
                shutil.copy(tf.name, dst)
        os.unlink(tf.name)
    # README files
    for src in find_files("README.md", rules_dir):
        rel = Path(src).relative_to(rules_dir)
        dst = target_dir / rel.name
        if not dst.exists() or force:
            shutil.copy(src, dst)
    # memory-bank
    mb_src = template_folder / "memory-bank"
    mb_dst = Path(project_folder) / "memory-bank"
    if mb_src.exists() and not mb_dst.exists():
        shutil.copytree(mb_src, mb_dst)
        console.print(f"[green]Copied memory-bank to {mb_dst}")
    console.print(f"[bold green]Done.")


@cli.command()
@click.argument("project_folder", type=click.Path(exists=True, file_okay=False))
def project_to_rules(project_folder):
    """Compare .cursor/rules/*.mdc to rules/*.md after reverse transform."""
    template_folder = Path(__file__).parent
    rules_dir = template_folder / "rules"
    mdc_dir = Path(project_folder) / ".cursor"
    project_basename = Path(project_folder).name
    for src in find_files("*.md", rules_dir, exclude="README"):
        rel = Path(src).relative_to(rules_dir)
        mdc_file = mdc_dir / ("rules" / rel).with_suffix(rel.suffix + "c")
        if not mdc_file.exists():
            console.print(f"[red]Missing {mdc_file}")
            continue
        # Load master description
        with open(src, "r") as f:
            master_content = f.read()
        master_frontmatter, _ = extract_frontmatter(master_content)
        master_description = master_frontmatter.get("description")
        with tempfile.NamedTemporaryFile("w+", delete=False) as tf:
            transform_to_rules(
                mdc_file,
                tf.name,
                project_basename=project_basename,
                master_description=master_description,
                final_dest=Path(__file__).parent,
            )
            tf.flush()
            if filecmp(tf.name, src):
                console.print(f"[green]Identical, skipping {src}")
            else:
                console.print(f"[red]Diff for {src}")
                run_compare(tf.name, src)
        os.unlink(tf.name)
    console.print(f"[bold green]Done.")


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


def filecmp(f1, f2):
    with open(f1, "rb") as a, open(f2, "rb") as b:
        return a.read() == b.read()


if __name__ == "__main__":
    cli()
    cli()
