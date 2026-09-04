import pandas as pd

from collector.incremental_price_updater import IncrementalPriceUpdater


class FakePriceCollector:
    def __init__(self, failing_tickers=None, empty_tickers=None):
        self.calls = []
        self.failing_tickers = set(failing_tickers or [])
        self.empty_tickers = set(empty_tickers or [])

    def collect(self, ticker, start_date, end_date):
        self.calls.append((ticker, start_date, end_date))
        return pd.DataFrame({"Close": [100.0, 101.0]})


class HarnessUpdater(IncrementalPriceUpdater):
    def __init__(self, latest_date, price_collector):
        self._latest_date = latest_date
        self.price_collector = price_collector

    def get_latest_price_date(self, ticker):
        return self._latest_date


def test_update_ticker_skips_when_up_to_date():
    collector = FakePriceCollector()
    updater = HarnessUpdater("2026-09-04", collector)

    result = updater.update_ticker("069500", "2026-09-04")

    assert result["status"] == "UP_TO_DATE"
    assert result["rows"] == 0
    assert collector.calls == []


def test_update_ticker_collects_only_missing_range():
    collector = FakePriceCollector()
    updater = HarnessUpdater("2026-08-04", collector)

    result = updater.update_ticker("069500", "2026-09-04")

    assert result["status"] == "UPDATED"
    assert result["start_date"] == "2026-08-05"
    assert result["end_date"] == "2026-09-04"
    assert result["rows"] == 1
    assert collector.calls == [
        ("069500", "2026-08-05", "2026-09-04")
    ]


def test_update_ticker_collects_initial_history_when_missing():
    collector = FakePriceCollector()
    updater = HarnessUpdater(None, collector)

    result = updater.update_ticker("069500", "2026-09-04")

    assert result["status"] == "UPDATED"
    assert result["start_date"] == "2025-01-01"
    assert result["end_date"] == "2026-09-04"
    assert result["rows"] == 1
    assert collector.calls == [
        ("069500", "2025-01-01", "2026-09-04")
    ]
import pandas as pd

from collector.incremental_price_updater import IncrementalPriceUpdater


class FakePriceCollector:
    def __init__(self, failing_tickers=None, empty_tickers=None):
        self.calls = []
        self.failing_tickers = set(failing_tickers or [])
        self.empty_tickers = set(empty_tickers or [])

    def collect(self, ticker, start_date, end_date):
        self.calls.append((ticker, start_date, end_date))
        if ticker in self.failing_tickers:
            raise RuntimeError(f"forced failure: {ticker}")
        if ticker in self.empty_tickers:
            return pd.DataFrame()
        return pd.DataFrame({"Close": [100.0]})


class BatchHarnessUpdater(IncrementalPriceUpdater):
    def __init__(self, latest_dates, price_collector):
        self.latest_dates = latest_dates
        self.price_collector = price_collector

    def get_etf_list(self):
        return list(self.latest_dates.keys())

    def get_latest_price_date(self, ticker):
        return self.latest_dates[ticker]


def test_update_all_returns_structured_summary_and_isolates_failures():
    collector = FakePriceCollector(failing_tickers=["305720"])
    updater = BatchHarnessUpdater(
        {
            "069500": "2026-09-04",
            "102110": "2026-08-04",
            "305720": "2026-08-04",
            "360750": None,
        },
        collector,
    )

    result = updater.update_all("2026-09-04")

    assert result["total"] == 4
    assert result["updated"] == 2
    assert result["up_to_date"] == 1
    assert result["no_new_data"] == 0
    assert result["failed"] == 1

    assert result["results"][0]["status"] == "UP_TO_DATE"
    assert result["results"][1]["status"] == "UPDATED"
    assert result["results"][2]["status"] == "FAILED"
    assert result["results"][3]["status"] == "UPDATED"

    assert collector.calls == [
        ("102110", "2026-08-05", "2026-09-04"),
        ("305720", "2026-08-05", "2026-09-04"),
        ("360750", "2025-01-01", "2026-09-04"),
    ]


def test_update_ticker_accepts_custom_initial_start_date():
    collector = FakePriceCollector()
    updater = HarnessUpdater(None, collector)

    result = updater.update_ticker(
        "069500",
        "2026-09-04",
        initial_start_date="2026-01-01",
    )

    assert result["status"] == "UPDATED"
    assert result["start_date"] == "2026-01-01"
    assert result["end_date"] == "2026-09-04"
    assert collector.calls == [
        ("069500", "2026-01-01", "2026-09-04")
    ]
def test_update_all_propagates_custom_initial_start_date():
    collector = FakePriceCollector()
    updater = BatchHarnessUpdater(
        {
            "360750": None,
        },
        collector,
    )

    result = updater.update_all(
        "2026-09-04",
        initial_start_date="2026-01-01",
    )

    assert result["total"] == 1
    assert result["updated"] == 1
    assert collector.calls == [
        ("360750", "2026-01-01", "2026-09-04")
    ]
def test_update_ticker_returns_no_new_data_when_collector_is_empty():
    collector = FakePriceCollector(empty_tickers=["069500"])

    updater = HarnessUpdater(
        "2026-08-04",
        collector,
    )

    result = updater.update_ticker(
        "069500",
        "2026-09-04",
    )

    assert result["status"] == "NO_NEW_DATA"
    assert result["rows"] == 0
    assert collector.calls == [
        ("069500", "2026-08-05", "2026-09-04")
    ]
