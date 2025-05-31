# CSV ⇄ JSON Converter Tool

A two-way data converter for CSV and JSON files.

## Features
- Converts CSV to JSON and JSON to CSV.
- Interactive: prompts for input/output files if not provided as arguments.
- CLI-friendly: supports short, memorable flags.
- Educational: code is heavily commented for learning purposes.

## Usage

### Interactive Mode
If you run the script without arguments, you will be prompted to choose the conversion direction and provide file paths:

```bash
python csv_to_json_converter_tool.py
```

### Command-Line Mode
You can also specify the conversion direction and file paths directly:

```bash
python csv_to_json_converter_tool.py --csv-to-json input.csv output.json
python csv_to_json_converter_tool.py --json-to-csv input.json output.csv
```

## Example

Convert CSV to JSON interactively:
```bash
python csv_to_json_converter_tool.py
# Choose 1, then provide file paths when prompted
```

Convert JSON to CSV with arguments:
```bash
python csv_to_json_converter_tool.py --json-to-csv input.json output.csv
```

## Excluding from Packaging
To exclude this tool from packaging or documentation, add a `.excluded` file to this directory:
```bash
touch .excluded
```

## Educational Notes
- The script is designed as a learning resource, with docstrings and comments explaining each step and concept.
- See the source code for detailed explanations of the logic and Python features used.
