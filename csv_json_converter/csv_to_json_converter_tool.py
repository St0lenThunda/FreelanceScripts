#!/usr/bin/env python3
"""
csv_to_json_converter_tool.py

A two-way data converter for CSV and JSON files. It contains functions to convert CSV files to JSON format and vice versa. The script can be run from the command line, allowing users to specify input and output files, or it can prompt for file paths interactively if no arguments are provided.

Key Features:
- Converts CSV to JSON and JSON to CSV.
- Interactive: prompts for input/output files if not provided as arguments.
- Lists local .csv and .json files for easy selection in interactive mode.
- Infers output file names from input if not provided (auto-naming).
- CLI-friendly: supports short, memorable flags.
- Robust error handling for missing or invalid files.
- Local file listing: lists all .csv and .json files in the current directory for easy selection.
- Robust error handling for missing or invalid files.
- Educational: code is heavily commented for learning purposes.

Intended as a learning resource: code is heavily commented to explain each step and concept.
"""

import csv
import json
import sys
from pathlib import Path

# Helper function to convert CSV to JSON
def csv_to_json(csv_path, json_path):
    """
    Reads a CSV file and writes its contents as JSON.
    """
    if not Path(csv_path).exists():
        print(f"❌ CSV file not found: {csv_path}")
        return
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = list(reader)
    with open(json_path, 'w', encoding='utf-8') as jsonfile:
        json.dump(rows, jsonfile, indent=2)
    print(f"✅ Converted {csv_path} to {json_path}")

# Helper function to convert JSON to CSV
def json_to_csv(json_path, csv_path):
    """
    Reads a JSON file and writes its contents as CSV.
    """
    with open(json_path, encoding='utf-8') as jsonfile:
        data = json.load(jsonfile)
    if not data:
        print("No data to write.")
        return
    with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
    print(f"✅ Converted {json_path} to {csv_path}")

# Helper function to list files by extension
def list_files_by_ext(ext):
    """
    List files in the current directory with the given extension.
    """
    return sorted([str(p) for p in Path('.').glob(f'*.{ext}')])

# Main function to handle CLI arguments and prompt user if needed
def main():
    """
    Main function to handle CLI arguments and prompt user for conversion direction and file paths.
    If only an input file is provided, infer the output file name by changing the extension.
    Lists local .csv and .json files as options for input.
    """
    args = sys.argv[1:]
    if not args:
        print("No arguments provided. Choose conversion direction:")
        print("1. CSV to JSON")
        print("2. JSON to CSV")
        choice = input("Enter 1 or 2: ").strip()
        if choice == '1':
            csv_files = list_files_by_ext('csv')
            if csv_files:
                print("Available CSV files:")
                for i, f in enumerate(csv_files, 1):
                    print(f"  {i}. {f}")
                csv_idx = input("Select CSV file by number or enter path: ").strip()
                if csv_idx.isdigit() and 1 <= int(csv_idx) <= len(csv_files):
                    csv_path = csv_files[int(csv_idx)-1]
                else:
                    csv_path = csv_idx
            else:
                csv_path = input("Enter CSV file path: ").strip()
            json_path = input("Enter output JSON file path (leave blank to infer): ").strip()
            if not json_path:
                json_path = str(Path(csv_path).with_suffix('.json'))
            csv_to_json(csv_path, json_path)
        elif choice == '2':
            json_files = list_files_by_ext('json')
            if json_files:
                print("Available JSON files:")
                for i, f in enumerate(json_files, 1):
                    print(f"  {i}. {f}")
                json_idx = input("Select JSON file by number or enter path: ").strip()
                if json_idx.isdigit() and 1 <= int(json_idx) <= len(json_files):
                    json_path = json_files[int(json_idx)-1]
                else:
                    json_path = json_idx
            else:
                json_path = input("Enter JSON file path: ").strip()
            csv_path = input("Enter output CSV file path (leave blank to infer): ").strip()
            if not csv_path:
                csv_path = str(Path(json_path).with_suffix('.csv'))
            json_to_csv(json_path, csv_path)
        else:
            print("Invalid choice.")
    elif args[0] == '--csv-to-json' and 2 <= len(args) <= 3:
        csv_path = args[1]
        if len(args) == 3:
            json_path = args[2]
        else:
            json_path = str(Path(csv_path).with_suffix('.json'))
        csv_to_json(csv_path, json_path)
    elif args[0] == '--json-to-csv' and 2 <= len(args) <= 3:
        json_path = args[1]
        if len(args) == 3:
            csv_path = args[2]
        else:
            csv_path = str(Path(json_path).with_suffix('.csv'))
        json_to_csv(json_path, csv_path)
    else:
        print("Usage:")
        print("  --csv-to-json <input.csv> [output.json]")
        print("  --json-to-csv <input.json> [output.csv]")

if __name__ == "__main__":
    main()
