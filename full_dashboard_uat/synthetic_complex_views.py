"""Complex synthetic dashboard views for isolated browser UAT.

Fictional, deterministic, read-only responses.
No operating database, provider, model, persistence or broker.
"""

from flask import jsonify

from full_dashboard_uat.synthetic_ai_core import _synthetic_decision_data
from full_dashboard_uat.synthetic_ranking import _SYNTHETIC_ROWS


def _signal(label):
    return {
        "name": label,
        "factor": label,
        "signal": label,
        "status": "SYNTHETIC",
        "value": "SYNTHETIC",
        "score": 80,
        "reason": "Fictional UAT signal.",
        "contribution": 0,
        "impact": "NEUTRAL",
        "description": "Fictional UAT signal.",
    }


def _synthetic_intelligence():
    decision = _synthetic_decision_data()
    return {
        "decision": decision["decision"],
        "final_action": "HOLD",
        "final_strategy": "SYNTHETIC_BALANCED",
        "strategy_mode": "balanced",
        "market_view": "SYNTHETIC_SIDEWAYS",
        "confidence": 80,
        "reliability": "SYNTHETIC_STABLE",
        "quality": "SYNTHETIC_HIGH",
        "quality_trend": "STABLE",
        "rebalance_action": "HOLD",
        "optimization_status": "SYNTHETIC_ONLY",
        "adaptive_action": "HOLD",
        "adaptive_confidence": 80,
        "adaptive_consistency": "CONSISTENT",
        "adaptive_direction": "NEUTRAL",
        "adaptive_grade_stability": "STABLE",
        "adaptive_momentum": "NEUTRAL",
        "adaptive_override": False,
        "adaptive_override_reason": "No synthetic override.",
        "adaptive_score": decision["decision_score"],
        "adaptive_stability": "STABLE",
        "adaptive_summary": "Fictional adaptive evaluation.",
        "decision_alignment": "ALIGNED",
        "decision_consistency": "CONSISTENT",
        "decision_consistency_score": 80,
        "decision_consistency_summary": "Fictional consistency.",
        "summary": "Isolated synthetic dashboard test only.",
    }


def _synthetic_assessment():
    return {
        "confidence_score": 80,
        "confidence_level": "MEDIUM",
        "confidence_grade": "B",
        "confidence_status": "SYNTHETIC",
        "confidence_summary": "Fictional confidence assessment.",
        "assessment": "SYNTHETIC_STABLE",
        "assessment_summary": "Fictional UAT assessment.",
        "strongest_signals": [_signal("SYNTHETIC_SCORE")],
        "supporting_signals": [_signal("SYNTHETIC_STABILITY")],
        "attention_signals": [],
        "positive_signals": [_signal("SYNTHETIC_POSITIVE")],
        "risk_signals": [],
        "explanation": "Fictional UAT explanation.",
        "action": "HOLD",
        "recommendation": "SYNTHETIC_HOLD",
        "recommendation_score": 80,
        "monitoring": "SYNTHETIC_ONLY",
        "summary": "No real investment recommendation.",
    }


def register_synthetic_complex_views(app):
    if app is None:
        raise ValueError("APP_REQUIRED")

    @app.get("/api/portfolio/explain")
    def synthetic_portfolio_explain_api():
        return jsonify(success=True, explanation={
            "decision_summary": "Fictional balanced portfolio.",
            "factor_analysis": [
                {
                    **_signal("SYNTHETIC_SCORE"),
                    "weight": 50,
                    "explanation": "Fictional factor.",
                }
            ],
            "market_analysis": {
                "regime": "SYNTHETIC_SIDEWAYS",
                "reason": "Fictional market condition.",
                "impact": "NEUTRAL",
            },
            "risk_analysis": {
                "risk_level": "MEDIUM",
                "cash_weight": 0,
                "reason": "Fictional risk evaluation.",
                "summary": "Synthetic risk only.",
            },
            "allocation_reason": [
                {
                    "ticker": row["ticker"],
                    "weight": 50,
                    "reason": "Fictional equal-weight UAT allocation.",
                }
                for row in _SYNTHETIC_ROWS
            ],
            "summary": "No operating portfolio was accessed.",
        })

    @app.get("/api/ai-decision/explain")
    def synthetic_ai_explain_api():
        decision = _synthetic_decision_data()
        top = _SYNTHETIC_ROWS[0]
        return jsonify(success=True, explanation={
            "decision": decision["decision"],
            "decision_grade": decision["grade"],
            "decision_score": decision["decision_score"],
            "recommended_action": "HOLD",
            "explanation": {
                "market": {
                    "confidence": 80,
                    "contribution": 0,
                    "reason": "Fictional market signal.",
                    "regime": "SYNTHETIC_SIDEWAYS",
                },
                "portfolio": {
                    "contribution": 0,
                    "health_score": 88,
                    "reason": "Fictional portfolio signal.",
                    "risk_level": "MEDIUM",
                },
                "top_etf": {
                    "ticker": top["ticker"],
                    "score": top["score"],
                    "contribution": 0,
                    "reason": "Fictional ETF ranking.",
                },
                "risk": {
                    "market_regime": "SYNTHETIC_SIDEWAYS",
                    "risk_level": "MEDIUM",
                },
                "confidence": {
                    "confidence": 80,
                    "level": "MEDIUM",
                },
            },
        })

    @app.get("/api/portfolio/decision-intelligence")
    def synthetic_decision_intelligence_api():
        intelligence = _synthetic_intelligence()
        assessment = _synthetic_assessment()
        decision = _synthetic_decision_data()

        validation = {
            "decision": decision["decision"],
            "validation": "SYNTHETIC_ONLY",
            "validation_score": 80,
            "confidence_score": 80,
            "reliability": "SYNTHETIC_STABLE",
            "decision_alignment": "ALIGNED",
            "decision_consistency": "CONSISTENT",
            "strategy_mode": "balanced",
            "optimization_status": "SYNTHETIC_ONLY",
            "validation_signals": [_signal("SYNTHETIC_VALIDATION")],
            "risk_signals": [],
            "summary": "Fictional validation; not certified.",
        }

        return jsonify({
            "success": True,
            "intelligence": intelligence,
            "intelligence_score": {
                "intelligence_score": decision["decision_score"],
                "intelligence_level": "SYNTHETIC_ONLY",
                "grade": decision["grade"],
                "components": {
                    "decision": 80,
                    "confidence": 80,
                    "risk": 80,
                    "portfolio": 80,
                },
            },
            "decision_confidence": assessment,
            "decision_confidence_explainability": assessment,
            "decision_confidence_assessment": assessment,
            "decision_confidence_recommendation": assessment,
            "ai_decision_validation": validation,
            "ai_decision_validation_explainability": {
                "explanation": "Fictional validation explanation.",
                "positive_signals": [_signal("SYNTHETIC_VALIDATION")],
                "supporting_signals": [],
                "risk_signals": [],
                "summary": "Synthetic UAT only.",
            },
            "final_decision": {},
            "final_decision_certification": {},
            "final_decision_execution_assurance": {},
            "final_decision_execution_control": {},
            "final_decision_execution_feedback": {},
            "final_decision_execution_monitoring": {},
            "final_decision_execution_reassessment": {},
            "final_decision_governance": {},
            "final_decision_integrated_intelligence": {},
            "final_decision_lifecycle": {},
            "final_decision_lifecycle_governance_control": {},
            "final_decision_master_control": {},
            "final_decision_operational_intelligence": {},
            "final_decision_orchestration": {},
            "final_execution_decision": {},
        })


    @app.post("/api/portfolio/chat")
    def synthetic_portfolio_chat_api():
        from flask import request

        payload = request.get_json(silent=True)

        if (
            type(payload) is not dict
            or type(payload.get("question")) is not str
            or not payload["question"].strip()
            or len(payload["question"]) > 500
        ):
            return {"error": "INVALID_SYNTHETIC_QUESTION"}, 400

        return {
            "response": {
                "answer": (
                    "Synthetic UAT portfolio: "
                    "111111 50%, 222222 50%."
                ),
                "reason": [
                    "Fictional equal-weight allocation.",
                    "No operating portfolio or AI service accessed."
                ],
                "recommendation": "SYNTHETIC_HOLD_NO_TRADES",
                "confidence": "SYNTHETIC_ONLY"
            }
        }

    return {
        ("/api/portfolio/chat", "POST"):
            "synthetic_portfolio_chat_api",
        ("/api/portfolio/explain", "GET"):
            "synthetic_portfolio_explain_api",
        ("/api/ai-decision/explain", "GET"):
            "synthetic_ai_explain_api",
        ("/api/portfolio/decision-intelligence", "GET"):
            "synthetic_decision_intelligence_api",
    }
