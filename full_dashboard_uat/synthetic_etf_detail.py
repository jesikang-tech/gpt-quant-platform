"""Synthetic ETF detail and ranking history for isolated browser UAT.

All values are fictional. No operating database, financial-data
provider, credentials, model or broker is accessed.
"""

from flask import jsonify

from full_dashboard_uat.synthetic_ranking import _SYNTHETIC_ROWS


def register_synthetic_etf_detail(app):
    """Register exact synthetic ETF detail and history routes."""
    if app is None:
        raise ValueError("Flask app required")

    rows = {row["ticker"]: row for row in _SYNTHETIC_ROWS}

    if set(rows) != {"111111", "222222"}:
        raise ValueError("Unexpected synthetic ETF universe")

    routes = {}

    for ticker in sorted(rows):
        detail_path = "/api/detail/" + ticker
        history_path = "/api/history/" + ticker

        def detail_handler(ticker=ticker):
            row = dict(rows[ticker])

            row["analysis"] = {
                "trend": "SYNTHETIC_TREND",
                "risk": "SYNTHETIC_TEST_ONLY",
                "opinion": "Fictional ETF analysis for UAT only.",
                "score_change": 1.5 if ticker == "111111" else -0.5,
                "prediction": row["prediction"],
            }

            return jsonify(row)

        def history_handler(ticker=ticker):
            row = rows[ticker]
            base_score = row["score"]
            rank = row["rank"]

            history = [
                {
                    "date": "2026-11-09",
                    "rank": rank,
                    "score": base_score - 4,
                },
                {
                    "date": "2026-11-10",
                    "rank": rank,
                    "score": base_score - 3,
                },
                {
                    "date": "2026-11-11",
                    "rank": rank,
                    "score": base_score - 2,
                },
                {
                    "date": "2026-11-12",
                    "rank": rank,
                    "score": base_score - 1,
                },
                {
                    "date": "2026-11-13",
                    "rank": rank,
                    "score": base_score,
                },
            ]

            return jsonify({
                "ticker": ticker,
                "history": history,
            })

        detail_endpoint = "synthetic_detail_" + ticker
        history_endpoint = "synthetic_history_" + ticker

        app.add_url_rule(
            detail_path,
            endpoint=detail_endpoint,
            view_func=detail_handler,
            methods=["GET"],
        )

        app.add_url_rule(
            history_path,
            endpoint=history_endpoint,
            view_func=history_handler,
            methods=["GET"],
        )

        routes[(detail_path, "GET")] = detail_endpoint
        routes[(history_path, "GET")] = history_endpoint

    return routes
