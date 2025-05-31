# 🌐 Simple Web Scraper
[← Back to Main README](../README.md)

> ## Purpose
>  Fetch titles and links from one or more URLs (default: [Hacker News](https://news.ycombinator.com)).
>  By default, fetches inner text and links of `<a>` elements inside `<span class="titleline">`, but you can use any CSS selector.

## 🚀 Usage


```bash
usage: simple_scraper_tool.py [-h] [--selector SELECTOR] [--suggest] [--no-save] [--print] [urls ...]

Scrape titles/links from provided URLs.

positional arguments:
  urls                 One or more URLs to scrape (default: Hacker News)

options:
  -h, --help           show this help message and exit
  --selector SELECTOR  CSS selector for elements to scrape (default: span.titleline a)
  --suggest            Scan the page and suggest scrapable tags/classes/ids
  --no-save            Do not save results to file (only print to terminal)
  --print              Print results to terminal (default: off if saving to file)


# Scrape the default (Hacker News)
python simple_scraper_tool.py

# Scrape one or more custom URLs
python simple_scraper_tool.py https://news.ycombinator.com https://example.com

# Use a custom CSS selector (e.g., all links in a div with class 'headline')
python simple_scraper_tool.py https://example.com --selector 'div.headline a'

# Print results to terminal (for chaining)
python simple_scraper_tool.py https://example.com --print

# Only scan and suggest scrapable elements (no extraction)
python simple_scraper_tool.py https://example.com --suggest

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
- Handles multiple URLs in one run
- Customizable output (print, save, or both)
- Suggests scrapable tags/classes/ids with `--suggest`
- Output files are named after the URL and saved in the `output/` directory
- Designed as a learning resource: code is heavily commented and modular

---

## 📜 License

MIT — grab and go.

---
[← Back to Main README](../README.md)