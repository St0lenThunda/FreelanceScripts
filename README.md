# 🚀 Python “Starter Pack” Tools
<!-- vscode-markdown-toc -->
* 1. [✨✨ Useful Takeaways!!! ✨✨](#UsefulTakeaways)
* 2. [📦 Tools Included](#ToolsIncluded)
* 3. [⚙️ Installation](#Installation)
	* 3.1. [🧰 Making All Tools Executable & Adding to PATH](#MakingAllToolsExecutableAddingtoPATH)
	* 3.2. [🔗 Add Tools to Your PATH](#AddToolstoYourPATH)
	* 3.3. [📁 Project Structure (Example)](#ProjectStructureExample)
	* 3.4. [Excluding Tools](#ExcludingTools)
	* 3.5. [Adding a New Tool to the Toolbox](#AddingaNewTooltotheToolbox)
	* 3.6. [Syntax for Tool Summaries](#SyntaxforToolSummaries)
* 4. [✅ Next Steps](#NextSteps)
* 5. [📜 License](#License)

<!-- vscode-markdown-toc-config
	numbering=true
	autoSave=true
	/vscode-markdown-toc-config -->
<!-- /vscode-markdown-toc --># 🚀 Python “Starter Pack” Tools

> ## Purpose
> A collection of small, battle-tested Python scripts to kickstart your freelancing journey. The scripts provide are to be extended or the concepts in them could be used to create new tools. Each tool is:

- **Standalone** – drop it into any project folder  
- **Interactive** – no arguments? You’ll get prompted  
- **CLI-friendly** – use short, memorable flags  
- **Well-documented** – logging, help text, and examples  
---
##  1. <a name='UsefulTakeaways'></a>✨✨ Useful Takeaways!!! ✨✨
<!-- CONCEPTS_START -->
<details><summary><strong>Pythonic Concepts found in this project</strong></summary>
<p>This section lists unique Pythonic concepts demonstrated across all tools in this project.</p>
<b>--</b>
<ul>
<li>--</li>
</ul>
<b>Argument parsing</b>
<ul>
<li>Handles command-line arguments and interactive prompts for flexible usage.</li>
<li>Handles command-line arguments for flexible usage.</li>
<li>Uses `argparse` for flexible CLI usage.</li>
</ul>
<b>Command-line</b>
<ul>
<li>Parameters: Handles CLI arguments for flexible script behavior.</li>
</ul>
<b>Csv and json handling</b>
<ul>
<li>Uses Python's built-in `csv` and `json` modules for data conversion.</li>
</ul>
<b>Docstring extraction and markdown conversion</b>
<ul>
<li>Extracts Python docstrings, preserves formatting, and safely converts HTML tags for markdown.</li>
</ul>
<b>Dynamic documentation</b>
<ul>
<li>Automates the generation of a combined README by reading and summarizing other README files.</li>
<li>Automates updates to README files based on project state.</li>
</ul>
<b>Educational comments</b>
<ul>
<li>Explains each step for learning purposes.</li>
</ul>
<b>Error handling</b>
<ul>
<li>Checks for file existence and handles missing/invalid files gracefully.</li>
<li>Provides robust error messages and suggestions.</li>
</ul>
<b>Exclusion by marker file</b>
<ul>
<li>Skips directories containing a `.excluded` file.</li>
<li>Skips directories with a `.excluded` marker.</li>
</ul>
<b>Exclusion logic</b>
<ul>
<li>Shows how to exclude files/folders based on patterns and marker files (e.g., `.excluded`).</li>
</ul>
<b>File and directory traversal</b>
<ul>
<li>Uses `pathlib.Path` and `rglob` to recursively walk directories and process files.</li>
</ul>
<b>File i/o</b>
<ul>
<li>Reading and writing files using `open`, with context managers for safety.</li>
</ul>
<b>File listing</b>
<ul>
<li>Lists files by extension using `pathlib` and `glob`.</li>
</ul>
<b>File parsing</b>
<ul>
<li>Reads and updates Markdown files programmatically.</li>
</ul>
<b>File permissions</b>
<ul>
<li>Shows how to make files executable using `os.chmod` and `stat`.</li>
</ul>
<b>File watching</b>
<ul>
<li>Uses `watchdog` to monitor file changes in real time.</li>
</ul>
<b>Heavy commenting</b>
<ul>
<li>Provides clear, educational comments for each step.</li>
</ul>
<b>Line ending normalization</b>
<ul>
<li>Converts Windows/CRLF line endings to Unix/LF for cross-platform compatibility.</li>
</ul>
<b>Logging</b>
<ul>
<li>Logs activity to both terminal and file for auditing.</li>
</ul>
<b>Modular task system</b>
<ul>
<li>Uses classes and inheritance to enable extensible task management.</li>
</ul>
<b>Modularity</b>
<ul>
<li>Organizes code into functions and classes for clarity.</li>
<li>Organizes code into functions for clarity and reuse.</li>
</ul>
<b>Multi-step</b>
<ul>
<li>Automation: Supports running multiple update steps in sequence with a single command (e.g., `--task=sync_and_table`).</li>
</ul>
<b>Output inference</b>
<ul>
<li>Infers output file names from input file paths.</li>
</ul>
<b>Path handling</b>
<ul>
<li>Leverages `pathlib` for robust file and directory operations.</li>
<li>Uses `pathlib` for robust, cross-platform file operations.</li>
</ul>
<b>Path manipulation</b>
<ul>
<li>Uses `pathlib` for robust, cross-platform path handling.</li>
</ul>
<b>Recursive file search</b>
<ul>
<li>Uses `pathlib.Path.rglob` to find files matching a pattern in all subdirectories.</li>
</ul>
<b>Regex usage</b>
<ul>
<li>Employs regular expressions for flexible text replacement and extraction.</li>
</ul>
<b>Robustness</b>
<ul>
<li>Uses checks for file existence and safe file removal.</li>
</ul>
<b>Selector suggestion and ranking</b>
<ul>
<li>Analyzes HTML structure to suggest and rank CSS selectors.</li>
</ul>
<b>Subprocess automation</b>
<ul>
<li>Runs other scripts automatically in response to file events.</li>
</ul>
<b>Symlinking</b>
<ul>
<li>Demonstrates creating symbolic links with `Path.symlink_to` for easy command-line access.</li>
</ul>
<b>Table output</b>
<ul>
<li>Formats results as Markdown tables for readability.</li>
</ul>
<b>User interactivity</b>
<ul>
<li>Prompts users for input and provides file selection menus.</li>
</ul>
<b>Web scraping</b>
<ul>
<li>Uses `requests` and `BeautifulSoup` for HTTP requests and HTML parsing.</li>
</ul>
<b>Zipfile handling</b>
<ul>
<li>Demonstrates creating and writing to zip archives with Python's `zipfile` module.</li>
</ul>
</details>

<!-- CONCEPTS_END -->
---
##  2. <a name='ToolsIncluded'></a>📦 Tools Included

<!-- TOOL_TABLE_START -->
| Tool | Description | Link |
|------|-------------|------|
| 🧙‍♂️ CSV ⇄ JSON Converter Tool | A two-way data converter for CSV and JSON files. | [csv_json_converter/README.md](csv_json_converter/README.md) |
| 📰 README Updater | This script provides a modular framework for dynamically updating the main project README and too... | [readme_updater/README.md](readme_updater/README.md) |
| 🌐 Simple Web Scraper | A modular web scraper that fetches titles and links from one or more URLs (default: Hacker News). | [scraper/README.md](scraper/README.md) |
| 👀 Watch Automation Tool | A utility that automatically updates your main project README tool table whenever any tool's READ... | [watch_automation/README.md](watch_automation/README.md) |
| 🪓 Executioner Tool | This script automates making Python scripts executable and symlinking them into a `bin/` director... | [executioner/README.md](executioner/README.md) |
| 🧰 Package Toolkit | package_toolkit.py | [package_toolkit/README.md](package_toolkit/README.md) |
<!-- TOOL_TABLE_END -->

##  3. <a name='Installation'></a>⚙️ Installation

```bash
git clone https://github.com/St0lenThunda/reelanceScripts
cd FreelanceScripts
python3 -m venv .venv             # optional but recommended
source .venv/bin/activate         # or `.venv\Scripts\activate` on Windows
pip install -r requirements.txt   # only needed if additional dependencies are added
```

---

###  3.1. <a name='MakingAllToolsExecutableAddingtoPATH'></a>🧰 Making All Tools Executable & Adding to PATH

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

###  3.2. <a name='AddToolstoYourPATH'></a>🔗 Add Tools to Your PATH

To use these tools from anywhere, add this to your shell profile (e.g., `~/.bashrc`, `~/.zshrc`):

```bash
export PATH="$(pwd)/bin:$PATH"
```

###  3.3. <a name='ProjectStructureExample'></a>📁 Project Structure (Example)
```
FreelanceScripts/
├── csv_converter/
│   └── csv_json_tool.py
├── scraper/
│   └── simple_scraper_tool.py
├── executioner.py
└── README.md
```

###  3.4. <a name='ExcludingTools'></a>Excluding Tools

To exclude a tool from the toolkit or README generation, add a `.excluded` marker file to the tool's directory. For example:

```bash
touch debug_demo/.excluded
```

This will ensure the `debug_demo` tool is skipped during packaging and documentation updates.

###  3.5. <a name='AddingaNewTooltotheToolbox'></a>Adding a New Tool to the Toolbox

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

###  3.6. <a name='SyntaxforToolSummaries'></a>Syntax for Tool Summaries

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

     ---

##  4. <a name='NextSteps'></a>✅ Next Steps

* [ ] Add a `requirements.txt` if needed
* [ ] Optional: Create a CLI launcher script for unified access

---

##  5. <a name='License'></a>📜 License

MIT © \StolenThunda
Use, modify, and share freely. No attribution required, but always appreciated!
