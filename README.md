# 🚀 Python “Starter Pack” Tools

> ## Purpose
> A collection of small, battle-tested Python scripts to kickstart your freelancing journey. The scripts provide are to be extended or the concepts in them could be used to create new tools. Each tool is:

- **Standalone** – drop it into any project folder  
- **Interactive** – no arguments? You’ll get prompted  
- **CLI-friendly** – use short, memorable flags  
- **Well-documented** – logging, help text, and examples  

### 📦 Tools Included

<!-- TOOL_TABLE_START -->
| Tool | Description | Link |
|------|-------------|------|
| 🧙‍♂️ CSV ⇄ JSON Converter Tool | A two-way data converter for CSV and JSON files. | [csv_json_converter/README.md](csv_json_converter/README.md) |
| 📰 README Updater | This script, `readme_updater.py`, provides a modular framework for dynamically updating the main... | [readme_updater/README.md](readme_updater/README.md) |
| 🌐 Simple Web Scraper | A modular, educational web scraper for extracting titles and links from any website. - Supports s... | [scraper/README.md](scraper/README.md) |
| 👀 Watch Automation Tool | A utility that automatically updates your main project README tool table whenever any tool's `REA... | [watch_automation/README.md](watch_automation/README.md) |
| 🪓 Executioner Tool | The `executioner_tool` automates the process of making Python scripts executable and symlinking t... | [executioner/README.md](executioner/README.md) |
| 🧰 Package Toolkit | The Package Toolkit is a utility script designed to create a zip archive of your freelance tools,... | [package_toolkit/README.md](package_toolkit/README.md) |
<!-- TOOL_TABLE_END -->

## ⚙️ Installation

```bash
git clone https://github.com/St0lenThunda/reelanceScripts
cd FreelanceScripts
python3 -m venv .venv             # optional but recommended
source .venv/bin/activate         # or `.venv\Scripts\activate` on Windows
pip install -r requirements.txt   # only needed if additional dependencies are added
```

---

## 🧰 Making All Tools Executable & Adding to PATH

To run any tool directly (e.g., `csv_json_tool`), use the included script:

```bash
python executioner.py
```

This will:
- Search the project for any file ending in `_tool.py`
- Convert line endings to Unix (LF)
- Make each tool executable
- Symlink each tool (without the `.py` extension) into a `bin/` directory

You can then run tools from the `bin/` directory using just their short names (e.g., `csv_json_tool`).

> ⚠️ **Note**: This applies only to Linux/macOS/WSL systems.
> On Windows, simply run:
> ```bash
> python path/to/tool_name_tool.py
> ```

### 🔗 Add Tools to Your PATH

To use these tools from anywhere, add this to your shell profile (e.g., `~/.bashrc`, `~/.zshrc`):

```bash
export PATH="$(pwd)/bin:$PATH"
```

## 📁 Project Structure (Example)
```
FreelanceScripts/
├── csv_converter/
│   └── csv_json_tool.py
├── scraper/
│   └── simple_scraper_tool.py
├── executioner.py
└── README.md
```
---

## ✅ Next Steps

* [ ] Add a `requirements.txt` if needed
* [ ] Optional: Create a CLI launcher script for unified access

---

## 📜 License

MIT © \StolenThunda
Use, modify, and share freely. No attribution required, but always appreciated!

### Excluding Tools

To exclude a tool from the toolkit or README generation, add a `.excluded` marker file to the tool's directory. For example:

```bash
touch debug_demo/.excluded
```

This will ensure the `debug_demo` tool is skipped during packaging and documentation updates.

### Adding a New Tool to the Toolbox

To add a new tool to the toolbox, follow these steps:

1. **Create the Tool**:
   - Place your tool in a dedicated directory under the project root (e.g., `my_new_tool/`).
   - Name the main script file with the `_tool.py` suffix (e.g., `my_new_tool_tool.py`). This ensures compatibility with the Executioner tool for activation.

2. **Document the Tool**:
   - Add a `README.md` file to the tool's directory.
   - Include a brief description of the tool, its purpose, and usage instructions.

3. **Exclude from Packaging (Optional)**:
   - If you want to exclude the tool from packaging or README generation, add a `.excluded` marker file to the tool's directory:
     ```bash
     touch my_new_tool/.excluded
     ```
   - This will ensure the tool is skipped during packaging and documentation updates.

4. **Activate the Tool**:
   - Run the Executioner tool to make the new tool executable and symlink it into the `bin/` directory:
     ```bash
     python executioner/executioner.py
     ```
   - The tool will now be accessible from the `bin/` directory using its short name (e.g., `my_new_tool_tool`).

5. **Update the Combined README**:
   - Ensure the `package_toolkit.py` script is run to regenerate the combined README and package the project:
     ```bash
     python package_toolkit/package_toolkit.py
     ```

### Syntax for Tool Summaries

When documenting a tool in its `README.md`, follow this syntax to ensure consistency across the project:

1. **Title**:
   - Use a clear and concise title for the tool.
     ```markdown
     # My New Tool
     ```

2. **Description**:
   - Provide a brief overview of the tool's purpose and functionality.
     ```markdown
     My New Tool is designed to simplify data processing by automating repetitive tasks.
     ```

3. **Usage Instructions**:
   - Include step-by-step instructions on how to use the tool.
     ```markdown
     ## Usage
     `python my_new_tool_tool.py --input data.csv --output result.json`
      ```

4. **Examples**:
   - Add examples to demonstrate the tool in action.
     ```markdown
     ## Examples
     `python my_new_tool_tool.py --help`
     ```

5. **Compatibility**:
   - Mention any system or Python version requirements.
     ```markdown
     ## Compatibility
     Requires Python 3.8 or higher.
     ```

6. **Exclusion Marker**:
   - If the tool should be excluded from packaging, mention the `.excluded` marker file.
   - Example:
     ```markdown
     ## Exclusion
     Add a `.excluded` file to the tool's directory to exclude it from packaging.
     ```