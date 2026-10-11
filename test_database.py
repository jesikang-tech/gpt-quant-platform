"""Initialize only the temporary database supplied by the fixture."""
from price_test_support import isolated_price_db


def test_database_initialization_is_idempotent(isolated_price_db):
    from database import init_database

    init_database()
    conn = isolated_price_db.connect()
    try:
        tables = {row[0] for row in conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table'")}
        assert {"etf_prices", "etf_ohlcv_prices", "etf_info"} <= tables
        assert conn.execute("SELECT COUNT(*) FROM etf_prices").fetchone() == (0,)
        assert conn.execute("SELECT COUNT(*) FROM etf_info").fetchone() == (0,)
    finally:
        conn.close()


def test_etf_collector_persists_mock_list_and_csv(isolated_price_db, tmp_path, monkeypatch):
    import pandas as pd
    from unittest.mock import Mock
    from collector.etf_collector import ETFCollector

    monkeypatch.chdir(tmp_path)
    frame = pd.DataFrame({"Symbol": ["111111", "222222"],
                          "Name": ["Mock ETF A", "Mock ETF B"]})
    collector = ETFCollector()
    collector.provider = Mock()
    collector.provider.get_etf_list.return_value = frame

    assert collector.collect() is frame
    collector.provider.get_etf_list.assert_called_once_with()
    csv_path = tmp_path / "data" / "etf_list.csv"
    actual = pd.read_csv(csv_path, encoding="utf-8-sig", dtype={"Symbol": str})
    pd.testing.assert_frame_equal(actual, frame)
    conn = isolated_price_db.connect()
    try:
        assert conn.execute(
            "SELECT ticker, name, market FROM etf_info ORDER BY ticker"
        ).fetchall() == [("111111", "Mock ETF A", "ETF"),
                         ("222222", "Mock ETF B", "ETF")]
    finally:
        conn.close()
