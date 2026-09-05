from datetime import date, timedelta

from database import get_connection
from collector.price_collector import PriceCollector


def calculate_update_range(latest_date, end_date, initial_start_date="2025-01-01"):
    if latest_date is None:
        return initial_start_date, end_date

    start_date = date.fromisoformat(latest_date) + timedelta(days=1)
    end = date.fromisoformat(end_date)

    if start_date > end:
        return None, end_date

    return start_date.isoformat(), end_date


class IncrementalPriceUpdater:

    def __init__(self, price_collector=None):
        self.price_collector = price_collector or PriceCollector()

    def get_latest_price_date(self, ticker):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT MAX(date)
            FROM etf_prices
            WHERE ticker = ?
            """,
            (ticker,),
        )

        row = cursor.fetchone()
        conn.close()

        return row[0] if row and row[0] else None

    def update_ticker(self, ticker, end_date, initial_start_date="2025-01-01"):
        latest_date = self.get_latest_price_date(ticker)

        start_date, end_date = calculate_update_range(
            latest_date,
            end_date,
            initial_start_date=initial_start_date,
        )

        if start_date is None:
            return {
                "ticker": ticker,
                "status": "UP_TO_DATE",
                "latest_date": latest_date,
                "start_date": None,
                "end_date": end_date,
                "rows": 0,
            }

        df = self.price_collector.collect(
            ticker,
            start_date,
            end_date,
        )

        rows = len(df)

        return {
            "ticker": ticker,
            "status": "UPDATED" if rows > 0 else "NO_NEW_DATA",
            "latest_date": latest_date,
            "start_date": start_date,
            "end_date": end_date,
            "rows": rows,
        }



    def get_etf_list(self):
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
            if len(str(row[0])) == 6
        ]

    def update_all(self, end_date, initial_start_date="2025-01-01"):
        tickers = self.get_etf_list()

        results = []
        updated = 0
        up_to_date = 0
        no_new_data = 0
        failed = 0

        for ticker in tickers:
            try:
                result = self.update_ticker(
                    ticker,
                    end_date,
                    initial_start_date=initial_start_date,
                )

                results.append(result)

                if result["status"] == "UPDATED":
                    updated += 1
                elif result["status"] == "UP_TO_DATE":
                    up_to_date += 1
                elif result["status"] == "NO_NEW_DATA":
                    no_new_data += 1

            except Exception as exc:
                failed += 1
                results.append(
                    {
                        "ticker": ticker,
                        "status": "FAILED",
                        "latest_date": None,
                        "start_date": None,
                        "end_date": end_date,
                        "rows": 0,
                        "error": str(exc),
                    }
                )

        return {
            "total": len(tickers),
            "updated": updated,
            "up_to_date": up_to_date,
            "no_new_data": no_new_data,
            "failed": failed,
            "results": results,
        }
