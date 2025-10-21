#!/usr/bin/env python3
"""
scraper_tool.py

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
- Prints results to the console after each scrape for easy chaining.
- Prompts before saving results to a JSON file in the output directory (use --auto-save to skip the prompt, or --no-save to skip saving).
- Output files are named after the URL.
- Designed as a learning resource: code is heavily commented and modular.
- Advanced bot protection debugging: Automatically analyzes response headers and body for clues (Cloudflare, Akamai, cookies, JavaScript, CAPTCHA, etc.) and outputs actionable suggestions.
- Only retries with the next User-Agent if no actionable suggestions are found; otherwise, stops and outputs next steps.
- Logs all progress, sent/received headers, and body snippets for robust debugging.

TODO: Add colorized output for better readability.
"""

import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urlparse
from pathlib import Path
import argparse
from collections import Counter
import sys

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

def split_selector_tokens(selector):
    """
    Break a selector path (e.g. 'ul.nav > li.item > a.link') into bare tag tokens.
    """
    tokens = []
    for part in selector.split('>'):
        token = part.strip()
        if not token:
            continue
        token = token.split('#', 1)[0]
        token = token.split('.', 1)[0]
        tokens.append(token)
    return tokens

def selector_has_list_ancestor(selector):
    """
    Return True if any ancestor token in the selector path is a list container.
    """
    tokens = split_selector_tokens(selector)
    # Ignore the final token (the current element)
    return any(tok in {'li', 'ul', 'ol'} for tok in tokens[:-1])

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
    if tag.name == 'a' and selector_has_list_ancestor(selector):
        score += 1  # Bonus for a inside a list
    return score

def get_selector_counters_and_ranking(soup, max_depth):
    selector_counter = Counter()
    selector_rank_totals = Counter()
    selector_pref_totals = Counter()
    for tag in soup.find_all(True):
        selector = get_selector_path(tag, max_depth)
        selector_counter[selector] += 1
        # Heuristic: score based on likelihood the selector yields usable links (1-100)
        score = 10
        # Highest: <a> tags with href
        if tag.name == 'a' and tag.get('href'):
            score = 100
        # <li> or <div> containing <a> with href
        elif tag.name in {'li', 'div', 'span', 'td', 'tr'}:
            score = 80 if tag.find('a', href=True) else 30
        elif tag.name in {'ul', 'ol'}:
            score = 60 if tag.find('a', href=True) else 25
        elif tag.name in {'h1', 'h2', 'h3', 'h4', 'h5', 'h6'}:
            if tag.find('a', href=True):
                score = 70
            else:
                score = 20
        elif tag.get('href'):
            score = 60
        selector_rank_totals[selector] += score
        # Add original preference score
        pref_score = get_selector_preference_score(tag, selector)
        selector_pref_totals[selector] += pref_score
    selector_ranking = {
        sel: selector_rank_totals[sel] / selector_counter[sel]
        for sel in selector_counter
    }
    selector_preference = {
        sel: selector_pref_totals[sel] / selector_counter[sel]
        for sel in selector_counter
    }
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
        print(f"{'Selector':<50} {'Rank':>7} {'Pref':>7} {'Freq':>7} {'Emoji':>7}")
        print('-' * 80)
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
            print(f"{sel:<50.50} {rank:>7.1f} {pref:>7.1f} {count:>7} {emoji:>7}")
        print('-' * 80)

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
    parser.add_argument('--auto-save', action='store_true', help='Automatically save results without prompting (useful for scripts)')
    parser.add_argument('--print', action='store_true', help='Print results to terminal (deprecated: results are now always shown)')
    parser.add_argument('--use-playwright', action='store_true', help='Use Playwright (headless browser) for scraping if bot protection is detected')
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    interactive_session = sys.stdin.isatty()
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
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:115.0) Gecko/20100101 Firefox/115.0",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1"
    ]
    for url in urls:
        notify(f"Fetching: {url}")
        response = None
        last_exception = None
        session = requests.Session()
        playwright_suggested = False
        playwright_used = False
        results = []
        html = None
        status_code = None
        suggest_ran = False
        extracted = False
        for idx, ua in enumerate(user_agents):
            headers = {
                "User-Agent": ua,
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.9",
                "Referer": url,
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1"
            }
            notify(f"Attempt {idx+1} with User-Agent: {ua}")
            try:
                response = session.get(url, headers=headers, timeout=15)
                notify(f"Status code: {response.status_code}")
                if response.status_code == 200:
                    status_code = response.status_code
                    break
                elif response.status_code == 403:
                    sent_headers = dict(headers)
                    resp_headers = dict(response.headers)
                    resp_body = response.text[:500]
                    notify(f"403 Forbidden with User-Agent {ua}.")
                    notify(f"Sent headers: {sent_headers}")
                    notify(f"Response headers: {resp_headers}")
                    notify(f"Response body (first 500 chars): {resp_body}")
                    suggestions = []
                    if any(k in resp_headers for k in ["CF-RAY", "Server", "Akamai", "X-Request-ID"]):
                        suggestions.append("Site uses advanced bot protection (Cloudflare/Akamai). Try a real browser (Playwright) or a residential proxy.")
                        playwright_suggested = True
                    if "Set-Cookie" in resp_headers:
                        suggestions.append("Site sets cookies. Try replaying cookies from a browser session or persisting session cookies.")
                    if "Access Denied" in resp_body or "Bot detected" in resp_body:
                        suggestions.append("Access Denied/Bot detected in response. Use a real browser or proxy.")
                        playwright_suggested = True
                    if "enable javascript" in resp_body.lower() or "captcha" in resp_body.lower():
                        suggestions.append("Site requires JavaScript or CAPTCHA. Use Playwright.")
                        playwright_suggested = True
                    if not suggestions:
                        suggestions.append("Try adding more headers (Origin, Cache-Control, Pragma, Accept-Encoding) or replaying cookies.")
                        notify(f"No actionable suggestions found. Retrying with next User-Agent...")
                        for s in suggestions:
                            print(f"[SUGGESTION] {s}")
                        print('')
                        continue  # Only retry if no actionable suggestions
                    else:
                        notify(f"Automated suggestions based on analysis:")
                        for s in suggestions:
                            print(f"[SUGGESTION] {s}")
                        print('')
                        # If Playwright is suggested and --use-playwright is set, ask user to confirm
                        if playwright_suggested or args.use_playwright:
                            use_playwright = args.use_playwright
                            if not use_playwright:
                                confirm = input("Bot protection detected. Would you like to try Playwright for this URL? (y/n): ").strip().lower()
                                use_playwright = confirm == 'y'
                            if use_playwright:
                                notify("Proceeding with Playwright...")
                                try:
                                    from playwright.sync_api import sync_playwright
                                    def fetch_with_playwright(target_url):
                                        with sync_playwright() as p:
                                            browser = p.chromium.launch(headless=True)
                                            page = browser.new_page()
                                            page.goto(target_url, timeout=30000)
                                            page_html = page.content()
                                            browser.close()
                                            return page_html
                                    html = fetch_with_playwright(url)
                                    playwright_used = True
                                    status_code = 200
                                    notify("Fetched page with Playwright. Proceeding to extract data...")
                                    if args.suggest:
                                        suggest_scrapables(html, top_n=args.suggest_top, max_depth=args.suggest_depth)
                                        suggest_ran = True
                                    notify(f"Parsing HTML and extracting with selector: {args.selector}")
                                    results = scrape_titles_and_links(html, args.selector)
                                    extracted = True
                                    notify(f"Extracted {len(results)} items.")
                                    response = None  # Prevent further retries
                                except Exception as e:
                                    notify(f"Playwright scraping failed: {e}")
                                break
                        break  # Stop retrying if actionable suggestions found
                else:
                    notify(f"Non-200/403 status code: {response.status_code}. Trying next User-Agent...")
            except requests.exceptions.RequestException as e:
                notify(f"Request failed with User-Agent {ua}: {e}")
                last_exception = e
                continue
        if response and response.status_code == 200:
            status_code = response.status_code
            html = response.text
        if status_code == 200 and html is not None:
            if args.suggest and not suggest_ran:
                suggest_scrapables(html, top_n=args.suggest_top, max_depth=args.suggest_depth)
                suggest_ran = True
            if not extracted:
                notify(f"Parsing HTML and extracting with selector: {args.selector}")
                results = scrape_titles_and_links(html, args.selector)
                extracted = True
                notify(f"Extracted {len(results)} items.")
            elif playwright_used:
                notify(f"Using Playwright results for selector: {args.selector}")
        elif response and response.status_code == 403:
            notify(f"Failed to fetch {url} (status code: 403 Forbidden) after trying all User-Agents.")
            # Automated header/body analysis for final suggestions
            resp_headers = dict(response.headers)
            resp_body = response.text[:500]
            suggestions = []
            if any(k in resp_headers for k in ["CF-RAY", "Server", "Akamai", "X-Request-ID"]):
                suggestions.append("Site uses advanced bot protection (Cloudflare/Akamai). Try a real browser (Selenium/Playwright) or a residential proxy.")
            if "Set-Cookie" in resp_headers:
                suggestions.append("Site sets cookies. Try replaying cookies from a browser session or persisting session cookies.")
            if "Access Denied" in resp_body or "Bot detected" in resp_body:
                suggestions.append("Access Denied/Bot detected in response. Use a real browser or proxy.")
            if "enable javascript" in resp_body.lower() or "captcha" in resp_body.lower():
                suggestions.append("Site requires JavaScript or CAPTCHA. Use Selenium/Playwright.")
            if not suggestions:
                suggestions.append("Try adding more headers (Origin, Cache-Control, Pragma, Accept-Encoding) or replaying cookies.")
            notify(f"Automated suggestions based on final analysis:")
            for s in suggestions:
                print(f"[SUGGESTION] {s}")
            print('')
        elif response:
            notify(f"Failed to fetch {url} (status code: {response.status_code}) after trying all User-Agents.")
        else:
            notify(f"All requests failed for {url}. Last exception: {last_exception}")
        # Always display results to the user
        notify(f"Scrape results for {url}:")
        print(json.dumps(results, indent=2))
        # Determine if results should be saved
        should_save = False
        if status_code == 200 and not args.no_save:
            if args.auto_save or not interactive_session:
                should_save = True
                if not interactive_session and not args.auto_save:
                    notify("Non-interactive session detected; auto-saving results.")
            else:
                prompt = input("Would you like to save these results to a file? (y/n): ").strip().lower()
                should_save = prompt in {'y', 'yes'}
        elif status_code == 200 and args.no_save:
            notify("Skipping save due to --no-save flag.")
        # Save to file if confirmed
        if should_save:
            output_file = OUTPUT_DIR / url_to_filename(url)
            with output_file.open("w", encoding="utf-8") as f:
                json.dump(results, f, indent=2)
            notify(f"Results saved to: {output_file}")
        elif status_code == 200 and not args.no_save:
            notify("Results were not saved.")
        # If no results were found, automatically suggest scrapable elements
        if status_code == 200 and not results and not args.suggest:
            notify("No results found with the current selector. Scanning for scrapable elements...")
            suggest_scrapables(html, top_n=args.suggest_top, max_depth=args.suggest_depth)
