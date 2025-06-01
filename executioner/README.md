# 🪓 Executioner Tool

> ## Purpose
> The `executioner_tool` automates the process of making Python scripts executable and symlinking them into a `bin/` directory for easy access via the system PATH.

## Features

- **Executable Conversion**: Automatically applies executable permissions to Python scripts.
- **Symlink Creation**: Creates symlinks in a `bin/` directory for easy command-line usage.
- **Unix Line Endings**: Ensures all scripts use Unix-style line endings (LF).

## Usage

1. Place the script in the `executioner_tool` directory.
2. Run the script:

   ```bash
   python executioner.py
   ```

3. Add the `bin/` directory to your PATH:

   ```bash
   export PATH="$(pwd)/bin:$PATH"
   ```

## Notes

- This tool is designed for Unix-like systems (Linux, macOS, WSL).
- On Windows, you can still run the scripts directly using `python`.

## License

MIT License. Use freely and modify as needed.
