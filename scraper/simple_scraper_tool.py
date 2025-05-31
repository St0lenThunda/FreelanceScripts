#!/usr/bin/env python3
"""
simple_scraper_tool.py

A modular web scraper that fetches titles and links from one or more URLs (default: Hacker News).

Key Features:
- Fetches inner text and links of <a> elements inside <span class="titleline"> (default selector).
- Handles multiple URLs from command-line arguments.
- Allows custom CSS selectors via --selector for flexible scraping of any site.
- Can scan the page and suggest common tags, classes, and ids for scrapable elements (--suggest).
- Prints results to the console (with --print or --no-save) for easy chaining.
- Saves results to a JSON file in the output directory (default behavior, can be disabled with --no-save).
- Output files are named after the URL.
- Designed as a learning resource: code is heavily commented and modular.
"""

import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urlparse
from pathlib import Path
import argparse

# URL to scrape
URL = "https://news.ycombinator.com"

# Helper to create a safe filename from a URL
def url_to_filename(url):
    parsed = urlparse(url)
    # Use netloc and path, replace non-alphanum with _
    base = (parsed.netloc + parsed.path).replace('/', '_').replace('.', '_')
    if not base.endswith('.json'):
        base += '.json'
    return base

# Output directory (root/output)
OUTPUT_DIR = Path(__file__).resolve().parent.parent / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

# Notify user of progress
def notify(msg):
    print(f"[INFO] {msg}")

# Modular scraping: allow user to specify a CSS selector (default is for Hacker News)
def scrape_titles_and_links(html, selector="span.titleline a"):
    """
    Scrape titles and links using a CSS selector (default: 'span.titleline a').
    Returns a list of dicts with 'title' and 'url'.
    """
    soup = BeautifulSoup(html, "html.parser")
    results = []
    for a in soup.select(selector):
        results.append({"title": a.get_text(), "url": a.get("href")})
    return results

# Suggest scrapable elements by scanning the DOM for common tags/classes/ids
def suggest_scrapables(html):
    """
    Scan the HTML and print a summary of common tags, classes, and ids.
    """
    soup = BeautifulSoup(html, "html.parser")
    tag_counts = {}
    for tag in soup.find_all(True):
        tag_counts[tag.name] = tag_counts.get(tag.name, 0) + 1
    print("\n[INFO] Tag summary (top 10):")
    for tag, count in sorted(tag_counts.items(), key=lambda x: -x[1])[:10]:
        print(f"  <{tag}>: {count}")
    # List common classes
    class_counts = {}
    for tag in soup.find_all(class_=True):
        for cls in tag.get("class", []):
            class_counts[cls] = class_counts.get(cls, 0) + 1
    if class_counts:
        print("[INFO] Common classes (top 10):")
        for cls, count in sorted(class_counts.items(), key=lambda x: -x[1])[:10]:
            print(f"  .{cls}: {count}")
    # List common ids
    id_counts = {}
    for tag in soup.find_all(id=True):
        id_counts[tag['id']] = id_counts.get(tag['id'], 0) + 1
    if id_counts:
        print("[INFO] Common ids (top 10):")
        for id_, count in sorted(id_counts.items(), key=lambda x: -x[1])[:10]:
            print(f"  #{id_}: {count}")

# Update argument parsing to allow selector and suggestion
def parse_args():
    parser = argparse.ArgumentParser(description="Scrape titles/links from provided URLs.")
    parser.add_argument('urls', nargs='*', default=[URL], help='One or more URLs to scrape (default: Hacker News)')
    parser.add_argument('--selector', default='span.titleline a', help='CSS selector for elements to scrape (default: span.titleline a)')
    parser.add_argument('--suggest', action='store_true', help='Scan the page and suggest scrapable tags/classes/ids')
    parser.add_argument('--no-save', action='store_true', help='Do not save results to file (only print to terminal)')
    parser.add_argument('--print', action='store_true', help='Print results to terminal (default: off if saving to file)')
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    for url in args.urls:
        notify(f"Fetching: {url}")
        response = requests.get(url)
        notify("Fetched page, status code: " + str(response.status_code))
        results = []
        if response.status_code == 200:
            html = response.text
            if args.suggest:
                suggest_scrapables(html)
            notify(f"Parsing HTML and extracting with selector: {args.selector}")
            results = scrape_titles_and_links(html, args.selector)
            notify(f"Extracted {len(results)} items.")
        else:
            notify(f"Failed to fetch {url} (status code: {response.status_code})")
        # Print to terminal if requested or if not saving
        if args.print or args.no_save:
            print(json.dumps(results, indent=2))
        # Save to file unless --no-save is set
        if not args.no_save:
            output_file = OUTPUT_DIR / url_to_filename(url)
            with output_file.open("w", encoding="utf-8") as f:
                json.dump(results, f, indent=2)
            notify(f"Results saved to: {output_file}")
