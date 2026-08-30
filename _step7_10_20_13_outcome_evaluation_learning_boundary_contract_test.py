from core.ai_decision_outcome_evaluation import (
    AIDecisionOutcomeEvaluation,
)


def assert_equal(actual, expected, label):
    if actual != expected:
        raise AssertionError(
            f"{label}: expected={expected!r}, actual={actual!r}"
        )
    print(f"{label}: PASS")


print("=" * 82)
print("PHASE 7-10-20-13")
print("OUTCOME HISTORY -> OUTCOME EVALUATION / LEARNING")
print("BOUNDARY CONTRACT TEST V1")
print("SOURCE-VERIFIED / MEMORY-ONLY / READ-ONLY")
print("=" * 82)

engine = AIDecisionOutcomeEvaluation()

snapshot = {
    "decision": "ACCUMULATE",
    "action": "PROCEED",
    "strategy": "GROWTH",
    "snapshot_status": "COLLECTED",
    "snapshot_purpose": "FUTURE_OUTCOME_EVALUATION",
}


print("")
print("=" * 82)
print("CASE: NO ACTUAL OUTCOME -> WAITING")
print("=" * 82)

waiting = engine.evaluate(
    outcome_snapshot=snapshot,
    actual_outcome=None,
)

assert_equal(
    waiting["evaluation_status"],
    "WAITING_FOR_OUTCOME",
    "missing outcome -> waiting status",
)

assert_equal(
    waiting["outcome_status"],
    "PENDING",
    "missing outcome -> pending status",
)

assert_equal(
    waiting["outcome_score"],
    0.0,
    "missing outcome -> score remains zero",
)

assert_equal(
    waiting["outcome_grade"],
    "N/A",
    "missing outcome -> grade N/A",
)

assert_equal(
    waiting["decision_effectiveness"],
    "PENDING",
    "missing outcome -> decision effectiveness pending",
)

assert_equal(
    waiting["strategy_effectiveness"],
    "PENDING",
    "missing outcome -> strategy effectiveness pending",
)

assert_equal(
    waiting["market_response"],
    "PENDING",
    "missing outcome -> market response pending",
)

assert_equal(
    waiting["portfolio_response"],
    "PENDING",
    "missing outcome -> portfolio response pending",
)

assert_equal(
    waiting["learning_status"],
    "WAITING_FOR_OUTCOME",
    "missing outcome -> learning waiting",
)

assert_equal(
    waiting["learning_signal"],
    "NONE",
    "missing outcome -> learning signal none",
)

assert_equal(
    waiting["learning_signal_strength"],
    0.0,
    "missing outcome -> learning signal strength zero",
)

assert_equal(
    waiting["actual_outcome_available"],
    False,
    "missing outcome -> availability false",
)


print("")
print("=" * 82)
print("CASE: SNAPSHOT IDENTITY PRESERVED WHILE WAITING")
print("=" * 82)

assert_equal(
    waiting["decision"],
    "ACCUMULATE",
    "waiting -> decision preserved",
)

assert_equal(
    waiting["action"],
    "PROCEED",
    "waiting -> action preserved",
)

assert_equal(
    waiting["strategy"],
    "GROWTH",
    "waiting -> strategy preserved",
)

assert_equal(
    waiting["snapshot_status"],
    "COLLECTED",
    "waiting -> snapshot status preserved",
)

assert_equal(
    waiting["snapshot_purpose"],
    "FUTURE_OUTCOME_EVALUATION",
    "waiting -> snapshot purpose preserved",
)


print("")
print("=" * 82)
print("CASE: NO ACTUAL OUTCOME DOES NOT FABRICATE PERFORMANCE")
print("=" * 82)

assert_equal(
    waiting["outcome_score"],
    0.0,
    "no outcome -> no fabricated score",
)

assert_equal(
    waiting["outcome_grade"],
    "N/A",
    "no outcome -> no fabricated grade",
)

assert_equal(
    waiting["decision_effectiveness"],
    "PENDING",
    "no outcome -> no fabricated decision effectiveness",
)

assert_equal(
    waiting["strategy_effectiveness"],
    "PENDING",
    "no outcome -> no fabricated strategy effectiveness",
)


print("")
print("=" * 82)
print("CASE: ACTUAL OUTCOME -> EVALUATED")
print("=" * 82)

actual_outcome = {
    "outcome_score": 92.0,
    "market_response": "POSITIVE",
    "portfolio_response": "POSITIVE",
}

evaluated = engine.evaluate(
    outcome_snapshot=snapshot,
    actual_outcome=actual_outcome,
)

assert_equal(
    evaluated["evaluation_status"],
    "EVALUATED",
    "actual outcome -> evaluated status",
)

assert_equal(
    evaluated["outcome_status"],
    "EVALUATED",
    "actual outcome -> outcome status",
)

assert_equal(
    evaluated["outcome_score"],
    92.0,
    "actual outcome -> score",
)

assert_equal(
    evaluated["outcome_grade"],
    "A",
    "actual outcome -> grade",
)

assert_equal(
    evaluated["decision_effectiveness"],
    "EFFECTIVE",
    "actual outcome -> decision effectiveness",
)

assert_equal(
    evaluated["strategy_effectiveness"],
    "EFFECTIVE",
    "actual outcome -> strategy effectiveness",
)

assert_equal(
    evaluated["market_response"],
    "POSITIVE",
    "actual outcome -> market response",
)

assert_equal(
    evaluated["portfolio_response"],
    "POSITIVE",
    "actual outcome -> portfolio response",
)


print("")
print("=" * 82)
print("CASE: EVALUATED OUTCOME -> LEARNING AVAILABLE")
print("=" * 82)

assert_equal(
    evaluated["learning_status"],
    "LEARNING_AVAILABLE",
    "evaluated -> learning available",
)

assert_equal(
    evaluated["actual_outcome_available"],
    True,
    "evaluated -> outcome available",
)

assert_equal(
    evaluated["learning_signal"],
    "POSITIVE",
    "evaluated -> positive learning signal",
)

assert_equal(
    evaluated["learning_signal_strength"],
    84.0,
    "evaluated -> learning signal strength",
)


print("")
print("=" * 82)
print("CASE: SNAPSHOT IDENTITY PRESERVED AFTER EVALUATION")
print("=" * 82)

assert_equal(
    evaluated["decision"],
    "ACCUMULATE",
    "evaluated -> decision preserved",
)

assert_equal(
    evaluated["action"],
    "PROCEED",
    "evaluated -> action preserved",
)

assert_equal(
    evaluated["strategy"],
    "GROWTH",
    "evaluated -> strategy preserved",
)

assert_equal(
    evaluated["snapshot_status"],
    "COLLECTED",
    "evaluated -> snapshot status preserved",
)

assert_equal(
    evaluated["snapshot_purpose"],
    "FUTURE_OUTCOME_EVALUATION",
    "evaluated -> snapshot purpose preserved",
)


print("")
print("=" * 82)
print("CASE: ACTUAL OUTCOME RESPONSE FALLBACK")
print("=" * 82)

fallback_outcome = {
    "outcome_score": 75.0,
}

fallback = engine.evaluate(
    outcome_snapshot=snapshot,
    actual_outcome=fallback_outcome,
)

assert_equal(
    fallback["market_response"],
    "EVALUATED",
    "missing market response -> evaluated fallback",
)

assert_equal(
    fallback["portfolio_response"],
    "EVALUATED",
    "missing portfolio response -> evaluated fallback",
)


print("")
print("=" * 82)
print("===== PHASE 7-10-20-13 OUTCOME EVALUATION / LEARNING BOUNDARY COMPLETE =====")
print("=" * 82)
