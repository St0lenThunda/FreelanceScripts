#!/usr/bin/env python3
"""
readme_updater.py

This script provides a modular framework for dynamically updating the main project README. It allows for the addition of multiple tasks, such as generating a tool table, and makes the process extensible for future enhancements.

Key Features:
- Modular task system using a ReadmeTask base class.
- Excludes directories with `.excluded` marker files.
- Can be extended with new tasks for README management.

Intended as a learning resource: code is heavily commented to explain each step and concept.
"""

from pathlib import Path
from typing import List

# Get the root directory of the project (parent of this script's directory)
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Base class for tasks that update the README
class ReadmeTask:
    """
    Base class for a README update task.
    Subclasses should implement the run() method.
    """
    def run(self, readme_path: Path):
        raise NotImplementedError

# Function to extract the title and description from a tool's README file
# - The title is the first-level header (e.g., "# Tool Name")
# - The description is the content under the "Purpose" section
#   (lines following "> ## Purpose" until the first empty line)
def extract_summary(readme_path: Path) -> tuple[str, str]:
    """Extracts the first-level header and the 'Purpose' section as summary."""
    title = "(No Title)"  # Default title if none is found
    desc = ""  # Default description if none is found
    with readme_path.open("r", encoding="utf-8") as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            if line.strip().startswith("# "):
                # Extract the title from the first-level header
                title = line.strip().replace("#", "").strip()
            elif line.strip().lower().startswith("> ## purpose"):
                # Collect all lines under the "Purpose" section
                desc_lines = []
                for desc_line in lines[i + 1:]:
                    if not desc_line.strip():
                        break  # Stop at the first empty line
                    desc_lines.append(desc_line.strip().lstrip("> "))
                desc = " ".join(desc_lines)  # Combine lines into a single string
                break
    return title, desc

# Example task: Generate a table of tools in the README
def find_tool_readmes():
    """
    Finds all tool README.md files in the project, skipping excluded directories.
    Returns a list of Path objects.
    """
    tool_readmes = []
    for path in PROJECT_ROOT.iterdir():
        # Skip if not a directory or if excluded
        if not path.is_dir() or (path / ".excluded").exists():
            continue
        readme = path / "README.md"
        if readme.exists():
            tool_readmes.append(readme)
    return tool_readmes

class ToolTableTask(ReadmeTask):
    """
    Task to generate a markdown table of tools for the main README.
    """
    def run(self, readme_path: Path):
        tool_readmes = find_tool_readmes()
        # List to store rows of the Markdown table for tools
        tool_rows = []
        for tool_readme in tool_readmes:
            title, desc = extract_summary(tool_readme)
            link = f"[{tool_readme.parent.name}/README.md]({tool_readme.parent.name}/README.md)"  # Relative link to the README
            tool_rows.append(f"| {title} | {desc} | {link} |")

        # Define the table structure
        marker_start = "<!-- TOOL_TABLE_START -->"
        marker_end = "<!-- TOOL_TABLE_END -->"
        table_header = "| Tool | Description | Link |\n|------|-------------|------|"
        table_body = "\n".join(tool_rows)
        full_table = f"{marker_start}\n{table_header}\n{table_body}\n{marker_end}"

        if not readme_path.exists():
            print("❌ No root README.md found.")
            return

        with readme_path.open("r", encoding="utf-8") as f:
            content = f.read()

        if marker_start in content and marker_end in content:
            # Replace the old table between the markers
            pre = content.split(marker_start)[0].rstrip()
            post = content.split(marker_end)[-1].lstrip()
            new_content = f"{pre}\n\n{full_table}\n\n{post}"
        else:
            # Append the table to the end if markers are not found
            new_content = f"{content.strip()}\n\n{full_table}"

        with readme_path.open("w", encoding="utf-8") as f:
            f.write(new_content)

        print("✅ README.md updated with tool table.")

# Main function to run all tasks
def main():
    """
    Main function to run all README update tasks.
    """
    readme_path = PROJECT_ROOT / "README.md"
    tasks: List[ReadmeTask] = [ToolTableTask()]
    for task in tasks:
        task.run(readme_path)
    print("✅ README update tasks complete.")

if __name__ == "__main__":
    main()