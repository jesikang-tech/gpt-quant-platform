"""Synthetic intelligence and recommendation for full-dashboard UAT.

All responses are fictional. No operating database, model,
market-data provider, credentials or broker is accessed.
"""

from flask import jsonify

from full_dashboard_uat.synthetic_ranking import _SYNTHETIC_ROWS


def register_synthetic_intelligence(app):
    """Register synthetic first-screen analysis and recommendation APIs."""
    if app is None:
        raise ValueError("Flask app required")

    rows = {row["ticker"]: row for row in _SYNTHETIC_ROWS}
    if not rows:
        raise ValueError("Synthetic ranking fixtures required")

    top = _SYNTHETIC_ROWS[0]

    @app.route("/api/intelligence", methods=["GET"])
    def synthetic_intelligence_api():
        return jsonify({
            "success": True,
            "ticker": top["ticker"],
            "score": top["score"],
            "enhanced_score": top["enhanced_score"],
            "grade": top["grade"],
            "prediction": top["prediction"],
            "stability": top["stability"],
            "trend": "SYNTHETIC_UPTREND",
            "risk": "SYNTHETIC_TEST_ONLY",
            "opinion": "UAT synthetic analysis; not investment advice.",
        })

    routes = {
        ("/api/intelligence", "GET"): "synthetic_intelligence_api",
    }

    for ticker in rows:
        path = "/api/recommendation/" + ticker

        def recommendation_handler(ticker=ticker):
            row = rows[ticker]
            return jsonify({
                "success": True,
                "ticker": ticker,
                "recommendation": {
                    "recommendation": "HOLD",
                    "confidence": "MEDIUM",
                    "reasons": [
                        "Synthetic score fixture",
                        "Synthetic ranking fixture",
                        "Synthetic risk fixture",
                    ],
                },
            })

        endpoint = "synthetic_recommendation_" + ticker

        app.add_url_rule(
            path,
            endpoint=endpoint,
            view_func=recommendation_handler,
            methods=["GET"],
        )

        routes[(path, "GET")] = endpoint

    return routes
