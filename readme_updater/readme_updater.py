#!/usr/bin/env python3
"""
generate_tool_table.py

Auto-generates a Markdown table of all tools from their individual READMEs
and updates the root README.md.
"""

import os
from pathlib import Path

# Define the root directory of the project (parent of the current script's directory)
ROOT = Path(__file__).parent.parent

# Define the path to the main README file in the root directory
README = ROOT / "README.md"

# List to store rows of the Markdown table for tools
TOOL_ROWS = []

# List of directories to exclude from processing
EXCLUDED_DIRS = {"debug_demo"}

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


# Function to find all tool README files in subdirectories
# - Each tool's README is expected to be named "README.md"
# - Extracts the title and description for each tool and adds it to the table rows
def find_tool_readmes():
    """Find tool README.md files in subdirectories."""
    for sub in ROOT.iterdir():
        if sub.is_dir() and sub.name not in EXCLUDED_DIRS:  # Skip excluded directories
            tool_readme = sub / "README.md"
            if tool_readme.exists():
                title, desc = extract_summary(tool_readme)
                link = f"[{sub.name}/README.md]({sub.name}/README.md)"  # Relative link to the README
                TOOL_ROWS.append(f"| {title} | {desc} | {link} |")


# Function to update the main README file with the generated tool table
# - The table is inserted between markers <!-- TOOL_TABLE_START --> and <!-- TOOL_TABLE_END -->
# - If markers are not found, the table is appended to the end of the README
def update_root_readme():
    """Inject the generated table into the README.md between markers."""
    if not README.exists():
        print("❌ No root README.md found.")
        return

    marker_start = "<!-- TOOL_TABLE_START -->"
    marker_end = "<!-- TOOL_TABLE_END -->"

    # Define the table structure
    table_header = "| Tool | Description | Link |\n|------|-------------|------|"
    table_body = "\n".join(TOOL_ROWS)
    full_table = f"{marker_start}\n{table_header}\n{table_body}\n{marker_end}"

    with README.open("r", encoding="utf-8") as f:
        content = f.read()

    if marker_start in content and marker_end in content:
        # Replace the old table between the markers
        pre = content.split(marker_start)[0].rstrip()
        post = content.split(marker_end)[-1].lstrip()
        new_content = f"{pre}\n\n{full_table}\n\n{post}"
    else:
        # Append the table to the end if markers are not found
        new_content = f"{content.strip()}\n\n{full_table}"

    with README.open("w", encoding="utf-8") as f:
        f.write(new_content)

    print("✅ README.md updated with tool table.")


# Define a base class for README tasks
class ReadmeTask:
    def execute(self):
        raise NotImplementedError("Subclasses must implement the execute method.")

# Task to generate a tool table and inject it into the README
class ToolTableTask(ReadmeTask):
    def execute(self):
        TOOL_ROWS.clear()  # Clear any existing rows
        find_tool_readmes()
        update_root_readme()

# Function to dynamically execute tasks for updating the README
def execute_readme_tasks(tasks: list[ReadmeTask]):
    for task in tasks:
        task.execute()

# Main script execution
# - Finds all tool READMEs and generates a Markdown table
# - Updates the main README with the generated table
if __name__ == "__main__":
    # Define the tasks to execute
    tasks = [
        ToolTableTask(),
        # Additional tasks can be added here
    ]

    # Execute all tasks
    execute_readme_tasks(tasks)
    print(f"🔧 Completed {len(tasks)} task(s) for README update.")