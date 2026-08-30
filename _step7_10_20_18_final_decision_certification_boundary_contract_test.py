"""
PHASE 7-10-20-18
FINAL DECISION INTEGRATION
-> FINAL DECISION CERTIFICATION
BOUNDARY CONTRACT TEST V1
SOURCE-VERIFIED / MEMORY-ONLY / READ-ONLY
"""

from core.ai_final_decision_certification import (
    AIFinalDecisionCertification
)


engine = AIFinalDecisionCertification()


def assert_equal(actual, expected, label):
    if actual != expected:
        raise AssertionError(
            f"{label}: expected={expected!r}, actual={actual!r}"
        )
    print(f"{label}: PASS")


def build_inputs(
    *,
    final_decision=None,
    execution_decision=None,
    validation=None,
    governance=None,
    lifecycle=None,
    operational=None,
    integrated=None,
    orchestration=None,
):
    return {
        "final_decision": final_decision or {},
        "validation": validation or {},
        "governance": governance or {},
        "lifecycle": lifecycle or {},
        "operational_intelligence": operational or {},
        "integrated_intelligence": integrated or {},
        "orchestration": orchestration or {},
        "execution_decision": execution_decision or {},
    }


def analyze_case(name, inputs):
    print("")
    print("=" * 82)
    print(f"CASE: {name}")
    print("=" * 82)

    result = engine.analyze(**inputs)

    print("decision:", result.get("decision"))
    print("action:", result.get("action"))
    print("certification_status:", result.get("certification_status"))
    print("certification_action:", result.get("certification_action"))
    print("certification_risk:", result.get("certification_risk"))
    print("execution_readiness:", result.get("execution_readiness"))
    print("decision_integrity:", result.get("decision_integrity"))
    print("certification_score:", result.get("certification_score"))
    print("certification_grade:", result.get("certification_grade"))

    return result


# ================================================================
# CASE 1
# All required certification states are healthy.
# ================================================================

result = analyze_case(
    "ALL REQUIRED STATES -> CERTIFIED",
    build_inputs(
        final_decision={
            "decision": "MAINTAIN",
            "action": "PROCEED",
            "confidence_score": 100,
        },
        validation={
            "validation_status": "VALID",
            "validation_score": 100,
        },
        governance={
            "governance_status": "APPROVED",
            "governance_score": 100,
        },
        lifecycle={
            "lifecycle_status": "HEALTHY",
            "lifecycle_score": 100,
        },
        operational={
            "operational_status": "OPERATIONALLY_HEALTHY",
            "operational_score": 100,
        },
        integrated={
            "integrated_status": "INTEGRATED_HEALTHY",
            "integrated_score": 100,
        },
        orchestration={
            "orchestration_status": "ORCHESTRATION_READY",
            "orchestration_score": 100,
        },
        execution_decision={
            "decision": "MAINTAIN",
            "action": "PROCEED",
            "execution_status": "EXECUTION_READY",
            "execution_authorization": "AUTHORIZED",
            "execution_score": 100,
            "confidence_score": 100,
        },
    ),
)

assert_equal(
    result["certification_status"],
    "CERTIFIED",
    "all required states -> certified",
)
assert_equal(
    result["certification_action"],
    "PROCEED",
    "certified -> action preserved",
)
assert_equal(
    result["execution_readiness"],
    "READY",
    "certified + execution ready + authorized -> ready",
)
assert_equal(
    result["decision_integrity"],
    "INTACT",
    "certified + low risk -> integrity intact",
)


# ================================================================
# CASE 2
# A blocked certification state must dominate.
# ================================================================

result = analyze_case(
    "BLOCKED STATE -> CERTIFICATION BLOCKED",
    build_inputs(
        final_decision={
            "decision": "MAINTAIN",
            "action": "PROCEED",
            "confidence_score": 100,
        },
        validation={
            "validation_status": "VALID",
            "validation_score": 100,
        },
        governance={
            "governance_status": "APPROVED",
            "governance_score": 100,
        },
        lifecycle={
            "lifecycle_status": "HEALTHY",
            "lifecycle_score": 100,
        },
        operational={
            "operational_status": "OPERATIONALLY_HEALTHY",
            "operational_score": 100,
        },
        integrated={
            "integrated_status": "INTEGRATED_HEALTHY",
            "integrated_score": 100,
        },
        orchestration={
            "orchestration_status": "ORCHESTRATION_READY",
            "orchestration_score": 100,
        },
        execution_decision={
            "action": "PROCEED",
            "execution_status": "EXECUTION_READY",
            "execution_authorization": "BLOCKED",
            "execution_score": 100,
            "confidence_score": 100,
        },
    ),
)

assert_equal(
    result["certification_status"],
    "CERTIFICATION_BLOCKED",
    "blocked state -> certification blocked",
)
assert_equal(
    result["certification_action"],
    "HALT",
    "blocked certification -> halt",
)
assert_equal(
    result["certification_risk"],
    "CRITICAL",
    "blocked state -> critical risk",
)
assert_equal(
    result["execution_readiness"],
    "NOT_READY",
    "blocked certification -> not ready",
)


# ================================================================
# CASE 3
# A review state must produce certification review.
# ================================================================

result = analyze_case(
    "REVIEW STATE -> CERTIFICATION REVIEW",
    build_inputs(
        final_decision={
            "decision": "MAINTAIN",
            "action": "PROCEED",
            "confidence_score": 100,
        },
        validation={
            "validation_status": "VALID",
            "validation_score": 100,
        },
        governance={
            "governance_status": "WARNING",
            "governance_score": 80,
        },
        lifecycle={
            "lifecycle_status": "HEALTHY",
            "lifecycle_score": 100,
        },
        operational={
            "operational_status": "OPERATIONALLY_HEALTHY",
            "operational_score": 100,
        },
        integrated={
            "integrated_status": "INTEGRATED_HEALTHY",
            "integrated_score": 100,
        },
        orchestration={
            "orchestration_status": "ORCHESTRATION_READY",
            "orchestration_score": 100,
        },
        execution_decision={
            "action": "PROCEED",
            "execution_status": "EXECUTION_READY",
            "execution_authorization": "AUTHORIZED",
            "execution_score": 100,
            "confidence_score": 100,
        },
)
)

assert_equal(
    result["certification_status"],
    "CERTIFICATION_REVIEW",
    "review state -> certification review",
)
assert_equal(
    result["certification_action"],
    "REVIEW",
    "certification review -> review action",
)
assert_equal(
    result["certification_risk"],
    "MEDIUM",
    "review state -> medium risk",
)
assert_equal(
    result["decision_integrity"],
    "REVIEW_REQUIRED",
    "review certification -> integrity review",
)


# ================================================================
# CASE 4
# Missing required healthy states must not fabricate certification.
# ================================================================

result = analyze_case(
    "INCOMPLETE REQUIRED STATES -> SAFE REVIEW",
    build_inputs(
        final_decision={
            "decision": "MAINTAIN",
            "action": "PROCEED",
        },
        validation={
            "validation_status": "VALID",
            "validation_score": 90,
        },
        execution_decision={
            "action": "PROCEED",
            "execution_status": "EXECUTION_READY",
            "execution_authorization": "AUTHORIZED",
            "execution_score": 90,
        },
    ),
)

assert_equal(
    result["certification_status"],
    "CERTIFICATION_REVIEW",
    "incomplete required states -> review",
)
assert_equal(
    result["certification_action"],
    "REVIEW",
    "incomplete certification -> review action",
)
assert_equal(
    result["execution_readiness"],
    "NOT_READY",
    "incomplete certification -> not ready",
)


# ================================================================
# CASE 5
# final_decision action has priority over execution_decision action.
# ================================================================

result = analyze_case(
    "FINAL DECISION ACTION PRIORITY",
    build_inputs(
        final_decision={
            "decision": "MAINTAIN",
            "action": "PROCEED_WITH_MONITORING",
        },
        validation={
            "validation_status": "VALID",
        },
        governance={
            "governance_status": "APPROVED",
        },
        lifecycle={
            "lifecycle_status": "HEALTHY",
        },
        operational={
            "operational_status": "OPERATIONALLY_HEALTHY",
        },
        integrated={
            "integrated_status": "INTEGRATED_HEALTHY",
        },
        orchestration={
            "orchestration_status": "ORCHESTRATION_READY",
        },
        execution_decision={
            "action": "PROCEED",
            "execution_status": "EXECUTION_READY",
            "execution_authorization": "AUTHORIZED",
        },
    ),
)

assert_equal(
    result["action"],
    "PROCEED_WITH_MONITORING",
    "final decision action -> priority preserved",
)
assert_equal(
    result["certification_status"],
    "CERTIFIED",
    "priority case -> certified",
)


# ================================================================
# CASE 6
# Empty final_decision action falls back to execution_decision action.
# ================================================================

result = analyze_case(
    "EXECUTION DECISION ACTION FALLBACK",
    build_inputs(
        final_decision={
            "decision": "MAINTAIN",
        },
        validation={
            "validation_status": "VALID",
        },
        governance={
            "governance_status": "APPROVED",
        },
        lifecycle={
            "lifecycle_status": "HEALTHY",
        },
        operational={
            "operational_status": "OPERATIONALLY_HEALTHY",
        },
        integrated={
            "integrated_status": "INTEGRATED_HEALTHY",
        },
        orchestration={
            "orchestration_status": "ORCHESTRATION_READY",
        },
        execution_decision={
            "action": "PROCEED_WITH_MONITORING",
            "execution_status": "EXECUTION_READY",
            "execution_authorization": "AUTHORIZED",
        },
    ),
)

assert_equal(
    result["action"],
    "PROCEED_WITH_MONITORING",
    "execution decision -> action fallback",
)
assert_equal(
    result["certification_status"],
    "CERTIFIED",
    "fallback case -> certified",
)


# ================================================================
# CASE 7
# Certification score uses valid score inputs only.
# 8 scores of 100 -> 100 / A+.
# ================================================================

result = analyze_case(
    "CERTIFICATION SCORE -> VALID SCORES ONLY",
    build_inputs(
        final_decision={
            "decision": "MAINTAIN",
            "action": "PROCEED",
            "confidence_score": 100,
        },
        validation={
            "validation_status": "VALID",
            "validation_score": 100,
        },
        governance={
            "governance_status": "APPROVED",
            "governance_score": 100,
        },
        lifecycle={
            "lifecycle_status": "HEALTHY",
            "lifecycle_score": 100,
        },
        operational={
            "operational_status": "OPERATIONALLY_HEALTHY",
            "operational_score": 100,
        },
        integrated={
            "integrated_status": "INTEGRATED_HEALTHY",
            "integrated_score": 100,
        },
        orchestration={
            "orchestration_status": "ORCHESTRATION_READY",
            "orchestration_score": 100,
        },
        execution_decision={
            "execution_status": "EXECUTION_READY",
            "execution_authorization": "AUTHORIZED",
            "execution_score": 100,
            "confidence_score": 100,
        },
    ),
)

assert_equal(
    result["certification_score"],
    100.0,
    "all valid scores -> certification score",
)
assert_equal(
    result["certification_grade"],
    "A+",
    "certification score -> grade",
)


# ================================================================
# CASE 8
# Empty input must safely remain certification-blocked.
# ================================================================

result = analyze_case(
    "EMPTY INPUT -> SAFE DEFAULTS",
    build_inputs(),
)

assert_equal(
    result["decision"],
    "UNKNOWN",
    "empty input -> decision default",
)
assert_equal(
    result["action"],
    "HOLD",
    "empty input -> action default",
)
assert_equal(
    result["certification_status"],
    "CERTIFICATION_BLOCKED",
    "empty input -> certification blocked",
)
assert_equal(
    result["certification_action"],
    "HALT",
    "empty input -> halt action",
)
assert_equal(
    result["execution_readiness"],
    "NOT_READY",
    "empty input -> not ready",
)


# ================================================================
# CASE 9
# Certification must not fabricate learning fields.
# ================================================================

result = analyze_case(
    "LEARNING FIELDS NOT FABRICATED",
    build_inputs(
        final_decision={
            "decision": "MAINTAIN",
            "action": "PROCEED",
        },
        validation={
            "validation_status": "VALID",
        },
    ),
)

assert_equal(
    "outcome_learning_signal" in result,
    False,
    "learning signal -> not fabricated",
)
assert_equal(
    "outcome_learning_signal_strength" in result,
    False,
    "learning strength -> not fabricated",
)
assert_equal(
    "adaptive_learning_required" in result,
    False,
    "adaptive learning requirement -> not fabricated",
)


print("")
print("=" * 82)
print("===== PHASE 7-10-20-18 FINAL DECISION -> CERTIFICATION COMPLETE =====")
print("=" * 82)
