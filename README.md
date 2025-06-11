
### [:boom: Live Site 💥](https://st0lenthunda.github.io/FreelanceScripts/)
###  *StolenThunda Presents*: 
---
# Freelance Scripts - 🐍 Python “Starter Pack” Tool
*A Python Starter Toolkit for Freelancers, Debuggers, and Builders*

![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)
![OS](https://img.shields.io/badge/OS-Mac%20%7C%20Linux%20%7C%20WSL-brightgreen)
![Last Commit](https://img.shields.io/github/last-commit/St0lenThunda/FreelanceScripts)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![GitHub Repo stars](https://img.shields.io/github/stars/St0lenThunda/FreelanceScripts?style=social)

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
<!-- /vscode-markdown-toc -->

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
<b>Api integration</b>
<ul>
<li>Fetches data from external platforms like GitHub, Behance, and Dribbble.</li>
</ul>
<b>Argument parsing</b>
<ul>
<li>Handles command-line arguments and interactive prompts for flexible usage.</li>
<li>Uses `argparse` for flexible CLI usage.</li>
</ul>
<b>Cli design</b>
<ul>
<li>Provides flexible command-line arguments for customization.</li>
</ul>
<b>Command-line</b>
<ul>
<li>Parameters: Handles CLI arguments for flexible script behavior.</li>
</ul>
<b>Csv and json handling</b>
<ul>
<li>Uses Python's built-in `csv` and `json` modules for data conversion.</li>
</ul>
<b>Data storage</b>
<ul>
<li>Saves structured data to JSON files for easy reuse.</li>
</ul>
<b>Data transformation</b>
<ul>
<li>Converts raw API responses into structured JSON or markdown.</li>
</ul>
<b>Docstring extraction and markdown conversion</b>
<ul>
<li>Extracts ython docstrings, preserves formatting, and safely converts HTML ags for markdown.</li>
</ul>
<b>Dynamic documentation</b>
<ul>
<li>Automates the generation of a combined README by reading and summarizing other README files.</li>
<li>Automates updates to README files ased on project state.</li>
</ul>
<b>Dynamic tool discovery</b>
<ul>
<li>Lists tools dynamically based on the project structure.</li>
</ul>
<b>Error handling</b>
<ul>
<li>Checks for file existence and handles missing/invalid files gracefully.</li>
<li>Gracefully handles API errors, invalid inputs, and network issues.</li>
<li>Gracefully handles failed requests and invalid selectors.</li>
<li>Gracefully handles invalid inputs and tool execution errors.</li>
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
<b>Extensibility</b>
<ul>
<li>Designed to easily add new tools and features.</li>
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
<li>Reads and updates Markdown files rogrammatically.</li>
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
<li>Provides clear, educational comments for ach step.</li>
<li>Provides clear, educational comments for each step.</li>
</ul>
<b>Interactive cli</b>
<ul>
<li>Prompts users for missing arguments and provides helpful feedback.</li>
</ul>
<b>Line ending normalization</b>
<ul>
<li>Converts Windows/CRLF line endings to Unix/LF for cross-platform compatibility.</li>
</ul>
<b>Logging</b>
<ul>
<li>Logs activity to both terminal and file for auditing.</li>
</ul>
<b>Menu-based</b>
<ul>
<li>CLI: Provides an interactive menu for tool selection and execution.</li>
</ul>
<b>Modular task system</b>
<ul>
<li>Uses classes and inheritance to nable extensible task management.</li>
</ul>
<b>Modularity</b>
<ul>
<li>Organizes code into functions and classes for clarity.</li>
</ul>
<b>Multi-step</b>
<ul>
<li>Automation: Supports running multiple update teps in sequence with a single command (e.g., --task=sync_and_table`).</li>
</ul>
<b>Output inference</b>
<ul>
<li>Infers output file names from input file paths.</li>
</ul>
<b>Path handling</b>
<ul>
<li>Leverages `pathlib` for robust file and irectory operations.</li>
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
<li>Employs regular expressions for flexible text eplacement and extraction.</li>
</ul>
<b>Robustness</b>
<ul>
<li>Uses checks for file existence and safe file removal.</li>
</ul>
<b>Subprocess automation</b>
<ul>
<li>Runs other scripts automatically in response to file events.</li>
</ul>
<b>Symlinking</b>
<ul>
<li>Demonstrates creating symbolic links with `Path.symlink_to` for easy command-line access.</li>
</ul>
<b>User interactivity</b>
<ul>
<li>Prompts users for input and provides file selection menus.</li>
</ul>
<b>Web scraping</b>
<ul>
<li>Uses libraries like `requests` and `BeautifulSoup` to fetch and parse HTML content.</li>
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
| Tool | Description | Use Cases |
|------|-------------|-----------|
| [🧙‍♂️ CSV ⇄ JSON Converter Tool]([csv_json_converter/README.md](csv_json_converter/README.md)) | A two-way data converter for CSV and JSON files. It contains functions to convert CSV files to JS... | <ol><li>Convert legacy data formats for client uploads</li><li>Clean and structure input/output data</li><li>Offer format conversion as a paid service</li></ol> |
| [📰 README Updater]([readme_updater/README.md](readme_updater/README.md)) | This script provides a modular framework for dynamically updating the main project README and too... | <ol><li>Keep documentation in sync</li><li>Automate release note generation</li><li>Maintain a professional project appearance</li></ol> |
| [🛠️ Tool Runner]([toolkit_runner/README.md](toolkit_runner/README.md)) | A unifying script to run all tools in the FreelanceScripts project. This script provides a menu-b... | <ol><li>Quickly access and run any tool in the project.</li><li>Provide a unified interface for managing tools.</li><li>Simplify tool usage for non-technical users.</li><li>Demonstrate menu-based CLI design.</li></ol> |
| [🌐 Simple Web Scraper]([scraper/README.md](scraper/README.md)) | A modular web scraper that fetches titles and links from one or more URLs (default: Hacker News). | <ol><li>Pull titles for blog digests.</li><li>Extract data from forums or news sites.</li><li>Automate content summaries for newsletters.</li><li>Learn web scraping techniques for personal projects.</li></ol> |
| [🗂️ Portfolio Generator Tool]([portfolio_generator/README.md](portfolio_generator/README.md)) | A CLI tool to generate a personal project portfolio page or JSON data by scraping GitHub, Behance... | <ol><li>Build a markdown or JSON résumé.</li><li>Provide GitHub summaries for clients.</li><li>Automate portfolio creation for freelancers.</li><li>Offer portfolio setup as a freelance service.</li></ol> |
| [👀 Watch Automation Tool]([watch_automation/README.md](watch_automation/README.md)) | A utility that automatically updates your main project README tool table whenever any tool's READ... | <ol><li>Auto-run tasks on file changes</li><li>Reduce human error in packaging</li><li>Speed up development & deployment cycles</li></ol> |
| [🪓 Executioner Tool]([executioner/README.md](executioner/README.md)) | This script automates making Python scripts executable and symlinking them into a `bin/` director... | <ol><li>Prep scripts for client use</li><li>Automate script permissions in CI</li><li>Save manual chmod effort across large toolkits</li></ol> |
| [🧰 Package Toolkit]([package_toolkit/README.md](package_toolkit/README.md)) | This script packages all tools in the FreelanceScripts project into a single zip archive, while r... | <ol><li>Generate deliverables for clients or marketplaces</li><li>Create backups or releases</li><li>Bundle scripts for tutorials or training</li></ol> |
<!-- TOOL_TABLE_END -->



##  3. <a name='Installation'></a>⚙️ Installation

```bash
git clone https://github.com/St0lenThunda/FreelanceScripts
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
│   └── README.md
├── scraper/
│   └── simple_scraper_tool.py
│   └── README.md
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
[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/A0A81FVBKZ)
---

##  5. <a name='License'></a>📜 License

MIT © \StolenThunda
Use, modify, and share freely. No attribution required, but always appreciated!
