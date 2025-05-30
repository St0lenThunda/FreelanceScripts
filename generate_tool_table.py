#!/usr/bin/env python3
"""
generate_tool_table.py

Auto-generates a Markdown table of all tools from their individual READMEs
and updates the root README.md.
"""

import os
from pathlib import Path

ROOT = Path(__file__).parent
README = ROOT / "README.md"
TOOL_ROWS = []

def extract_summary(readme_path: Path) -> tuple[str, str]:
    """Extracts the first-level header and first paragraph as summary."""
    title = "(No Title)"
    desc = ""
    with readme_path.open("r", encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines:
            if line.strip().startswith("# "):
                title = line.strip().replace("#", "").strip()
            elif line.strip() and not line.strip().startswith("#"):
                desc = line.strip()
                break
    return title, desc


def find_tool_readmes():
    """Find tool README.md files in subdirectories."""
    for sub in ROOT.iterdir():
        if sub.is_dir():
            tool_readme = sub / "README.md"
            if tool_readme.exists():
                title, desc = extract_summary(tool_readme)
                link = f"[{sub.name}/README.md]({sub.name}/README.md)"
                TOOL_ROWS.append(f"| {title} | {desc} | {link} |")


def update_root_readme():
    """Inject the generated table into the README.md between markers."""
    if not README.exists():
        print("❌ No root README.md found.")
        return

    header = "# 🚀 Python “Starter Pack” Tools"
    marker_start = "<!-- TOOL_TABLE_START -->"
    marker_end = "<!-- TOOL_TABLE_END -->"

    table_header = "| Tool | Description | Link |\n|------|-------------|------|"
    table_body = "\n".join(TOOL_ROWS)
    full_table = f"{marker_start}\n{table_header}\n{table_body}\n{marker_end}"

    with README.open("r", encoding="utf-8") as f:
        content = f.read()

    if marker_start in content and marker_end in content:
        # Replace old table
        pre = content.split(marker_start)[0].rstrip()
        post = content.split(marker_end)[-1].lstrip()
        new_content = f"{pre}\n\n{full_table}\n\n{post}"
    else:
        # Append at the bottom if no markers
        new_content = f"{content.strip()}\n\n{full_table}"

    with README.open("w", encoding="utf-8") as f:
        f.write(new_content)

    print("✅ README.md updated with tool table.")


if __name__ == "__main__":
    find_tool_readmes()
    update_root_readme()
    print(f"🔧 Found {len(TOOL_ROWS)} tool(s) to document.")