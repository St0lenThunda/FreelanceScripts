"""
portfolio_generator_tool.py

A CLI tool to generate a personal project portfolio page or JSON data by scraping GitHub, Behance, or Dribbble links.

Features:
- Accepts multiple profile URLs
- Supports GitHub, Behance, and Dribbble
- Outputs Markdown or JSON format
- Ideal for freelancers showcasing their work
"""
# TODO: ouput to output directory and add platform, and timestamp to filename

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

def parse_github(html):
    # scrape selectors as of 06/10/2025
    soup = BeautifulSoup(html, 'html.parser')
    repos = []   
    
    primary_title_selector = "a:has(span.repo), a[itemprop$='codeRepository']"
    secondary_title_selector = "span.repo"
    
    
    for repo in soup.select(primary_title_selector):
        name = repo.select_one(secondary_title_selector)
        if not name:
            name = repo.text.strip()
        else:
            name = name.text.strip()
        href = repo['href']
        # Check for description using both selectors
        description = repo.find_next('p', class_='pinned-item-desc') or repo.find_next('p[itemprop$="description"]')
        description_text = description.text.strip() if description else "No description provided"
        repos.append({"title": name, "url": f"https://github.com{href}", "description": description_text})
    return  repos

def parse_behance(html):
    soup = BeautifulSoup(html, 'html.parser')
    projects = []
    for a in soup.select('div.ProjectCoverNeue-details-LLY > div.ProjectCoverNeue-info-paj > span > a'):
        title = a.text.strip()
        href = a['href']
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

def parse_dribbble(html):
    soup = BeautifulSoup(html, 'html.parser')
    shots = []
    for a in soup.select('a[data-testid="shot-thumbnail-link"]'):
        title = a.get('aria-label') or a.get('title') or "Untitled"
        href = a['href']
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
            'url': "https://www.behance.net/",  # Example URL for trending Behance projects
            'title_selector': 'div.ProjectCoverNeue-details-LLY > div.ProjectCoverNeue-info-paj > span > a',
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
    html = fetch_html(platform_config['url'])
    if not html:
        print(f"[!] Failed to fetch trending entries for {platform}.")
        return []

    soup = BeautifulSoup(html, 'html.parser')
    entries = []
    for item in soup.select(platform_config['title_selector']):
        if platform == 'github':
            name = item.text.strip() 
            title = name.split("/")[0] if '/' in name else title  # Get the first part before '/' eg. user/project
        else:
            title = item.text.strip()
        href = item['href']
        description = "No description provided"
        if platform_config['description_selector']:
            description_element = item.find_next(platform_config['description_selector'])
            description = description_element.text.strip() if description_element else description
        entries.append({"title": title, "url": f"{platform_config['base_url']}{href}", "description": description})
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
            # Extract the GitHub username from the URL
            username = url.split('github.com/')[-1].split('/')[0]
            print(f"[+] GitHub Username: {username}")
            entries = parse_github(html)
        elif platform == 'behance':
            # Extract the Behance username from the URL
            username = url.split('behance.net/')[-1].split('/')[0]
            print(f"[+] Behance Username: {username}")
            entries = parse_behance(html)
        elif platform == 'dribbble':
            # Extract the Dribbble username from the URL
            username = url.split('dribbble.com/')[-1].split('/')[0]
            print(f"[+] Dribbble Username: {username}")
            entries = parse_dribbble(html)
        else:
            print(f"[!] Unsupported platform for URL: {url}")
            continue

        collected.extend(entries)

    if fmt == 'json':
        with open(output_path, 'w') as f:  # Overwrite the file by default
            json.dump(collected, f, indent=2)
        print(f"[+] Portfolio data saved to {output_path}")
    else:
        with open(output_path, 'w') as f:  # Overwrite the file by default
            f.write(f"# {platform.capitalize()} Portfolio\n\n")
            f.write(f"__by {username}__\n\n")
            f.write("| Name | Description |\n")
            f.write("|------|-------------|\n")
            for entry in collected:
                f.write(f"| [{entry['title']}]({entry['url']}) | {entry.get('description', 'No description provided')} |\n")
        print(f"[+] Portfolio markdown saved to {output_path}")

# --- Entry Point ---

def main():
    parser = argparse.ArgumentParser(description="Generate a portfolio from profile links.")
    parser.add_argument('urls', nargs='*', help='List of GitHub/Behance/Dribbble URLs')
    parser.add_argument('--output', '-o', default='portfolio.md', help='Output file name')
    parser.add_argument('--format', '-f', choices=['md', 'json'], default='md', help='Output format')
    parser.add_argument('--platform', '-p', choices=['github', 'behance', 'dribbble'], default='github', help='Platform to use if no URLs are provided (default: github)')
    args = parser.parse_args()
    # TODO: Add more platforms like LinkedIn, Twitter, etc. in the 
    # TODO: Add trending options for each platform
    
    # Validate output file extension
    if not args.output.endswith(('.md', '.json')):
        print("[!] Output file must have a .md or .json extension.")
        return
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
    if output_file.exists() and not output_file.is_writable():
        print(f"[!] Output file {args.output} is not writable.")
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
    # Ensure the output file is not a named pipe
    if output_file.is_named_pipe():
        print(f"[!] Output path {args.output} is a named pipe, not a regular file.")
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
                f.write(f"# {args.platform.capitalize()} Trending Entries\n\n")
                f.write("| Name | Description |\n")
                f.write("|------|-------------|\n")
                for entry in trending_entries:
                    f.write(f"| [{entry['title']}]({entry['url']}) | {entry['description']} |\n")
            print(f"[+] Trending entries markdown saved to ./{args.output}")
        return

    generate_portfolio(args.urls, args.output, args.format)

if __name__ == '__main__':
    main()
