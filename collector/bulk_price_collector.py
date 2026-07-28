from database import get_connection
from collector.price_collector import PriceCollector
from repository import has_price_data


class BulkPriceCollector:

    def __init__(self):
        self.price_collector = PriceCollector()


    def get_etf_list(self):
        """
        DB에서 ETF 목록 조회
        """

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT ticker
            FROM etf_info
            ORDER BY ticker
            """
        )

        rows = cursor.fetchall()

        conn.close()

        return [
            row[0]
            for row in rows
            if str(row[0]).isdigit()
            and len(str(row[0])) == 6
        ]


    def collect(
        self,
        start_date,
        end_date,
        limit=None
    ):
        """
        ETF 전체 가격 데이터 수집

        limit:
            테스트용 처리 개수 제한
        """

        tickers = self.get_etf_list()


        if limit:
            tickers = tickers[:limit]


        total = len(tickers)

        print(f"수집 대상 ETF : {total}개")


        success = 0
        fail = 0


        for index, ticker in enumerate(tickers, start=1):

            try:

                if has_price_data(ticker):
                    print(
                        f"[{index}/{total}] {ticker} 이미 존재 - Skip"
                    )
                    success += 1
                    continue

                print(
                    f"[{index}/{total}] {ticker} 수집 중..."
                )


                self.price_collector.collect(
                    ticker,
                    start_date,
                    end_date
                )


                success += 1


            except Exception as e:

                print(
                    f"{ticker} 오류 : {e}"
                )

                fail += 1


        print()
        print("===== 수집 완료 =====")
        print(f"성공 : {success}")
        print(f"실패 : {fail}")