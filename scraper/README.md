# 🌐 Simple Web Scraper
[← Back to Main README](../README.md)

> ## Purpose
>  A modular, educational web scraper for extracting titles and links from any website.
>  - Supports scraping one or many URLs (from the command line or a file).
>  - Lets you use any CSS selector to target elements for extraction.
>  - Can automatically analyze and suggest scrapable tags, classes, ids, and nested selectors if your selector yields no results.
>  - The number of top suggestions and the maximum selector depth are adjustable via `--suggest-top` and `--suggest-depth`.
>  - Suggestion output is ranked using a composite emoji system (🏆, 🥇, 🥈, 🥉, 🎖️, 🔸) that combines link-likelihood, structural preference, and frequency.
>  - Only the top 5 selector suggestions show detailed metrics and the composite emoji in a table; the rest show selector and count for clarity.
>  - Outputs results to the terminal or to JSON files named after each URL.
>  - Designed for learning: code is heavily commented and easy to extend.

## 🚀 Usage

```bash
usage: simple_scraper_tool.py [-h] [--url-file URL_FILE] [--selector SELECTOR] [--suggest] [--suggest-top SUGGEST_TOP] [--suggest-depth SUGGEST_DEPTH] [--no-save] [--print] [urls ...]

Scrape titles/links from provided URLs.

positional arguments:
  urls                 One or more URLs to scrape (default: Hacker News)

options:
  -h, --help           show this help message and exit
  --url-file URL_FILE  Path to a file containing newline-separated URLs to scrape
  --selector SELECTOR  CSS selector for elements to scrape (default: span.titleline a)
  --suggest            Scan the page and suggest scrapable tags/classes/ids and nested selectors
  --suggest-top SUGGEST_TOP   How many top tags/classes/ids/selectors to show (default: 10)
  --suggest-depth SUGGEST_DEPTH  Max depth for nested selector suggestions (default: 2)
  --no-save            Do not save results to file (only print to terminal)
  --print              Print results to terminal (default: off if saving to file)


# Scrape the default (Hacker News)
python simple_scraper_tool.py

# Scrape one or more custom URLs
python simple_scraper_tool.py https://news.ycombinator.com https://example.com

# Scrape URLs from a file
python simple_scraper_tool.py --url-file urls.txt

# Use a custom CSS selector (e.g., all links in a div with class 'headline')
python simple_scraper_tool.py https://example.com --selector 'div.headline a'

# Print results to terminal (for chaining)
python simple_scraper_tool.py https://example.com --print

# Only scan and suggest scrapable elements (no extraction)
python simple_scraper_tool.py https://example.com --suggest

# Adjust number of top suggestions and selector depth
python simple_scraper_tool.py https://example.com --suggest --suggest-top 20 --suggest-depth 3

# Disable saving to file
python simple_scraper_tool.py https://example.com --no-save
```

---

## 📤 Output Example

```json
[
  {
    "title": "Breaking News: AI Beats Humans at Chess",
    "url": "https://example.com/chess"
  },
  {
    "title": "How to Build a Web Scraper",
    "url": "https://example.com/scraper"
  },
  {
    "title": "Why Python is Great for Freelancers",
    "url": "https://example.com/python"
  }
]
```

---

## ⚙️ Features
- Modular: works with any site and selector
- Handles multiple URLs in one run (from CLI or file)
- Customizable output (print, save, or both)
- Suggests scrapable tags/classes/ids and nested selectors with `--suggest` or automatically if no results are found
- Number of top suggestions and selector depth are adjustable via `--suggest-top` and `--suggest-depth`
- Output files are named after the URL and saved in the `output/` directory
- Designed as a learning resource: code is heavily commented and modular

---

## 📜 License

MIT — grab and go.

---
[← Back to Main README](../README.md)