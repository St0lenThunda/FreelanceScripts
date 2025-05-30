#!/usr/bin/env python3
"""
simple_scraper_tool.py

Scrapes inner text from all <a> tags inside <span class="titleline"> from a given URL.
Useful for scraping article headlines (e.g., Hacker News).

Usage:
    python simple_scraper_tool.py                     # interactive mode
    python simple_scraper_tool.py <URL>               # uses default output
    python simple_scraper_tool.py <URL> <output.json> # custom output path
"""

import argparse
import json
import logging
import sys
from pathlib import Path
from urllib.parse import urlparse
from typing import List

import requests
from bs4 import BeautifulSoup


def setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%H:%M:%S",
    )


def fetch_titles(url: str) -> List[dict]:
    """Fetch inner text and links of <a> elements inside <span class="titleline">."""
    logging.info(f"Fetching headlines from: {url}")
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
    except Exception as e:
        logging.error(f"Request failed: {e}")
        sys.exit(1)

    soup = BeautifulSoup(resp.text, "html.parser")
    titles = [
        {"title": a.get_text(strip=True), "link": a.get("href")}
        for span in soup.select("span.titleline")
        for a in span.find_all("a")
    ]

    logging.info(f"Found {len(titles)} headlines")
    return titles


def default_output_path(url: str) -> Path:
    """Generate an output filename based on the domain."""
    domain = urlparse(url).netloc or "output"
    output_dir = Path.cwd() / "output"
    output_dir.mkdir(exist_ok=True)
    return output_dir / f"{domain}_titles.json"


def save_to_json(data: List[dict], path: Path) -> None:
    logging.info(f"Saving {len(data)} items to: {path}")
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    logging.info("Save complete.")


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Scrape <span.titleline a> text and save as JSON"
    )
    parser.add_argument("url", nargs="?", help="Target URL to scrape")
    parser.add_argument("output", nargs="?", type=Path, help="Output file (JSON)")

    args = parser.parse_args()

    if not args.url:
        try:
            args.url = input("Enter a URL to scrape: ").strip()
        except (KeyboardInterrupt, EOFError):
            logging.info("Cancelled by user.")
            sys.exit(0)

    if not args.url.startswith(("http://", "https://")):
        args.url = "https://" + args.url

    output = args.output or default_output_path(args.url)
    return argparse.Namespace(url=args.url, output=output)


def main() -> None:
    setup_logging()
    try:
        args = parse_arguments()
        titles = fetch_titles(args.url)
        save_to_json(titles, args.output)
    except KeyboardInterrupt:
        logging.info("Operation cancelled by user.")
        sys.exit(0)
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
