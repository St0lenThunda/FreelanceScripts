# 🧰 Package Toolkit

> ## Purpose 
> The Package Toolkit is a utility script designed to create a zip archive of your freelance tools, excluding unnecessary files. It also generates a combined README summarizing the tools in the project.

## Features

- Dynamically generates a combined README summarizing tool READMEs.
- Excludes directories and files marked with `.excluded` or matching predefined patterns.
- Creates a zip archive of the project for easy distribution.

## Usage

1. Run the script to generate the combined README and package the project:

   ```bash
   python3 package_toolkit.py
   ```

2. The output zip file will be created in the project root as `freelance_toolkit.zip`.

## Exclusion Rules

- Files and directories matching the following patterns are excluded:
  - `.git`, `__pycache__`, `.venv`, `venv`, `env`, `.DS_Store`, `.pytest_cache`, `.idea`, `.mypy_cache`, `output`, `freelance_toolkit.zip`, `bin`, `package_toolkit.py`, `.gitignore`
- Directories containing a `.excluded` marker file are also excluded.

## Combined README

The script generates a `COMBINED_README.md` file in the project root, summarizing the README files of all tools in the project. Excluded tools are listed in a separate section.

## Notes

- Ensure Python 3 is installed on your system.
- The script must be run from the `package_toolkit` directory.
