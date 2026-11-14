"""Synthetic market regime and strategy for isolated dashboard UAT.

Fictional, deterministic, in-memory responses only.
No operating DB, persistence, provider, model or broker calls.
"""

from flask import jsonify

from full_dashboard_uat.synthetic_ranking import _SYNTHETIC_ROWS


def _synthetic_market_metrics():
    if len(_SYNTHETIC_ROWS) != 2:
        raise ValueError("Exactly two synthetic ETFs required")

    scores = [row["score"] for row in _SYNTHETIC_ROWS]

    return {
        "avg_score": round(sum(scores) / len(scores), 2),
        "max_score": max(scores),
        "min_score": min(scores),
        "score_spread": max(scores) - min(scores),
        "breadth": 50.0,
        "market_strength": "SYNTHETIC_NEUTRAL",
        "regime": "SYNTHETIC_SIDEWAYS",
        "risk": "MEDIUM",
        "confidence": 80,
        "strategy": "balanced",
    }


def register_synthetic_market_views(app):
    if app is None:
        raise ValueError("Flask app required")

    @app.route("/api/market-regime", methods=["GET"])
    def synthetic_market_regime_api():
        return jsonify({
            "success": True,
            **_synthetic_market_metrics(),
        })

    @app.route("/api/market-strategy", methods=["GET"])
    def synthetic_market_strategy_api():
        metrics = _synthetic_market_metrics()

        return jsonify({
            "success": True,
            "strategy": "SYNTHETIC_BALANCED",
            "portfolio_mode": "balanced",
            "market_strength": metrics["market_strength"],
            "confidence": metrics["confidence"],
            "cash_target": 20.0,
            "rebalance_action": "SYNTHETIC_HOLD",
            "recommendation": "Fictional UAT strategy only.",
            "message": "Synthetic market strategy for browser UAT only.",
        })

    return {
        ("/api/market-regime", "GET"):
            "synthetic_market_regime_api",
        ("/api/market-strategy", "GET"):
            "synthetic_market_strategy_api",
    }
