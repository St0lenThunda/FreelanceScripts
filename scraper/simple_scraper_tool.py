#!/usr/bin/env python3
"""
simple_scraper_tool.py

A modular web scraper that fetches titles and links from one or more URLs (default: Hacker News).

Key Features:
- Fetches inner text and links of <a> elements inside <span class="titleline"> (default selector).
- Handles multiple URLs from command-line arguments or a file (--url-file).
- Allows custom CSS selectors via --selector for flexible scraping of any site.
- Can scan the page and suggest common tags, classes, ids, and nested selectors for scrapable elements (--suggest).
- The number of top suggestions and the maximum selector depth are adjustable via --suggest-top and --suggest-depth.
- Suggestion output is ranked using a composite emoji system (🏆, 🥇, 🥈, 🥉, 🎖️, 🔸) that combines link-likelihood, structural preference, and frequency.
- Only the top 5 selector suggestions show detailed metrics and the composite emoji; the rest show selector and count for clarity.
- Automatically suggests scrapable elements if no results are found with the current selector.
- Prints results to the console (with --print or --no-save) for easy chaining.
- Saves results to a JSON file in the output directory (default behavior, can be disabled with --no-save).
- Output files are named after the URL.
- Designed as a learning resource: code is heavily commented and modular.

TODO: Add colorized output for better readability.
"""

import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urlparse
from pathlib import Path
import argparse
from collections import Counter

# URL to scrape
URL = "https://news.ycombinator.com"

# --- Configurable suggestion parameters ---
SUGGEST_TOP_N = 10  # How many top tags/classes/ids/selectors to show
SUGGEST_MAX_DEPTH = 2  # Max depth for nested selector suggestions
# -----------------------------------------

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
    return extract_titles_and_links(soup, selector)

def extract_titles_and_links(soup, selector):
    results = []
    for a in soup.select(selector):
        results.append({"title": a.get_text(), "url": a.get("href")})
    return results

# --- Helper functions for suggestion system ---
def get_tag_counts(soup):
    tag_counts = {}
    for tag in soup.find_all(True):
        tag_counts[tag.name] = tag_counts.get(tag.name, 0) + 1
    return tag_counts

def get_class_counts(soup):
    class_counts = {}
    for tag in soup.find_all(class_=True):
        for cls in tag.get("class", []):
            class_counts[cls] = class_counts.get(cls, 0) + 1
    return class_counts

def get_id_counts(soup):
    id_counts = {}
    for tag in soup.find_all(id=True):
        id_counts[tag['id']] = id_counts.get(tag['id'], 0) + 1
    return id_counts

def get_selector_path(tag, max_depth):
    path = []
    current = tag
    depth = 0
    while current and current.name != '[document]' and depth < max_depth:
        part = current.name
        if current.get('class'):
            part += '.' + '.'.join(current.get('class'))
        if current.get('id'):
            part += f"#{current.get('id')}"
        path.append(part)
        current = current.parent
        depth += 1
    return ' > '.join(reversed(path))

def get_selector_preference_score(tag, selector):
    """
    Original preference score: prefers selectors ending in 'a', 'li', 'ul', 'ol', and 'a' inside lists.
    """
    score = 0
    if tag.name == 'a':
        score += 3
    if tag.name in {'li', 'ul', 'ol'}:
        score += 2
    if tag.name == 'a' and any(p in selector for p in ['li', 'ul', 'ol']):
        score += 1  # Bonus for a inside a list
    return score

def get_selector_counters_and_ranking(soup, max_depth):
    selector_counter = Counter()
    selector_ranking = {}
    selector_preference = {}
    for tag in soup.find_all(True):
        selector = get_selector_path(tag, max_depth)
        selector_counter[selector] += 1
        # Heuristic: score based on likelihood the selector yields usable links (1-100)
        score = 0
        # Highest: <a> tags with href
        if tag.name == 'a' and tag.get('href'):
            score = 100
        # <li> or <div> containing <a> with href
        elif tag.name in {'li', 'div', 'span', 'td', 'tr', 'ul', 'ol'}:
            if tag.find('a', href=True):
                score = 80
            else:
                score = 30
        elif tag.name in {'ul', 'ol'}:
            score = 60
        elif tag.name in {'h1', 'h2', 'h3', 'h4', 'h5', 'h6'}:
            if tag.find('a', href=True):
                score = 70
            else:
                score = 20
        elif tag.get('href'):
            score = 60
        else:
            score = 10
        selector_ranking[selector] = max(selector_ranking.get(selector, 0), score)
        # Add original preference score
        pref_score = get_selector_preference_score(tag, selector)
        selector_preference[selector] = max(selector_preference.get(selector, 0), pref_score)
    return selector_counter, selector_ranking, selector_preference

def print_tag_summary(tag_counts, top_n):
    print(f"\n[INFO] Tag summary (top {top_n}):")
    for tag, count in sorted(tag_counts.items(), key=lambda x: -x[1])[:top_n]:
        print(f"  <{tag}>: {count}")

def print_class_summary(class_counts, top_n):
    if class_counts:
        print(f"[INFO] Common classes (top {top_n}):")
        for cls, count in sorted(class_counts.items(), key=lambda x: -x[1])[:top_n]:
            print(f"  .{cls}: {count}")

def print_id_summary(id_counts, top_n):
    if id_counts:
        print(f"[INFO] Common ids (top {top_n}):")
        for id_, count in sorted(id_counts.items(), key=lambda x: -x[1])[:top_n]:
            print(f"  #{id_}: {count}")

def print_selector_summary(ranked_selectors, selector_ranking, selector_preference, top_n):
    if ranked_selectors:
        print(f"[INFO] Common nested selectors (top {top_n}, ranked):")
        # Table header
        print(f"{'Selector':<50} {'Count':>7} {'Rank':>7} {'Pref':>7} {'Freq':>7} {'Emoji':>7}")
        print('-' * 90)
        max_rank = 100
        max_pref = max(selector_preference.values()) if selector_preference else 1
        max_count = max([count for _, count in ranked_selectors]) if ranked_selectors else 1
        def composite_emoji(rank, pref, count):
            rank_norm = rank / max_rank if max_rank else 0
            pref_norm = pref / max_pref if max_pref else 0
            count_norm = count / max_count if max_count else 0
            composite = 0.5 * rank_norm + 0.3 * pref_norm + 0.2 * count_norm
            if composite > 0.9:
                return '🏆'
            elif composite > 0.75:
                return '🥇'
            elif composite > 0.6:
                return '🥈'
            elif composite > 0.4:
                return '🥉'
            elif composite > 0.2:
                return '🎖️'
            else:
                return '🔸'
        for i, (sel, count) in enumerate(ranked_selectors[:top_n]):
            rank = selector_ranking.get(sel, 0)
            pref = selector_preference.get(sel, 0)
            emoji = composite_emoji(rank, pref, count) if i < 5 else ''
            print(f"{sel:<50.50} {count:>7} {rank:>7} {pref:>7} {count:>7} {emoji:>7}")
        print('-' * 90)

# Suggest scrapable elements by scanning the DOM for common tags/classes/ids

def suggest_scrapables(html, top_n=None, max_depth=None):
    """
    Scan the HTML and print a summary of common tags, classes, ids, and nested selectors.
    """
    if top_n is None:
        top_n = SUGGEST_TOP_N
    if max_depth is None:
        max_depth = SUGGEST_MAX_DEPTH
    soup = BeautifulSoup(html, "html.parser")
    tag_counts = get_tag_counts(soup)
    print_tag_summary(tag_counts, top_n)
    class_counts = get_class_counts(soup)
    print_class_summary(class_counts, top_n)
    id_counts = get_id_counts(soup)
    print_id_summary(id_counts, top_n)
    selector_counter, selector_ranking, selector_preference = get_selector_counters_and_ranking(soup, max_depth)
    ranked_selectors = sorted(selector_counter.items(), key=lambda x: (selector_ranking.get(x[0], 0), x[1]), reverse=True)
    print_selector_summary(ranked_selectors, selector_ranking, selector_preference, top_n)

# Update argument parsing to allow selector and suggestion
def parse_args():
    parser = argparse.ArgumentParser(description="Scrape titles/links from provided URLs.")
    parser.add_argument('urls', nargs='*', default=[URL], help='One or more URLs to scrape (default: Hacker News)')
    parser.add_argument('--url-file', type=str, help='Path to a file containing newline-separated URLs to scrape')
    parser.add_argument('--selector', default='span.titleline a', help='CSS selector for elements to scrape (default: span.titleline a)')
    parser.add_argument('--suggest', action='store_true', help='Scan the page and suggest scrapable tags/classes/ids')
    parser.add_argument('--suggest-top', type=int, default=SUGGEST_TOP_N, help=f'How many top tags/classes/ids/selectors to show (default: {SUGGEST_TOP_N})')
    parser.add_argument('--suggest-depth', type=int, default=SUGGEST_MAX_DEPTH, help=f'Max depth for nested selector suggestions (default: {SUGGEST_MAX_DEPTH})')
    parser.add_argument('--no-save', action='store_true', help='Do not save results to file (only print to terminal)')
    parser.add_argument('--print', action='store_true', help='Print results to terminal (default: off if saving to file)')
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    # Gather URLs from CLI and/or file
    urls = list(args.urls)
    if args.url_file:
        url_file_path = Path(args.url_file)
        if url_file_path.exists():
            with url_file_path.open("r", encoding="utf-8") as f:
                file_urls = [line.strip() for line in f if line.strip()]
                urls.extend(file_urls)
        else:
            notify(f"URL file not found: {args.url_file}")
    # Remove duplicates while preserving order
    seen = set()
    urls = [u for u in urls if not (u in seen or seen.add(u))]
    for url in urls:
        notify(f"Fetching: {url}")
        response = requests.get(url)
        notify("Fetched page, status code: " + str(response.status_code))
        results = []
        if response.status_code == 200:
            html = response.text
            if args.suggest:
                suggest_scrapables(html, top_n=args.suggest_top, max_depth=args.suggest_depth)
            # Use default selector if none supplied
            selector = args.selector if args.selector else "span.titleline a"
            notify(f"Parsing HTML and extracting with selector: {selector}")
            results = scrape_titles_and_links(html, selector=selector)
            notify(f"Extracted {len(results)} items.")
        else:
            notify(f"Failed to fetch {url} (status code: {response.status_code})")
        # Print to terminal if requested or if not saving
        if args.print or args.no_save:
            print(json.dumps(results, indent=2))
        # Save to file unless --no-save is set and only if response was successful
        if not args.no_save and response.status_code == 200:
            output_file = OUTPUT_DIR / url_to_filename(url)
            with output_file.open("w", encoding="utf-8") as f:
                json.dump(results, f, indent=2)
            notify(f"Results saved to: {output_file}")
        # If no results were found, automatically suggest scrapable elements
        if response.status_code == 200 and not results and not args.suggest:
            notify("No results found with the current selector. Scanning for scrapable elements...")
            suggest_scrapables(html, top_n=args.suggest_top, max_depth=args.suggest_depth)
