from datetime import date
from pathlib import Path

import collector.incremental_price_updater as updater_module


def test_main_passes_current_date_to_price_updater():
    source = Path("main.py").read_text(encoding="utf-8")

    assert "current_date=date.today()" in source


def test_update_all_propagates_current_date():
    class FakeCollector:
        def __init__(self):
            self.calls = []

        def collect(self, ticker, start_date, end_date):
            self.calls.append((ticker, start_date, end_date))
            return [object()]

    class HarnessUpdater(updater_module.IncrementalPriceUpdater):
        def __init__(self, collector):
            self.price_collector = collector

        def get_etf_list(self):
            return ["069500"]

        def get_latest_price_date(self, ticker):
            return "2026-09-14"

    collector = FakeCollector()
    updater = HarnessUpdater(collector)

    result = updater.update_all(
        "2026-09-16",
        current_date=date(2026, 9, 16),
    )

    assert result["updated"] == 1
    assert collector.calls == [
        ("069500", "2026-09-15", "2026-09-15")
    ]
