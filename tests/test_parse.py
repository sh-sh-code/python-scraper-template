"""Tests for scraper.parse — HTML → dict list."""

from scraper.parse import parse_items, _safe_int

# Minimal HN-style HTML fixture
SAMPLE_HTML = """
<html><body>
<table>
  <tr class="athing" id="41000001">
    <td align="right" valign="top" class="title">
      <span class="rank">1.</span>
    </td>
    <td class="title">
      <span class="titleline">
        <a href="https://example.com/post-one">First Post Title</a>
        <span class="sitestr">example.com</span>
      </span>
    </td>
  </tr>
  <tr>
    <td colspan="2"></td>
    <td class="subtext">
      <span class="score" id="score_41000001">256 points</span>
      by alice
      <a href="item?id=41000001">103&nbsp;comments</a>
    </td>
  </tr>

  <tr class="athing" id="41000002">
    <td align="right" valign="top" class="title">
      <span class="rank">2.</span>
    </td>
    <td class="title">
      <span class="titleline">
        <a href="https://example.org/post-two">Second Post Title</a>
      </span>
    </td>
  </tr>
  <tr>
    <td colspan="2"></td>
    <td class="subtext">
      <span class="score" id="score_41000002">72 points</span>
      by bob
      <a href="item?id=41000002">18&nbsp;comments</a>
    </td>
  </tr>

  <tr class="athing" id="41000003">
    <td align="right" valign="top" class="title">
      <span class="rank">3.</span>
    </td>
    <td class="title">
      <span class="titleline">
        <a href="https://example.net/post-three">Third Post</a>
      </span>
    </td>
  </tr>
  <tr>
    <td colspan="2"></td>
    <td class="subtext">
      by charlie
      <a href="item?id=41000003">discuss</a>
    </td>
  </tr>
</table>
</body></html>
"""


class TestSafeInt:
    def test_extracts_leading_number(self):
        assert _safe_int("256 points") == 256

    def test_returns_none_on_none(self):
        assert _safe_int(None) is None

    def test_returns_none_on_no_digits(self):
        assert _safe_int("discuss") is None

    def test_extracts_from_mixed(self):
        assert _safe_int("103\xa0comments") == 103


class TestParseItems:
    def test_count(self):
        items = parse_items(SAMPLE_HTML, limit=30)
        assert len(items) == 3

    def test_limit(self):
        items = parse_items(SAMPLE_HTML, limit=1)
        assert len(items) == 1

    def test_first_item_fields(self):
        item = parse_items(SAMPLE_HTML, limit=1)[0]
        assert item["title"] == "First Post Title"
        assert item["url"] == "https://example.com/post-one"
        assert item["rank"] == 1
        assert item["item_id"] == 41000001
        assert item["points"] == 256
        assert item["comments_count"] == 103
        assert item["source"] == "https://news.ycombinator.com"

    def test_scraped_at_present(self):
        item = parse_items(SAMPLE_HTML, limit=1)[0]
        assert "T" in item["scraped_at"]

    def test_no_points_is_none(self):
        """Third item has no <span class='score'>."""
        items = parse_items(SAMPLE_HTML, limit=30)
        assert items[2]["points"] is None

    def test_discuss_gives_none_comments(self):
        """'discuss' link has no digits → comments_count should be None."""
        items = parse_items(SAMPLE_HTML, limit=30)
        assert items[2]["comments_count"] is None

    def test_empty_html(self):
        assert parse_items("<html></html>") == []

    def test_malformed_row_skipped(self):
        bad = '<table><tr class="athing" id="999"></tr></table>'
        assert parse_items(bad) == []

    def test_returns_dicts(self):
        items = parse_items(SAMPLE_HTML, limit=1)
        assert isinstance(items[0], dict)
