# 🌐 Simple Web Scraper
[← Back to Main README](../README.md)

> ## Purpose
> A modular web scraper that fetches titles and links from one or more URLs (default: Hacker News).
>
> Key Features:
> - Fetches inner text and links of `<a>` elements inside `<span class="titleline">` (default selector).
> - Handles multiple URLs from command-line arguments or a file (--url-file).
> - Allows custom CSS selectors via --selector for flexible scraping of any site.
> - Can scan the page and suggest common tags, classes, ids, and nested selectors for scrapable elements (--suggest).
> - The number of top suggestions and the maximum selector depth are adjustable via --suggest-top and --suggest-depth.
> - Suggestion output is ranked using a composite emoji system (🏆, 🥇, 🥈, 🥉, 🎖️, 🔸) that combines link-likelihood, structural preference, and frequency.
> - Only the top 5 selector suggestions show detailed metrics and the composite emoji; the rest show selector and count for clarity.
> - Automatically suggests scrapable elements if no results are found with the current selector.
> - Prints results to the console (with --print or --no-save) for easy chaining.
> - Saves results to a JSON file in the output directory (default behavior, can be disabled with --no-save).
> - Output files are named after the URL.
> - Designed as a learning resource: code is heavily commented and modular.
>
> TODO: Add colorized output for better readability.
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

## Concepts

This tool demonstrates several Pythonic concepts useful for beginners:

- **Web Scraping:** Uses `requests` and `BeautifulSoup` for HTTP requests and HTML parsing.
- **Selector Suggestion and Ranking:** Analyzes HTML structure to suggest and rank CSS selectors.
- **Table Output:** Formats results as Markdown tables for readability.
- **Modularity:** Organizes code into functions for clarity and reuse.
- **Argument Parsing:** Handles command-line arguments for flexible usage.
- **Error Handling:** Provides robust error messages and suggestions.
- **Educational Comments:** Explains each step for learning purposes.

## 📜 License

MIT — grab and go.

---
[← Back to Main README](../README.md)