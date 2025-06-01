#!/usr/bin/env python3
"""
readme_updater_tool.py

This script provides a modular framework for dynamically updating the main project README and tool READMEs. It allows for the addition of multiple tasks, such as generating a tool table and syncing Purpose sections from script docstrings, and makes the process extensible for future enhancements.

Key Features:
- Modular task system using a Task base class.
- Excludes directories with `.excluded` marker files.
- Can be extended with new tasks for README management.
- Syncs the Purpose section of each tool README with the main docstring from its *_tool.py script, preserving formatting and safely handling HTML tags.
- Updates the main tool table in the root README with tool names, descriptions, and links.
- Supports a combined task (`--task=sync_and_table`) to sync all Purpose sections and immediately update the tool table in one step.
Intended as a learning resource: code is heavily commented to explain each step and concept.
"""
import re
from pathlib import Path
import argparse

ROOT = Path(__file__).resolve().parent.parent
TOOL_DIRS = [
    d for d in ROOT.iterdir()
    if d.is_dir()
    and not d.name.startswith('.')
    and d.name not in {"bin", "output", "__pycache__"}
    and not (d / ".excluded").exists()
]

TABLE_HEADER = "| Tool | Description | Link |\n|------|-------------|------|"

# Helper to extract title and Purpose section from a README.md
def extract_title_and_purpose(readme_path):
    title = ""
    purpose = ""
    with open(readme_path, encoding="utf-8") as f:
        lines = f.readlines()
    # Find title (first line starting with #)
    for line in lines:
        if line.strip().startswith("#"):
            title = line.strip().lstrip("# ")
            break
    # Find Purpose section
    purpose_lines = []
    in_purpose = False
    for line in lines:
        if line.strip().lower().startswith("> ## purpose"):
            in_purpose = True
            continue
        if in_purpose:
            if line.strip().startswith(">  -") or line.strip().startswith(">  -"):
                # List item, keep
                purpose_lines.append(line.strip().lstrip("> "))
            elif line.strip().startswith("> "):
                # Paragraph, keep
                purpose_lines.append(line.strip().lstrip("> "))
            elif line.strip() == "" or line.strip().startswith("> #") or line.strip().startswith("> ##"):
                # End of section
                break
            else:
                break
    purpose = " ".join(purpose_lines).strip()
    return title, purpose

def generate_tool_table():
    rows = []
    for tool_dir in TOOL_DIRS:
        readme_path = tool_dir / "README.md"
        if not readme_path.exists():
            continue
        title, purpose = extract_title_and_purpose(readme_path)
        if not title:
            title = tool_dir.name
        if not purpose:
            purpose = "No description."
        # Limit description to 100 chars
        if len(purpose) > 100:
            purpose = purpose[:97].rstrip() + "..."
        rel_link = f"[{tool_dir.name}/README.md]({tool_dir.name}/README.md)"
        rows.append(f"| {title} | {purpose} | {rel_link} |")
    table = [TABLE_HEADER] + rows
    return "\n".join(table)

def update_readme_with_table(readme_path, tool_table):
    with open(readme_path, encoding="utf-8") as f:
        content = f.read()
    start_tag = "<!-- TOOL_TABLE_START -->"
    end_tag = "<!-- TOOL_TABLE_END -->"
    if start_tag in content and end_tag in content:
        new_content = re.sub(
            f"{re.escape(start_tag)}.*?{re.escape(end_tag)}",
            f"{start_tag}\n{tool_table}\n{end_tag}",
            content,
            flags=re.DOTALL
        )
    else:
        # Append at the end
        new_content = content.rstrip() + f"\n\n{start_tag}\n{tool_table}\n{end_tag}\n"
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print(f"[INFO] Tool table updated in {readme_path}")

# --- Helper functions for SyncPurposeTask ---
def extract_main_docstring(py_script):
    """
    Extract the main (top-level) docstring from a Python script.
    Returns a list of lines (with original line breaks).
    """
    with open(py_script, encoding="utf-8") as f:
        lines = f.readlines()
    in_doc = False
    doc_lines = []
    for line in lines:
        if '"""' in line or "'''" in line:
            if not in_doc:
                in_doc = True
                # Handle single-line docstring
                if line.count('"""') == 2 or line.count("'''") == 2:
                    doc_content = line.split('"""')[1] if '"""' in line else line.split("'''")[1]
                    doc_lines.append(doc_content)
                    break
                continue
            else:
                break
        if in_doc:
            doc_lines.append(line.rstrip())
    return doc_lines

def clean_docstring_lines(doc_lines, py_script):
    """
    Remove the filename line and the following blank line from the docstring lines.
    Returns a cleaned list of lines.
    """
    tool_base = py_script.name.replace('.py', '')
    cleaned_lines = []
    skip_next_blank = False
    for l in doc_lines:
        line_stripped = l.strip()
        if line_stripped == py_script.name or line_stripped == tool_base:
            skip_next_blank = True
            continue
        if skip_next_blank:
            if not line_stripped:
                skip_next_blank = False
                continue
            skip_next_blank = False
        cleaned_lines.append(l.rstrip("\n"))
    return cleaned_lines

def format_html_tags_for_md(docstring):
    """
    Surround HTML tags (e.g., <tag>) with backticks for markdown safety.
    Returns the docstring with tags formatted.
    """
    import re as _re
    def html_tag_to_md(line):
        return _re.sub(r'(<[^>]+>)', r'`\1`', line)
    return "\n".join([html_tag_to_md(l) for l in docstring.splitlines()])

def blockquote_markdown(text):
    """
    Prepend '> ' to each line for markdown blockquote, preserving blank lines.
    """
    return '\n'.join(('> ' + l if l.strip() else '>') for l in text.splitlines())

# --- Modular Task System ---
class Task:
    def run(self, args):
        raise NotImplementedError

class ToolTableTask(Task):
    def run(self, args):
        tool_table = generate_tool_table()
        update_readme_with_table(args.readme, tool_table)

class SyncPurposeTask(Task):
    def run(self, args):
        for tool_dir in TOOL_DIRS:
            py_script = next(tool_dir.glob("*_tool.py"), None)
            readme_path = tool_dir / "README.md"
            if not py_script or not readme_path.exists():
                continue
            # --- Extract and clean docstring ---
            doc_lines = extract_main_docstring(py_script)
            cleaned_lines = clean_docstring_lines(doc_lines, py_script)
            docstring = "\n".join(cleaned_lines).strip()
            if not docstring:
                continue
            # --- Format HTML tags for markdown ---
            docstring = format_html_tags_for_md(docstring)
            # --- Blockquote for markdown ---
            docstring_md = blockquote_markdown(docstring)
            # --- Update the Purpose section in the README ---
            with open(readme_path, encoding="utf-8") as f:
                content = f.read()
            # Replace the Purpose section (markdown blockquote)
            new_content = re.sub(
                r'((>\s*## Purpose.*?)(?=>\s*##|^#|^\Z|^\s*$))',
                f"> ## Purpose\n{docstring_md}",
                content,
                flags=re.DOTALL | re.MULTILINE
            )
            # If no Purpose section, insert after first heading
            if new_content == content:
                new_content = re.sub(
                    r'(^#.*$)',
                    r"\1\n\n> ## Purpose\n" + docstring_md,
                    content,
                    flags=re.MULTILINE
                )
            with open(readme_path, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"[INFO] Synced Purpose for {tool_dir.name}")

class ConsolidateConceptsTask(Task):
    def run(self, args):
        # Collect all concept bullet points from each tool README
        concepts_by_title = {}
        for tool_dir in TOOL_DIRS:
            readme_path = tool_dir / "README.md"
            if not readme_path.exists():
                continue
            with open(readme_path, encoding="utf-8") as f:
                lines = f.readlines()
            in_concepts = False
            for line in lines:
                if line.strip().lower().startswith("## concepts"):
                    in_concepts = True
                    continue
                if in_concepts:
                    if line.strip().startswith("##") and not line.strip().lower().startswith("## concepts"):
                        break  # End of Concepts section
                    if line.strip().startswith("-") or line.strip().startswith("*"):
                        # Remove markdown bullet and any bold/italic markdown
                        concept = line.strip()[1:].strip().replace("**", "")
                        # Use the first phrase before a colon or dash as the concept title
                        import re as _re
                        match = _re.match(r'([A-Za-z0-9 /]+?)(:| -| –|—|\.|$)', concept)
                        if match:
                            title = match.group(1).strip().lower()
                        else:
                            title = concept.split()[0].lower()
                        # Normalize title for grouping (lowercase, no punctuation)
                        norm_title = _re.sub(r'[^a-z0-9 ]', '', title)
                        if norm_title not in concepts_by_title:
                            concepts_by_title[norm_title] = {"title": title, "examples": set()}
                        concepts_by_title[norm_title]["examples"].add(concept)
        # Format the consolidated concepts as HTML
        summary = "Pythonic Concepts found in this project"
        details_md = [f'<details><summary><strong>{summary}</strong></summary>\n',
                      '<p>This section lists unique Pythonic concepts demonstrated across all tools in this project.</p>\n']
        for group in sorted(concepts_by_title.values(), key=lambda g: g["title"]):
            details_md.append(f'<b>{group["title"].capitalize()}</b>\n<ul>\n')
            for example in sorted(group["examples"]):
                # Remove the title from the example if it is at the start
                ex = example[len(group["title"]):].lstrip(" :-–—.")
                details_md.append(f'<li>{ex if ex else group["title"].capitalize()}</li>\n')
            details_md.append('</ul>\n')
        details_md.append('</details>\n\n')
        # Insert between <!-- CONCEPTS_START --> and <!-- CONCEPTS_END -->
        root_readme = Path(args.readme)
        with open(root_readme, encoding="utf-8") as f:
            content = f.read()
        start_tag = "<!-- CONCEPTS_START -->"
        end_tag = "<!-- CONCEPTS_END -->"
        if start_tag in content and end_tag in content:
            new_content = re.sub(
                f"{re.escape(start_tag)}.*?{re.escape(end_tag)}",
                f"{start_tag}\n" + "".join(details_md) + f"{end_tag}",
                content,
                flags=re.DOTALL
            )
        else:
            # Fallback: append at the top
            new_content = "".join(details_md) + content
        with open(root_readme, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"[INFO] Consolidated concepts inserted into {root_readme}")

TASKS = {
    "sync_purpose": SyncPurposeTask(),
    "tool_table": ToolTableTask(),
    "consolidate_concepts": ConsolidateConceptsTask(),
    # Future tasks can be added here
}

def parse_args():
    parser = argparse.ArgumentParser(description="Update README with tool info.")
    parser.add_argument('--task', default="tool_table", choices=list(TASKS.keys()) + ["sync_and_table", "all"], help="Task to run (default: tool_table)")
    parser.add_argument('--readme', type=str, default=str(ROOT / "README.md"), help="Path to README to update (default: root README.md)")
    return parser.parse_args()

def main():
    args = parse_args()
    if args.task == "all":
        TASKS["consolidate_concepts"].run(args)
        TASKS["sync_purpose"].run(args)
        TASKS["tool_table"].run(args)
    elif args.task == "sync_and_table":
        TASKS["sync_purpose"].run(args)
        TASKS["tool_table"].run(args)
    else:
        TASKS[args.task].run(args)

if __name__ == "__main__":
    main()
