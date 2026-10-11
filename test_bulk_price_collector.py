"""Bulk collection uses synthetic data and an isolated SQLite database."""
from price_test_support import isolated_price_db


def test_bulk_collection_skips_existing_prices(isolated_price_db):
    import pandas as pd
    from unittest.mock import Mock
    from collector.bulk_price_collector import BulkPriceCollector
    from repository import get_etf_prices, save_etf_price

    conn = isolated_price_db.connect()
    with conn:
        conn.executemany("INSERT INTO etf_info(ticker, name) VALUES (?, ?)",
                         [("111111", "Existing"), ("222222", "New"), ("333333", "Limited")])
    conn.close()
    save_etf_price("111111", "2026-01-02", 90)
    frame = pd.DataFrame({"Open": [99], "High": [105], "Low": [98],
                          "Close": [100], "Volume": [10]},
                         index=pd.to_datetime(["2026-01-02"]))
    collector = BulkPriceCollector()
    provider = Mock()
    provider.get_price.return_value = frame
    collector.price_collector.provider = provider
    collector.collect("2026-01-01", "2026-01-05", limit=2)
    provider.get_price.assert_called_once_with("222222", "2026-01-01", "2026-01-05")
    assert get_etf_prices("111111") == [("2026-01-02", 90)]
    assert get_etf_prices("222222") == [("2026-01-02", 100)]
    assert get_etf_prices("333333") == []
