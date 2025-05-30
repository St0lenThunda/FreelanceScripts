#!/usr/bin/env python3
"""
scraper_bugfix_tool.py

Fixed version of scraper that grabs <a> titles from <span class="titleline">,
and saves structured output to an `output/` directory.
"""

import argparse
import json
import logging
import sys
from pathlib import Path
from urllib.parse import urlparse, urljoin
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
    """Fetch inner text and resolved links of <a> in span.titleline"""
    logging.info(f"Fetching from: {url}")
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
    except Exception as e:
        logging.error(f"Request failed: {e}")
        sys.exit(1)

    soup = BeautifulSoup(resp.text, "html.parser")
    titles = [
        {
            "title": a.get_text(strip=True),
            "link": urljoin(url, a.get("href"))
        }
        for span in soup.select("span.titleline")
        for a in span.find_all("a")
    ]
    logging.info(f"Extracted {len(titles)} headlines")
    return titles


def default_output_path(url: str) -> Path:
    domain = urlparse(url).netloc or "output"
    output_dir = Path.cwd() / "output"
    output_dir.mkdir(exist_ok=True)
    return output_dir / f"{domain}_titles.json"


def save_to_json(data: List[dict], path: Path) -> None:
    logging.info(f"Saving to: {path}")
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    logging.info("Save complete.")


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Scrape span.titleline a and output to JSON."
    )
    parser.add_argument("url", nargs="?", help="Target URL to scrape")
    parser.add_argument("output", nargs="?", type=Path, help="Output JSON path")

    args = parser.parse_args()

    if not args.url:
        try:
            args.url = input("Enter URL: ").strip()
        except (KeyboardInterrupt, EOFError):
            logging.info("Cancelled.")
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
        logging.info("Interrupted.")
        sys.exit(0)
    except Exception as e:
        logging.error(f"Unhandled error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
