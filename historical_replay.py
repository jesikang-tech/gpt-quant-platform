from datetime import datetime
from database import get_connection
from factor_engine import (
    calculate_return,
    calculate_return_score,
    calculate_trend_score,
    calculate_uptrend_ratio,
    calculate_slope_score,
    calculate_final_score,
)


class HistoricalReplayEngine:
    """
    Read-only Historical Replay Core Engine.

    Historical Replay rules:
    - Only price data on or before analysis_date may be used.
    - Minimum 60 trading days are required.
    - 3-month return must be >= 15%.
    - Uptrend ratio must be >= 70%.
    - Historical ranking is calculated in memory only.
    - No INSERT / UPDATE / DELETE operation is performed.
    """

    MIN_TRADING_DAYS = 60
    MIN_RETURN_RATE = 15.0
    MIN_UPTREND_RATIO = 70.0
    TOP_N = 10

    def __init__(self, analysis_date):
        self.analysis_date = self._validate_analysis_date(
            analysis_date
        )

    @staticmethod
    def _validate_analysis_date(analysis_date):
        if isinstance(analysis_date, datetime):
            return analysis_date.strftime("%Y-%m-%d")

        if not isinstance(analysis_date, str):
            raise ValueError(
                "analysis_date must be a YYYY-MM-DD string"
            )

        try:
            datetime.strptime(
                analysis_date,
                "%Y-%m-%d"
            )
        except ValueError as exc:
            raise ValueError(
                "analysis_date must be a valid YYYY-MM-DD date"
            ) from exc

        return analysis_date

    def _get_tickers(self):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT DISTINCT ticker
            FROM etf_prices
            WHERE date <= ?
            ORDER BY ticker
            """,
            (self.analysis_date,)
        )

        tickers = [
            row[0]
            for row in cursor.fetchall()
        ]

        conn.close()

        return tickers

    def _get_historical_prices(self, ticker):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT date, close_price
            FROM etf_prices
            WHERE ticker = ?
              AND date <= ?
            ORDER BY date
            """,
            (
                ticker,
                self.analysis_date
            )
        )

        rows = cursor.fetchall()

        conn.close()

        return rows

    @staticmethod
    def _calculate_three_month_prices(rows):
        """
        Use the latest approximately 3-month trading window
        ending at the replay analysis date.

        The returned list contains close prices only.
        """
        if len(rows) < 2:
            return []

        end_index = len(rows) - 1

        end_date = datetime.strptime(
            rows[end_index][0],
            "%Y-%m-%d"
        )

        for index in range(end_index - 1, -1, -1):
            current_date = datetime.strptime(
                rows[index][0],
                "%Y-%m-%d"
            )

            days = (
                end_date - current_date
            ).days

            if days >= 90:
                return [
                    row[1]
                    for row in rows[index:]
                ]

        return [
            row[1]
            for row in rows
        ]

    def _evaluate_ticker(self, ticker):
        rows = self._get_historical_prices(
            ticker
        )

        if len(rows) < self.MIN_TRADING_DAYS:
            return None

        prices = self._calculate_three_month_prices(
            rows
        )

        if len(prices) < 2:
            return None

        return_rate = calculate_return(
            prices[0],
            prices[-1]
        )

        trend_score = calculate_trend_score(
            prices
        )

        uptrend_ratio = calculate_uptrend_ratio(
            prices
        )

        if return_rate < self.MIN_RETURN_RATE:
            return None

        if uptrend_ratio < self.MIN_UPTREND_RATIO:
            return None

        return_score = calculate_return_score(
            return_rate
        )

        slope_score = calculate_slope_score(
            prices
        )

        final_score = calculate_final_score(
            return_score,
            trend_score,
            slope_score
        )

        return {
            "ticker": ticker,
            "analysis_date": self.analysis_date,
            "trading_days": len(rows),
            "return_rate": round(
                return_rate,
                2
            ),
            "uptrend_ratio": round(
                uptrend_ratio,
                2
            ),
            "return_score": return_score,
            "trend_score": trend_score,
            "slope_score": slope_score,
            "final_score": final_score,
        }

    def replay(self, limit=TOP_N):
        if not isinstance(limit, int):
            raise ValueError(
                "limit must be an integer"
            )

        if limit <= 0:
            raise ValueError(
                "limit must be greater than zero"
            )

        results = []

        for ticker in self._get_tickers():
            result = self._evaluate_ticker(
                ticker
            )

            if result is not None:
                results.append(result)

        results.sort(
            key=lambda item: (
                -item["final_score"],
                item["ticker"]
            )
        )

        return results[:limit]

