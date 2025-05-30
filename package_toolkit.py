#!/usr/bin/env python3
"""
package_toolkit.py

Creates a zip archive of your freelance tools, excluding unnecessary files.
"""

import os
import zipfile
from pathlib import Path

# Define the root directory of the project
PROJECT_ROOT = Path(__file__).resolve().parent

# Define the output zip file name and location
OUTPUT_ZIP = PROJECT_ROOT / "freelance_toolkit.zip"

# Patterns and folders to skip during packaging
# - Includes common system files, caches, virtual environments, and the output zip itself
# - Also excludes the `bin` folder, which contains symlinks or executables
EXCLUDE_NAMES = {
    ".git", "__pycache__", ".venv", "venv", "env",
    ".DS_Store", ".pytest_cache", ".idea", ".mypy_cache",
    "output", "freelance_toolkit.zip", "bin", "package_toolkit.py", ".gitignore"
}

# Function to determine if a file or folder should be excluded
# - Checks if any part of the path matches the exclusion patterns
# - Returns True if the path should be excluded, False otherwise
def should_exclude(path: Path) -> bool:
    return any(part in EXCLUDE_NAMES for part in path.parts) or path.name in EXCLUDE_NAMES

# Function to add files to the zip archive
# - Recursively scans the project directory for files
# - Skips files and folders that match the exclusion patterns
# - Adds valid files to the zip archive with their relative paths
def add_files_to_zip(zipf: zipfile.ZipFile, current_dir: Path):
    for item in current_dir.rglob("*"):
        if item.is_file() and not should_exclude(item.relative_to(PROJECT_ROOT)):
            arcname = item.relative_to(PROJECT_ROOT)  # Get the relative path for the archive
            zipf.write(item, arcname)  # Add the file to the zip archive
            print(f"Added: {arcname}")  # Log the added file

# Main function to create the zip archive
def main():
    # Check if the output zip file already exists
    if OUTPUT_ZIP.exists():
        OUTPUT_ZIP.unlink()  # Remove the existing zip file
        print(f"Deleted old zip: {OUTPUT_ZIP.name}")

    # Create a new zip archive
    with zipfile.ZipFile(OUTPUT_ZIP, "w", zipfile.ZIP_DEFLATED) as zipf:
        add_files_to_zip(zipf, PROJECT_ROOT)  # Add files to the archive

    print(f"\n✅ Packaged into: {OUTPUT_ZIP}")  # Log the completion message

# Entry point of the script
if __name__ == "__main__":
    main()
