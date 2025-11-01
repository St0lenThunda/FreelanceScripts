import subprocess
import json
from pathlib import Path

def test_scrape_valid_url(tmp_path):
    """Test scraping a valid URL."""
    # Using a known static page for testing
    url = "https://httpbin.org/html"
    result = subprocess.run(["python3", "scraper/scraper_tool.py", url, "--selector", "h1", "--auto-save"], capture_output=True, text=True)
    assert result.returncode == 0
    output_file = Path("output/httpbin_org_html.json")
    assert output_file.exists()
    with open(output_file, 'r') as f:
        data = json.load(f)
    assert len(data) > 0
    assert data[0]["title"] == "Herman Melville - Moby-Dick"
    output_file.unlink()

def test_scrape_non_existent_url():
    """Test scraping a non-existent URL."""
    url = "https://nonexistent.url.xyz"
    result = subprocess.run(["python3", "scraper/scraper_tool.py", url], capture_output=True, text=True)
    assert result.returncode == 0
    assert "name or service not known" in result.stdout.lower()

def test_scrape_with_custom_selector(tmp_path):
    """Test scraping with a custom selector."""
    # Using a known static page for testing
    url = "https://httpbin.org/html"
    result = subprocess.run(["python3", "scraper/scraper_tool.py", url, "--selector", "h1", "--auto-save"], capture_output=True, text=True)
    assert result.returncode == 0
    output_file = Path("output/httpbin_org_html.json")
    assert output_file.exists()
    with open(output_file, 'r') as f:
        data = json.load(f)
    assert len(data) > 0
    assert data[0]["title"] == "Herman Melville - Moby-Dick"
    output_file.unlink()

def test_suggest_selectors():
    """Test suggesting selectors."""
    # Using a known static page for testing
    url = "https://httpbin.org/html"
    result = subprocess.run(["python3", "scraper/scraper_tool.py", url, "--suggest"], capture_output=True, text=True)
    assert result.returncode == 0
    assert "[info] tag summary" in result.stdout.lower()