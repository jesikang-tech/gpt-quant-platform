"""
PHASE 7-10-20-17
AI DECISION VALIDATION
-> VALIDATION ACTION
BOUNDARY CONTRACT TEST V1
SOURCE-VERIFIED / MEMORY-ONLY / READ-ONLY
"""

from core.ai_decision_validation_action import (
    AIDecisionValidationAction
)


engine = AIDecisionValidationAction()


def assert_equal(actual, expected, label):
    if actual != expected:
        raise AssertionError(
            f"{label}: expected={expected!r}, actual={actual!r}"
        )

    print(f"{label}: PASS")


def run_case(
    name,
    validation,
    confidence=None,
    recommendation=None,
    expected_action=None,
    expected_execution_status=None,
    expected_monitoring=None,
    expected_risk_level=None
):
    result = engine.decide(
        validation=validation,
        confidence=confidence or {},
        recommendation=recommendation or {}
    )

    print("")
    print("=" * 82)
    print(f"CASE: {name}")
    print("=" * 82)

    assert_equal(
        result["action"],
        expected_action,
        f"{name} -> action"
    )

    assert_equal(
        result["execution_status"],
        expected_execution_status,
        f"{name} -> execution status"
    )

    assert_equal(
        result["monitoring"],
        expected_monitoring,
        f"{name} -> monitoring"
    )

    assert_equal(
        result["risk_level"],
        expected_risk_level,
        f"{name} -> risk level"
    )

    return result


# ================================================================
# CASE 1
# INVALID must block execution.
# ================================================================

run_case(
    "INVALID -> BLOCK EXECUTION",
    {
        "validation": "INVALID",
        "validation_score": 50,
        "decision": "MAINTAIN",
        "strategy_mode": "BALANCED",
        "decision_alignment": "CONFLICT",
        "decision_consistency": "CONFLICT",
    },
    {
        "confidence_score": 50,
        "confidence_level": "LOW",
    },
    {
        "recommendation": "PROCEED",
    },
    "BLOCK_EXECUTION",
    "BLOCKED",
    "CRITICAL",
    "CRITICAL",
)


# ================================================================
# ================================================================
# CASE 2
# REVIEW_REQUIRED with sufficient confidence and validation
# may proceed with monitoring.
# ================================================================

run_case(
    "REVIEW_REQUIRED + STRONG THRESHOLD -> MONITORED PROCEED",
    {
        "validation": "REVIEW_REQUIRED",
        "validation_score": 70,
        "decision": "MAINTAIN",
        "strategy_mode": "BALANCED",
        "decision_alignment": "ALIGNED",
        "decision_consistency": "CONSISTENT",
    },
    {
        "confidence_score": 80,
        "confidence_level": "HIGH",
    },
    {
        "recommendation": "PROCEED",
    },
    "PROCEED_WITH_MONITORING",
    "AUTHORIZED_WITH_MONITORING",
    "ELEVATED",
    "MEDIUM",
)




# ================================================================
# CASE 3
# REVIEW_REQUIRED with insufficient confidence must remain
# under review.
# ================================================================

run_case(
    "REVIEW_REQUIRED + LOW CONFIDENCE -> REVIEW",
    {
        "validation": "REVIEW_REQUIRED",
        "validation_score": 70,
        "decision": "MAINTAIN",
        "strategy_mode": "BALANCED",
        "decision_alignment": "ALIGNED",
        "decision_consistency": "CONSISTENT",
    },
    {
        "confidence_score": 79,
        "confidence_level": "MEDIUM",
    },
    {
        "recommendation": "PROCEED",
    },
    "REVIEW_REQUIRED",
    "PENDING_REVIEW",
    "HIGH",
    "MEDIUM",
)


# ================================================================
# CASE 4
# VALID + strong scores + PROCEED recommendation
# must authorize execution.
# ================================================================

run_case(
    "VALID + STRONG + PROCEED -> AUTHORIZED",
    {
        "validation": "VALID",
        "validation_score": 90,
        "decision": "MAINTAIN",
        "strategy_mode": "BALANCED",
        "decision_alignment": "ALIGNED",
        "decision_consistency": "CONSISTENT",
    },
    {
        "confidence_score": 90,
        "confidence_level": "VERY_HIGH",
    },
    {
        "recommendation": "PROCEED",
    },
    "PROCEED",
    "AUTHORIZED",
    "STANDARD",
    "LOW",
)


# ================================================================
# CASE 5
# VALID + strong scores + monitoring recommendation
# must preserve monitored execution.
# ================================================================

run_case(
    "VALID + STRONG + MONITORING -> MONITORED PROCEED",
    {
        "validation": "VALID",
        "validation_score": 95,
        "decision": "MAINTAIN",
        "strategy_mode": "BALANCED",
        "decision_alignment": "ALIGNED",
        "decision_consistency": "CONSISTENT",
    },
    {
        "confidence_score": 95,
        "confidence_level": "VERY_HIGH",
    },
    {
        "recommendation": "PROCEED_WITH_MONITORING",
    },
    "PROCEED_WITH_MONITORING",
    "AUTHORIZED_WITH_MONITORING",
    "ELEVATED",
    "LOW",
)


# ================================================================
# CASE 6
# VALID but below strong validation threshold must not authorize
# direct execution.
# ================================================================

run_case(
    "VALID + BELOW STRONG THRESHOLD -> MONITORED PROCEED",
    {
        "validation": "VALID",
        "validation_score": 89,
        "decision": "MAINTAIN",
        "strategy_mode": "BALANCED",
        "decision_alignment": "ALIGNED",
        "decision_consistency": "CONSISTENT",
    },
    {
        "confidence_score": 95,
        "confidence_level": "VERY_HIGH",
    },
    {
        "recommendation": "PROCEED",
    },
    "PROCEED_WITH_MONITORING",
    "AUTHORIZED_WITH_MONITORING",
    "ELEVATED",
    "MEDIUM",
)


# ================================================================
# CASE 7
# EMPTY validation must use safe defaults.
# ================================================================

run_case(
    "EMPTY VALIDATION -> SAFE REVIEW",
    {},
    {},
    {},
    "REVIEW_REQUIRED",
    "PENDING_REVIEW",
    "HIGH",
    "HIGH",
)


# ================================================================
# CASE 8
# Identity and validation fields must be propagated.
# ================================================================

print("")
print("=" * 82)
print("CASE: VALIDATION INPUTS PRESERVED")
print("=" * 82)

result = engine.decide(
    validation={
        "validation": "VALID",
        "validation_score": 96,
        "decision": "ACCUMULATE",
        "strategy_mode": "GROWTH",
        "adaptive_action": "INCREASE_RISK",
        "decision_alignment": "ALIGNED",
        "decision_consistency": "CONSISTENT",
        "reliability": "HIGH",
        "optimization_status": "OPTIMIZED",
    },
    confidence={
        "confidence_score": 96,
        "confidence_level": "VERY_HIGH",
    },
    recommendation={
        "recommendation": "PROCEED",
    }
)

assert_equal(
    result["decision"],
    "ACCUMULATE",
    "decision identity -> preserved"
)

assert_equal(
    result["strategy_mode"],
    "GROWTH",
    "strategy mode -> preserved"
)

assert_equal(
    result["adaptive_action"],
    "INCREASE_RISK",
    "adaptive action -> preserved"
)

assert_equal(
    result["decision_alignment"],
    "ALIGNED",
    "decision alignment -> preserved"
)

assert_equal(
    result["decision_consistency"],
    "CONSISTENT",
    "decision consistency -> preserved"
)

assert_equal(
    result["confidence_score"],
    96,
    "confidence score -> preserved"
)

assert_equal(
    result["reliability"],
    "HIGH",
    "reliability -> preserved"
)

assert_equal(
    result["optimization_status"],
    "OPTIMIZED",
    "optimization status -> preserved"
)


# ================================================================
# CASE 9
# Recommendation input takes precedence over validation fallback.
# ================================================================

print("")
print("=" * 82)
print("CASE: RECOMMENDATION INPUT PRIORITY")
print("=" * 82)

result = engine.decide(
    validation={
        "validation": "VALID",
        "validation_score": 95,
        "decision": "MAINTAIN",
        "strategy_mode": "BALANCED",
    },
    confidence={
        "confidence_score": 95,
        "confidence_level": "VERY_HIGH",
    },
    recommendation={
        "recommendation": "PROCEED_WITH_MONITORING",
    }
)

assert_equal(
    result["action"],
    "PROCEED_WITH_MONITORING",
    "recommendation input -> action priority"
)

assert_equal(
    result["execution_status"],
    "AUTHORIZED_WITH_MONITORING",
    "recommendation input -> execution status"
)

assert_equal(
    result["monitoring"],
    "ELEVATED",
    "recommendation input -> monitoring"
)


# ================================================================
# CASE 10
# Learning fields are not fabricated by Validation Action.
# ================================================================

print("")
print("=" * 82)
print("CASE: LEARNING FIELDS NOT FABRICATED")
print("=" * 82)

result = engine.decide(
    validation={
        "validation": "VALID",
        "validation_score": 95,
        "decision": "MAINTAIN",
        "strategy_mode": "BALANCED",
    },
    confidence={
        "confidence_score": 95,
        "confidence_level": "VERY_HIGH",
    },
    recommendation={
        "recommendation": "PROCEED",
    }
)

assert_equal(
    "outcome_learning_signal" in result,
    False,
    "learning signal -> not fabricated"
)

assert_equal(
    "outcome_learning_signal_strength" in result,
    False,
    "learning strength -> not fabricated"
)

assert_equal(
    "adaptive_learning_required" in result,
    False,
    "adaptive learning requirement -> not fabricated"
)


print("")
print("=" * 82)
print("===== PHASE 7-10-20-17 VALIDATION -> ACTION COMPLETE =====")
print("=" * 82)
