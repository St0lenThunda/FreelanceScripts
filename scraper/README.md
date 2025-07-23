# 🌐 Simple Web Scraper

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

### Use Cases
- Pull titles for blog digests.
- Extract data from forums or news sites.
- Automate content summaries for newsletters.
- Learn web scraping techniques for personal projects.

## 🚀 Usage

```bash
# Scrape one or more custom URLs
python simple_scraper_tool.py --url https://news.ycombinator.com

# Scrape URLs from a file
python simple_scraper_tool.py --url-file urls.txt

# Use a custom CSS selector (e.g., all links in a div with class 'headline')
python simple_scraper_tool.py --url https://example.com --selector 'div.headline a'

# Print results to terminal (for chaining)
python simple_scraper_tool.py --url https://example.com --print

# Only scan and suggest scrapable elements (no extraction)
python simple_scraper_tool.py --url https://example.com --suggest

# Adjust number of top suggestions and selector depth
python simple_scraper_tool.py --url https://example.com --suggest --suggest-top 20 --suggest-depth 3

# Disable saving to file
python simple_scraper_tool.py --url https://example.com --no-save
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