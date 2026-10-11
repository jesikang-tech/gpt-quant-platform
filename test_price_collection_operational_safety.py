from price_test_support import isolated_price_db, phase8_test_scope
import pytest
from datetime import date
from pathlib import Path



def test_main_passes_current_date_to_price_updater():
    source = (Path(__file__).resolve().parent / "main.py").read_text(encoding="utf-8")

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
        yield scope
