"""
watch_automation_tool.py

A utility that automatically updates your main project README tool table whenever any tool's README.md is changed.

Key Features:
- Monitors all tool directories for changes to their README.md files (excluding .excluded and system folders).
- Automatically runs the readme_updater_tool.py to keep the main tool table in sync.
- Logs all activity to both the terminal and a log file for easy auditing.
- Designed for extensibility and easy integration into your workflow.

Usage:
    python watch_automation_tool.py

Leave this running in a terminal while you work on your tools and documentation. Any update to a tool's README.md will trigger an automatic update to the main tool table.
"""

import time
import logging
from pathlib import Path
import subprocess

# --- Configuration ---
# Get the root directory of the project
ROOT = Path(__file__).resolve().parent.parent
# List all tool directories, excluding hidden/system and .excluded
TOOL_DIRS = [
    d for d in ROOT.iterdir()
    if d.is_dir()
    and not d.name.startswith('.')
    and d.name not in {"bin", "output", "__pycache__", "watch_automation"}
    and not (d / ".excluded").exists()
]
# Log file for watcher events
LOG_FILE = ROOT / "watch_automation" / "watch_automation.log"
# Path to the README updater tool
README_UPDATER = ROOT / "readme_updater" / "readme_updater_tool.py"

# --- Logging Setup ---
# Configure logging to file and terminal
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s %(message)s',
    force=True  # Overwrite any previous logging config
)
# Add a stream handler to also log to the terminal
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)


def get_readme_mtimes():
    """
    Scan all tool directories and return a dict mapping README.md paths to their last modified times.
    Only includes README.md files that exist in tool directories.
    """
    mtimes = {}
    for tool_dir in TOOL_DIRS:
        readme = tool_dir / "README.md"
        if readme.exists():
            mtimes[str(readme)] = readme.stat().st_mtime
    return mtimes


def run_readme_updater():
    """
    Run the readme_updater_tool.py script to update the main README tool table.
    Logs the result, stdout, and stderr to both the log file and the terminal.
    """
    try:
        result = subprocess.run([
            "python3", str(README_UPDATER)
        ], capture_output=True, text=True)
        logging.info("Ran readme_updater_tool.py. Return code: %s", result.returncode)
        if result.stdout:
            logging.info("STDOUT:\n%s", result.stdout)
        if result.stderr:
            logging.warning("STDERR:\n%s", result.stderr)
    except Exception as e:
        logging.error("Error running readme_updater_tool.py: %s", e)


def main():
    """
    Main loop: watches all tool README.md files for changes and runs the updater if any change is detected.
    Logs all events to both the log file and the terminal.
    """
    logging.info("Starting README watcher...")
    last_mtimes = get_readme_mtimes()
    while True:
        time.sleep(2)  # Poll every 2 seconds
        current_mtimes = get_readme_mtimes()
        updated = False
        for path, mtime in current_mtimes.items():
            # If a README.md is new or has changed, trigger the updater
            if path not in last_mtimes or mtime != last_mtimes[path]:
                logging.info(f"Detected change in {path}. Running updater.")
                run_readme_updater()
                updated = True
                break  # Only run once per cycle to avoid duplicate updates
        last_mtimes = current_mtimes


if __name__ == "__main__":
    main()
