"""Mock provider persistence test; no live collection entry point."""
from price_test_support import isolated_price_db


def test_price_collector_persists_mock_observation(isolated_price_db):
    import pandas as pd
    from unittest.mock import Mock
    from collector.price_collector import PriceCollector
    from repository import get_etf_prices, get_etf_ohlcv_prices

    frame = pd.DataFrame({"Open": [99], "High": [105], "Low": [98],
                          "Close": [100], "Volume": [10]},
                         index=pd.to_datetime(["2026-01-02"]))
    collector = PriceCollector()
    provider = Mock()
    provider.get_price.return_value = frame
    collector.provider = provider
    assert collector.collect("111111", "2026-01-01", "2026-01-05") is frame
    provider.get_price.assert_called_once_with("111111", "2026-01-01", "2026-01-05")
    assert get_etf_prices("111111") == [("2026-01-02", 100)]
    assert get_etf_ohlcv_prices("111111") == [("2026-01-02", 99, 105, 98, 100, 10)]
