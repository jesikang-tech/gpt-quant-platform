import pandas as pd
import FinanceDataReader as fdr

from .base_provider import BaseProvider
from core.price_provenance_gate import (
    assess_price_provenance,
    require_persistence_authorization,
)


class FDRProvider(BaseProvider):
    """
    FinanceDataReader 기반 데이터 공급자
    """

    def get_etf_list(self) -> pd.DataFrame:
        listings = fdr.StockListing("ETF/KR")
        return listings

    def get_price(
        self,
        ticker: str,
        start_date: str,
        end_date: str
    ) -> pd.DataFrame:

        decision = assess_price_provenance()
        require_persistence_authorization(decision)
        return fdr.DataReader(
            ticker,
            start_date,
            end_date
        )
