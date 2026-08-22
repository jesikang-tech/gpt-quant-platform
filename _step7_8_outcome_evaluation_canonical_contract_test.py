from core.ai_decision_outcome_evaluation import (
    AIDecisionOutcomeEvaluation,
)

print("=" * 82)
print("PHASE 7-8 OUTCOME EVALUATION CANONICAL CONTRACT TEST")
print("SCORE -> SIGNAL -> STRENGTH")
print("MEMORY-ONLY / READ-ONLY")
print("=" * 82)

engine = AIDecisionOutcomeEvaluation()

snapshot = {
    "decision": "TEST_DECISION",
    "action": "TEST_ACTION",
    "strategy": "TEST_STRATEGY",
    "snapshot_status": "COLLECTED",
    "snapshot_purpose": "MEMORY_ONLY_CONTRACT_TEST",
}

cases = [
    {
        "name": "SCORE_90",
        "score": 90.0,
        "signal": "POSITIVE",
        "strength": 80.0,
    },
    {
        "name": "SCORE_80",
        "score": 80.0,
        "signal": "POSITIVE",
        "strength": 60.0,
    },
    {
        "name": "SCORE_70",
        "score": 70.0,
        "signal": "STABLE",
        "strength": 40.0,
    },
    {
        "name": "SCORE_60",
        "score": 60.0,
        "signal": "STABLE",
        "strength": 20.0,
    },
    {
        "name": "SCORE_50",
        "score": 50.0,
        "signal": "NEGATIVE",
        "strength": 0.0,
    },
    {
        "name": "SCORE_40",
        "score": 40.0,
        "signal": "NEGATIVE",
        "strength": 20.0,
    },
]

for case in cases:
    print()
    print("=" * 82)
    print("CASE:", case["name"])
    print("=" * 82)

    result = engine.evaluate(
        outcome_snapshot=snapshot,
        actual_outcome={
            "outcome_score": case["score"],
            "market_response": "EVALUATED",
            "portfolio_response": "EVALUATED",
        },
    )

    evaluation_status = result.get("evaluation_status")
    outcome_status = result.get("outcome_status")
    outcome_score = result.get("outcome_score")
    signal = result.get("learning_signal")
    strength = result.get("learning_signal_strength")
    learning_status = result.get("learning_status")

    print("evaluation status:", evaluation_status)
    print("outcome status:", outcome_status)
    print("outcome score:", outcome_score)
    print("learning signal:", signal)
    print("learning strength:", strength)
    print("learning status:", learning_status)

    assert evaluation_status == "EVALUATED"
    assert outcome_status == "EVALUATED"
    assert outcome_score == case["score"]
    assert signal == case["signal"]
    assert strength == case["strength"]
    assert learning_status == "LEARNING_AVAILABLE"

    print("canonical signal contract: PASS")
    print("canonical strength contract: PASS")
    print("evaluation contract: PASS")


print()
print("=" * 82)
print("CASE: WAITING_FOR_OUTCOME")
print("=" * 82)

pending = engine.evaluate(
    outcome_snapshot=snapshot,
    actual_outcome={},
)

print("evaluation status:", pending.get("evaluation_status"))
print("outcome status:", pending.get("outcome_status"))
print("outcome score:", pending.get("outcome_score"))
print("learning signal:", pending.get("learning_signal"))
print("learning strength:", pending.get("learning_signal_strength"))
print("learning status:", pending.get("learning_status"))

assert pending.get("evaluation_status") == "WAITING_FOR_OUTCOME"
assert pending.get("outcome_status") == "PENDING"
assert pending.get("outcome_score") == 0.0
assert pending.get("learning_signal") == "NONE"
assert pending.get("learning_signal_strength") == 0.0
assert pending.get("learning_status") == "WAITING_FOR_OUTCOME"

print("pending contract: PASS")


print()
print("=" * 82)
print("FINAL ASSERTIONS")
print("=" * 82)

print("90 -> POSITIVE -> 80.0: PASS")
print("80 -> POSITIVE -> 60.0: PASS")
print("70 -> STABLE -> 40.0: PASS")
print("60 -> STABLE -> 20.0: PASS")
print("50 -> NEGATIVE -> 0.0: PASS")
print("40 -> NEGATIVE -> 20.0: PASS")
print("EMPTY OUTCOME -> NONE -> 0.0: PASS")


print()
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

print()
print("=" * 82)
print("===== PHASE 7-8 OUTCOME EVALUATION CANONICAL CONTRACT TEST COMPLETE =====")
print("=" * 82)
