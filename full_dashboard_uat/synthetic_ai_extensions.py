"""Deterministic synthetic AI dashboard extensions.

UAT-only responses. No database, provider, broker, persistence,
operating AI model, or order execution.
"""

from flask import jsonify

from full_dashboard_uat.synthetic_ai_core import _synthetic_decision_data
from full_dashboard_uat.synthetic_ranking import _SYNTHETIC_ROWS


def _scores():
    current = _synthetic_decision_data()["decision_score"]
    return [current - 4, current - 2, current]


def register_synthetic_ai_extensions(app):
    if app is None:
        raise ValueError("APP_REQUIRED")

    @app.get("/api/ai-decision/history")
    def synthetic_ai_history_api():
        scores = _scores()
        return jsonify(success=True, history=[
            {
                "created_at": f"2026-11-{day:02d}T12:00:00",
                "decision": "SYNTHETIC_HOLD",
                "decision_score": score,
                "grade": "A",
                "market_regime": "SYNTHETIC_SIDEWAYS",
                "market_view": "SYNTHETIC_SIDEWAYS",
                "top_etf": _SYNTHETIC_ROWS[0]["ticker"],
                "reason": "Fictional UAT decision",
            }
            for day, score in zip((10, 11, 12), scores)
        ])

    @app.get("/api/ai-decision/chart")
    def synthetic_ai_chart_api():
        return jsonify(success=True, chart={
            "labels": ["UAT-1", "UAT-2", "UAT-3"],
            "scores": _scores(),
        })

    @app.get("/api/ai-decision/statistics")
    def synthetic_ai_statistics_api():
        scores = _scores()
        return jsonify(success=True, statistics={
            "highest_score": max(scores),
            "lowest_score": min(scores),
            "average_score": round(sum(scores) / len(scores), 2),
            "recent_average": round(sum(scores[-2:]) / 2, 2),
            "score_spread": max(scores) - min(scores),
        })

    @app.get("/api/ai-decision/outcome-learning-summary")
    def synthetic_ai_outcome_learning_api():
        return jsonify(success=True, summary={
            "total_outcomes": 3,
            "evaluated_outcomes": 2,
            "pending_outcomes": 1,
            "average_outcome_score": 80,
            "average_portfolio_return": 0,
            "positive_outcomes": 1,
            "negative_outcomes": 1,
            "adaptive_learning_required": False,
            "reassessment_required": False,
        })

    @app.get("/api/ai-decision/performance")
    def synthetic_ai_performance_api():
        scores = _scores()
        return jsonify(success=True, performance={
            "reliability": "SYNTHETIC_STABLE",
            "total_decisions": len(scores),
            "average_score": round(sum(scores) / len(scores), 2),
            "highest_score": max(scores),
            "lowest_score": min(scores),
            "latest_score": scores[-1],
        })

    @app.get("/api/ai-decision/reliability")
    def synthetic_ai_reliability_api():
        scores = _scores()
        return jsonify(success=True, reliability={
            "reliability_level": "SYNTHETIC_STABLE",
            "confidence": 80,
            "stability": "STABLE",
            "average_score": round(sum(scores) / len(scores), 2),
            "score_change": scores[-1] - scores[-2],
            "message": "Fictional reliability for UAT only.",
        })

    @app.get("/api/ai-decision/adaptive-strategy")
    def synthetic_ai_adaptive_strategy_api():
        score = _scores()[-1]
        return jsonify(success=True, strategy={
            "strategy": "SYNTHETIC_BALANCED",
            "action": "HOLD",
            "confidence": 80,
            "score": score,
            "direction": "NEUTRAL",
            "stability": "STABLE",
            "momentum": "NEUTRAL",
            "grade_stability": "STABLE",
            "consistency": "CONSISTENT",
            "summary": "Fictional adaptive strategy for UAT only.",
        })

    @app.get("/api/portfolio/ai-rebalance")
    def synthetic_ai_rebalance_api():
        return jsonify(success=True, recommendation={
            "rebalance_action": "HOLD",
            "confidence": "MEDIUM",
            "market_view": "SYNTHETIC_SIDEWAYS",
            "recommended_mode": "balanced",
            "changes": [
                {
                    "ticker": row["ticker"],
                    "action": "HOLD",
                    "reason": "Fictional UAT allocation",
                }
                for row in _SYNTHETIC_ROWS
            ],
            "message": "No real investment recommendation.",
        })

    @app.get("/api/portfolio/ai-optimization")
    def synthetic_ai_optimization_api():
        if len(_SYNTHETIC_ROWS) != 2:
            raise ValueError("SYNTHETIC_UNIVERSE_MISMATCH")
        return jsonify(success=True, optimization={
            "optimization_status": "SYNTHETIC_ONLY",
            "optimized_allocation": [
                {
                    "ticker": row["ticker"],
                    "current_weight": 50,
                    "target_weight": 50,
                }
                for row in _SYNTHETIC_ROWS
            ],
            "message": "Fictional optimization; no trades.",
        })

    return {
        ("/api/ai-decision/history", "GET"): "synthetic_ai_history_api",
        ("/api/ai-decision/chart", "GET"): "synthetic_ai_chart_api",
        ("/api/ai-decision/statistics", "GET"): "synthetic_ai_statistics_api",
        ("/api/ai-decision/outcome-learning-summary", "GET"): "synthetic_ai_outcome_learning_api",
        ("/api/ai-decision/performance", "GET"): "synthetic_ai_performance_api",
        ("/api/ai-decision/reliability", "GET"): "synthetic_ai_reliability_api",
        ("/api/ai-decision/adaptive-strategy", "GET"): "synthetic_ai_adaptive_strategy_api",
        ("/api/portfolio/ai-rebalance", "GET"): "synthetic_ai_rebalance_api",
        ("/api/portfolio/ai-optimization", "GET"): "synthetic_ai_optimization_api",
    }
