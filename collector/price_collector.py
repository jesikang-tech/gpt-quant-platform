from providers.fdr_provider import FDRProvider
from repository import save_etf_price


class PriceCollector:

    def __init__(self):
        self.provider = FDRProvider()


    def collect(
        self,
        ticker,
        start_date,
        end_date
    ):
        """
        ETF 가격 데이터 수집 및 저장
        """

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


        return df