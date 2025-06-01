# 🧙‍♂️ CSV ⇄ JSON Converter Tool

> ## Purpose 
> A two-way data converter for CSV and JSON files.

## Features
- Converts CSV to JSON and JSON to CSV.
- Interactive: prompts for input/output files if not provided as arguments.
- Lists local `.csv` and `.json` files for easy selection in interactive mode.
- Infers output file names from input if not provided (auto-naming).
- CLI-friendly: supports short, memorable flags.
- Robust error handling for missing or invalid files.
- Educational: code is heavily commented for learning purposes.

## What's New
- **Output file inference:** If you leave the output file blank, the tool will auto-name it based on your input file.
- **Local file listing:** When run interactively, the tool lists available `.csv` or `.json` files for you to select.
- **Improved error handling:** Clear messages for missing or invalid files, and better user experience.

## Usage

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
