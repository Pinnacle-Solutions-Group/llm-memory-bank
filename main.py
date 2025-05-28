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


def run_compare(file1, file2):
    if shutil.which("bcompare"):
        subprocess.run(["bcompare", file1, file2])
    else:
        subprocess.run(["diff", file1, file2])
        # TODO: after showing diff, then what?


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
        try:
            # Quote glob patterns to prevent YAML parsing errors
            frontmatter_text = re.sub(r"(\*\*?/.*?\*)", r'"\1"', match.group(1))
            frontmatter = yaml.safe_load(frontmatter_text)
            body = match.group(2)
            return frontmatter, body
        except yaml.YAMLError as e:
            console.print(f"[red]Error parsing frontmatter: {e}")
            return {"description": None}, content
    return {"description": None}, content


def dump_frontmatter(frontmatter, body):
    parts = body.split("---")
    if len(parts) == 1:
        return f"---\n{yaml.safe_dump(frontmatter, sort_keys=False)}---\n{body}"
    # here we have a case where the body has a frontmatter block and shouldn't
    console.print(f"[red]Warning: {body} has a frontmatter block and shouldn't")
    console.print(
        f"[yellow]Expected frontmatter:\n{yaml.safe_dump(frontmatter, sort_keys=False)}"
    )
    return body


approved_links = set()


def transform_to_rules(
    src_path, dst_path, project_basename=None, master_description=None
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
    with open(dst_path, "w") as f:
        if (not frontmatter.get("description")) and master_description:
            frontmatter["description"] = master_description
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
    rules_files = list(rules_dir.glob("**/*.md"))
    target_dir = Path(project_folder) / ".cursor" / "rules"
    target_dir.mkdir(parents=True, exist_ok=True)
    for src in rules_files:
        if src.name == "README.md":
            continue
        rel = Path(src).relative_to(rules_dir)
        dst = target_dir / rel
        if rel.suffix == ".md":
            dst = dst.with_suffix(".mdc")
        dst.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile("w+", delete=False) as tf:
            transform_to_project(src, tf.name)
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


@cli.command()
@click.argument("project_folder", type=click.Path(exists=True, file_okay=False))
def project_to_rules(project_folder):
    """Compare .cursor/rules/*.mdc to rules/*.md after reverse transform."""
    template_folder = Path(__file__).parent

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
    mdc_dir = Path(project_folder) / ".cursor"
    project_basename = Path(project_folder).name
    rules_files = list(rules_dir.glob("**/*.md"))
    mdc_files = [
        f
        for f in list(mdc_dir.glob("rules/**/*.mdc"))
        if str(f).find("/project/") == -1
    ]

    # First check existing files
    for src in rules_files:
        if src.name == "README.md":
            continue
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
            )
            tf.flush()
            if filecmp(tf.name, src):
                console.print(f"[green]Identical, skipping {src}")
            else:
                shutil.copy(tf.name, src)
                console.print(f"[yellow]Updated {src}")
        os.unlink(tf.name)

    # Then check for new files in mdc_dir
    for mdc_file in mdc_files:
        if mdc_file.name == "README.md":
            continue
        rel = Path(mdc_file).relative_to(mdc_dir / "rules")
        target_md = rules_dir / rel.with_suffix(".md")
        if not target_md.exists():
            console.print(f"[yellow]Found new file: {mdc_file}")
            with tempfile.NamedTemporaryFile("w+", delete=False) as tf:
                transform_to_rules(
                    mdc_file,
                    tf.name,
                    project_basename=project_basename,
                )
                target_md.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy(tf.name, target_md)
                console.print(f"[green]Copied new file to {target_md}")
            os.unlink(tf.name)

    # Handle LLM-README.md
    src = template_folder / "LLM-README.md"
    dst = mdc_dir / "LLM-README.md"
    if dst.exists():
        if not filecmp(src, dst):
            shutil.copy(dst, src)
            console.print(f"[yellow]Updated {src}")
        else:
            console.print(f"[green]Identical, skipping {src}")

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
