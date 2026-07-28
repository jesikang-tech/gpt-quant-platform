from pykrx import stock
import pandas as pd


class KRXCollector:
    """KRX ETF 종목 수집기"""

    def get_etf_list(self) -> pd.DataFrame:
        """
        KRX 상장 ETF 목록 반환
        """
        tickers = stock.get_etf_ticker_list()

        data = []

        for ticker in tickers:
            name = stock.get_etf_ticker_name(ticker)

            data.append({
                "ticker": ticker,
                "name": name
            })

        df = pd.DataFrame(data)

        return df


if __name__ == "__main__":
    collector = KRXCollector()

    df = collector.get_etf_list()

    print(df.head())
    print()
    print(f"ETF 개수 : {len(df)}")