# 🧰 Package Toolkit

> ## Purpose
> package_toolkit.py
>
> This script packages all tools in the FreelanceScripts project into a single zip archive, while respecting exclusion rules and generating a combined README.
>
> Key Features:
> - Recursively scans the project for tool directories and files.
> - Excludes files/folders based on patterns and `.excluded` marker files.
> - Dynamically generates a combined README summarizing all included tools.
> - Packages everything into an `output/freelance_toolkit.zip` archive.
>
> Intended as a learning resource: code is heavily commented to explain each step and concept.

## Exclusion Rules

- Files and directories matching the following patterns are excluded:
  - `.git`, `__pycache__`, `.venv`, `venv`, `env`, `.DS_Store`, `.pytest_cache`, `.idea`, `.mypy_cache`, `output`, `freelance_toolkit.zip`, `bin`, `package_toolkit.py`, `.gitignore`
- Directories containing a `.excluded` marker file are also excluded.

## Combined README

The script generates a `COMBINED_README.md` file in the project root, summarizing the README files of all tools in the project. Excluded tools are listed in a separate section.

## Concepts

This tool demonstrates several Pythonic concepts useful for beginners:

- **File and Directory Traversal:** Uses `pathlib.Path` and `rglob` to recursively walk directories and process files.
- **Exclusion Logic:** Shows how to exclude files/folders based on patterns and marker files (e.g., `.excluded`).
- **Zipfile Handling:** Demonstrates creating and writing to zip archives with Python's `zipfile` module.
- **Dynamic Documentation:** Automates the generation of a combined README by reading and summarizing other README files.
- **Command-Line Parameters:** Handles CLI arguments for flexible script behavior.
- **Robustness:** Uses checks for file existence and safe file removal.
- **Heavy Commenting:** Provides clear, educational comments for each step.

## Notes

- Ensure Python 3 is installed on your system.
- The script must be run from the `package_toolkit` directory.
