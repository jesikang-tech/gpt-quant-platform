from core.ai_decision_validation import AIDecisionValidation

print("=" * 82)
print("PHASE 7-8 PORTFOLIO -> VALIDATION PROPAGATION CONTRACT TEST")
print("SOURCE-VERIFIED CANONICAL POLICY")
print("MEMORY-ONLY / READ-ONLY")
print("=" * 82)

engine = AIDecisionValidation()

cases = [
    {
        "name": "DEFENSIVE",
        "intelligence": {
            "decision": "DEFENSIVE",
            "strategy_mode": "DEFENSIVE",
            "adaptive_action": "REDUCE_RISK",
            "decision_alignment": "ALIGNED",
            "decision_consistency": "CONSISTENT",
            "confidence": 90,
            "reliability": "HIGH",
            "optimization_status": "COMPLETED",
            "adaptive_override": False,
        },
        "expected": {
            "strategy_mode": "DEFENSIVE",
            "adaptive_action": "REDUCE_RISK",
        },
    },
    {
        "name": "GROWTH",
        "intelligence": {
            "decision": "ACCUMULATE",
            "strategy_mode": "GROWTH",
            "adaptive_action": "INCREASE_RISK",
            "decision_alignment": "ALIGNED",
            "decision_consistency": "CONSISTENT",
            "confidence": 90,
            "reliability": "HIGH",
            "optimization_status": "COMPLETED",
            "adaptive_override": False,
        },
        "expected": {
            "strategy_mode": "GROWTH",
            "adaptive_action": "INCREASE_RISK",
        },
    },
    {
        "name": "BALANCED",
        "intelligence": {
            "decision": "ACCUMULATE",
            "strategy_mode": "BALANCED",
            "adaptive_action": "MAINTAIN_BALANCE",
            "decision_alignment": "ALIGNED",
            "decision_consistency": "CONSISTENT",
            "confidence": 90,
            "reliability": "HIGH",
            "optimization_status": "COMPLETED",
            "adaptive_override": False,
        },
        "expected": {
            "strategy_mode": "BALANCED",
            "adaptive_action": "MAINTAIN_BALANCE",
        },
    },
    {
        "name": "MAINTAIN",
        "intelligence": {
            "decision": "MAINTAIN",
            "strategy_mode": "MAINTAIN",
            "adaptive_action": "MAINTAIN_ALLOCATION",
            "decision_alignment": "ALIGNED",
            "decision_consistency": "CONSISTENT",
            "confidence": 90,
            "reliability": "HIGH",
            "optimization_status": "COMPLETED",
            "adaptive_override": False,
        },
        "expected": {
            "strategy_mode": "MAINTAIN",
            "adaptive_action": "MAINTAIN_ALLOCATION",
        },
    },
]

for case in cases:
    print("")
    print("=" * 82)
    print(f"CASE: {case['name']}")
    print("=" * 82)

    intelligence = case["intelligence"]

    validation = engine.validate(
        intelligence=intelligence,
        confidence={
            "confidence_score": intelligence["confidence"],
            "confidence_level": "HIGH",
        },
        assessment={
            "attention_signals": [],
        },
        recommendation={
            "recommendation": "PROCEED",
        },
    )

    strategy_mode = validation.get("strategy_mode")
    adaptive_action = validation.get("adaptive_action")

    print("validation status:", validation.get("validation_status"))
    print("validation score:", validation.get("validation_score"))
    print("strategy mode:", strategy_mode)
    print("adaptive action:", adaptive_action)
    print("decision alignment:", validation.get("decision_alignment"))
    print("decision consistency:", validation.get("decision_consistency"))

    assert strategy_mode == case["expected"]["strategy_mode"]
    assert adaptive_action == case["expected"]["adaptive_action"]

    print("strategy propagation: PASS")
    print("adaptive action propagation: PASS")
    print("VALIDATION PROPAGATION CONTRACT: PASS")

print("")
print("=" * 82)
print("FINAL ASSERTIONS")
print("=" * 82)
print("DEFENSIVE -> REDUCE_RISK -> VALIDATION: PASS")
print("GROWTH -> INCREASE_RISK -> VALIDATION: PASS")
print("BALANCED -> MAINTAIN_BALANCE -> VALIDATION: PASS")
print("MAINTAIN -> MAINTAIN_ALLOCATION -> VALIDATION: PASS")

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
print("===== PHASE 7-8 PORTFOLIO -> VALIDATION PROPAGATION TEST COMPLETE =====")
print("=" * 82)
