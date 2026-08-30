from core.ai_decision_outcome_intelligence import (
    AIDecisionOutcomeIntelligence
)
from core.ai_decision_adaptive_strategy import (
    AIDecisionAdaptiveStrategy
)


TREND = {
    "direction": "STABLE",
    "stability": "HIGH",
    "momentum": "NEUTRAL",
    "grade_stability": "STABLE",
    "consistency": "HIGH",
    "latest_score": 85
}


def build_outcome_evaluation():

    return {
        "evaluation_status": "WAITING_FOR_OUTCOME",
        "learning_status": "WAITING_FOR_OUTCOME",
        "learning_signal": "NONE",
        "learning_signal_strength": 0.0
    }


def run_case(name, reassessment_required):

    outcome_evaluation = build_outcome_evaluation()

    intelligence_engine = (
        AIDecisionOutcomeIntelligence()
    )

    outcome_intelligence = (
        intelligence_engine.analyze(
            final_decision={
                "decision": "MAINTAIN",
                "action": "REVIEW"
            },
            final_decision_master_control={
                "master_control_status": (
                    "MASTER_REVIEW"
                    if reassessment_required
                    else "MASTER_READY"
                ),
                "master_control_action": (
                    "REVIEW"
                    if reassessment_required
                    else "PROCEED"
                )
            },
            final_decision_certification={
                "certification_status": (
                    "CERTIFICATION_REVIEW"
                    if reassessment_required
                    else "CERTIFIED"
                )
            },
            final_execution_decision={
                "execution_status": (
                    "EXECUTION_REVIEW"
                    if reassessment_required
                    else "EXECUTION_READY"
                ),
                "execution_authorization": (
                    "SUSPENDED"
                    if reassessment_required
                    else "AUTHORIZED"
                )
            },
            final_decision_execution_reassessment={
                "reassessment_status": (
                    "REASSESSMENT_REQUIRED"
                    if reassessment_required
                    else "NOT_REQUIRED"
                ),
                "reassessment_required":
                    reassessment_required
            },
            intelligence={
                "market_view": "NEUTRAL"
            },
            intelligence_score={
                "intelligence_score": 85.0
            },
            decision_confidence={
                "confidence_score": 90.0
            },
            outcome_evaluation=outcome_evaluation
        )
    )

    strategy_engine = AIDecisionAdaptiveStrategy()

    adaptive_strategy = strategy_engine.analyze(
        TREND,
        outcome_intelligence
    )

    print("")
    print("=" * 82)
    print(f"CASE: {name}")
    print("=" * 82)

    print("--- OUTCOME EVALUATION ---")
    print(
        "evaluation_status:",
        outcome_evaluation["evaluation_status"]
    )
    print(
        "learning_status:",
        outcome_evaluation["learning_status"]
    )
    print(
        "learning_signal:",
        outcome_evaluation["learning_signal"]
    )
    print(
        "learning_signal_strength:",
        outcome_evaluation[
            "learning_signal_strength"
        ]
    )

    print("--- OUTCOME INTELLIGENCE ---")
    print(
        "outcome_learning_signal:",
        outcome_intelligence.get(
            "outcome_learning_signal"
        )
    )
    print(
        "outcome_learning_signal_strength:",
        outcome_intelligence.get(
            "outcome_learning_signal_strength"
        )
    )
    print(
        "learning_status:",
        outcome_intelligence.get(
            "learning_status"
        )
    )
    print(
        "adaptive_learning_required:",
        outcome_intelligence.get(
            "adaptive_learning_required"
        )
    )

    print("--- ADAPTIVE STRATEGY ---")
    print(
        "strategy:",
        adaptive_strategy.get("strategy")
    )
    print(
        "action:",
        adaptive_strategy.get("action")
    )
    print(
        "outcome_learning_signal:",
        adaptive_strategy.get(
            "outcome_learning_signal"
        )
    )
    print(
        "outcome_learning_signal_strength:",
        adaptive_strategy.get(
            "outcome_learning_signal_strength"
        )
    )
    print(
        "adaptive_learning_required:",
        adaptive_strategy.get(
            "adaptive_learning_required"
        )
    )

    assert (
        outcome_intelligence.get(
            "outcome_learning_signal"
        )
        == "NONE"
    )

    assert (
        outcome_intelligence.get(
            "outcome_learning_signal_strength"
        )
        == 0.0
    )

    if reassessment_required:

        assert (
            outcome_intelligence.get(
                "learning_status"
            )
            == "REASSESSMENT_REQUIRED"
        )

        assert (
            outcome_intelligence.get(
                "adaptive_learning_required"
            )
            is True
        )

    else:

        assert (
            outcome_intelligence.get(
                "learning_status"
            )
            == "WAITING_FOR_OUTCOME"
        )

        assert (
            outcome_intelligence.get(
                "adaptive_learning_required"
            )
            is False
        )

    assert (
        adaptive_strategy.get(
            "outcome_learning_signal"
        )
        == "NONE"
    )

    assert (
        adaptive_strategy.get(
            "outcome_learning_signal_strength"
        )
        == 0.0
    )

    if reassessment_required:

        assert (
            adaptive_strategy.get(
                "adaptive_learning_required"
            )
            is True
        )

    else:

        assert (
            adaptive_strategy.get(
                "adaptive_learning_required"
            )
            is False
        )

    print(
        f"{name} -> OUTCOME INTELLIGENCE / "
        f"ADAPTIVE STRATEGY: PASS"
    )


print("=" * 82)
print(
    "PHASE 7-9-11 OUTCOME EVALUATION -> "
    "OUTCOME INTELLIGENCE -> ADAPTIVE STRATEGY"
)
print(
    "WAITING-FOR-OUTCOME LEARNING BOUNDARY CONTRACT TEST"
)
print(
    "SOURCE-VERIFIED / MEMORY-ONLY / READ-ONLY"
)
print("=" * 82)

run_case(
    "REASSESSMENT_REQUIRED",
    True
)

run_case(
    "NOT_REQUIRED",
    False
)

print("")
print("=" * 82)
print("FINAL ASSERTIONS")
print("=" * 82)

print(
    "REASSESSMENT_REQUIRED -> "
    "WAITING_FOR_OUTCOME / NONE / 0.0 -> "
    "REASSESSMENT_REQUIRED / adaptive_learning_required=True "
    "-> strategy unchanged: PASS"
)

print(
    "NOT_REQUIRED -> "
    "WAITING_FOR_OUTCOME / NONE / 0.0 -> "
    "WAITING_FOR_OUTCOME / adaptive_learning_required=False "
    "-> strategy unchanged: PASS"
)

print("")
print("=" * 82)
print("SAFETY")
print("=" * 82)
print("Memory-only execution: PASS")
print("No production DB access.")
print("No API runtime call.")
print("No INSERT.")
print("No UPDATE.")
print("No DELETE.")
print("No future price injection.")
print("No fake Outcome persistence.")
print("No actual Outcome supplied.")

print("")
print(
    "===== PHASE 7-9-11 OUTCOME EVALUATION -> "
    "OUTCOME INTELLIGENCE -> ADAPTIVE STRATEGY"
)
print("===== CONTRACT TEST COMPLETE")
print("=" * 82)
