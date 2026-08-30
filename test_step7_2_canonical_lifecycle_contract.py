from core.ai_decision_outcome_intelligence import (
    AIDecisionOutcomeIntelligence,
)
from core.ai_decision_adaptive_strategy import (
    AIDecisionAdaptiveStrategy,
)


OUTCOME_ENGINE = AIDecisionOutcomeIntelligence()
ADAPTIVE_ENGINE = AIDecisionAdaptiveStrategy()


TREND = {
    "direction": "STABLE",
    "stability": "HIGH",
    "momentum": "NEUTRAL",
    "grade_stability": "STABLE",
    "consistency": "HIGH",
    "latest_score": 85,
}


def outcome_case(
    name,
    signal,
    score,
    expected_learning,
    expected_feedback,
    expected_adaptive,
    expected_reassessment,
    expected_status="EVALUATED",
):
    result = OUTCOME_ENGINE.analyze(
        final_decision={
            "decision": "TEST",
            "action": "TEST",
            "strategy": "TEST",
        },
        final_decision_execution_reassessment={
            "reassessment_required": expected_reassessment,
            "reassessment_status": (
                "REASSESSMENT_REQUIRED"
                if expected_reassessment
                else "NOT_REQUIRED"
            ),
        },
        intelligence={},
        intelligence_score={
            "intelligence_score": 86.6,
        },
        decision_confidence={
            "confidence_score": 100.0,
        },
        outcome_evaluation={
            "outcome_status": expected_status,
            "outcome_score": score,
            "outcome_grade": (
                "N/A"
                if score is None
                else ("F" if score < 60 else "B")
            ),
            "learning_status": (
                "BLOCKED"
                if expected_status == "PENDING"
                else "LEARNING_AVAILABLE"
            ),
            "learning_signal": signal,
            "learning_signal_strength": (
                0.0 if score is None else score
            ),
            "decision_effectiveness": "PENDING",
            "strategy_effectiveness": "PENDING",
            "market_response": "PENDING",
            "portfolio_response": "PENDING",
        },
    )

    assert result["outcome_status"] == expected_status
    assert result["outcome_learning_signal"] == signal
    assert result["learning_status"] == expected_learning
    assert result["feedback_state"] == expected_feedback
    assert result["adaptive_learning_required"] is expected_adaptive
    assert result["reassessment_required"] is expected_reassessment

    print(
        f"{name}: PASS | "
        f"{signal} -> "
        f"{result['learning_status']} / "
        f"{result['feedback_state']} | "
        f"adaptive={result['adaptive_learning_required']} | "
        f"reassessment={result['reassessment_required']}"
    )

    return result


print("=" * 60)
print("PHASE 7-2-4 CANONICAL LIFECYCLE CONTRACT")
print("=" * 60)


print("")
print("=== OUTCOME LIFECYCLE ===")

outcome_case(
    "CASE 1 PENDING",
    "NONE",
    None,
    "BLOCKED",
    "BLOCKED",
    False,
    False,
    expected_status="PENDING",
)

outcome_case(
    "CASE 2 POSITIVE",
    "POSITIVE",
    87.5,
    "LEARNING_AVAILABLE",
    "LEARNING_AVAILABLE",
    False,
    False,
)

outcome_case(
    "CASE 3 NEGATIVE",
    "NEGATIVE",
    40.0,
    "ADAPTIVE_LEARNING_REQUIRED",
    "ADAPTIVE_LEARNING",
    True,
    True,
)


print("")
print("=== ADAPTIVE STRATEGY ===")

ADAPTIVE_CASES = [
    {
        "name": "CASE 4 PENDING",
        "outcome": {
            "outcome_status": "PENDING",
            "outcome_learning_signal": "NONE",
            "outcome_learning_signal_strength": 0.0,
            "adaptive_learning_required": False,
        },
        "expected_strategy": "MAINTAIN",
        "expected_action": "MAINTAIN_ALLOCATION",
    },
    {
        "name": "CASE 5 POSITIVE",
        "outcome": {
            "outcome_status": "EVALUATED",
            "outcome_learning_signal": "POSITIVE",
            "outcome_learning_signal_strength": 100.0,
            "adaptive_learning_required": False,
        },
        "expected_strategy": "MAINTAIN",
        "expected_action": "MAINTAIN_ALLOCATION",
    },
    {
        "name": "CASE 6 NEGATIVE",
        "trend": {
            "direction": "DOWN",
            "stability": "HIGH",
            "momentum": "NEGATIVE",
            "grade_stability": "STABLE",
            "consistency": "HIGH",
            "latest_score": 70,
        },
        "outcome": {
            "outcome_status": "EVALUATED",
            "outcome_learning_signal": "NEGATIVE",
            "outcome_learning_signal_strength": 100.0,
            "adaptive_learning_required": True,
        },
        "expected_strategy": "DEFENSIVE",
        "expected_action": "REDUCE_RISK",
    },
]


for case in ADAPTIVE_CASES:
    result = ADAPTIVE_ENGINE.analyze(
        case.get("trend", TREND),
        outcome_intelligence=case["outcome"],
    )

    assert result["strategy"] == case["expected_strategy"]
    assert result["action"] == case["expected_action"]
    assert (
        result["outcome_learning_signal"]
        == case["outcome"]["outcome_learning_signal"]
    )
    assert (
        result["adaptive_learning_required"]
        == case["outcome"]["adaptive_learning_required"]
    )

    print(
        f"{case['name']}: PASS | "
        f"strategy={result['strategy']} | "
        f"action={result['action']} | "
        f"signal={result['outcome_learning_signal']} | "
        f"adaptive={result['adaptive_learning_required']}"
    )


print("")
print("=" * 60)
print("OVERALL RESULT: PASS")
print("=" * 60)
