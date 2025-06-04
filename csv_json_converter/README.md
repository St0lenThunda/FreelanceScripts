# 🧙‍♂️ CSV ⇄ JSON Converter Tool

> ## Purpose
> A two-way data converter for CSV and JSON files. It contains functions to convert CSV files to JSON format and vice versa. The script can be run from the command line, allowing users to specify input and output files, or it can prompt for file paths interactively if no arguments are provided.
>
> Key Features:
> - Converts CSV to JSON and JSON to CSV.
> - Interactive: prompts for input/output files if not provided as arguments.
> - Lists local .csv and .json files for easy selection in interactive mode.
> - Infers output file names from input if not provided (auto-naming).
> - CLI-friendly: supports short, memorable flags.
> - Robust error handling for missing or invalid files.
> - Local file listing: lists all .csv and .json files in the current directory for easy selection.
> - Robust error handling for missing or invalid files.
> - Educational: code is heavily commented for learning purposes.
>
> Intended as a learning resource: code is heavily commented to explain each step and concept. 


 ### Interactive Mode
If you run the script without arguments, you will be prompted to choose the conversion direction and provide file paths. The tool will list available files for you to select, and can infer output file names:

```bash
python csv_to_json_converter_tool.py
```

### Command-Line Mode
You can also specify the conversion direction and file paths directly. If you omit the output file, it will be inferred automatically:

```bash
python csv_to_json_converter_tool.py --csv-to-json input.csv [output.json]
python csv_to_json_converter_tool.py --json-to-csv input.json [output.csv]
```

## Example

Convert CSV to JSON interactively:
```bash
python csv_to_json_converter_tool.py
# Choose 1, then select or enter file paths when prompted
```

Convert JSON to CSV with arguments (output file inferred):
```bash
python csv_to_json_converter_tool.py --json-to-csv input.json
# Output will be input.csv
```

## Excluding from Packaging
To exclude this tool from packaging or documentation, add a `.excluded` file to this directory:
```bash
touch .excluded
```

## Educational Notes
- The script is designed as a learning resource, with docstrings and comments explaining each step and concept.
- See the source code for detailed explanations of the logic and Python features used.

## Concepts

This tool demonstrates several Pythonic concepts useful for beginners:

- **File I/O:** Reading and writing files using `open`, with context managers for safety.
- **CSV and JSON Handling:** Uses Python's built-in `csv` and `json` modules for data conversion.
- **Argument Parsing:** Handles command-line arguments and interactive prompts for flexible usage.
- **File Listing:** Lists files by extension using `pathlib` and `glob`.
- **Output Inference:** Infers output file names from input file paths.
- **Error Handling:** Checks for file existence and handles missing/invalid files gracefully.
- **User Interactivity:** Prompts users for input and provides file selection menus.
- **Heavy Commenting:** Provides clear, educational comments for each step.
