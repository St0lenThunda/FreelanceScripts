import unittest

SCRAPER_IMPORT_ERROR = None

try:
    from bs4 import BeautifulSoup  # noqa: F401
    from scraper.scraper_tool import (
        url_to_filename,
        split_selector_tokens,
        selector_has_list_ancestor,
        get_selector_counters_and_ranking,
        scrape_titles_and_links,
    )
except ModuleNotFoundError as exc:  # pragma: no cover - dependency missing
    SCRAPER_IMPORT_ERROR = exc


@unittest.skipIf(
    SCRAPER_IMPORT_ERROR is not None,
    reason=f"scraper_tool dependencies missing: {SCRAPER_IMPORT_ERROR}",
)
class TestScraperToolHelpers(unittest.TestCase):
    def test_url_to_filename_appends_json_and_sanitizes(self):
        filename = url_to_filename("https://news.ycombinator.com/item?id=12345")
        self.assertEqual(filename, "news_ycombinator_com_item.json")

    def test_split_selector_tokens(self):
        tokens = split_selector_tokens("ul.nav > li.item.active > a.link#cta")
        self.assertEqual(tokens, ["ul", "li", "a"])

    def test_selector_has_list_ancestor(self):
        self.assertTrue(selector_has_list_ancestor("ul.nav > li.item > a.link"))
        self.assertFalse(selector_has_list_ancestor("div.gallery > span.caption"))

    def test_scrape_titles_and_links_default_selector(self):
        html = """
        <html><body>
            <span class="titleline">
                <a href="https://example.com/1">Example One</a>
            </span>
            <span class="titleline">
                <a href="https://example.com/2">Example Two</a>
            </span>
        </body></html>
        """
        results = scrape_titles_and_links(html)
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]["title"], "Example One")
        self.assertEqual(results[1]["url"], "https://example.com/2")

    def test_get_selector_counters_and_ranking_averages_scores(self):
        html = """
        <html><body>
            <div class="cards">
                <div class="card">
                    <a href="https://example.com/card-1">Card One</a>
                </div>
                <div class="card">
                    <span>No link here</span>
                </div>
            </div>
            <ul class="items">
                <li class="item"><a href="https://example.com/list-1">List One</a></li>
                <li class="item"><a href="https://example.com/list-2">List Two</a></li>
            </ul>
        </body></html>
        """
        soup = BeautifulSoup(html, "html.parser")
        selector_counter, selector_ranking, selector_preference = get_selector_counters_and_ranking(
            soup, max_depth=2
        )

        # Ensure counters tracked each selector occurrence
        self.assertEqual(selector_counter["div.cards > div.card"], 2)
        self.assertEqual(selector_counter["li.item > a"], 2)

        # Ranking should average scores across all occurrences
        self.assertAlmostEqual(selector_ranking["div.cards > div.card"], 55.0)
        self.assertAlmostEqual(selector_ranking["li.item > a"], 100.0)

        # Preference scores should reflect averaged list-aware weighting
        self.assertAlmostEqual(selector_preference["li.item > a"], 4.0)
        self.assertAlmostEqual(selector_preference["div.cards > div.card"], 0.0)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
