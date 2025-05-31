#!/usr/bin/env python3
"""
simple_scraper_tool.py

A simple web scraper that fetches all titles from Hacker News.

Key Features:
- Fetches inner text and links of <a> elements inside <span class="titleline">.
- Prints the results to the console.

Intended as a learning resource: code is heavily commented to explain each step and concept.
"""

import requests
from bs4 import BeautifulSoup

# URL to scrape
URL = "https://news.ycombinator.com"

# Fetch the page content using requests
response = requests.get(URL)
# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")
    # Find all <span class="titleline"> elements
    for span in soup.find_all("span", class_="titleline"):
        # Find the <a> tag inside the span
        a = span.find("a")
        if a:
            # Print the text and the link
            print(f"{a.text} -> {a['href']}")
else:
    print(f"Failed to fetch {URL} (status code: {response.status_code})")
