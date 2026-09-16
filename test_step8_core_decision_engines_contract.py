from core.ai_decision_explainability import AIDecisionExplainability
from core.ai_decision_trend import AIDecisionTrend
from core.decision_confidence_explainability import DecisionConfidenceExplainability
from core.optimization_scoring import OptimizationScoringEngine


def test_optimization_scoring_weighted_calculation():
    engine = OptimizationScoringEngine()

    assert engine.calculate_score(
        100, 80, 60, 40, 20
    ) == 70.0


def test_optimization_scoring_boundaries_and_factor_classification():
    engine = OptimizationScoringEngine()

    assert engine.calculate_score(0, 0, 0, 0, 0) == 0.0
    assert engine.calculate_score(100, 100, 100, 100, 100) == 100.0

    assert engine.analyze_factors(90, 80, 70) == {
        "return": "Excellent",
        "trend": "Strong",
        "slope": "Good",
    }


def test_ai_decision_trend_direction_and_momentum():
    engine = AIDecisionTrend()

    history = [
        {"decision_score": 90, "grade": "A+", "decision": "MAINTAIN"},
        {"decision_score": 85, "grade": "A", "decision": "MAINTAIN"},
        {"decision_score": 80, "grade": "A", "decision": "MAINTAIN"},
    ]

    result = engine.analyze(history)

    assert result["direction"] == "UP"
    assert result["momentum"] == "POSITIVE"
    assert result["consistency"] == "HIGH"


def test_ai_decision_trend_empty_history():
    result = AIDecisionTrend().analyze([])

    assert result["direction"] == "STABLE"
    assert result["stability"] == "UNKNOWN"
    assert result["momentum"] == "NEUTRAL"
    assert result["decision"] == "UNKNOWN"


def test_ai_decision_explainability_contributions_and_grade():
    engine = AIDecisionExplainability()

    result = engine.calculate_contributions(
        {"confidence": 90},
        {"health_score": 80},
        {"score": 70},
    )

    assert result["market_contribution"] == 36.0
    assert result["portfolio_contribution"] == 32.0
    assert result["etf_contribution"] == 14.0
    assert result["decision_score"] == 82.0

    assert engine._get_grade(95) == "A+"
    assert engine._get_grade(85) == "A"
    assert engine._get_grade(75) == "B"
    assert engine._get_grade(65) == "C"


def test_decision_confidence_explainability_signal_boundaries():
    result = DecisionConfidenceExplainability().explain({
        "confidence_score": 95,
        "confidence_grade": "A+",
        "confidence_level": "Very High",
        "confidence_status": "STRONG",
        "components": {
            "reliability": 90,
            "decision_consistency": 80,
            "adaptive_strategy": 79.9,
            "decision_quality": 80,
            "rebalance": 80,
            "optimization": 80,
        },
    })

    assert result["positive_signals"] == [
        {"name": "Reliability", "score": 90.0}
    ]

    assert result["supporting_signals"] == [
        {"name": "Decision Consistency", "score": 80.0},
        {"name": "Decision Quality", "score": 80.0},
        {"name": "Rebalance", "score": 80.0},
        {"name": "Optimization", "score": 80.0},
    ]

    assert result["risk_signals"] == [
        {"name": "Adaptive Strategy", "score": 79.9}
    ]

    assert result["confidence_score"] == 95.0
