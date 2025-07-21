# 🪓 Executioner Tool

> ## Purpose
> This script automates making Python scripts executable and symlinking them into a `bin/` directory for easy PATH usage.
>
> Key Features:
> - Searches for Python scripts ending with `_tool.py`.
> - Converts line endings to Unix (LF) for compatibility.
> - Makes each tool executable (chmod +x).
> - Symlinks each tool (without the `.py` extension) into a `bin/` directory.
>
> Intended as a learning resource: code is heavily commented to explain each step and concept.

## 🚀 Usage
   ```bash
   export PATH="$(pwd)/bin:$PATH"
   ```

## Notes

- This tool is designed for Unix-like systems (Linux, macOS, WSL).
- On Windows, you can still run the scripts directly using `python`.

## Concepts

This tool demonstrates several Pythonic concepts useful for beginners:

- **Recursive File Search:** Uses `pathlib.Path.rglob` to find files matching a pattern in all subdirectories.
- **File Permissions:** Shows how to make files executable using `os.chmod` and `stat`.
- **Symlinking:** Demonstrates creating symbolic links with `Path.symlink_to` for easy command-line access.
- **Line Ending Normalization:** Converts Windows/CRLF line endings to Unix/LF for cross-platform compatibility.
- **Exclusion by Marker File:** Skips directories containing a `.excluded` file.
- **Path Manipulation:** Uses `pathlib` for robust, cross-platform path handling.
- **Heavy Commenting:** Provides clear, educational comments for each step.

## License

MIT License. Use freely and modify as needed.
