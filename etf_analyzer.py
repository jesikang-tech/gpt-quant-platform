from factor_engine import (
    calculate_return,
    calculate_return_score,
    calculate_trend_score,
    calculate_final_score,
    check_etf_condition
)

from repository import save_or_update_etf_score


def analyze_etf(
    ticker,
    prices
):
    """
    ETF 분석 Pipeline
    """

    if not check_etf_condition(prices):
        return None


    return_rate = calculate_return(
        prices[0],
        prices[-1]
    )


    return_score = calculate_return_score(
        return_rate
    )


    trend_score = calculate_trend_score(
        prices
    )


    final_score = calculate_final_score(
        return_score,
        trend_score
    )


    save_or_update_etf_score(
    ticker,
    return_score,
    trend_score,
    0,
    final_score,
   "2026-07-27"
    )


    return {
        "ticker": ticker,
        "return": return_rate,
        "score": final_score
    }