#!/usr/bin/env python3
"""
simple_scraper_tool.py

Minimal interactive web scraper for <h2> headlines.

Features:
- Interactive mode (no args): prompts for URL, auto-names output file.
- Explicit mode: pass URL and optional output path.
- Graceful handling of Ctrl+C/EOF.
- Logging for clear progress updates.

Usage:
  # Interactive
  $ python simple_scraper_tool.py

  # Explicit (default output: domain_headlines.json)
  $ python simple_scraper_tool.py https://news.ycombinator.com

  # Explicit with custom output
  $ python simple_scraper_tool.py https://example.com my_headlines.json
"""

import argparse
import json
import logging
import sys
from pathlib import Path
from typing import List
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup


def setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%H:%M:%S",
    )


def fetch_headlines(url: str) -> List[str]:
    """Fetch all <h2> texts from the given URL."""
    logging.info(f"Fetching headlines from: {url}")
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    headers = [h.get_text(strip=True) for h in soup.find_all("h2")]
    logging.info(f"Found {len(headers)} <h2> tags")
    return headers


def default_output_path(url: str) -> Path:
    """
    Build a default filename based on the URL’s domain.
    e.g. news.ycombinator.com → news.ycombinator.com_headlines.json
    """
    domain = urlparse(url).netloc or "output"
    return Path(f"{domain}_headlines.json")


def save_to_json(data: List[str], path: Path) -> None:
    """Write the list to JSON with indentation."""
    logging.info(f"Saving {len(data)} items to: {path}")
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    logging.info("Save complete.")


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Simple <h2> scraper: URL → JSON headlines"
    )
    parser.add_argument(
        "url", nargs="?", help="Target URL to scrape (interactive if omitted)"
    )
    parser.add_argument(
        "output",
        nargs="?",
        type=Path,
        help="Output JSON path (defaults to domain_headlines.json)",
    )
    args = parser.parse_args()

    # Interactive fallback
    if not args.url:
        try:
            args.url = input("Enter URL to scrape: ").strip()
        except (KeyboardInterrupt, EOFError):
            logging.info("Cancelled by user.")
            sys.exit(0)

    # Validate URL
    if not args.url.startswith(("http://", "https://")):
        args.url = "https://" + args.url

    # Determine output
    if args.output:
        out_path = args.output
    else:
        out_path = default_output_path(args.url)

    return argparse.Namespace(url=args.url, output=out_path)


def main() -> None:
    setup_logging()
    try:
        opts = parse_arguments()
        headlines = fetch_headlines(opts.url)
        save_to_json(headlines, opts.output)
    except KeyboardInterrupt:
        logging.info("Operation cancelled by user.")
        sys.exit(0)
    except Exception as e:
        logging.error(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
