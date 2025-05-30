#!/usr/bin/env python3
"""
scraper_buggy_tool.py

Broken version of the scraper tool. Only grabs <h2> text and lacks error handling.
Used for demonstration purposes.
"""

import requests
from bs4 import BeautifulSoup

def fetch_headlines(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    return [h.get_text() for h in soup.find_all("h2")]

if __name__ == "__main__":
    url = "https://news.ycombinator.com"
    headlines = fetch_headlines(url)
    for h in headlines:
        print(h)
