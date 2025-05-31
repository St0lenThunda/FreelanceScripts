#!/usr/bin/env python3
"""
simple_scraper_tool.py

A simple web scraper that fetches all titles from Hacker News.

Key Features:
- Fetches inner text and links of <a> elements inside <span class="titleline">.
- Prints the results to the console.
- Generates a JSON file with the results in the output directory.
- Saves results to a JSON file named after the URL in the output directory. 

Intended as a learning resource: code is heavily commented to explain each step and concept.
"""

import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urlparse
from pathlib import Path

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

notify(f"Fetching: {URL}")
response = requests.get(URL)
notify("Fetched page, status code: " + str(response.status_code))

results = []
if response.status_code == 200:
    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")
    notify("Parsing HTML and extracting titles/links...")
    # Find all <span class="titleline"> elements
    for span in soup.find_all("span", class_="titleline"):
        # Find the <a> tag inside the span
        a = span.find("a")
        if a:
            results.append({"title": a.text, "url": a['href']})
    notify(f"Extracted {len(results)} items.")
else:
    notify(f"Failed to fetch {URL} (status code: {response.status_code})")

# Save results to JSON file in output dir
output_file = OUTPUT_DIR / url_to_filename(URL)
with output_file.open("w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)
notify(f"Results saved to: {output_file}")
