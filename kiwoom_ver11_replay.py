"""Explicit KIWOOM Ver1.1 historical ranking replay.

Caller-supplied price rows only; no database, HTTP, persistence,
broker access, or implicit source authorization.
"""

from kiwoom_ver11_analysis import score_kiwoom_ver11_close_prices


def replay_kiwoom_ver11_prices(
    ticker_prices, *, analysis_date, period="3m", limit=10
):
    """Rank eligible tickers using prices no later than analysis_date."""
    if type(ticker_prices) is not dict:
        raise ValueError("Invalid ticker price mapping")
    if type(limit) is not int or limit < 1 or limit > 100:
        raise ValueError("Invalid replay limit")
    if len(ticker_prices) > 5000:
        raise ValueError("Too many tickers")

    results = []
    unavailable = []
    for ticker, dated_closes in ticker_prices.items():
        score = score_kiwoom_ver11_close_prices(
            ticker,
            dated_closes,
            analysis_date=analysis_date,
            period=period,
        )
        if not score["available"]:
            unavailable.append(ticker)
        elif score["selection_pass"]:
            results.append(score)

    results.sort(
        key=lambda item: (-item["final_score"], item["ticker"])
    )
    return {
        "success": True,
        "source": "KIWOOM",
        "input_origin": "CALLER_SUPPLIED_UNVERIFIED",
        "analysis_date": analysis_date,
        "period": period,
        "limit": limit,
        "total_selected": len(results),
        "unavailable_tickers": sorted(unavailable),
        "results": results[:limit],
        "persistence": False,
        "db_write": False,
    }