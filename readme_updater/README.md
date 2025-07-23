# 📰 README Updater

> ## Purpose
> This script provides a modular framework for dynamically updating the main project README and tool READMEs. It allows for the addition of multiple tasks, such as generating a tool table and syncing Purpose sections from script docstrings, and makes the process extensible for future enhancements.
>
> Key Features:
> - Modular task system using a Task base class.
> - Excludes directories with `.excluded` marker files.
> - Can be extended with new tasks for README management.
> - Syncs the Purpose section of each tool README with the main docstring from its *_tool.py script, preserving formatting and safely handling HTML tags.
> - Updates the main tool table in the root README with tool names, descriptions, and links.
> - Supports a combined task (`--task=sync_and_table`) to sync all Purpose sections and immediately update the tool table in one step.
> Intended as a learning resource: code is heavily commented to explain each step and concept.>
### Use Cases
- Keep documentation in sync
- Automate release note generation
- Maintain a professional project appearance

## Expected Tool README Format

Each tool's `README.md` should include:

- A first-level header (`# Tool Name`) for the title.
- A `> ## Purpose
> This script provides a modular framework for dynamically updating the main project README and tool READMEs. It allows for the addition of multiple tasks, such as generating a tool table and syncing Purpose sections from script docstrings, and makes the process extensible for future enhancements.
>
> Key Features:
> - Modular task system using a Task base class.
> - Excludes directories with `.excluded` marker files.
> - Can be extended with new tasks for README management.
> - Syncs the Purpose section of each tool README with the main docstring from its *_tool.py script, preserving formatting and safely handling HTML tags.
> - Updates the main tool table in the root README with tool names, descriptions, and links.
> - Supports a combined task (`--task=sync_and_table`) to sync all Purpose sections and immediately update the tool table in one step.
> Intended as a learning resource: code is heavily commented to explain each step and concept. 
 MIT License. Use freely and modify as needed.
 
 ## Concepts
 
 This tool demonstrates several Pythonic concepts useful for eginners:
 
 - **Modular Task System:** Uses classes and inheritance to nable extensible task management.
 - **File Parsing:** Reads and updates Markdown files rogrammatically.
 - **Regex Usage:** Employs regular expressions for flexible text eplacement and extraction.
 - **Dynamic Documentation:** Automates updates to README files ased on project state.
 - **Docstring Extraction and Markdown Conversion:** Extracts ython docstrings, preserves formatting, and safely converts HTML ags for markdown.
 - **Multi-step Automation:** Supports running multiple update teps in sequence with a single command (e.g., --task=sync_and_table`).
 - **Argument Parsing:** Uses `argparse` for flexible CLI usage.
 - **Path Handling:** Leverages `pathlib` for robust file and irectory operations.
 - **Heavy Commenting:** Provides clear, educational comments for ach step.
 
 ## New Features
 
 - **Purpose Syncing:** The `sync_purpose` task updates the Purpose section of each tool's README with the main docstring from its *_tool.py script, preserving formatting and safely handling HTML tags.
 - **Combined Task:** Use `--task=sync_and_table` to sync all Purpose sections and immediately update the tool table in one step.
 - **Improved Modularity:** The codebase is now broken into helper functions for extraction, cleaning, formatting, and blockquoting, making it easier to extend and maintain.
 - **Tool Table Generation:** Automatically generates a Markdown table in the root README with tool names, descriptions (limited to 100 characters), and use cases formatted as an ordered list.
 - **Flexible Use Case Formatting:** Allows switching between different formats for use cases (e.g., ordered list, unordered list, newline-separated).
