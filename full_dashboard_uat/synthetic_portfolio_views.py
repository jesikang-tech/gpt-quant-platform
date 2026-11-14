"""Read-only synthetic portfolio views for isolated dashboard UAT.

All records are fictional and constructed in memory.
No operating DB, persistence, provider, model or broker calls.
"""

from flask import jsonify

from full_dashboard_uat.synthetic_ranking import _SYNTHETIC_ROWS


def _synthetic_portfolio_history():
    rows = []

    for index, (mode, weights) in enumerate(
        (
            ("balanced", (50, 50)),
            ("aggressive", (70, 30)),
            ("conservative", (30, 70)),
        ),
        start=1,
    ):
        for row, weight in zip(_SYNTHETIC_ROWS, weights):
            rows.append(
                {
                    "created_at": f"2026-11-{9 + index:02d}T12:00:00",
                    "mode": mode,
                    "health_score": 88,
                    "market_condition": "SYNTHETIC_NEUTRAL",
                    "confidence": "MEDIUM",
                    "ticker": row["ticker"],
                    "weight": weight,
                    "score": row["score"],
                    "reason": "Fictional UAT allocation",
                }
            )

    return rows


def register_synthetic_portfolio_views(app):
    if app is None:
        raise ValueError("Flask app required")

    if len(_SYNTHETIC_ROWS) != 2:
        raise ValueError("Exactly two synthetic ETFs required")

    @app.route("/api/portfolio/history", methods=["GET"])
    def synthetic_portfolio_history_api():
        return jsonify(
            {
                "success": True,
                "history": _synthetic_portfolio_history(),
            }
        )

    @app.route("/api/portfolio/analytics", methods=["GET"])
    def synthetic_portfolio_analytics_api():
        history = _synthetic_portfolio_history()

        return jsonify(
            {
                "success": True,
                "analytics": {
                    "total_history": len({
                        (item["mode"], item["created_at"])
                        for item in history
                    }),
                    "latest_mode": history[-1]["mode"],
                    "mode_analysis": [
                        ["balanced", 1],
                        ["aggressive", 1],
                        ["conservative", 1],
                    ],
                    "weight_analysis": [
                        [_SYNTHETIC_ROWS[0]["name"], 50.0],
                        [_SYNTHETIC_ROWS[1]["name"], 50.0],
                    ],
                },
            }
        )

    @app.route("/api/portfolio/market-condition", methods=["GET"])
    def synthetic_portfolio_market_condition_api():
        average_score = round(
            sum(row["score"] for row in _SYNTHETIC_ROWS)
            / len(_SYNTHETIC_ROWS),
            2,
        )

        return jsonify(
            {
                "success": True,
                "market_condition": {
                    "market": "SYNTHETIC_NEUTRAL",
                    "average_score": average_score,
                    "confidence": "MEDIUM",
                    "recommended_mode": "balanced",
                },
            }
        )

    return {
        ("/api/portfolio/history", "GET"):
            "synthetic_portfolio_history_api",
        ("/api/portfolio/analytics", "GET"):
            "synthetic_portfolio_analytics_api",
        ("/api/portfolio/market-condition", "GET"):
            "synthetic_portfolio_market_condition_api",
    }
