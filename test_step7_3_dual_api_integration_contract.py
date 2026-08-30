from pathlib import Path

print("=" * 60)
print("PHASE 7-3-5 DUAL API INTEGRATION CONTRACT")
print("=" * 60)

path = Path("api_server.py")
lines = path.read_text(encoding="utf-8").splitlines()

adaptive_block = "\n".join(
    lines[1149:1214]
)

portfolio_block = "\n".join(
    lines[1430:1498]
)

required_fragments = [
    "get_ai_decision_outcome_history",
    'if outcome_row[15] != "EVALUATED":',
    "outcome_score = outcome_row[18]",
    "outcome_learning_required = bool(",
    "canonical_learning_signal(",
    "canonical_learning_signal_strength(",
    "effective_adaptive_required = (",
    '"outcome_status": outcome_row[15]',
    '"outcome_score": outcome_score',
    '"outcome_grade": outcome_row[19]',
    '"outcome_learning_status": outcome_row[24]',
    '"feedback_state": outcome_row[25]',
    '"adaptive_learning_required":',
    '"reassessment_required": bool(',
    '"reassessment_status": outcome_row[28]',
    '"outcome_learning_signal":',
    '"outcome_learning_signal_strength":',
    '"source_history_id": outcome_row[0]',
    "AIDecisionAdaptiveStrategy()",
    ".analyze(",
]

print()
print("=== CONTRACT FRAGMENT CHECK ===")

adaptive_pass = []
portfolio_pass = []

for fragment in required_fragments:
    a = fragment in adaptive_block
    p = fragment in portfolio_block

    adaptive_pass.append(a)
    portfolio_pass.append(p)

    print(
        f"{fragment}: "
        f"ADAPTIVE={'PASS' if a else 'FAIL'} | "
        f"PORTFOLIO={'PASS' if p else 'FAIL'}"
    )

print()
print("=== DUAL PATH CONSISTENCY ===")

all_adaptive = all(adaptive_pass)
all_portfolio = all(portfolio_pass)

print(
    "ADAPTIVE STRATEGY API CONTRACT:",
    "PASS" if all_adaptive else "FAIL"
)

print(
    "PORTFOLIO DECISION API CONTRACT:",
    "PASS" if all_portfolio else "FAIL"
)

print(
    "DUAL API CONTRACT:",
    "PASS" if all_adaptive and all_portfolio else "FAIL"
)

print()
print("=== ADAPTIVE STRATEGY INVOCATION ===")

adaptive_invocation = (
    "strategy_engine.analyze(" in adaptive_block
    and "trend," in adaptive_block
    and "outcome_intelligence" in adaptive_block
)

portfolio_invocation = (
    "adaptive_strategy_engine.analyze(" in portfolio_block
    and "adaptive_trend," in portfolio_block
    and "outcome_intelligence" in portfolio_block
)

print(
    "ADAPTIVE API -> trend + outcome_intelligence:",
    "PASS" if adaptive_invocation else "FAIL"
)

print(
    "PORTFOLIO API -> adaptive_trend + outcome_intelligence:",
    "PASS" if portfolio_invocation else "FAIL"
)

overall = (
    all_adaptive
    and all_portfolio
    and adaptive_invocation
    and portfolio_invocation
)

print()
print("=" * 60)
print(
    "OVERALL RESULT:",
    "PASS" if overall else "FAIL"
)
print("=" * 60)
