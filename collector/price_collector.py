from providers.fdr_provider import FDRProvider
from repository import save_etf_price, save_etf_ohlcv_price
import pandas as pd

from core.price_provenance_gate import PriceProvenanceRejected


class PriceCollector:

    def __init__(self):
        self.provider = FDRProvider()
        self._initial_provider = self.provider


    def collect(
        self,
        ticker,
        start_date,
        end_date
    ):
        """
        ETF 가격 데이터 수집 및 저장
        """

        if self.provider is not self._initial_provider:
            raise PriceProvenanceRejected(
                "Replaced provider cannot use legacy price writers"
            )

        if getattr(self.provider, "provider", None) == "NAVER":
            raise PriceProvenanceRejected(
                "Unverified NAVER provider cannot use legacy price writers"
            )

        df = self.provider.get_price(
            ticker,
            start_date,
            end_date
        )


        for date, row in df.iterrows():

            save_etf_price(
                ticker,
                str(date.date()),
                float(row["Close"])
            )

            values = [row.get(column) for column in ("Open", "High", "Low", "Close", "Volume")]
            save_etf_ohlcv_price(
                ticker,
                str(date.date()),
                *[None if pd.isna(value) else float(value) for value in values],
            )


        return df
