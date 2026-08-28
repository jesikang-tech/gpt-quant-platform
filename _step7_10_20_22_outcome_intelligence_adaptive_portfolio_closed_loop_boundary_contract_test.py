from core.ai_decision_outcome_evaluation import AIDecisionOutcomeEvaluation
from core.ai_decision_outcome_intelligence import AIDecisionOutcomeIntelligence
from core.ai_decision_adaptive_strategy import AIDecisionAdaptiveStrategy
from core.portfolio_decision_intelligence import PortfolioDecisionIntelligence


def assert_equal(actual, expected, label):
    if actual != expected:
        raise AssertionError(
            f"{label}: expected={expected!r}, actual={actual!r}"
        )
    print(f"{label}: PASS")


def evaluate(score):
    engine = AIDecisionOutcomeEvaluation()

    portfolio_return = (
        float(score) - 50.0
    ) / 5.0

    return engine.evaluate(
        outcome_snapshot={
            "decision": "MAINTAIN",
            "action": "PROCEED",
            "strategy": "BALANCED",
            "snapshot_status": "COLLECTED",
            "snapshot_purpose": "FUTURE_OUTCOME_EVALUATION",
        },
        actual_outcome={
            "portfolio_return": portfolio_return,
            "market_response": "EVALUATED",
            "portfolio_response": "EVALUATED",
        },
    )


def intelligence(evaluation):
    engine = AIDecisionOutcomeIntelligence()

    return engine.analyze(
        final_decision={
            "decision": "MAINTAIN",
            "action": "PROCEED",
            "strategy": "BALANCED",
        },
        final_decision_master_control={
            "master_control_status": "MASTER_READY",
            "execution_authorization": "AUTHORIZED",
            "execution_status": "EXECUTION_READY",
        },
        final_decision_certification={
            "certification_status": "CERTIFIED",
        },
        outcome_evaluation=evaluation,
        intelligence_score={
            "intelligence_score": 90.0,
        },
        decision_confidence={
            "confidence_score": 90.0,
        },
    )


def adaptive(outcome_intelligence, trend):
    engine = AIDecisionAdaptiveStrategy()

    return engine.analyze(
        trend,
        outcome_intelligence,
    )

positive_trend = {
    "direction": "STABLE",
    "stability": "HIGH",
    "momentum": "NEUTRAL",
    "grade_stability": "STABLE",
    "consistency": "MEDIUM",
    "latest_score": 85,
}

negative_trend = {
    "direction": "DOWN",
    "stability": "LOW",
    "momentum": "NEGATIVE",
    "grade_stability": "CHANGING",
    "consistency": "LOW",
    "latest_score": 40,
}

pending_trend = {
    "direction": "STABLE",
    "stability": "HIGH",
    "momentum": "NEUTRAL",
    "grade_stability": "STABLE",
    "consistency": "HIGH",
    "latest_score": 85,
}



def portfolio(adaptive_strategy):
    engine = PortfolioDecisionIntelligence()

    return engine.generate(
        {
            "decision": "MAINTAIN",
            "market_view": "NEUTRAL",
            "confidence": 90,
        },
        {},
        {
            "confidence": 90,
            "reliability_level": "HIGH",
        },
        adaptive_strategy,
        {},
        {},
        {
            "summary": "Closed loop portfolio decision",
        },
    )


print("=" * 82)
print("PHASE 7-10-20-22")
print("OUTCOME -> INTELLIGENCE -> ADAPTIVE STRATEGY -> PORTFOLIO DECISION")
print("CLOSED LOOP PROPAGATION BOUNDARY CONTRACT TEST V1")
print("SOURCE-VERIFIED / MEMORY-ONLY / READ-ONLY")
print("=" * 82)


print("")
print("=" * 82)
print("CASE: POSITIVE OUTCOME -> GROWTH -> PORTFOLIO DECISION")
print("=" * 82)

positive_evaluation = evaluate(100.0)
positive_intelligence = intelligence(positive_evaluation)
positive_adaptive = adaptive(positive_intelligence, positive_trend)
positive_portfolio = portfolio(positive_adaptive)

assert_equal(
    positive_evaluation["learning_signal"],
    "POSITIVE",
    "positive -> evaluation signal",
)

assert_equal(
    positive_intelligence["outcome_learning_signal"],
    "POSITIVE",
    "positive -> intelligence signal",
)

assert_equal(
    positive_adaptive["outcome_learning_signal"],
    "POSITIVE",
    "positive -> adaptive signal",
)

assert_equal(
    positive_adaptive["strategy"],
    "GROWTH",
    "positive -> adaptive growth",
)

assert_equal(
    positive_portfolio["final_strategy"],
    "GROWTH",
    "positive -> portfolio growth",
)


print("")
print("=" * 82)
print("CASE: NEGATIVE OUTCOME -> DEFENSIVE -> PORTFOLIO OVERRIDE")
print("=" * 82)

negative_evaluation = evaluate(0.0)
negative_intelligence = intelligence(negative_evaluation)
negative_adaptive = adaptive(negative_intelligence, negative_trend)
negative_adaptive = adaptive(negative_intelligence, negative_trend)
negative_portfolio = portfolio(negative_adaptive)

assert_equal(
    negative_evaluation["learning_signal"],
    "NEGATIVE",
    "negative -> evaluation signal",
)

assert_equal(
    negative_intelligence["outcome_learning_signal"],
    "NEGATIVE",
    "negative -> intelligence signal",
)

assert_equal(
    negative_intelligence["adaptive_learning_required"],
    True,
    "negative -> adaptive learning required",
)

assert_equal(
    negative_adaptive["strategy"],
    "DEFENSIVE",
    "negative -> adaptive defensive",
)

assert_equal(
    negative_portfolio["final_strategy"],
    "DEFENSIVE",
    "negative -> portfolio defensive",
)

assert_equal(
    negative_portfolio["adaptive_override"],
    True,
    "negative -> portfolio defensive override",
)


print("")
print("=" * 82)
print("CASE: PENDING OUTCOME -> NO FABRICATED LEARNING -> BASE PORTFOLIO")
print("=" * 82)

pending_intelligence = intelligence({
    "outcome_status": "PENDING",
    "outcome_score": 0.0,
    "learning_signal": "NONE",
    "learning_signal_strength": 0.0,
})

pending_adaptive = adaptive(pending_intelligence, pending_trend)
pending_portfolio = portfolio(pending_adaptive)

assert_equal(
    pending_intelligence["outcome_learning_signal"],
    "NONE",
    "pending -> no fabricated intelligence signal",
)

assert_equal(
    pending_adaptive["outcome_learning_signal"],
    "NONE",
    "pending -> no fabricated adaptive signal",
)

assert_equal(
    pending_adaptive["strategy"],
    "MAINTAIN",
    "pending -> base strategy preserved",
)

assert_equal(
    pending_portfolio["final_strategy"],
    "MAINTAIN",
    "pending -> base portfolio strategy preserved",
)


print("")
print("=" * 82)
print("CASE: LEARNING FIELDS PRESERVED THROUGH CLOSED LOOP")
print("=" * 82)

assert_equal(
    negative_portfolio["outcome_learning_signal"],
    "NEGATIVE",
    "closed loop -> learning signal preserved",
)

assert_equal(
    negative_portfolio["outcome_learning_signal_strength"],
    negative_adaptive["outcome_learning_signal_strength"],
    "closed loop -> learning strength preserved",
)

assert_equal(
    negative_portfolio["adaptive_learning_required"],
    True,
    "closed loop -> adaptive requirement preserved",
)


print("")
print("=" * 82)
print("===== PHASE 7-10-20-22 CLOSED LOOP BOUNDARY COMPLETE =====")
print("=" * 82)
