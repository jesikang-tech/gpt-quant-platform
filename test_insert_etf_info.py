"""ETF information insertion and replacement against an isolated database."""
from price_test_support import isolated_price_db


def test_etf_info_save_and_readback(isolated_price_db):
    from repository import save_etf_info, get_all_etf_info

    save_etf_info("111111", "Mock ETF A", "KR")
    assert get_all_etf_info() == [("111111", "Mock ETF A", "KR")]


def test_etf_info_duplicate_replaces_existing_row(isolated_price_db):
    from repository import save_etf_info, get_all_etf_info

    save_etf_info("111111", "Original", "KR")
    save_etf_info("222222", "Unaffected", "KR")
    save_etf_info("111111", "Updated", "ETF")
    assert get_all_etf_info() == [("111111", "Updated", "ETF"),
                                  ("222222", "Unaffected", "KR")]
