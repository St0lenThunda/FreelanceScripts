# 🪛 Scraper Debug Demo Tool

[← Back to Main README](../README.md)

> ## Demo - Purpose
>This tool demonstrates a real-world debugging and refactoring process taken from the `scraper/simple_scraper_tool.py`. It includes both a **broken** and a **fixed** version of the scraper to illustrate how problems were identified and solved in a freelance-style workflow.

---

## 🐛🔍 Buggy Version: `scraper_buggy_tool.py`

- Scrapes only generic `<h2>` tags — often misses real content
- No error handling — crashes on failed requests
- Just prints to terminal — not reusable
- Ignores article links

---

## ✅ Fixes in `scraper_bugfix_tool.py`

- Targeted correct selector: `span.titleline a`
- Captured structured data: `{"title", "link"}`
- Used `urljoin()` to resolve relative URLs
- Added proper logging and error handling
- Gracefully handles failed requests and keyboard interrupts
- Writes results to `output/<domain>_titles.json`

---

## 🧪 Run

```bash
python scraper_bugfix_tool.py
```



### 💥 Output Example:
```

Traceback (most recent call last):
...
KeyError: 'href'

````

---


### 🧪 To Run:

__Buggy (print-only, no links, no fallback)__
`python scraper_buggy_tool.py`

__Fixed (structured output + logging + links)__
`python scraper_bugfix_tool.py https://news.ycombinator.com
`

---

## 📤 Output Example (from `bugfix_tool.py`)

```json
[
  {
    "title": "Show HN: My open-source AI assistant",
    "link": "https://news.ycombinator.com/item?id=123456"
  },
  ...
]
```

---

## 🎯 What This Demonstrates

* Real debugging experience, not hypothetical bugs
* Progressive enhancement: error handling, structured data, usability
* Typical client workflow: "It’s kinda broken, make it better."

---

## 📜 License

MIT — use to demonstrate your debugging expertise.

---
[← Back to Main README](../README.md)