#!/usr/bin/env python3
"""
executioner_tool.py

This script automates making Python scripts executable and symlinking them into a `bin/` directory for easy PATH usage.

Key Features:
- Searches for Python scripts ending with `_tool.py`.
- Converts line endings to Unix (LF) for compatibility.
- Makes each tool executable (chmod +x).
- Symlinks each tool (without the `.py` extension) into a `bin/` directory.

Intended as a learning resource: code is heavily commented to explain each step and concept.
"""

import os
import stat
from pathlib import Path
import argparse

# Get the root directory of the project (parent of this script's directory)
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Directory where symlinks to tools will be placed
BIN_DIR = PROJECT_ROOT / "bin"
BIN_DIR.mkdir(exist_ok=True)  # Create the bin directory if it doesn't exist

# Helper function to find all Python tool scripts in the project
# - Looks for files ending with '_tool.py' recursively
# - Skips files in directories containing a `.excluded` marker file
# - Returns a list of Path objects

def find_tool_scripts():
    tool_scripts = []
    for path in PROJECT_ROOT.rglob("*_tool.py"):
        # Skip if any parent directory contains a .excluded marker file
        if any((parent / ".excluded").exists() for parent in path.parents):
            continue
        tool_scripts.append(path)
    return tool_scripts

# Helper function to convert line endings to Unix (LF)
def convert_to_unix_line_endings(path: Path):
    with path.open("rb") as f:
        content = f.read()
    # Replace CRLF and CR with LF
    new_content = content.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    with path.open("wb") as f:
        f.write(new_content)

# Helper function to make a file executable (chmod +x)
def make_executable(path: Path):
    mode = path.stat().st_mode
    path.chmod(mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

# Helper function to create a symlink in the bin directory
def symlink_tool(path: Path):
    tool_name = path.stem  # Remove .py extension
    symlink_path = BIN_DIR / tool_name
    if symlink_path.exists() or symlink_path.is_symlink():
        symlink_path.unlink()  # Remove existing symlink or file
    symlink_path.symlink_to(path)
    print(f"🔗 Symlinked: {tool_name} -> {path.relative_to(PROJECT_ROOT)}")

# Main function to process all tools
def main():
    """
    Main function to:
    - Find all tool scripts.
    - Convert line endings to Unix (LF).
    - Make each tool executable.
    - Symlink each tool into the bin directory.
    """
    parser = argparse.ArgumentParser(description="Manage tool scripts in the project.")
    parser.add_argument("--install", action="store_true", help="Install the tools (default action).")
    parser.add_argument("--uninstall", action="store_true", help="Uninstall the tools.")
    args = parser.parse_args()

    if args.uninstall:
        uninstall_tools()
    else:
        install_tools()

def install_tools():
    """
    Finds, prepares, and symlinks all tool scripts.
    """
    tool_scripts = find_tool_scripts()
    if not tool_scripts:
        print("No tool scripts found.")
        return
    print("Installing tools...")
    for tool_path in tool_scripts:
        print(f"\nProcessing: {tool_path.relative_to(PROJECT_ROOT)}")
        print("  - Converting line endings to Unix (LF)...")
        convert_to_unix_line_endings(tool_path)
        print("  - Making the script executable...")
        make_executable(tool_path)
        symlink_tool(tool_path)
    print(f"\n✅ All tools installed. Symlinks are in: {BIN_DIR}")

def uninstall_tools():
    """
    Removes all tool symlinks from the bin directory.
    """
    print("Uninstalling tools...")
    for symlink_path in BIN_DIR.glob("*"):
        if symlink_path.is_symlink():
            print(f"  - Removing symlink: {symlink_path.name}")
            symlink_path.unlink()
    print("\n✅ All tools uninstalled.")

if __name__ == "__main__":
    main()
