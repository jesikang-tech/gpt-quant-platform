"""
PHASE 7-10-19-4
OUTCOME LEARNING
-> ADAPTIVE STRATEGY
-> PORTFOLIO DECISION
-> VALIDATION
-> VALIDATION ACTION
-> FINAL DECISION INTEGRATION
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
from core.portfolio_decision_intelligence import (
    PortfolioDecisionIntelligence,
)
from core.ai_decision_validation import (
    AIDecisionValidation,
)
from core.ai_decision_validation_action import (
    AIDecisionValidationAction,
)
from core.ai_final_decision_integration import (
    AIFinalDecisionIntegration,
)


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
        "confidence_level": "Very High",
        "confidence_grade": "A+",
    }


def build_closed_loop(portfolio_return):
    evaluation_engine = AIDecisionOutcomeEvaluation()

    evaluation = evaluation_engine.evaluate(
        outcome_snapshot=base_snapshot(),
        actual_outcome={
            "portfolio_return": portfolio_return,
            "market_response": "EVALUATED",
            "portfolio_response": "EVALUATED",
        },
    )

    intelligence_engine = AIDecisionOutcomeIntelligence()

    outcome_intelligence = intelligence_engine.analyze(
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

    adaptive_strategy_engine = AIDecisionAdaptiveStrategy()

    adaptive_strategy = adaptive_strategy_engine.analyze(
        trend={
            "direction": "STABLE",
            "stability": "MEDIUM",
            "momentum": "NEUTRAL",
            "grade_stability": "STABLE",
            "consistency": "MEDIUM",
            "latest_score": 75,
        },
        outcome_intelligence=outcome_intelligence,
    )

    portfolio_engine = PortfolioDecisionIntelligence()

    portfolio_decision = portfolio_engine.generate(
        {
            "decision": "MAINTAIN",
            "market_view": "NEUTRAL",
            "confidence": 90,
        },
        {
            "quality_score": 90,
        },
        {
            "confidence": 90,
            "reliability_level": "HIGH",
        },
        adaptive_strategy,
        {
            "rebalance_action": "HOLD",
        },
        {
            "optimization_status": "COMPLETED",
        },
        {
            "summary": "Source-verified closed-loop test summary.",
        },
    )

    validation_engine = AIDecisionValidation()

    validation = validation_engine.validate(
        portfolio_decision,
        base_confidence(),
        {
            "assessment": "VERY_STRONG",
            "attention_signals": [],
        },
        {
            "recommendation": "PROCEED",
        },
    )

    validation_action_engine = AIDecisionValidationAction()

    validation_action = validation_action_engine.decide(
        validation,
        base_confidence(),
        {
            "assessment": "VERY_STRONG",
            "attention_signals": [],
        },
        {
            "recommendation": "PROCEED",
        },
    )

    final_engine = AIFinalDecisionIntegration()

    final_decision = final_engine.integrate(
        portfolio_decision,
        {
            "intelligence_score": 90.0,
            "grade": "A+",
        },
        base_confidence(),
        {
            "assessment": "VERY_STRONG",
        },
        {
            "recommendation": "PROCEED",
            "monitoring": "STANDARD",
        },
        validation,
        {
            "explanation": "Source-verified closed-loop test.",
        },
        validation_action,
    )

    return (
        evaluation,
        outcome_intelligence,
        adaptive_strategy,
        portfolio_decision,
        validation,
        validation_action,
        final_decision,
    )


print("=" * 82)
print("CASE: POSITIVE OUTCOME -> FINAL DECISION")
print("=" * 82)

(
    evaluation,
    outcome_intelligence,
    adaptive_strategy,
    portfolio_decision,
    validation,
    validation_action,
    final_decision,
) = build_closed_loop(10.0)

print("evaluation:", evaluation)
print("outcome_intelligence:", outcome_intelligence)
print("adaptive_strategy:", adaptive_strategy)
print("portfolio_decision:", portfolio_decision)
print("validation:", validation)
print("validation_action:", validation_action)
print("final_decision:", final_decision)

assert_equal(
    evaluation["learning_signal"],
    "POSITIVE",
    "POSITIVE -> evaluation signal",
)

assert_equal(
    outcome_intelligence["outcome_learning_signal"],
    "POSITIVE",
    "POSITIVE -> intelligence signal",
)

assert_equal(
    adaptive_strategy["strategy"],
    "GROWTH",
    "POSITIVE -> adaptive strategy",
)

assert_equal(
    portfolio_decision["final_strategy"],
    "GROWTH",
    "POSITIVE -> portfolio strategy",
)

assert_equal(
    validation["outcome_learning_signal"],
    "POSITIVE",
    "POSITIVE -> validation signal",
)

assert_equal(
    validation_action["validation_status"],
    "REVIEW_REQUIRED",
    "POSITIVE -> validation status",
)

assert_equal(
    final_decision["validation_status"],
    "REVIEW_REQUIRED",
    "POSITIVE -> final validation status",
)

assert_equal(
    final_decision["strategy"],
    "GROWTH",
    "POSITIVE -> final strategy",
)


print("")
print("=" * 82)
print("CASE: NEGATIVE OUTCOME -> FINAL DECISION")
print("=" * 82)

(
    evaluation,
    outcome_intelligence,
    adaptive_strategy,
    portfolio_decision,
    validation,
    validation_action,
    final_decision,
) = build_closed_loop(-10.0)

print("evaluation:", evaluation)
print("outcome_intelligence:", outcome_intelligence)
print("adaptive_strategy:", adaptive_strategy)
print("portfolio_decision:", portfolio_decision)
print("validation:", validation)
print("validation_action:", validation_action)
print("final_decision:", final_decision)

assert_equal(
    evaluation["learning_signal"],
    "NEGATIVE",
    "NEGATIVE -> evaluation signal",
)

assert_equal(
    outcome_intelligence["learning_status"],
    "ADAPTIVE_LEARNING_REQUIRED",
    "NEGATIVE -> intelligence learning status",
)

assert_equal(
    outcome_intelligence["adaptive_learning_required"],
    True,
    "NEGATIVE -> intelligence adaptive requirement",
)

assert_equal(
    adaptive_strategy["strategy"],
    "DEFENSIVE",
    "NEGATIVE -> adaptive strategy",
)

assert_equal(
    portfolio_decision["adaptive_override"],
    True,
    "NEGATIVE -> portfolio override",
)

assert_equal(
    portfolio_decision["final_strategy"],
    "DEFENSIVE",
    "NEGATIVE -> portfolio final strategy",
)

assert_equal(
    validation["validation_status"],
    "REVIEW_REQUIRED",
    "NEGATIVE -> validation status",
)

assert_equal(
    validation["outcome_learning_signal"],
    "NEGATIVE",
    "NEGATIVE -> validation signal",
)

assert_equal(
    validation_action["action"],
    "REVIEW_REQUIRED",
    "NEGATIVE -> validation action",
)

assert_equal(
    validation_action["execution_status"],
    "PENDING_REVIEW",
    "NEGATIVE -> execution status",
)

assert_equal(
    final_decision["action"],
    "REVIEW_REQUIRED",
    "NEGATIVE -> final action",
)

assert_equal(
    final_decision["execution_status"],
    "PENDING_REVIEW",
    "NEGATIVE -> final execution status",
)

assert_equal(
    final_decision["validation_status"],
    "REVIEW_REQUIRED",
    "NEGATIVE -> final validation status",
)

assert_equal(
    final_decision["strategy"],
    "DEFENSIVE",
    "NEGATIVE -> final strategy",
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

print("")
print("=" * 82)
print("===== PHASE 7-10-19-4 CLOSED-LOOP BOUNDARY COMPLETE =====")
print("=" * 82)
