# README Updater

> ## Purpose
> This script, `generate_tool_table.py`, automates the process of documenting tools in the main project README. It scans subdirectories for tool-specific `README.md` files, extracts their titles and descriptions, and generates a Markdown table to include in the main README.

## Features

- **Automatic Table Generation**: Extracts tool information from their `README.md` files.
- **Customizable Markers**: Inserts the table between `<!-- TOOL_TABLE_START -->` and `<!-- TOOL_TABLE_END -->` markers in the main README.
- **Fallback Behavior**: Appends the table to the end of the README if markers are not found.

## Usage

1. Place this script in the `readme_updater` directory.
2. Run the script:

   ```bash
   python generate_tool_table.py
   ```

3. The main README will be updated with a table of tools.

## Expected Tool README Format

Each tool's `README.md` should include:

- A first-level header (`# Tool Name`) for the title.
- A `> ## Purpose` section for the description. The description ends at the first empty line.

## Example Table

| Tool     | Description                          | Link                                     |
| -------- | ------------------------------------ | ---------------------------------------- |
| CSV Tool | Converts CSV files to JSON and back. | [csv_tool/README.md](csv_tool/README.md) |
| Scraper  | Scrapes headlines from websites.     | [scraper/README.md](scraper/README.md)   |

## Notes

- Ensure each tool has a properly formatted `README.md`.
- The script assumes the main README is located in the root directory of the project.

## License

MIT License. Use freely and modify as needed.
