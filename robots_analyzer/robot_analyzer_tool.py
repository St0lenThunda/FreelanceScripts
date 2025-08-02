#!/usr/bin/env python3
"""
robot_analyzer_tool.py

Fetches and analyzes the /robots.txt file for a given URL, then produces a human-readable report of allowed/disallowed paths, user-agents, and crawl-delay rules.

Usage:
    python robot_analyzer_tool.py <url>
"""

import sys
import requests
from urllib.parse import urlparse, urljoin

def fetch_robots_txt(url):
    parsed = urlparse(url)
    robots_url = urljoin(f"{parsed.scheme}://{parsed.netloc}", "/robots.txt")
    print(f"[INFO] Fetching: {robots_url}")
    try:
        resp = requests.get(robots_url, timeout=10)
        if resp.status_code == 200:
            return resp.text
        else:
            print(f"[ERROR] Could not fetch robots.txt (status: {resp.status_code})")
            return None
    except Exception as e:
        print(f"[ERROR] Exception fetching robots.txt: {e}")
        return None

def parse_robots_txt(text):
    rules = []
    current_agent = None
    sitemaps = []
    hosts = []
    request_rates = []
    clean_params = []
    comments = []
    nonstandard = []
    for line in text.splitlines():
        orig_line = line
        line = line.strip()
        if not line:
            continue
        if line.startswith('#'):
            comments.append(line)
            continue
        lcline = line.lower()
        if lcline.startswith('user-agent:'):
            current_agent = line.split(':',1)[1].strip()
            rules.append({'User-agent': current_agent, 'Allow': [], 'Disallow': [], 'Crawl-delay': None, 'Request-rate': None, 'Clean-param': []})
        elif lcline.startswith('allow:') and current_agent:
            rules[-1]['Allow'].append(line.split(':',1)[1].strip())
        elif lcline.startswith('disallow:') and current_agent:
            rules[-1]['Disallow'].append(line.split(':',1)[1].strip())
        elif lcline.startswith('crawl-delay:') and current_agent:
            rules[-1]['Crawl-delay'] = line.split(':',1)[1].strip()
        elif lcline.startswith('request-rate:') and current_agent:
            rules[-1]['Request-rate'] = line.split(':',1)[1].strip()
            request_rates.append(line.split(':',1)[1].strip())
        elif lcline.startswith('clean-param:') and current_agent:
            rules[-1]['Clean-param'].append(line.split(':',1)[1].strip())
            clean_params.append(line.split(':',1)[1].strip())
        elif lcline.startswith('sitemap:'):
            sitemaps.append(line.split(':',1)[1].strip())
        elif lcline.startswith('host:'):
            hosts.append(line.split(':',1)[1].strip())
        elif lcline.startswith('noindex') or lcline.startswith('nofollow'):
            nonstandard.append(line)
    return rules, sitemaps, hosts, request_rates, clean_params, comments, nonstandard

def generate_report(rules, sitemaps, hosts, request_rates, clean_params, comments, nonstandard):
    if not rules:
        return "No robots.txt rules found."
    report = []
    # 1. Summary Section
    report.append("# ROBOTS.TXT SCRAPING GUIDANCE\n")
    user_agents = [r['User-agent'] for r in rules]
    if '*' in user_agents:
        recommended_agent = '*'
    else:
        recommended_agent = user_agents[0] if user_agents else None
    report.append(f"Recommended User-agent for scraping: '{recommended_agent}'\n")
    # Find the rule for the recommended agent
    rule = None
    for r in rules:
        if r['User-agent'] == recommended_agent:
            rule = r
            break
    if rule:
        allowed = rule['Allow'] if rule['Allow'] else ['(none specified)']
        disallowed = rule['Disallow'] if rule['Disallow'] else ['(none specified)']
        crawl_delay = rule.get('Crawl-delay')
        request_rate = rule.get('Request-rate')
        report.append("Allowed paths:")
        for path in allowed:
            report.append(f"  - {path}")
        report.append("Disallowed paths:")
        for path in disallowed:
            report.append(f"  - {path}")
        if crawl_delay:
            report.append(f"Crawl-delay: {crawl_delay} seconds (wait this long between requests)")
        if request_rate:
            report.append(f"Request-rate: {request_rate}")
        if rule.get('Clean-param'):
            for cp in rule['Clean-param']:
                report.append(f"Clean-param: {cp}")
    report.append("")
    # 2. Sitemaps and Hosts
    if sitemaps:
        report.append("Sitemaps:")
        for s in sitemaps:
            report.append(f"  - {s}")
        report.append("")
    if hosts:
        report.append("Host directives:")
        for h in hosts:
            report.append(f"  - {h}")
        report.append("")
    # 3. Non-standard directives
    if nonstandard:
        report.append("Non-standard directives:")
        for n in nonstandard:
            report.append(f"  {n}")
        report.append("")
    # 4. Comments
    if comments:
        report.append("# Comments found in robots.txt:")
        for c in comments:
            report.append(f"  {c}")
        report.append("")
    # 5. Scraping Tips
    report.append("# Scraping Tips based on robots.txt:")
    if crawl_delay:
        report.append(f"- Respect the crawl-delay of {crawl_delay} seconds between requests.")
    else:
        report.append("- No crawl-delay specified; use a reasonable delay (e.g., 1-2 seconds) to avoid blocking.")
    if disallowed and disallowed != ['(none specified)']:
        report.append("- Do NOT scrape disallowed paths listed above.")
    else:
        report.append("- No disallowed paths; scraping is broadly permitted.")
    if allowed and allowed != ['(none specified)']:
        report.append("- Focus scraping on allowed paths for best compliance.")
    if nonstandard:
        report.append("- Non-standard directives found; review them for additional restrictions.")
    if sitemaps:
        report.append("- Sitemaps may help you discover content to scrape.")
    report.append("- Always identify your bot with a User-Agent string and follow site policies.")
    report.append("")
    return '\n'.join(report)

def main():
    if len(sys.argv) < 2:
        print("Usage: python robot_analyzer_tool.py <url>")
        sys.exit(1)
    url = sys.argv[1]
    robots_txt = fetch_robots_txt(url)
    if not robots_txt:
        print("No robots.txt found or could not fetch.")
        sys.exit(1)
    rules, sitemaps, hosts, request_rates, clean_params, comments, nonstandard = parse_robots_txt(robots_txt)
    report = generate_report(rules, sitemaps, hosts, request_rates, clean_params, comments, nonstandard)
    print("\n--- ROBOTS.TXT ANALYSIS REPORT ---\n")
    print(report)

if __name__ == "__main__":
    main()
