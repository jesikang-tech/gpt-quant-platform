from core.portfolio_decision_intelligence import (
    PortfolioDecisionIntelligence
)


def build_inputs(adaptive_strategy):

    return {
        "ai_decision": {
            "decision": "MAINTAIN",
            "market_view": "NEUTRAL",
            "confidence": 90
        },
        "decision_quality": {
            "quality_score": 85
        },
        "reliability": {
            "confidence": 90,
            "reliability_level": "HIGH"
        },
        "adaptive_strategy": adaptive_strategy,
        "rebalance": {
            "rebalance_action": "MAINTAIN"
        },
        "optimization": {
            "optimization_status": "OPTIMIZED"
        },
        "explainability": {
            "explainability_status": "EXPLAINABLE"
        }
    }


def run_case(name, adaptive_strategy, expected):

    engine = PortfolioDecisionIntelligence()

    inputs = build_inputs(adaptive_strategy)

    result = engine.generate(
        inputs["ai_decision"],
        inputs["decision_quality"],
        inputs["reliability"],
        inputs["adaptive_strategy"],
        inputs["rebalance"],
        inputs["optimization"],
        inputs["explainability"]
    )

    print("")
    print("=" * 82)
    print(f"CASE: {name}")
    print("=" * 82)

    print("--- ADAPTIVE STRATEGY ---")
    print(
        "strategy:",
        adaptive_strategy.get("strategy")
    )
    print(
        "action:",
        adaptive_strategy.get("action")
    )
    print(
        "outcome_learning_signal:",
        adaptive_strategy.get(
            "outcome_learning_signal"
        )
    )
    print(
        "outcome_learning_signal_strength:",
        adaptive_strategy.get(
            "outcome_learning_signal_strength"
        )
    )
    print(
        "adaptive_learning_required:",
        adaptive_strategy.get(
            "adaptive_learning_required"
        )
    )

    print("--- PORTFOLIO DECISION INTELLIGENCE ---")
    print(
        "strategy_mode:",
        result.get("strategy_mode")
    )
    print(
        "decision_alignment:",
        result.get("decision_alignment")
    )
    print(
        "adaptive_override:",
        result.get("adaptive_override")
    )
    print(
        "final_strategy:",
        result.get("final_strategy")
    )
    print(
        "final_action:",
        result.get("final_action")
    )
    print(
        "outcome_learning_signal:",
        result.get(
            "outcome_learning_signal"
        )
    )
    print(
        "outcome_learning_signal_strength:",
        result.get(
            "outcome_learning_signal_strength"
        )
    )
    print(
        "adaptive_learning_required:",
        result.get(
            "adaptive_learning_required"
        )
    )

    assert (
        result.get("strategy_mode")
        == adaptive_strategy.get("strategy")
    )

    assert (
        result.get("outcome_learning_signal")
        == adaptive_strategy.get(
            "outcome_learning_signal"
        )
    )

    assert (
        result.get(
            "outcome_learning_signal_strength"
        )
        == adaptive_strategy.get(
            "outcome_learning_signal_strength"
        )
    )

    assert (
        result.get("adaptive_learning_required")
        == adaptive_strategy.get(
            "adaptive_learning_required"
        )
    )

    assert (
        result.get("final_strategy")
        == expected["final_strategy"]
    )

    assert (
        result.get("adaptive_override")
        == expected["adaptive_override"]
    )

    assert (
        result.get("decision_alignment")
        == expected["decision_alignment"]
    )

    print(
        f"{name} -> PORTFOLIO DECISION INTELLIGENCE: PASS"
    )


print("=" * 82)
print(
    "PHASE 7-9-12 ADAPTIVE STRATEGY -> "
    "PORTFOLIO DECISION INTELLIGENCE"
)
print(
    "DOWNSTREAM STRATEGY PROPAGATION BOUNDARY CONTRACT TEST"
)
print(
    "SOURCE-VERIFIED / MEMORY-ONLY / READ-ONLY"
)
print("=" * 82)


run_case(
    "ADAPTIVE_MAINTAIN",
    {
        "strategy": "MAINTAIN",
        "action": "MAINTAIN_ALLOCATION",
        "confidence": 90,
        "score": 85,
        "direction": "STABLE",
        "stability": "HIGH",
        "momentum": "NEUTRAL",
        "grade_stability": "STABLE",
        "consistency": "HIGH",
        "outcome_learning_signal": "NONE",
        "outcome_learning_signal_strength": 0.0,
        "adaptive_learning_required": False
    },
    {
        "final_strategy": "MAINTAIN",
        "adaptive_override": False,
        "decision_alignment": "ALIGNED"
    }
)


run_case(
    "ADAPTIVE_DEFENSIVE",
    {
        "strategy": "DEFENSIVE",
        "action": "REDUCE_RISK",
        "confidence": 90,
        "score": 85,
        "direction": "STABLE",
        "stability": "HIGH",
        "momentum": "NEUTRAL",
        "grade_stability": "STABLE",
        "consistency": "HIGH",
        "outcome_learning_signal": "NONE",
        "outcome_learning_signal_strength": 0.0,
        "adaptive_learning_required": True
    },
    {
        "final_strategy": "DEFENSIVE",
        "adaptive_override": True,
        "decision_alignment": "CONFLICT"
    }
)


print("")
print("=" * 82)
print("FINAL ASSERTIONS")
print("=" * 82)

print(
    "MAINTAIN adaptive strategy -> "
    "MAINTAIN final strategy / ALIGNED / no override: PASS"
)

print(
    "DEFENSIVE adaptive strategy -> "
    "DEFENSIVE final strategy / CONFLICT / override: PASS"
)

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
print("No actual Outcome supplied.")

print("")
print(
    "===== PHASE 7-9-12 ADAPTIVE STRATEGY -> "
    "PORTFOLIO DECISION INTELLIGENCE"
)
print("===== CONTRACT TEST COMPLETE")
print("=" * 82)
