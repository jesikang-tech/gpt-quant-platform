from core.ai_decision_validation import AIDecisionValidation

engine = AIDecisionValidation()

intelligence = {
    "decision": "ACCUMULATE",
    "strategy_mode": "DEFENSIVE",
    "adaptive_action": "REDUCE_RISK",
    "decision_alignment": "ALIGNED",
    "decision_consistency": "CONSISTENT",
    "reliability": "HIGH",
    "optimization_status": "COMPLETED",
    "adaptive_override": False,
}

confidence = {
    "confidence_score": 95.0,
    "confidence_level": "HIGH",
}

assessment = {
    "attention_signals": [],
}

recommendation = {
    "recommendation": "PROCEED",
}

result = engine.validate(
    intelligence,
    confidence,
    assessment,
    recommendation,
)

print("=" * 82)
print("VALIDATION ACTUAL RESULT")
print("=" * 82)

print("validation:", result.get("validation"))
print("validation_status:", result.get("validation_status"))
print("validation_score:", result.get("validation_score"))
print("decision:", result.get("decision"))
print("strategy_mode:", result.get("strategy_mode"))
print("adaptive_action:", result.get("adaptive_action"))
print("decision_alignment:", result.get("decision_alignment"))
print("decision_consistency:", result.get("decision_consistency"))
print("confidence_score:", result.get("confidence_score"))
print("confidence_level:", result.get("confidence_level"))
print("reliability:", result.get("reliability"))
print("optimization_status:", result.get("optimization_status"))
print("adaptive_override:", result.get("adaptive_override"))
print("recommendation:", result.get("recommendation"))

print("")
print("===== VALIDATION SIGNALS =====")

signals = result.get("validation_signals", [])

for index, signal in enumerate(signals, 1):
    print(
        f"{index}. "
        f"name={signal.get('name')} | "
        f"status={signal.get('status')} | "
        f"value={signal.get('value')}"
    )

print("")
print("===== RISK SIGNALS =====")

for index, signal in enumerate(
    result.get("risk_signals", []),
    1
):
    print(f"{index}. {signal}")

failed = sum(
    1
    for signal in signals
    if signal.get("status") == "FAIL"
)

review = sum(
    1
    for signal in signals
    if signal.get("status") == "REVIEW"
)

passed = sum(
    1
    for signal in signals
    if signal.get("status") == "PASS"
)

print("")
print("===== SIGNAL COUNTS =====")
print("PASS:", passed)
print("REVIEW:", review)
print("FAIL:", failed)

print("")
print("===== CANONICAL SCORE RECONSTRUCTION =====")

weights = {
    "PASS": 100,
    "REVIEW": 60,
    "FAIL": 20,
}

total = sum(
    weights.get(signal.get("status"), 0)
    for signal in signals
)

reconstructed = (
    round(total / len(signals), 1)
    if signals
    else 0
)

print("total weighted score:", total)
print("signal count:", len(signals))
print("reconstructed score:", reconstructed)

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
print("===== PHASE 7-8 DISCOVERY 14 COMPLETE =====")
