"""Tests for scraper.export — HNItem → JSON / CSV."""

import csv
import json

from scraper.export import export_csv, export_json
from scraper.models import HNItem


def _make_items(n: int = 2) -> list[HNItem]:
    return [
        HNItem(
            title=f"Title {i}",
            url=f"https://example.com/{i}",
            rank=i,
            item_id=40000000 + i,
            points=100 + i,
            comments_count=10 + i,
            scraped_at="2026-01-01T00:00:00+00:00",
        )
        for i in range(1, n + 1)
    ]


class TestExportJSON:
    def test_creates_file(self, tmp_path):
        path = tmp_path / "out.json"
        export_json(_make_items(), path)
        assert path.exists()

    def test_valid_json(self, tmp_path):
        path = tmp_path / "out.json"
        export_json(_make_items(), path)
        data = json.loads(path.read_text())
        assert isinstance(data, list)
        assert len(data) == 2

    def test_fields_present(self, tmp_path):
        path = tmp_path / "out.json"
        export_json(_make_items(1), path)
        item = json.loads(path.read_text())[0]
        for key in ("title", "url", "rank", "item_id", "points", "scraped_at", "source"):
            assert key in item

    def test_nested_dir_created(self, tmp_path):
        path = tmp_path / "a" / "b" / "out.json"
        export_json(_make_items(1), path)
        assert path.exists()


class TestExportCSV:
    def test_creates_file(self, tmp_path):
        path = tmp_path / "out.csv"
        export_csv(_make_items(), path)
        assert path.exists()

    def test_header_and_rows(self, tmp_path):
        path = tmp_path / "out.csv"
        export_csv(_make_items(3), path)
        with path.open() as f:
            reader = csv.reader(f)
            rows = list(reader)
        assert rows[0][0] == "rank"
        assert len(rows) == 4  # header + 3 data rows

    def test_none_values_handled(self, tmp_path):
        items = [
            HNItem(
                title="No points",
                url=None,
                rank=1,
                item_id=1,
                points=None,
                comments_count=None,
            )
        ]
        path = tmp_path / "out.csv"
        export_csv(items, path)
        text = path.read_text()
        assert "No points" in text
