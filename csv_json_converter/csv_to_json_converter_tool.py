#!/usr/bin/env python3
"""
csv_json_converter.py

Bidirectional CSV ⇄ JSON converter with short flags (c2j, j2c).

Interactive mode (no args):
  - Prompts for direction (c2j/j2c)
  - Prompts for input file path
  - Derives output filename from input stem

Usage:
  # Interactive:
  $ python csv_json_converter.py

  # Explicit:
  $ python csv_json_converter.py c2j data.csv
  $ python csv_json_converter.py j2c data.json
  $ python csv_json_converter.py c2j input.csv output.json
  $ python csv_json_converter.py j2c input.json output.csv
"""

import argparse
import csv
import json
import logging
import sys
from pathlib import Path
from typing import List, Dict, Any


def setup_logging() -> None:
    """Configure logging for the script."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def convert_csv_to_json(csv_path: Path, json_path: Path) -> None:
    """Convert a CSV file to JSON."""
    logging.info(f"Converting CSV → JSON: {csv_path} → {json_path}")
    try:
        with csv_path.open("r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            data: List[Dict[str, Any]] = list(reader)
            logging.debug(f"Read {len(data)} records from CSV")
    except Exception as e:
        logging.error(f"Error reading CSV: {e}")
        sys.exit(1)
    try:
        with json_path.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
            logging.info(f"Wrote {len(data)} records to JSON")
    except Exception as e:
        logging.error(f"Error writing JSON: {e}")
        sys.exit(1)


def convert_json_to_csv(json_path: Path, csv_path: Path) -> None:
    """Convert a JSON file (list of objects) to CSV."""
    logging.info(f"Converting JSON → CSV: {json_path} → {csv_path}")
    try:
        with json_path.open("r", encoding="utf-8") as f:
            data: List[Dict[str, Any]] = json.load(f)
            logging.debug(f"Loaded {len(data)} records from JSON")
    except Exception as e:
        logging.error(f"Error reading JSON: {e}")
        sys.exit(1)
    if not isinstance(data, list) or not data:
        logging.error("JSON must be a non-empty list of objects")
        sys.exit(1)
    fieldnames = list(data[0].keys())
    try:
        with csv_path.open("w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
            logging.info(f"Wrote {len(data)} records to CSV")
    except Exception as e:
        logging.error(f"Error writing CSV: {e}")
        sys.exit(1)


def parse_arguments() -> argparse.Namespace:
    """
    Parse command-line arguments, with interactive fallback.
    """
    parser = argparse.ArgumentParser(
        description="Convert between CSV and JSON formats (short flags: c2j, j2c)."
    )
    parser.add_argument(
        "direction",
        choices=["c2j", "j2c"],
        nargs="?",
        help="Conversion direction: c2j or j2c (default: interactive c2j)",
    )
    parser.add_argument(
        "input",
        type=Path,
        nargs="?",
        help="Path to input file (CSV or JSON)",
    )
    parser.add_argument(
        "output",
        type=Path,
        nargs="?",
        help="Path to output file (defaults to input stem + extension)",
    )

    args = parser.parse_args()

    # Interactive mode if no args provided
    if args.direction is None and args.input is None:
        try:
            direction = input("Direction (c2j/j2c?) [c2j]: ").strip() or "c2j"
            if direction not in ("c2j", "j2c"):
                raise ValueError("Invalid direction")
            inp = input("Enter input file path: ").strip()
            input_path = Path(inp)
            if not input_path.exists():
                logging.error(f"Input file not found: {input_path}")
                sys.exit(1)
            ext = ".json" if direction == "c2j" else ".csv"
            output_path = input_path.with_suffix(ext)
            return argparse.Namespace(direction=direction, input=input_path, output=output_path)
        except (KeyboardInterrupt, EOFError):
            logging.info("Operation cancelled by user.")
            sys.exit(0)

    # Non-interactive: fill defaults
    direction = args.direction or "c2j"
    input_path = args.input
    if not input_path or not input_path.exists():
        parser.error(f"Input file does not exist: {input_path}")

    if args.output:
        output_path = args.output
    else:
        ext = ".json" if direction == "c2j" else ".csv"
        output_path = input_path.with_suffix(ext)

    return argparse.Namespace(direction=direction, input=input_path, output=output_path)


def main() -> None:
    setup_logging()
    try:
        args = parse_arguments()
    except KeyboardInterrupt:
        logging.info("Operation cancelled by user.")
        sys.exit(0)

    if args.direction == "c2j":
        convert_csv_to_json(args.input, args.output)
    else:
        convert_json_to_csv(args.input, args.output)


if __name__ == "__main__":
    main()
