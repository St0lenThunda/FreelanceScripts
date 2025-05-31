#!/usr/bin/env python3
"""
package_toolkit.py

This script packages all tools in the FreelanceScripts project into a single zip archive, while respecting exclusion rules and generating a combined README. 

Key Features:
- Recursively scans the project for tool directories and files.
- Excludes files/folders based on patterns and `.excluded` marker files.
- Dynamically generates a combined README summarizing all included tools.
- Packages everything into an `output/freelance_toolkit.zip` archive.

Intended as a learning resource: code is heavily commented to explain each step and concept.
"""

import os
import zipfile
from pathlib import Path

# Get the root directory of the project (parent of this script's directory)
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Ensure the output directory exists and set the output zip file path
OUTPUT_DIR = PROJECT_ROOT / "output"
OUTPUT_DIR.mkdir(exist_ok=True)  # Create the output directory if it doesn't exist
OUTPUT_ZIP = OUTPUT_DIR / "freelance_toolkit.zip"

# Set of names to exclude from packaging (folders, files, and system artifacts)
EXCLUDE_NAMES = {
    ".git", "__pycache__", ".venv", "venv", "env",
    ".DS_Store", ".pytest_cache", ".idea", ".mypy_cache",
    "output", "freelance_toolkit.zip", "bin", ".gitignore"
}

def should_exclude(path: Path) -> bool:
    """
    Determines if a file or folder should be excluded from packaging.
    - Excludes if any parent directory contains a `.excluded` marker file.
    - Excludes if any part of the path matches EXCLUDE_NAMES.
    """
    # Check for `.excluded` marker file in any parent directory
    for parent in path.parents:
        if (parent / ".excluded").exists():
            return True
    # Exclude if any part of the path matches EXCLUDE_NAMES
    return any(part in EXCLUDE_NAMES for part in path.parts) or path.name in EXCLUDE_NAMES

def add_files_to_zip(zipf: zipfile.ZipFile, current_dir: Path):
    """
    Recursively adds files to the zip archive, skipping excluded files and directories.
    - Uses rglob to walk the directory tree.
    - Skips files/folders based on should_exclude.
    - Skips COMBINED_README.md (added separately).
    """
    for item in current_dir.rglob("*"):
        # Only add files that are not excluded and not the combined README
        if item.is_file() and not should_exclude(item.relative_to(PROJECT_ROOT)) and item.name != "COMBINED_README.md":
            arcname = item.relative_to(PROJECT_ROOT)  # Store the relative path for correct zip structure
            zipf.write(item, arcname)  # Add the file to the zip archive
            print(f"✅ Added: {arcname}")  # Log the added file

def generate_combined_readme(output_path: Path):
    """
    Generates a combined README file summarizing all included tools.
    - Lists excluded tools in a dedicated section.
    - For each included tool, adds the first 10 lines of its README.md.
    - Writes the result to output_path.
    """
    combined_readme = []
    combined_readme.append("# Freelance Toolkit\n")
    combined_readme.append("A collection of Python tools for freelancers.\n\n")

    excluded_tools = []  # Track excluded tool directories

    # Scan all directories in the project root
    for tool_dir in PROJECT_ROOT.iterdir():
        # If the directory is excluded, add to the excluded_tools list
        if tool_dir.is_dir() and should_exclude(tool_dir):
            excluded_tools.append(tool_dir.name)
            print(f"😜 Excluded Directory: {tool_dir.name}")  # Log excluded tools

    # If there are excluded tools, add a section to the README
    if excluded_tools:
        combined_readme.append("# Excluded Tools\n")
        combined_readme.append("The following tools are excluded from the combined README:\n\n")
        for tool in excluded_tools:
            combined_readme.append(f"- {tool}\n")
        combined_readme.append("\n")

    # For each included tool, add a summary from its README
    for tool_dir in PROJECT_ROOT.iterdir():
        if tool_dir.is_dir() and not should_exclude(tool_dir):
            tool_readme = tool_dir / "README.md"
            if tool_readme.exists():
                combined_readme.append(f"## {tool_dir.name.capitalize()}\n")
                with tool_readme.open("r", encoding="utf-8") as f:
                    # Only include the first 10 lines for brevity
                    for i, line in enumerate(f):
                        if i >= 10:
                            combined_readme.append("...\n")
                            break
                        combined_readme.append(line)
                combined_readme.append("\n")

    # Write the combined README to the specified output path
    with output_path.open("w", encoding="utf-8") as f:
        f.writelines(combined_readme)

    # Double-check the file was created
    if not output_path.exists():
        print("❌ Failed to generate combined README.")
        return

    print(f"\n✅ Combined README generated at: {output_path}")

def main():
    """
    Main function to orchestrate packaging:
    - Deletes any existing output zip file.
    - Generates a fresh combined README.
    - Adds all valid files to the zip archive.
    - Adds the combined README to the archive.
    - Cleans up the temporary combined README.
    """
    # Remove the old zip if it exists
    if OUTPUT_ZIP.exists():
        OUTPUT_ZIP.unlink()
        print(f"Deleted old zip: {OUTPUT_ZIP.name}")

    # Path for the combined README (in the project root)
    combined_readme_path = PROJECT_ROOT / "COMBINED_README.md"

    # Remove any old combined README
    if combined_readme_path.exists():
        combined_readme_path.unlink()
        print(f"Deleted old combined README: {combined_readme_path.name}")

    # Always generate a new combined README file
    generate_combined_readme(combined_readme_path)

    # Create the zip archive
    with zipfile.ZipFile(OUTPUT_ZIP, "w", zipfile.ZIP_DEFLATED) as zipf:
        add_files_to_zip(zipf, PROJECT_ROOT)  # Add all files except the combined README
        zipf.write(combined_readme_path, "COMBINED_README.md")  # Add the combined README
        print(f"✅ Added: Combined README to zip")

    # Remove the temporary combined README file after adding it to the zip
    combined_readme_path.unlink()

    print(f"\n✅ Packaged into: {OUTPUT_ZIP}")

# Entry point of the script
if __name__ == "__main__":
    main()
