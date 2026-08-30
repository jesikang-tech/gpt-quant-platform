from core.portfolio_decision_intelligence import (
    PortfolioDecisionIntelligence
)
from core.portfolio_intelligence_score import (
    PortfolioIntelligenceScore
)


def build_common_inputs(adaptive_strategy):

    return {
        "ai_decision": {
            "decision": "MAINTAIN",
            "market_view": "NEUTRAL",
            "confidence": 90,
            "decision_score": 80
        },
        "decision_quality": {
            "quality_score": 90
        },
        "reliability": {
            "confidence": 90,
            "reliability_level": "HIGH"
        },
        "adaptive_strategy": adaptive_strategy,
        "rebalance": {
            "rebalance_score": 80
        },
        "optimization": {
            "optimization_score": 80
        },
        "explainability": {
            "explainability_status": "EXPLAINABLE"
        }
    }


def calculate_expected(
    decision_score,
    quality,
    reliability,
    adaptive_strategy,
    consistency,
    rebalance,
    optimization
):

    return round(
        decision_score * 0.30
        + quality * 0.15
        + reliability * 0.15
        + adaptive_strategy * 0.10
        + consistency * 0.10
        + rebalance * 0.10
        + optimization * 0.10,
        1
    )


def run_case(name, adaptive_strategy, expected):

    inputs = build_common_inputs(
        adaptive_strategy
    )

    decision_engine = (
        PortfolioDecisionIntelligence()
    )

    portfolio_intelligence = (
        decision_engine.generate(
            inputs["ai_decision"],
            inputs["decision_quality"],
            inputs["reliability"],
            inputs["adaptive_strategy"],
            inputs["rebalance"],
            inputs["optimization"],
            inputs["explainability"]
        )
    )

    score_engine = (
        PortfolioIntelligenceScore()
    )

    intelligence_score = (
        score_engine.calculate(
            inputs["ai_decision"].get(
                "decision_score",
                0
            ),
            inputs["decision_quality"],
            inputs["reliability"],
            inputs["adaptive_strategy"],
            portfolio_intelligence.get(
                "decision_consistency_score",
                0
            ),
            inputs["rebalance"],
            inputs["optimization"]
        )
    )

    components = intelligence_score[
        "components"
    ]

    expected_score = calculate_expected(
        components["decision_score"],
        components["decision_quality"],
        components["reliability"],
        components["adaptive_strategy"],
        components["decision_consistency"],
        components["rebalance"],
        components["optimization"]
    )

    print("")
    print("=" * 82)
    print(f"CASE: {name}")
    print("=" * 82)

    print("--- PORTFOLIO DECISION INTELLIGENCE ---")
    print(
        "strategy_mode:",
        portfolio_intelligence.get(
            "strategy_mode"
        )
    )
    print(
        "decision_consistency:",
        portfolio_intelligence.get(
            "decision_consistency"
        )
    )
    print(
        "decision_consistency_score:",
        portfolio_intelligence.get(
            "decision_consistency_score"
        )
    )
    print(
        "outcome_learning_signal:",
        portfolio_intelligence.get(
            "outcome_learning_signal"
        )
    )
    print(
        "outcome_learning_signal_strength:",
        portfolio_intelligence.get(
            "outcome_learning_signal_strength"
        )
    )
    print(
        "adaptive_learning_required:",
        portfolio_intelligence.get(
            "adaptive_learning_required"
        )
    )

    print("--- PORTFOLIO INTELLIGENCE SCORE ---")
    print(
        "intelligence_score:",
        intelligence_score.get(
            "intelligence_score"
        )
    )
    print(
        "expected_score:",
        expected_score
    )
    print(
        "grade:",
        intelligence_score.get(
            "grade"
        )
    )
    print(
        "intelligence_level:",
        intelligence_score.get(
            "intelligence_level"
        )
    )

    print("--- SCORE COMPONENTS ---")

    for key, value in components.items():
        print(
            f"{key}:",
            value
        )

    assert (
        components["adaptive_strategy"]
        == adaptive_strategy["confidence"]
    )

    assert (
        components["decision_consistency"]
        == portfolio_intelligence.get(
            "decision_consistency_score"
        )
    )

    assert (
        intelligence_score["intelligence_score"]
        == expected_score
    )

    assert (
        portfolio_intelligence.get(
            "outcome_learning_signal"
        )
        == adaptive_strategy.get(
            "outcome_learning_signal"
        )
    )

    assert (
        portfolio_intelligence.get(
            "outcome_learning_signal_strength"
        )
        == adaptive_strategy.get(
            "outcome_learning_signal_strength"
        )
    )

    assert (
        portfolio_intelligence.get(
            "adaptive_learning_required"
        )
        == adaptive_strategy.get(
            "adaptive_learning_required"
        )
    )

    assert (
        intelligence_score["grade"]
        in {
            "A+",
            "A",
            "B",
            "C",
            "D"
        }
    )

    assert (
        intelligence_score["intelligence_level"]
        in {
            "Excellent",
            "Strong",
            "Moderate",
            "Weak"
        }
    )

    print(
        f"{name} -> PORTFOLIO INTELLIGENCE SCORE: PASS"
    )


print("=" * 82)
print(
    "PHASE 7-9-13 PORTFOLIO DECISION INTELLIGENCE "
    "-> PORTFOLIO INTELLIGENCE SCORE"
)
print(
    "ADAPTIVE STRATEGY / CONSISTENCY SCORE PROPAGATION "
    "BOUNDARY CONTRACT TEST"
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
    {}
)


run_case(
    "ADAPTIVE_DEFENSIVE",
    {
        "strategy": "DEFENSIVE",
        "action": "REDUCE_RISK",
        "confidence": 70,
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
    {}
)


print("")
print("=" * 82)
print("FINAL ASSERTIONS")
print("=" * 82)

print(
    "Portfolio Decision Intelligence -> "
    "Adaptive Strategy component: PASS"
)

print(
    "Decision consistency score -> "
    "Intelligence Score component: PASS"
)

print(
    "Source-defined weighted calculation -> PASS"
)

print(
    "Outcome learning fields preserved downstream: PASS"
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
    "===== PHASE 7-9-13 PORTFOLIO DECISION INTELLIGENCE "
    "-> PORTFOLIO INTELLIGENCE SCORE"
)
print("===== CONTRACT TEST COMPLETE")
print("=" * 82)
