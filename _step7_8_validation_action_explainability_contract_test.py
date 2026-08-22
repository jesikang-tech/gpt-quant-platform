from core.ai_decision_validation import AIDecisionValidation
from core.ai_decision_validation_action import AIDecisionValidationAction
from core.ai_decision_validation_explainability import AIDecisionValidationExplainability

print("=" * 82)
print("PHASE 7-8 VALIDATION -> ACTION / EXPLAINABILITY CONTRACT TEST")
print("SOURCE-VERIFIED CANONICAL POLICY")
print("MEMORY-ONLY / READ-ONLY")
print("=" * 82)

validation_engine = AIDecisionValidation()
action_engine = AIDecisionValidationAction()
explainability_engine = AIDecisionValidationExplainability()

cases = [
    {
        "name": "DEFENSIVE",
        "intelligence": {
            "decision": "DEFENSIVE",
            "strategy_mode": "DEFENSIVE",
            "adaptive_action": "REDUCE_RISK",
            "decision_alignment": "ALIGNED",
            "decision_consistency": "CONSISTENT",
            "confidence_score": 95,
            "confidence_level": "HIGH",
            "reliability": "HIGH",
            "optimization_status": "COMPLETED",
            "validation_score": 100,
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
            "confidence_score": 95,
            "confidence_level": "HIGH",
            "reliability": "HIGH",
            "optimization_status": "COMPLETED",
            "validation_score": 100,
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
            "confidence_score": 95,
            "confidence_level": "HIGH",
            "reliability": "HIGH",
            "optimization_status": "COMPLETED",
            "validation_score": 100,
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
            "confidence_score": 95,
            "confidence_level": "HIGH",
            "reliability": "HIGH",
            "optimization_status": "COMPLETED",
            "validation_score": 100,
        },
    },
]

for case in cases:
    print("")
    print("=" * 82)
    print(f"CASE: {case['name']}")
    print("=" * 82)

    intelligence = case["intelligence"]

    confidence = {
        "confidence_score": intelligence["confidence_score"],
        "confidence_level": intelligence["confidence_level"],
    }

    assessment = {
        "attention_signals": [],
    }

    recommendation = {
        "recommendation": "PROCEED",
    }

    validation = validation_engine.validate(
        intelligence=intelligence,
        confidence=confidence,
        assessment=assessment,
        recommendation=recommendation,
    )

    print("validation status:", validation.get("validation_status"))
    print("validation score:", validation.get("validation_score"))
    print("strategy mode:", validation.get("strategy_mode"))
    print("adaptive action:", validation.get("adaptive_action"))

    assert validation.get("validation_status") == "VALID"
    assert validation.get("strategy_mode") == intelligence["strategy_mode"]
    assert validation.get("adaptive_action") == intelligence["adaptive_action"]

    print("validation contract: PASS")

    action = action_engine.decide(
        validation=validation,
        confidence=confidence,
        assessment=assessment,
        recommendation=recommendation,
    )

    print("executable action:", action.get("action"))
    print("execution status:", action.get("execution_status"))
    print("action strategy mode:", action.get("strategy_mode"))
    print("action adaptive action:", action.get("adaptive_action"))

    assert action.get("strategy_mode") == intelligence["strategy_mode"]
    assert action.get("adaptive_action") == intelligence["adaptive_action"]

    print("strategy propagation to action: PASS")
    print("adaptive action propagation to action: PASS")

    explainability = explainability_engine.explain(
        validation=validation,
        confidence=confidence,
        assessment=assessment,
        recommendation=recommendation,
    )

    print("explainability strategy mode:", explainability.get("strategy_mode"))
    print("explainability adaptive action:", explainability.get("adaptive_action"))
    print("explainability alignment:", explainability.get("decision_alignment"))
    print("explainability consistency:", explainability.get("decision_consistency"))

    assert explainability.get("strategy_mode") == intelligence["strategy_mode"]
    assert explainability.get("adaptive_action") == intelligence["adaptive_action"]
    assert explainability.get("decision_alignment") == "ALIGNED"
    assert explainability.get("decision_consistency") == "CONSISTENT"

    print("explainability strategy propagation: PASS")
    print("explainability adaptive action propagation: PASS")
    print("explainability alignment propagation: PASS")
    print("explainability consistency propagation: PASS")

    print("VALIDATION -> ACTION / EXPLAINABILITY CONTRACT: PASS")

print("")
print("=" * 82)
print("FINAL ASSERTIONS")
print("=" * 82)
print("DEFENSIVE -> REDUCE_RISK -> ACTION / EXPLAINABILITY: PASS")
print("GROWTH -> INCREASE_RISK -> ACTION / EXPLAINABILITY: PASS")
print("BALANCED -> MAINTAIN_BALANCE -> ACTION / EXPLAINABILITY: PASS")
print("MAINTAIN -> MAINTAIN_ALLOCATION -> ACTION / EXPLAINABILITY: PASS")

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
print("===== PHASE 7-8 VALIDATION -> ACTION / EXPLAINABILITY TEST COMPLETE =====")
print("=" * 82)
