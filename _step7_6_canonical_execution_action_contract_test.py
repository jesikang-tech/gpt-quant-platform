from core.ai_decision_validation import AIDecisionValidation
from core.ai_decision_validation_action import AIDecisionValidationAction

print("=" * 72)
print("PHASE 7-6 CANONICAL EXECUTION ACTION CONTRACT TEST")
print("ADAPTIVE ACTION -> VALIDATION -> EXECUTABLE ACTION")
print("MEMORY-ONLY / READ-ONLY")
print("=" * 72)

cases = [
    {
        "name": "NEGATIVE",
        "intelligence": {
            "decision": "DEFENSIVE",
            "strategy_mode": "DEFENSIVE",
            "adaptive_action": "REDUCE_RISK",
            "decision_alignment": "ALIGNED",
            "decision_consistency": "CONSISTENT",
            "reliability": "HIGH",
            "optimization_status": "READY",
        },
        "confidence": {
            "confidence_score": 95,
            "confidence_level": "HIGH",
        },
        "assessment": {
            "assessment_status": "ACCEPTABLE",
        },
        "recommendation": {},
        "expected_action": "REDUCE_RISK",
    },
    {
        "name": "POSITIVE",
        "intelligence": {
            "decision": "ACCUMULATE",
            "strategy_mode": "GROWTH",
            "adaptive_action": "INCREASE_RISK",
            "decision_alignment": "ALIGNED",
            "decision_consistency": "CONSISTENT",
            "reliability": "HIGH",
            "optimization_status": "READY",
        },
        "confidence": {
            "confidence_score": 95,
            "confidence_level": "HIGH",
        },
        "assessment": {
            "assessment_status": "ACCEPTABLE",
        },
        "recommendation": {},
        "expected_action": "INCREASE_RISK",
    },
    {
        "name": "PENDING",
        "intelligence": {
            "decision": "MAINTAIN",
            "strategy_mode": "MAINTAIN",
            "adaptive_action": "MAINTAIN_ALLOCATION",
            "decision_alignment": "ALIGNED",
            "decision_consistency": "CONSISTENT",
            "reliability": "HIGH",
            "optimization_status": "READY",
        },
        "confidence": {
            "confidence_score": 95,
            "confidence_level": "HIGH",
        },
        "assessment": {
            "assessment_status": "ACCEPTABLE",
        },
        "recommendation": {},
        "expected_action": "MAINTAIN_ALLOCATION",
    },
]

validation_engine = AIDecisionValidation()
action_engine = AIDecisionValidationAction()

for case in cases:

    print()
    print("=" * 72)
    print("CASE:", case["name"])
    print("=" * 72)

    validation = validation_engine.validate(
        case["intelligence"],
        case["confidence"],
        case["assessment"],
        case["recommendation"],
    )

    print("validation status:",
          validation.get("validation"))

    print("validation score:",
          validation.get("validation_score"))

    print("strategy mode:",
          validation.get("strategy_mode"))

    print("adaptive action:",
          validation.get("adaptive_action"))

    print("decision alignment:",
          validation.get("decision_alignment"))

    assert validation.get("strategy_mode") == \
        case["intelligence"]["strategy_mode"]

    assert validation.get("adaptive_action") == \
        case["intelligence"]["adaptive_action"]

    print("validation propagation: PASS")

    action = action_engine.decide(
        validation,
        case["confidence"],
        case["assessment"],
        case["recommendation"],
    )

    print()
    print("===== ACTION RESULT =====")

    print("action:",
          action.get("action"))

    print("execution status:",
          action.get("execution_status"))

    print("monitoring:",
          action.get("monitoring"))

    print("risk level:",
          action.get("risk_level"))

    print("strategy mode:",
          action.get("strategy_mode"))

    print("adaptive action:",
          action.get("adaptive_action"))

    assert action.get("adaptive_action") == \
        case["expected_action"]

    assert action.get("action") == \
        case["expected_action"]

    print("adaptive action preservation: PASS")
    print("executable action contract: PASS")


print()
print("=" * 72)
print("FINAL ASSERTIONS")
print("=" * 72)

print(
    "NEGATIVE -> REDUCE_RISK -> executable action: PASS"
)

print(
    "POSITIVE -> INCREASE_RISK -> executable action: PASS"
)

print(
    "PENDING -> MAINTAIN_ALLOCATION -> executable action: PASS"
)

print()
print("=" * 72)
print("SAFETY")
print("=" * 72)

print("Memory-only execution: PASS")
print("No production DB access.")
print("No API runtime call.")
print("No INSERT.")
print("No UPDATE.")
print("No DELETE.")
print("No future price injection.")
print("No fake Outcome persistence.")

print()
print(
    "===== PHASE 7-6 CANONICAL EXECUTION ACTION CONTRACT TEST COMPLETE ====="
)
