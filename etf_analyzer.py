from factor_engine import (
    calculate_return,
    calculate_return_score,
    calculate_trend_score,
    calculate_slope_score,
    calculate_final_score,
    check_etf_condition
)

from repository import (
    save_or_update_etf_score,
    save_score_history
)


def analyze_etf(
    ticker,
    prices,
    analysis_date=None
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


    slope_score = calculate_slope_score(
        prices
    )


    final_score = calculate_final_score(
        return_score,
        trend_score,
        slope_score
    )


    if analysis_date is None:
        from datetime import date
        analysis_date = date.today().isoformat()


    save_or_update_etf_score(
        ticker,
        return_score,
        trend_score,
        slope_score,
        final_score,
        analysis_date
    )


    save_score_history(
        ticker,
        return_score,
        trend_score,
        slope_score,
        final_score,
        analysis_date
    )


    return {
        "ticker": ticker,
        "return": return_rate,
        "score": final_score
    }