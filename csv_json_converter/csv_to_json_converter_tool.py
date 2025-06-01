#!/usr/bin/env python3
"""
csv_to_json_converter_tool.py

A two-way data converter for CSV and JSON files.

Key Features:
- Converts CSV to JSON and JSON to CSV.
- Interactive: prompts for input/output files if not provided as arguments.
- CLI-friendly: supports short, memorable flags.

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

# Main function to handle CLI arguments and prompt user if needed
def main():
    """
    Main function to handle CLI arguments and prompt user for conversion direction and file paths.
    """
    args = sys.argv[1:]
    if not args:
        print("No arguments provided. Choose conversion direction:")
        print("1. CSV to JSON")
        print("2. JSON to CSV")
        choice = input("Enter 1 or 2: ").strip()
        if choice == '1':
            csv_path = input("Enter CSV file path: ").strip()
            json_path = input("Enter output JSON file path: ").strip()
            csv_to_json(csv_path, json_path)
        elif choice == '2':
            json_path = input("Enter JSON file path: ").strip()
            csv_path = input("Enter output CSV file path: ").strip()
            json_to_csv(json_path, csv_path)
        else:
            print("Invalid choice.")
    elif args[0] == '--csv-to-json' and len(args) == 3:
        csv_to_json(args[1], args[2])
    elif args[0] == '--json-to-csv' and len(args) == 3:
        json_to_csv(args[1], args[2])
    else:
        print("Usage:")
        print("  --csv-to-json <input.csv> <output.json>")
        print("  --json-to-csv <input.json> <output.csv>")

if __name__ == "__main__":
    main()
