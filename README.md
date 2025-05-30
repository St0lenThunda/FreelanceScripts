# 🚀 Python “Starter Pack” Tools

A collection of small, battle-tested Python scripts to kickstart your freelancing journey. Each tool is:

- **Standalone** – drop it into any project folder  
- **Interactive** – no arguments? You’ll get prompted  
- **CLI-friendly** – use short, memorable flags  
- **Well-documented** – logging, help text, and examples  

### 📦 Tools Included

1. **CSV ⇄ JSON Converter** (`csv_json_tool.py`)  
2. **Simple Web Scraper** (`simple_scraper_tool.py`)

<!-- TOOL_TABLE_START -->
| Tool | Description | Link |
|------|-------------|------|
| 🧮 CSV ⇄ JSON Tool | A two-way data converter built in Python. Use it to transform: | [csv_json_converter/README.md](csv_json_converter/README.md) |
| README Updater | This script, `generate_tool_table.py`, automates the process of documenting tools in the main project README. It scans subdirectories for tool-specific `README.md` files, extracts their titles and descriptions, and generates a Markdown table to include in the main README. | [readme_updater/README.md](readme_updater/README.md) |
| 🌐 Simple Web Scraper | Fetch all titles from [Hacker News](https://news.ycombinator.com ). Fetches inner text and links of  `<a>` elements inside `<span class="titleline">`. | [scraper/README.md](scraper/README.md) |
| 🪛 Scraper Debug Demo Tool | This tool demonstrates a real-world debugging and refactoring process taken from the `scraper/simple_scraper_tool.py`. It includes both a **broken** and a **fixed** version of the scraper to illustrate how problems were identified and solved in a freelance-style workflow. | [debug_demo/README.md](debug_demo/README.md) |
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
* [ ] Finish Day 3 tool: bug fixer demo
* [ ] Optional: Create a CLI launcher script for unified access

---

## 📜 License

MIT © \StolenThunda
Use, modify, and share freely. No attribution required, but always appreciated!