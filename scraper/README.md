# 🌐 Simple Web Scraper
[← Back to Main README](../README.md)

> ## Purpose
>  Fetch all titles from [Hacker News](https://news.ycombinator.com
). Fetches inner text and links of  `<a>` elements inside `<span class="titleline">`.

## 🚀 Usage

```bash
# Interactive mode
python simple_scraper_tool.py

# Explicit scrape
python simple_scraper_tool.py https://news.ycombinator.com

# Custom output file
python simple_scraper_tool.py https://example.com my_headlines.json
```

---

## 📤 Output Example

```json
[
  {
    "title": "Breaking News: AI Beats Humans at Chess",
    "link": "https://example.com/chess"
  },
  {
    "title": "How to Build a Web Scraper",
    "link": "https://example.com/scraper"
  },
  {
    "title": "Why Python is Great for Freelancers",
    "link": "https://example.com/python"
  }
]
```

---

## 🔧 Upcoming Features

* Selector override (`--selector`)
* Support for text/CSV output
* Bulk scraping from a list of URLs

---

## 📜 License

MIT — grab and go.

---
[← Back to Main README](../README.md)