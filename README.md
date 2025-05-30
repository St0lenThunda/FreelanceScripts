# 🚀 Python “Starter Pack” Tools

A collection of small, battle-tested Python scripts to kickstart your freelancing journey. Each tool is:

- **Standalone** – drop it into any project folder  
- **Interactive** – no arguments? You’ll get prompted  
- **CLI-friendly** – use short, memorable flags  
- **Well-documented** – logging, help text, and examples  

### 📦 Tools Included

1. **CSV ⇄ JSON Converter** (`csv_json_tool.py`)  
2. **Simple Web Scraper** (`simple_scraper_tool.py`)

---

## ⚙️ Installation

```bash
git clone https://github.com/St0lenThunda/reelanceScripts
cd FreelanceScripts
python3 -m venv .venv             # optional but recommended
source .venv/bin/activate         # or `.venv\Scripts\activate` on Windows
pip install -r requirements.txt   # only needed if additional dependencies are added
````

---

## 🧰 Making All Tools Executable

To run any tool directly like `./csv_json_tool.py`, make it executable:

`python executioner.py`

This script will search the project for any file ending in `_tool.py` and `chmod +x` it automatically.

⚠️ **Note**: This applies only to Linux/macOS/WSL systems.
 On Windows, simply run:
 ```bash
 python path/to/tool_name_tool.py
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