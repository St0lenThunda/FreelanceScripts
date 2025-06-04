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
> Intended as a learning resource: code is heavily commented to explain each step and concept.
To add a new task:

1. Create a new class that inherits from `ReadmeTask`.
2. Implement the `execute` method with the desired functionality.
3. Add the new task to the `tasks` list in the `__main__` section of the script.

### Example

```python
class CustomTask(ReadmeTask):
    def execute(self):
        print("Executing custom task...")

# Add the task to the list
if __name__ == "__main__":
    tasks = [
        ToolTableTask(),
        CustomTask(),
    ]
    execute_readme_tasks(tasks)
```

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
- Ensure each tool has a properly formatted `README.md`.
- The script assumes the main README is located in the root directory of the project.

## License

MIT License. Use freely and modify as needed.

## Concepts

This tool demonstrates several Pythonic concepts useful for beginners:

- **Modular Task System:** Uses classes and inheritance to enable extensible task management.
- **File Parsing:** Reads and updates Markdown files programmatically.
- **Regex Usage:** Employs regular expressions for flexible text replacement and extraction.
- **Dynamic Documentation:** Automates updates to README files based on project state.
- **Docstring Extraction and Markdown Conversion:** Extracts Python docstrings, preserves formatting, and safely converts HTML tags for markdown.
- **Multi-step Automation:** Supports running multiple update steps in sequence with a single command (e.g., `--task=sync_and_table`).
- **Argument Parsing:** Uses `argparse` for flexible CLI usage.
- **Path Handling:** Leverages `pathlib` for robust file and directory operations.
- **Heavy Commenting:** Provides clear, educational comments for each step.

## New Features

- **Purpose Syncing:** The `sync_purpose` task updates the Purpose section of each tool's README with the main docstring from its *_tool.py script, preserving formatting and safely handling HTML tags.
- **Combined Task:** Use `--task=sync_and_table` to sync all Purpose sections and immediately update the tool table in one step.
- **Improved Modularity:** The codebase is now broken into helper functions for extraction, cleaning, formatting, and blockquoting, making it easier to extend and maintain.
