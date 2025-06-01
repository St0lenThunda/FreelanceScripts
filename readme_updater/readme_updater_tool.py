#!/usr/bin/env python3
"""
readme_updater_tool.py

This script provides a modular framework for dynamically updating the main project README. It allows for the addition of multiple tasks, such as generating a tool table, and makes the process extensible for future enhancements.

Key Features:
- Modular task system using a ReadmeTask base class.
- Excludes directories with `.excluded` marker files.
- Can be extended with new tasks for README management.

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

# --- Modular Task System ---
class Task:
    def run(self, args):
        raise NotImplementedError

class ToolTableTask(Task):
    def run(self, args):
        tool_table = generate_tool_table()
        update_readme_with_table(args.readme, tool_table)

TASKS = {
    "tool_table": ToolTableTask(),
    # Future tasks can be added here
}

def parse_args():
    parser = argparse.ArgumentParser(description="Update README with tool info.")
    parser.add_argument('--task', default="tool_table", choices=TASKS.keys(), help="Task to run (default: tool_table)")
    parser.add_argument('--readme', type=str, default=str(ROOT / "README.md"), help="Path to README to update (default: root README.md)")
    return parser.parse_args()

def main():
    args = parse_args()
    TASKS[args.task].run(args)

if __name__ == "__main__":
    main()
