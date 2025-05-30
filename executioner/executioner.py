#!/usr/bin/env python3
"""
executioner.py

Searches the entire repo for Python files ending in `_tool.py`, makes them executable,
and symlinks them into a ./bin directory for easy PATH usage.
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

def symlink_to_bin(py_file: Path, bin_dir: Path) -> None:
    bin_dir.mkdir(exist_ok=True)
    # Use only the stem (filename without .py) for the symlink name
    link_name = bin_dir / py_file.stem
    try:
        if link_name.exists() or link_name.is_symlink():
            link_name.unlink()
        link_name.symlink_to(py_file.resolve())
        print(f"🔗 Symlinked: {link_name.name} -> {py_file.relative_to(Path.cwd())}")
    except Exception as e:
        print(f"❌ Failed to symlink {py_file.name}: {e}")

def ensure_unix_line_endings(path: Path) -> None:
    # Read file and rewrite with LF endings
    content = path.read_text(encoding='utf-8')
    new_content = content.replace('\r\n', '\n').replace('\r', '\n')
    if content != new_content:
        path.write_text(new_content, encoding='utf-8')
        print(f"📝 Converted to Unix line endings: {path.relative_to(Path.cwd())}")

def main():
    root = Path.cwd()
    bin_dir = root / "bin"
    count = 0
    for py_file in root.rglob("*_tool.py"):
        try:
            ensure_unix_line_endings(py_file)
            chmod_executable(py_file)
            symlink_to_bin(py_file, bin_dir)
            count += 1
        except Exception as e:
            print(f"❌ Failed on {py_file.name}: {e}")
    print(f"\n🔧 Done. {count} tool(s) made executable and symlinked to ./bin")
    print(f"\n👉 To use these tools from anywhere, add this to your shell profile (~/.bashrc, ~/.zshrc, etc):")
    print(f'   export PATH="{bin_dir}:$PATH"')

if __name__ == "__main__":
    main()
