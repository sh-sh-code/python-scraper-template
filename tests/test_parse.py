"""Tests for scraper.parse — HTML → HNItem."""

from scraper.parse import parse_items, _safe_int

# Minimal HN-like HTML fixture
SAMPLE_HTML = """
<html><body>
<table>
  <tr class="athing" id="40001111">
    <td align="right" valign="top" class="title">
      <span class="rank">1.</span>
    </td>
    <td class="title">
      <span class="titleline">
        <a href="https://example.com/article">Example Article Title</a>
        <span class="sitestr">example.com</span>
      </span>
    </td>
  </tr>
  <tr>
    <td colspan="2"></td>
    <td class="subtext">
      <span class="score" id="score_40001111">142 points</span>
      by someuser
      <a href="item?id=40001111">87&nbsp;comments</a>
    </td>
  </tr>

  <tr class="athing" id="40002222">
    <td align="right" valign="top" class="title">
      <span class="rank">2.</span>
    </td>
    <td class="title">
      <span class="titleline">
        <a href="https://example.org/post">Another Post</a>
      </span>
    </td>
  </tr>
  <tr>
    <td colspan="2"></td>
    <td class="subtext">
      <span class="score" id="score_40002222">58 points</span>
      by otheruser
      <a href="item?id=40002222">12&nbsp;comments</a>
    </td>
  </tr>
</table>
</body></html>
"""


class TestSafeInt:
    def test_extracts_number(self):
        assert _safe_int("142 points") == 142

    def test_returns_none_for_none(self):
        assert _safe_int(None) is None

    def test_returns_none_for_no_digits(self):
        assert _safe_int("discuss") is None


class TestParseItems:
    def test_parses_correct_count(self):
        items = parse_items(SAMPLE_HTML, limit=30)
        assert len(items) == 2

    def test_limit_respected(self):
        items = parse_items(SAMPLE_HTML, limit=1)
        assert len(items) == 1

    def test_first_item_fields(self):
        items = parse_items(SAMPLE_HTML, limit=30)
        item = items[0]
        assert item.title == "Example Article Title"
        assert item.url == "https://example.com/article"
        assert item.rank == 1
        assert item.item_id == 40001111
        assert item.points == 142
        assert item.comments_count == 87
        assert item.source == "https://news.ycombinator.com"

    def test_scraped_at_is_iso(self):
        items = parse_items(SAMPLE_HTML, limit=1)
        assert "T" in items[0].scraped_at

    def test_empty_html_returns_empty(self):
        assert parse_items("<html></html>") == []

    def test_malformed_row_skipped(self):
        bad = '<table><tr class="athing" id="999"></tr></table>'
        assert parse_items(bad) == []
