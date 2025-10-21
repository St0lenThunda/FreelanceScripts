# 🌐 Web Scraper Tool

> ## Purpose
> A modular web scraper that fetches titles and links from one or more URLs (default: Hacker News).
>
> Key Features:
> - Fetches inner text and links of `<a>` elements inside `<span class="titleline">` (default selector).
> - Handles multiple URLs from command-line arguments or a file (--url-file).
> - Allows custom CSS selectors via --selector for flexible scraping of any site.
> - Can scan the page and suggest common tags, classes, ids, and nested selectors for scrapable elements (--suggest).
> - The number of top suggestions and the maximum selector depth are adjustable via --suggest-top and --suggest-depth.
> - Suggestion output is ranked using averaged link-likelihood, structural preference, and frequency, then annotated with a composite emoji system (🏆, 🥇, 🥈, 🥉, 🎖️, 🔸).
> - Only the top 5 selector suggestions show a composite emoji; the remaining rows list their averaged metrics without the emoji for clarity.
> - Automatically suggests scrapable elements if no results are found with the current selector.
> - Prints results to the console (with --print or --no-save) for easy chaining.
> - Saves results to a JSON file in the output directory (default behavior, can be disabled with --no-save).
> - Output files are named after the URL.
> - Designed as a learning resource: code is heavily commented and modular.
> - Optional Playwright fallback: pass --use-playwright to automatically launch a headless browser when bot protection is detected.
>
> TODO: Add colorized output for better readability.

### Use Cases
- Pull titles for blog digests.
- Extract data from forums or news sites.
- Automate content summaries for newsletters.
- Learn web scraping techniques for personal projects.

## 🚀 Usage

```bash
# Scrape one or more custom URLs
python scraper_tool.py https://news.ycombinator.com

# Scrape URLs from a file
python scraper_tool.py --url-file urls.txt

# Use a custom CSS selector (e.g., all links in a div with class 'headline')
python scraper_tool.py https://example.com --selector 'div.headline a'

# Print results to terminal (for chaining)
python scraper_tool.py https://example.com --print

# Only scan and suggest scrapable elements (no extraction)
python scraper_tool.py https://example.com --suggest

# Adjust number of top suggestions and selector depth
python scraper_tool.py https://example.com --suggest --suggest-top 20 --suggest-depth 3

# Disable saving to file
python scraper_tool.py https://example.com --no-save

# Force a headless-browser fetch when bot protection is likely
python scraper_tool.py https://example.com --use-playwright
```

## Notes

- Ensure the target website allows scraping and complies with its terms of service.
- The tool is designed for Unix-like systems (Linux, macOS, WSL).

## Concepts

This tool demonstrates several Pythonic concepts useful for beginners:

- **Web Scraping:** Uses libraries like `requests` and `BeautifulSoup` to fetch and parse HTML content.
- **Error Handling:** Gracefully handles failed requests and invalid selectors.
- **Data Storage:** Saves structured data to JSON files for easy reuse.
- **CLI Design:** Provides flexible command-line arguments for customization.

## License

MIT License. Use freely and modify as needed.

---
