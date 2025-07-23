# 🗂️ Portfolio Generator Tool

> ## Purpose
> A CLI tool to generate a personal project portfolio page or JSON data by scraping GitHub, Behance, or Dribbble links.
>
> Features:
> - Accepts multiple profile URLs
> - Supports GitHub, Behance, and Dribbble
> - Outputs Markdown or JSON format
> - Ideal for freelancers showcasing their work

### Use Cases
- Build a markdown or JSON résumé.
- Provide GitHub summaries for clients.
- Automate portfolio creation for freelancers.
- Offer portfolio setup as a freelance service.

## 🚀 Usage

```bash
# Generate a markdown portfolio from GitHub
python portfolio_generator_tool.py --platform github --username yourhandle --format markdown --output my_portfolio.md
```

## Notes

- Ensure you have valid API keys or access tokens for platforms requiring authentication.
- The tool is designed for Unix-like systems (Linux, macOS, WSL).

## Concepts

This tool demonstrates several Pythonic concepts useful for beginners:

- **API Integration:** Fetches data from external platforms like GitHub, Behance, and Dribbble.
- **Data Transformation:** Converts raw API responses into structured JSON or markdown.
- **Interactive CLI:** Prompts users for missing arguments and provides helpful feedback.
- **Error Handling:** Gracefully handles API errors, invalid inputs, and network issues.

## License

MIT License. Use freely and modify as needed.
