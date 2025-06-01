# 📰 README Updater

> ## Purpose
> This script, `readme_updater.py`, provides a modular framework for dynamically updating the main project README. It allows for the addition of multiple tasks, such as generating a tool table, and makes the process extensible for future enhancements.

## Features

- **Modular Task System**: Tasks are encapsulated in classes, making it easy to add new functionality.
- **Automatic Table Generation**: Extracts tool information from their `README.md` files and generates a Markdown table.
- **Customizable Markers**: Inserts the table between `<!-- TOOL_TABLE_START -->` and `<!-- TOOL_TABLE_END -->` markers in the main README.
- **Fallback Behavior**: Appends the table to the end of the README if markers are not found.

## Usage

1. Place this script in the `readme_updater` directory.
2. Run the script:

   ```bash
   python readme_updater.py
   ```

3. The main README will be updated based on the defined tasks.

## Adding New Tasks

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
- A `> ## Purpose` section for the description. The description ends at the first empty line.

## Example Table

| Tool     | Description                          | Link                                     |
| -------- | ------------------------------------ | ---------------------------------------- |
| CSV Tool | Converts CSV files to JSON and back. | [csv_tool/README.md](csv_tool/README.md) |
| Scraper  | Scrapes headlines from websites.     | [scraper/README.md](scraper/README.md)   |

## Excluding Tools

To exclude a tool from being included in the README table or combined README file, create a `.excluded` marker file in the tool's directory. For example:

```bash
touch debug_demo/.excluded
```

This will ensure the `debug_demo` tool is skipped during processing.

## Notes

- Ensure each tool has a properly formatted `README.md`.
- The script assumes the main README is located in the root directory of the project.

## License

MIT License. Use freely and modify as needed.
