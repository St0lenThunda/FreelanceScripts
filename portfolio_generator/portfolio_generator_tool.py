"""
portfolio_generator_tool.py

A CLI tool to generate a personal project portfolio page or JSON data by scraping GitHub, Behance, or Dribbble profiles, or by fetching trending projects from these platforms.

Features:
- Accepts multiple profile URLs for GitHub, Behance, and Dribbble
- Can fetch and parse trending projects for github by default; other supported platform to come
- Outputs Markdown or JSON format, with automatic file extension inference
- Robust selector logic and error handling for scraping
- Ideal for freelancers and creators showcasing their work
- Extensible for additional platforms (e.g., LinkedIn, Twitter) in the future
"""

import argparse
import json
import re
from pathlib import Path
from bs4 import BeautifulSoup
import requests

# --- Helpers ---

def fetch_html(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"[!] Error fetching {url}: {e}")
        return None

def parse_github(html, title_selector_override=None, description_selector_override=None):
    # scrape selectors as of 06/10/2025
    soup = BeautifulSoup(html, 'html.parser')
    repos = []   
    primary_title_selector = title_selector_override or "a:has(span.repo), a[itemprop$='codeRepository']"
    secondary_title_selector = "span.repo"
    for repo in soup.select(primary_title_selector):
        name = repo.select_one(secondary_title_selector)
        if not name:
            name = repo.text.strip()
        else:
            name = name.text.strip()
        # If name contains '/', remove all extra spaces and newlines
        if '/' in name:
            name = name.replace('\n', '').replace('\r', '').replace(' ', '')
        
        href = repo['href']
        # Use description selector override if provided
        if description_selector_override:
            description = repo.find_next(description_selector_override)
        else:
            description = repo.find_next('p', class_='pinned-item-desc') or repo.find_next('p[itemprop$="description"]')
        description_text = description.text.strip() if description else "No description provided"
        repos.append({"title": name, "url": f"https://github.com{href}", "description": description_text})
    return  repos

def parse_behance(html, title_selector_override=None, description_selector_override=None):
    soup = BeautifulSoup(html, 'html.parser')
    projects = []
    selector = title_selector_override or 'div.ProjectCoverNeue-details-LLY > div.ProjectCoverNeue-info-paj > span > a'
    
    for a in soup.select(selector):
        title = a.text.strip()
        href = a['href']
        # Use description selector override if provided
        if description_selector_override:
            stats = a.find_next(description_selector_override)
        else:
            stats = a.find_next('div', class_='Stats-stats-Q1s')
        if stats:
            spans = stats.find_all('span')
            likes = spans[0].text.strip() if len(spans) > 0 else "0"
            watchers = spans[1].text.strip() if len(spans) > 1 else "0"
        else:
            likes = "0"
            watchers = "0"
        description = f"❤️ {likes} Likes | 👀 {watchers} Watchers"
        projects.append({"title": title, "url": f"https://behance.net{href}", "description": description})
    return projects

def parse_dribbble(html, title_selector_override=None, description_selector_override=None):
    soup = BeautifulSoup(html, 'html.parser')
    selector = title_selector_override or 'a[data-testid="shot-thumbnail-link"]'
    shots = []
    for a in soup.select(selector):
        title = a.get('aria-label') or a.get('title') or "Untitled"
        href = a['href']
        # Dribbble doesn't use description selector override, but could be extended here if needed
        shots.append({"title": title, "url": f"https://dribbble.com{href}"})
    return shots

def detect_platform(url):
    if 'github.com' in url:
        return 'github'
    elif 'behance.net' in url:
        return 'behance'
    elif 'dribbble.com' in url:
        return 'dribbble'
    return None

def extract_json_from_script(html, key_hint=None, pretty=False):
    """
    Looks for <script> tags containing JSON data. Optionally filter by a key_hint string.
    Returns a list of parsed JSON objects found in script tags.
    If pretty=True, returns pretty-printed JSON strings instead of objects.
    """
    import json as _json
    soup = BeautifulSoup(html, 'html.parser')
    found = []
    for script in soup.find_all('script'):
        script_text = script.string or script.text or ''
        # Heuristic: look for JSON-like content
        if '{' in script_text and '}' in script_text:
            # Optionally filter by key_hint
            if key_hint and key_hint not in script_text:
                continue
            try:
                # Try to extract the first JSON object in the script
                start = script_text.find('{')
                end = script_text.rfind('}') + 1
                json_candidate = script_text[start:end]
                data = _json.loads(json_candidate)
                if pretty:
                    found.append(_json.dumps(data, indent=2, ensure_ascii=False))
                else:
                    found.append(data)
            except Exception as e:
                # Not valid JSON, skip
                continue
    return found

def fetch_trending_entries(platform):
    config = {
        'github': {
            'url': "https://github.com/trending",
            # scrape selectors as of 06/10/2025
            'title_selector': "h2 a[data-hydro-click*='REPOSITORY']",
            'description_selector': 'p',
            'base_url': "https://github.com"
        },
        'behance': {
            'url': "https://www.behance.net/galleries/best-of-behance",  # Example URL for trending Behance projects
            'title_selector': 'a.Owners-owner-EEG',
            'description_selector': 'div.Stats-stats-Q1s',
            'base_url': "https://behance.net"
        },
        'dribbble': {
            'url': "https://dribbble.com/shots/popular",  # Example URL for trending Dribbble shots
            'title_selector': 'a[data-testid="shot-thumbnail-link"]',
            'description_selector': None,  # Dribbble might not have a description selector
            'base_url': "https://dribbble.com"
        }
    }

    if platform not in config:
        print(f"[!] Unsupported platform: {platform}")
        return []

    platform_config = config[platform]
    print(f"[DEBUG] Fetching trending for platform: {platform}")
    print(f"[DEBUG] URL: {platform_config['url']}")
    print(f"[DEBUG] Title selector: {platform_config['title_selector']}")
    print(f"[DEBUG] Description selector: {platform_config.get('description_selector')}")
    html = fetch_html(platform_config['url'])
    if not html:
        print(f"[!] Failed to fetch trending entries for {platform}.")
        return []
    print(f"[DEBUG] HTML fetched, length: {len(html)}")

    # Print pretty JSON for each found script block
    # json_blocks = extract_json_from_script(html, pretty=True)
    # if json_blocks:
    #     print("[DEBUG] JSON blocks found in <script> tags:")
    #     for i, block in enumerate(json_blocks):
    #         print(f"[DEBUG] JSON block {i+1}:")
    #         print(block)
    # else:
    #     print("[DEBUG] No JSON blocks found in <script> tags.")

    # Check for presence of title and description selectors in the HTML
    soup = BeautifulSoup(html, 'html.parser')
    title_selector = platform_config.get('title_selector')
    description_selector = platform_config.get('description_selector')
    if title_selector and not soup.select(title_selector):
        print(f"[!] Title selector '{title_selector}' not found in HTML for {platform}. Aborting parse.")
        return []
    if description_selector and not soup.select(description_selector):
        print(f"[!] Description selector '{description_selector}' not found in HTML for {platform}. Descriptions may be missing or incorrect.")

    # Use the appropriate parser with the trending selector and description selector override
    if platform == 'github':
        entries = parse_github(html, title_selector_override=title_selector, description_selector_override=description_selector)
    elif platform == 'behance':
        entries = parse_behance(html, title_selector_override=title_selector, description_selector_override=description_selector)
    elif platform == 'dribbble':
        entries = parse_dribbble(html, title_selector_override=title_selector, description_selector_override=description_selector)
    else:
        print(f"[!] No parser for platform: {platform}")
        return []

    print(f"[DEBUG] Entries found: {len(entries)}")
    if not entries:
        print(f"[!] No entries parsed for {platform}. Possible selector mismatch or page structure change.")
    else:
        print(f"[DEBUG] Entry Preview")
        for i, entry in enumerate(entries[:3]):
            
            print(f"[DEBUG] Entry {i+1}: {entry}")
    return entries



# --- Main Logic ---

def generate_portfolio(urls, output_path, fmt):
    collected = []
    for url in urls:
        html = fetch_html(url)
        if not html:
            continue

        platform = detect_platform(url)  # Infer platform from the URL
        if platform == 'github':
            # Extract the GitHub Context from the URL
            Context = url.split('github.com/')[-1].split('/')[0]
            print(f"[+] GitHub Context: {Context}")
            entries = parse_github(html)
            
        elif platform == 'behance':
            # Extract the Behance Context from the URL
            Context = url.split('behance.net/')[-1].split('/')[0]
            print(f"[+] Behance Context: {Context}")
            # TODO: retreive dynamic data using webdriver
            # DOES NOT WORK RN
            entries = parse_behance(html)
        elif platform == 'dribbble':
            # Extract the Dribbble Context from the URL
            Context = url.split('dribbble.com/')[-1].split('/')[0]
            print(f"[+] Dribbble Context: {Context}")
            entries = parse_dribbble(html)
        else:
            print(f"[!] Unsupported platform for URL: {url}")
            continue
  
        print(f"[DEBUG] Entries found: {len(entries)}")
  
        collected.extend(entries)

    if fmt == 'json':
        with open(output_path, 'w') as f:  # Overwrite the file by default
            json.dump(collected, f, indent=2)
        print(f"[+] Portfolio data saved to {output_path}")
    else:
        with open(output_path, 'w') as f:  # Overwrite the file by default
            f.write(f"# {platform.capitalize()} Portfolio\n\n")
            f.write(f"__by {Context}__\n\n")
            f.write("| Name | Description |\n")
            f.write("|------|-------------|\n")
            for entry in collected:
                f.write(f"| [{entry['title']}]({entry['url']}) | {entry.get('description', 'No description provided')} |\n")
        print(f"[+] Portfolio markdown saved to {output_path}")

# --- Entry Point ---

def main():
    parser = argparse.ArgumentParser(description="Generate a portfolio from profile links.")
    parser.add_argument('urls', nargs='*', help='List of GitHub/Behance/Dribbble URLs')
    parser.add_argument('--output', '-o', default='./portfolio', help='Output file name')
    parser.add_argument('--format', '-f', choices=['md', 'json'], default='md', help='Output format')
    parser.add_argument('--platform', '-p', choices=['github', 'behance', 'dribbble'], default='github', help='Platform to use if no URLs are provided (default: github)')
    args = parser.parse_args()
    # TODO: Add more platforms like LinkedIn, Twitter, etc. in the 
    # TODO: Add trending options for each platform
    
    # Validate output file extension
    if not args.output.endswith(('.md', '.json')):
        if args.format == 'json':
            args.output += '.json'
            print(f"[+] Output file extension inferred as .json: {args.output}")
        else:
            # Default to Markdown if no format is specified
            args.output += '.md'
            print(f"[+] Output file extension inferred as .md: {args.output}")
    # Ensure the output directory exists
    output_dir = Path(args.output).parent
    if not output_dir.exists():
        output_dir.mkdir(parents=True, exist_ok=True)
        print(f"[+] Created output directory: {output_dir}")
    else:
        print(f"[+] Output directory already exists: {output_dir}")
    # Ensure the output file is writable
    output_file = Path(args.output)
    if output_file.exists() and not output_file.is_file():
        print(f"[!] Output path {args.output} is not a file.")
        return
    if args.format == 'json':
        if not args.output.endswith('.json'):
            print("[!] Output file must have a .json extension for JSON format.")
            return
    elif args.format == 'md':           
        if not args.output.endswith('.md'):
            print("[!] Output file must have a .md extension for Markdown format.")
            return
    # Ensure the output file is not empty
    if output_file.exists() and output_file.stat().st_size == 0:
        print(f"[!] Output file {args.output} is empty. It will be overwritten.")
    else:
        print(f"[+] Output file {args.output} is ready for writing.")
    # Ensure the output file is not a directory
    if output_file.is_dir():
        print(f"[!] Output path {args.output} is a directory, not a file.")
        return
    # Ensure the output file is not a symlink
    if output_file.is_symlink():
        print(f"[!] Output path {args.output} is a symlink, not a regular file.")
        return
    # Ensure the output file is not a special file
    if output_file.is_socket() or output_file.is_fifo():
        print(f"[!] Output path {args.output} is a special file (socket or FIFO), not a regular file.")
        return
    # Ensure the output file is not a device file
    if output_file.is_block_device() or output_file.is_char_device():
        print(f"[!] Output path {args.output} is a device file, not a regular file.")
        return
    # Ensure the output file is not a socket
    if output_file.is_socket():
        print(f"[!] Output path {args.output} is a socket, not a regular file.")
        return  
    
    # Fetch trending entries if no URLs are provided
    if not args.urls:
        print(f"Fetching trending entries for {args.platform}...")
        trending_entries = fetch_trending_entries(args.platform)
        if args.format == 'json':
            with open(args.output, 'w') as f:
                json.dump(trending_entries, f, indent=2)
            print(f"[+] Trending entries saved to {args.output}")
        else:
            with open(args.output, 'w') as f:
                f.write(f"# {args.platform.capitalize()} Trending Projects\n\n")
                f.write("| Name | Description |\n")
                f.write("|------|-------------|\n")
                for entry in trending_entries:
                    f.write(f"| [{entry['title']}]({entry['url']}) | {entry['description']} |\n")
            print(f"[+] Trending entries markdown saved to ./{args.output}")
        return

    generate_portfolio(args.urls, args.output, args.format)

if __name__ == '__main__':
    main()
