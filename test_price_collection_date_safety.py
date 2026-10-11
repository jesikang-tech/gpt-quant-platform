from price_test_support import isolated_price_db, phase8_test_scope
import pytest
from datetime import date



class FakeCollector:
    def __init__(self):
        self.calls = []

    def collect(self, ticker, start_date, end_date):
        self.calls.append((ticker, start_date, end_date))
        return [object()]




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


def _install_harnesses(IncrementalPriceUpdater):
    class HarnessUpdater(IncrementalPriceUpdater):
        def __init__(self, latest_date, collector):
            self.latest_date = latest_date
            self.price_collector = collector

        def get_latest_price_date(self, ticker):
            return self.latest_date

    return {'HarnessUpdater': HarnessUpdater}


@pytest.fixture(autouse=True)
def _protected_collection(isolated_price_db):
    with phase8_test_scope(isolated_price_db) as scope:
        import sys
        import collector.incremental_price_updater as updater
        module = sys.modules[__name__]
        for name, value in {"config": scope.config, "database": scope.database,
                            "repository": scope.repository, "updater_module": updater,
                            "IncrementalPriceUpdater": updater.IncrementalPriceUpdater,
                            "calculate_update_range": updater.calculate_update_range,
                            "_scope": scope}.items():
            scope.patches.setattr(module, name, value, raising=False)
        for name, value in _install_harnesses(updater.IncrementalPriceUpdater).items():
            scope.patches.setattr(module, name, value, raising=False)
        yield scope
