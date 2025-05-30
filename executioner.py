#!/usr/bin/env python3
"""
executioner.py

Searches the entire repo for Python files ending in `_tool.py` and makes them executable.
Only works on Unix-like systems (Linux, macOS, WSL).

Usage:
    python executioner.py
"""

import os
import stat
from pathlib import Path

def chmod_executable(path: Path) -> None:
    current = path.stat().st_mode
    path.chmod(current | stat.S_IEXEC)
    print(f"✅ Made executable: {path.relative_to(Path.cwd())}")

def main():
    root = Path.cwd()
    count = 0
    for py_file in root.rglob("*_tool.py"):
        try:
            chmod_executable(py_file)
            count += 1
        except Exception as e:
            print(f"❌ Failed on {py_file.name}: {e}")
    print(f"\n🔧 Done. {count} tool(s) made executable.")

if __name__ == "__main__":
    main()
