"""
PHASE 7-10-19-2
OUTCOME EVALUATION
-> OUTCOME INTELLIGENCE
-> ADAPTIVE STRATEGY
CLOSED-LOOP BOUNDARY CONTRACT TEST V1

SOURCE-VERIFIED / MEMORY-ONLY / READ-ONLY
"""

from core.ai_decision_outcome_evaluation import (
    AIDecisionOutcomeEvaluation,
)
from core.ai_decision_outcome_intelligence import (
    AIDecisionOutcomeIntelligence,
)
from core.ai_decision_adaptive_strategy import (
    AIDecisionAdaptiveStrategy,
)


evaluation_engine = AIDecisionOutcomeEvaluation()
outcome_intelligence_engine = AIDecisionOutcomeIntelligence()
adaptive_strategy_engine = AIDecisionAdaptiveStrategy()


def assert_equal(actual, expected, label):
    if actual != expected:
        raise AssertionError(
            f"{label}: expected={expected!r}, actual={actual!r}"
        )
    print(f"{label}: PASS")


def base_snapshot():
    return {
        "decision": "MAINTAIN",
        "action": "PROCEED",
        "strategy": "BALANCED",
        "snapshot_status": "COLLECTED",
        "snapshot_purpose": "FUTURE_OUTCOME_EVALUATION",
    }


def base_final_decision():
    return {
        "decision": "MAINTAIN",
        "action": "PROCEED",
    }


def base_master_control():
    return {
        "decision": "MAINTAIN",
        "master_control_action": "PROCEED",
        "execution_status": "EXECUTION_READY",
        "execution_authorization": "AUTHORIZED",
        "master_control_status": "MASTER_READY",
    }


def base_certification():
    return {
        "certification_status": "CERTIFIED",
    }


def base_execution():
    return {
        "decision": "MAINTAIN",
        "action": "PROCEED",
        "execution_status": "EXECUTION_READY",
        "execution_authorization": "AUTHORIZED",
    }


def base_feedback():
    return {
        "feedback_status": "STABLE",
    }


def base_monitoring():
    return {
        "monitoring_status": "STANDARD_MONITORING",
    }


def base_reassessment():
    return {
        "reassessment_required": False,
        "reassessment_status": "NOT_REQUIRED",
    }


def base_intelligence():
    return {
        "intelligence_score": 90.0,
    }


def base_confidence():
    return {
        "confidence_score": 90.0,
    }


def evaluate_and_bridge(portfolio_return):
    evaluation = evaluation_engine.evaluate(
        outcome_snapshot=base_snapshot(),
        actual_outcome={
            "portfolio_return": portfolio_return,
            "market_response": "EVALUATED",
            "portfolio_response": "EVALUATED",
        },
    )

    intelligence = outcome_intelligence_engine.analyze(
        final_decision=base_final_decision(),
        final_decision_master_control=base_master_control(),
        final_decision_certification=base_certification(),
        final_execution_decision=base_execution(),
        final_decision_execution_feedback=base_feedback(),
        final_decision_execution_monitoring=base_monitoring(),
        final_decision_execution_reassessment=base_reassessment(),
        intelligence=base_intelligence(),
        intelligence_score=base_intelligence(),
        decision_confidence=base_confidence(),
        outcome_evaluation=evaluation,
    )

    strategy = adaptive_strategy_engine.analyze(
        trend={
            "direction": "STABLE",
            "stability": "MEDIUM",
            "momentum": "NEUTRAL",
            "grade_stability": "STABLE",
            "consistency": "MEDIUM",
            "latest_score": 75,
        },
        outcome_intelligence=intelligence,
    )

    return evaluation, intelligence, strategy


print("=" * 82)
print("CASE: POSITIVE OUTCOME -> GROWTH")
print("=" * 82)

evaluation, intelligence, strategy = evaluate_and_bridge(
    10.0
)

print("evaluation:", evaluation)
print("outcome_intelligence:", intelligence)
print("adaptive_strategy:", strategy)

assert_equal(
    evaluation["outcome_status"],
    "EVALUATED",
    "POSITIVE -> evaluation status",
)

assert_equal(
    evaluation["learning_signal"],
    "POSITIVE",
    "POSITIVE -> evaluation signal",
)

assert_equal(
    intelligence["outcome_learning_signal"],
    "POSITIVE",
    "POSITIVE -> intelligence signal",
)

assert_equal(
    intelligence["outcome_learning_signal_strength"],
    100.0,
    "POSITIVE -> intelligence signal strength",
)

assert_equal(
    strategy["outcome_learning_signal"],
    "POSITIVE",
    "POSITIVE -> strategy signal",
)

assert_equal(
    strategy["strategy"],
    "GROWTH",
    "POSITIVE -> adaptive strategy",
)

assert_equal(
    strategy["action"],
    "INCREASE_RISK",
    "POSITIVE -> adaptive action",
)


print("")
print("=" * 82)
print("CASE: NEGATIVE OUTCOME -> DEFENSIVE")
print("=" * 82)

evaluation, intelligence, strategy = evaluate_and_bridge(
    -10.0
)

print("evaluation:", evaluation)
print("outcome_intelligence:", intelligence)
print("adaptive_strategy:", strategy)

assert_equal(
    evaluation["outcome_status"],
    "EVALUATED",
    "NEGATIVE -> evaluation status",
)

assert_equal(
    evaluation["learning_signal"],
    "NEGATIVE",
    "NEGATIVE -> evaluation signal",
)

assert_equal(
    intelligence["outcome_learning_signal"],
    "NEGATIVE",
    "NEGATIVE -> intelligence signal",
)

assert_equal(
    intelligence["learning_status"],
    "ADAPTIVE_LEARNING_REQUIRED",
    "NEGATIVE -> intelligence learning status",
)

assert_equal(
    intelligence["adaptive_learning_required"],
    True,
    "NEGATIVE -> adaptive learning required",
)

assert_equal(
    strategy["outcome_learning_signal"],
    "NEGATIVE",
    "NEGATIVE -> strategy signal",
)

assert_equal(
    strategy["strategy"],
    "DEFENSIVE",
    "NEGATIVE -> adaptive strategy",
)

assert_equal(
    strategy["action"],
    "REDUCE_RISK",
    "NEGATIVE -> adaptive action",
)


print("")
print("=" * 82)
print("===== PHASE 7-10-19-2 CLOSED-LOOP BOUNDARY COMPLETE =====")
print("=" * 82)
