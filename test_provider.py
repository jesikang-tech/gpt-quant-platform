"""ETF listing contract with a mocked FDR source; no import-time requests."""
from price_test_support import isolated_price_db


def test_provider_returns_mock_etf_list(isolated_price_db, monkeypatch):
    import pandas as pd
    from unittest.mock import Mock
    import FinanceDataReader as fdr
    from providers.fdr_provider import FDRProvider

    frame = pd.DataFrame({"Symbol": ["111111", "222222"],
                          "Name": ["Mock ETF A", "Mock ETF B"]})
    listing = Mock(return_value=frame)
    monkeypatch.setattr(fdr, "StockListing", listing)

    assert FDRProvider().get_etf_list() is frame
    listing.assert_called_once_with("ETF/KR")
