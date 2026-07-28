import pandas as pd
import FinanceDataReader as fdr

from .base_provider import BaseProvider


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

        return fdr.DataReader(
            ticker,
            start_date,
            end_date
        )