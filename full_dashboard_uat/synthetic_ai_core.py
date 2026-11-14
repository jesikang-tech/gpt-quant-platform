"""Core synthetic AI responses for isolated full-dashboard UAT.

All values are fictional and deterministic. No operating AI engine,
database, provider, persistence, or broker is accessed.
"""

from flask import jsonify

from full_dashboard_uat.synthetic_ranking import _SYNTHETIC_ROWS


def _synthetic_decision_data():
    if len(_SYNTHETIC_ROWS) != 2:
        raise ValueError("SYNTHETIC_UNIVERSE_MISMATCH")

    top = max(_SYNTHETIC_ROWS, key=lambda row: row["score"])
    score = int(top["score"])

    return {
        "decision": "SYNTHETIC_HOLD",
        "action": "HOLD",
        "confidence": 80,
        "decision_score": score,
        "grade": "A",
        "reason": "Fictional AI decision for isolated UAT.",
        "summary": "Synthetic dashboard rendering test only.",
        "top_etf": top["ticker"],
    }


def register_synthetic_ai_core(app):
    if app is None:
        raise ValueError("APP_REQUIRED")

    @app.route("/api/ai-decision", methods=["GET"])
    def synthetic_ai_decision_api():
        decision = _synthetic_decision_data()
        return jsonify({"success": True, "decision": decision})

    @app.route("/api/ai-decision/summary", methods=["GET"])
    def synthetic_ai_summary_api():
        decision = _synthetic_decision_data()
        return jsonify({
            "success": True,
            "summary": {
                "total_decisions": 3,
                "average_score": 90.0,
                "latest_decision": decision["decision"],
                "latest_grade": decision["grade"],
                "market_view": "SYNTHETIC_SIDEWAYS",
                "top_etf": decision["top_etf"],
            },
        })

    @app.route("/api/ai-decision/quality", methods=["GET"])
    def synthetic_ai_quality_api():
        return jsonify({
            "success": True,
            "quality": {
                "quality_level": "SYNTHETIC_HIGH",
                "score_stability": "STABLE",
                "recent_trend": "UP",
                "evaluation": "Fictional quality evaluation only.",
            },
        })

    @app.route("/api/ai-decision/trend", methods=["GET"])
    def synthetic_ai_trend_api():
        decision = _synthetic_decision_data()
        latest = decision["decision_score"]
        previous = latest - 2

        return jsonify({
            "success": True,
            "trend": {
                "trend": "SYNTHETIC_UPWARD",
                "latest_score": latest,
                "previous_score": previous,
                "score_change": latest - previous,
                "direction": "UP",
                "stability": "STABLE",
                "momentum": "POSITIVE",
                "grade_stability": "STABLE",
                "consistency": "CONSISTENT",
                "decision": decision["decision"],
                "summary": "Fictional AI trend for UAT only.",
            },
        })

    return {
        ("/api/ai-decision", "GET"): "synthetic_ai_decision_api",
        ("/api/ai-decision/summary", "GET"): "synthetic_ai_summary_api",
        ("/api/ai-decision/quality", "GET"): "synthetic_ai_quality_api",
        ("/api/ai-decision/trend", "GET"): "synthetic_ai_trend_api",
    }
