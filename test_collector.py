"""Mock ETF collection persists only to a temporary DB and CSV directory."""
from price_test_support import isolated_price_db


def test_collector_saves_mock_etfs_and_csv(isolated_price_db, tmp_path, monkeypatch):
    import pandas as pd
    from unittest.mock import Mock
    from collector.etf_collector import ETFCollector
    from repository import get_all_etf_info

    monkeypatch.chdir(tmp_path)
    frame = pd.DataFrame({"Symbol": ["111111", "222222"],
                          "Name": ["Mock ETF A", "Mock ETF B"]})
    collector = ETFCollector()
    collector.provider = Mock()
    collector.provider.get_etf_list.return_value = frame

    assert collector.collect() is frame
    collector.provider.get_etf_list.assert_called_once_with()
    collector.provider.get_price.assert_not_called()
    assert get_all_etf_info() == [("111111", "Mock ETF A", "ETF"),
                                  ("222222", "Mock ETF B", "ETF")]
    csv_path = tmp_path / "data" / "etf_list.csv"
    actual = pd.read_csv(csv_path, encoding="utf-8-sig", dtype={"Symbol": str})
    pd.testing.assert_frame_equal(actual, frame)
