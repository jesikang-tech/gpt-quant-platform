"""Synthetic portfolio API for isolated full-dashboard browser UAT.

No operating database, history persistence, credentials,
financial-data provider, model or broker is accessed.

The save query parameter is accepted for browser compatibility,
but no data is ever persisted.
"""

from flask import jsonify, request

from full_dashboard_uat.synthetic_ranking import _SYNTHETIC_ROWS


_WEIGHTS = {
    "balanced": (50, 50),
    "aggressive": (70, 30),
    "conservative": (30, 70),
}


def register_synthetic_portfolio(app):
    """Register a synthetic, non-persistent portfolio API."""
    if app is None:
        raise ValueError("Flask app required")

    if len(_SYNTHETIC_ROWS) != 2:
        raise ValueError("Exactly two synthetic ETFs required")

    @app.route("/api/portfolio", methods=["GET"])
    def synthetic_portfolio_api():
        mode = request.args.get("mode", "balanced")
        save = request.args.get("save", "false")

        if mode not in _WEIGHTS:
            return jsonify({
                "success": False,
                "error": "Unsupported synthetic portfolio mode",
            }), 400

        if save not in ("true", "false"):
            return jsonify({
                "success": False,
                "error": "Invalid synthetic save flag",
            }), 400

        weights = _WEIGHTS[mode]
        portfolio = []

        for row, weight in zip(_SYNTHETIC_ROWS, weights):
            portfolio.append({
                "ticker": row["ticker"],
                "weight": weight,
                "score": row["score"],
                "optimization_score": row["enhanced_score"],
                "return_score": row["return_score"],
                "trend_score": row["trend_score"],
                "slope_score": row["slope_score"],
                "factor_analysis": {
                    "return": "SYNTHETIC_RETURN",
                    "trend": "SYNTHETIC_TREND",
                    "slope": "SYNTHETIC_SLOPE",
                },
                "reason": "Fictional UAT allocation",
            })

        intelligence = {
            "health_score": 88,
            "risk_level": "Balanced",
            "confidence": "MEDIUM",
            "cash_weight": 0,
            "rebalance": "SYNTHETIC_UAT_ONLY_NO_TRADES",
            "allocation": {
                item["ticker"]: item["weight"]
                for item in portfolio
            },
        }

        insight = {
            "summary": "Synthetic portfolio for browser UAT only.",
            "opinion": "Fictional allocation; not investment advice.",
            "analytics": {
                "market_regime": "SIDEWAYS",
                "market_strength": "SYNTHETIC_MODERATE",
                "market_confidence": 80,
                "average_score": round(
                    sum(item["score"] for item in portfolio)
                    / len(portfolio), 2
                ),
                "top_etf": max(
                    portfolio, key=lambda item: item["score"]
                )["ticker"],
                "top_score": max(item["score"] for item in portfolio),
                "diversification": "SYNTHETIC_TWO_ETF",
                "cash_weight": 0,
            },
        }

        return jsonify({
            "success": True,
            "strategy": mode.capitalize(),
            "portfolio": portfolio,
            "insight": insight,
            "intelligence": intelligence,
        })

    return {
        ("/api/portfolio", "GET"): "synthetic_portfolio_api",
    }
