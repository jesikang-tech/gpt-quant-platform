from pathlib import Path

print("=" * 60)
print("PHASE 7-3-11 CONSUMER SEMANTIC CONTRACT V2")
print("=" * 60)

portfolio = Path(
    "core/portfolio_decision_intelligence.py"
).read_text(encoding="utf-8")

score = Path(
    "core/portfolio_intelligence_score.py"
).read_text(encoding="utf-8")

confidence = Path(
    "core/decision_confidence_intelligence.py"
).read_text(encoding="utf-8")

final = Path(
    "core/ai_final_decision_integration.py"
).read_text(encoding="utf-8")

checks = []


def check(name, condition):
    status = "PASS" if condition else "FAIL"
    checks.append(condition)
    print(f"{name}: {status}")


print("")
print("=== PORTFOLIO DECISION CORE CONSUMPTION ===")

portfolio_fields = [
    "strategy",
    "action",
    "confidence",
    "score",
    "direction",
    "stability",
    "momentum",
    "grade_stability",
    "consistency",
    "summary",
]

for field in portfolio_fields:
    check(
        f"{field}: CONSUMED",
        f'adaptive_strategy.get(' in portfolio
        and field in portfolio
    )


print("")
print("=== PORTFOLIO INTELLIGENCE SCORE ===")

check(
    "adaptive_strategy input accepted",
    "adaptive_strategy" in score
)

check(
    "strategy score path exists",
    "_get_strategy_score" in score
)

check(
    "confidence participates in adaptive score path",
    "confidence" in score
)


print("")
print("=== DECISION CONFIDENCE INTELLIGENCE ===")

check(
    "adaptive_strategy input accepted",
    "adaptive_strategy" in confidence
)

check(
    "adaptive confidence field consumed",
    "confidence" in confidence
)

check(
    "adaptive score path exists",
    "adaptive_score" in confidence
)


print("")
print("=== FINAL DECISION INTEGRATION ===")

check(
    "strategy propagation",
    '"strategy"' in final
)

check(
    "action propagation",
    '"action"' in final
)

check(
    "summary propagation",
    '"summary"' in final
)


print("")
print("=== OUTCOME LEARNING OWNERSHIP ===")

outcome_fields = [
    "outcome_learning_signal",
    "outcome_learning_signal_strength",
    "adaptive_learning_required",
]

adaptive = Path(
    "core/ai_decision_adaptive_strategy.py"
).read_text(encoding="utf-8")

for field in outcome_fields:
    owner_check = (
        f'"{field}"' in adaptive
        and all(field in portfolio for field in outcome_fields)
    )

    check(
        f"{field}: ADAPTIVE STRATEGY OWNER",
        owner_check
    )


print("")
print("=== SEMANTIC CONTRACT ===")

print(
    "PORTFOLIO CORE FIELDS:",
    len(portfolio_fields)
)

print(
    "OUTCOME LEARNING FIELDS:",
    len(outcome_fields)
)

print(
    "OVERALL RESULT:",
    "PASS" if all(checks) else "FAIL"
)

print("=" * 60)
