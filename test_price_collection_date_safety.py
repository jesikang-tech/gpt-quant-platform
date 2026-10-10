from datetime import date

from collector.incremental_price_updater import (
    IncrementalPriceUpdater,
)


class FakeCollector:
    def __init__(self):
        self.calls = []

    def collect(self, ticker, start_date, end_date):
        self.calls.append((ticker, start_date, end_date))
        return [object()]


class HarnessUpdater(IncrementalPriceUpdater):
    def __init__(self, latest_date, collector):
        self.latest_date = latest_date
        self.price_collector = collector

    def get_latest_price_date(self, ticker):
        return self.latest_date


def test_today_is_excluded_from_collection():
    collector = FakeCollector()
    updater = HarnessUpdater("2026-09-15", collector)

    result = updater.update_ticker(
        "069500",
        "2026-09-16",
        current_date=date(2026, 9, 16),
    )

    assert result["status"] == "UP_TO_DATE"
    assert collector.calls == []


def test_previous_date_remains_collectable():
    collector = FakeCollector()
    updater = HarnessUpdater("2026-09-14", collector)

    result = updater.update_ticker(
        "069500",
        "2026-09-16",
        current_date=date(2026, 9, 16),
    )

    assert result["status"] == "UPDATED"
    assert collector.calls == [
        ("069500", "2026-09-15", "2026-09-15")
    ]


def test_future_end_date_is_clamped():
    collector = FakeCollector()
    updater = HarnessUpdater("2026-09-14", collector)

    result = updater.update_ticker(
        "069500",
        "2026-09-30",
        current_date=date(2026, 9, 16),
    )

    assert result["status"] == "UPDATED"
    assert collector.calls == [
        ("069500", "2026-09-15", "2026-09-15")
    ]
