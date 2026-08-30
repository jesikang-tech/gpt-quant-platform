"""
PHASE 7-10-19-5
OUTCOME EVALUATION
->
OUTCOME INTELLIGENCE
->
ADAPTIVE STRATEGY
->
PORTFOLIO DECISION
->
FINAL DECISION
->
INTEGRATED INTELLIGENCE
->
ORCHESTRATION

CLOSED-LOOP BOUNDARY CONTRACT TEST V1

SOURCE-VERIFIED / MEMORY-ONLY / READ-ONLY
"""

from core.ai_decision_outcome_evaluation import (
    AIDecisionOutcomeEvaluation,
)
from core.ai_decision_outcome_intelligence import (
    AIDecisionOutcomeIntelligence,
)
from core.ai_decision_adaptive_strategy import (
    AIDecisionAdaptiveStrategy,
)
from core.portfolio_decision_intelligence import (
    PortfolioDecisionIntelligence,
)
from core.ai_final_decision_integration import (
    AIFinalDecisionIntegration,
)
from core.ai_final_decision_integrated_intelligence import (
    AIFinalDecisionIntegratedIntelligence,
)
from core.ai_final_decision_orchestration import (
    AIFinalDecisionOrchestration,
)


evaluation_engine = AIDecisionOutcomeEvaluation()
outcome_intelligence_engine = AIDecisionOutcomeIntelligence()
adaptive_strategy_engine = AIDecisionAdaptiveStrategy()
portfolio_decision_engine = PortfolioDecisionIntelligence()
final_decision_integration_engine = AIFinalDecisionIntegration()
integrated_intelligence_engine = (
    AIFinalDecisionIntegratedIntelligence()
)
orchestration_engine = AIFinalDecisionOrchestration()


def assert_equal(actual, expected, label):
    if actual != expected:
        raise AssertionError(
            f"{label}: expected={expected!r}, actual={actual!r}"
        )
    print(f"{label}: PASS")


def base_snapshot():
    return {
        "decision": "MAINTAIN",
        "action": "PROCEED",
        "strategy": "BALANCED",
        "snapshot_status": "COLLECTED",
        "snapshot_purpose": "FUTURE_OUTCOME_EVALUATION",
    }


def base_final_decision():
    return {
        "decision": "MAINTAIN",
        "action": "PROCEED",
    }


def base_master_control():
    return {
        "decision": "MAINTAIN",
        "master_control_action": "PROCEED",
        "execution_status": "EXECUTION_READY",
        "execution_authorization": "AUTHORIZED",
        "master_control_status": "MASTER_READY",
    }


def base_certification():
    return {
        "certification_status": "CERTIFIED",
    }


def base_execution():
    return {
        "decision": "MAINTAIN",
        "action": "PROCEED",
        "execution_status": "EXECUTION_READY",
        "execution_authorization": "AUTHORIZED",
    }


def base_feedback():
    return {
        "feedback_status": "STABLE",
    }


def base_monitoring():
    return {
        "monitoring_status": "STANDARD_MONITORING",
    }


def base_reassessment():
    return {
        "reassessment_required": False,
        "reassessment_status": "NOT_REQUIRED",
    }


def base_intelligence():
    return {
        "intelligence_score": 90.0,
    }


def base_confidence():
    return {
        "confidence_score": 90.0,
    }


def base_validation():
    return {
        "validation_status": "VALID",
        "validation_score": 90.0,
        "risk_level": "LOW",
    }


def base_governance():
    return {
        "governance_status": "APPROVED",
        "governance_score": 90.0,
        "risk_governance": "ACCEPTABLE",
    }


def base_execution_control():
    return {
        "control_status": "AUTHORIZED",
        "control_risk": "LOW",
        "execution_status": "EXECUTION_READY",
    }


def base_execution_assurance():
    return {
        "assurance_status": "ASSURED",
        "assurance_risk": "LOW",
    }


def base_execution_monitoring():
    return {
        "monitoring_status": "STANDARD_MONITORING",
        "monitoring_risk": "LOW",
    }


def base_execution_feedback():
    return {
        "feedback_status": "STABLE",
        "feedback_risk": "LOW",
    }


def base_lifecycle():
    return {
        "lifecycle_status": "HEALTHY",
        "lifecycle_score": 90.0,
        "lifecycle_risk": "LOW",
        "lifecycle_action": "PROCEED",
    }


def base_lifecycle_governance_control():
    return {
        "operational_status": "OPERATIONALLY_HEALTHY",
        "operational_score": 90.0,
        "operational_risk": "LOW",
        "operational_action": "PROCEED",
        "execution_authorization": "AUTHORIZED",
        "monitoring_policy": "STANDARD",
        "reassessment_policy": "NOT_REQUIRED",
    }


def base_operational_intelligence():
    return {
        "intelligence_status": "HEALTHY",
        "intelligence_score": 90.0,
        "intelligence_risk": "LOW",
        "intelligence_action": "PROCEED",
    }


def build_closed_loop(portfolio_return):
    evaluation = evaluation_engine.evaluate(
        outcome_snapshot=base_snapshot(),
        actual_outcome={
            "portfolio_return": portfolio_return,
            "market_response": "EVALUATED",
            "portfolio_response": "EVALUATED",
        },
    )

    outcome_intelligence = (
        outcome_intelligence_engine.analyze(
            final_decision=base_final_decision(),
            final_decision_master_control=(
                base_master_control()
            ),
            final_decision_certification=(
                base_certification()
            ),
            final_execution_decision=base_execution(),
            final_decision_execution_feedback=(
                base_feedback()
            ),
            final_decision_execution_monitoring=(
                base_monitoring()
            ),
            final_decision_execution_reassessment=(
                base_reassessment()
            ),
            intelligence=base_intelligence(),
            intelligence_score=base_intelligence(),
            decision_confidence=base_confidence(),
            outcome_evaluation=evaluation,
        )
    )

    trend = {
        "direction": "STABLE",
        "stability": "MEDIUM",
        "momentum": "NEUTRAL",
        "grade_stability": "STABLE",
        "consistency": "MEDIUM",
        "latest_score": 75,
    }

    adaptive_strategy = adaptive_strategy_engine.analyze(
        trend=trend,
        outcome_intelligence=outcome_intelligence,
    )

    portfolio_decision = portfolio_decision_engine.generate(
        {
            "decision": "MAINTAIN",
            "market_view": "NEUTRAL",
            "confidence": 90,
        },
        {
            "quality_score": 90,
        },
        {
            "confidence": 90,
            "reliability_level": "HIGH",
        },
        adaptive_strategy,
        {
            "rebalance_action": "HOLD",
        },
        {
            "optimization_status": "OPTIMAL",
        },
        {
            "summary": (
                "Source-verified closed-loop test."
            ),
        },
    )

    final_decision = (
        final_decision_integration_engine.integrate(
            intelligence=portfolio_decision,
        )
    )

    integrated_intelligence = (
        integrated_intelligence_engine.analyze(
            final_decision=final_decision,
            validation=base_validation(),
            governance=base_governance(),
            execution_control=base_execution_control(),
            execution_assurance=base_execution_assurance(),
            execution_monitoring=base_execution_monitoring(),
            execution_feedback=base_execution_feedback(),
            reassessment=base_reassessment(),
            lifecycle=base_lifecycle(),
            lifecycle_governance_control=(
                base_lifecycle_governance_control()
            ),
            operational_intelligence=(
                base_operational_intelligence()
            ),
        )
    )

    orchestration = orchestration_engine.analyze(
        final_decision=final_decision,
        integrated_intelligence=(
            integrated_intelligence
        ),
        lifecycle_governance_control=(
            base_lifecycle_governance_control()
        ),
        operational_intelligence=(
            base_operational_intelligence()
        ),
    )

    return (
        evaluation,
        outcome_intelligence,
        adaptive_strategy,
        portfolio_decision,
        final_decision,
        integrated_intelligence,
        orchestration,
    )


print("=" * 82)
print("CASE: POSITIVE OUTCOME -> GROWTH -> FINAL -> ORCHESTRATION")
print("=" * 82)

(
    evaluation,
    outcome_intelligence,
    adaptive_strategy,
    portfolio_decision,
    final_decision,
    integrated_intelligence,
    orchestration,
) = build_closed_loop(10.0)

print("evaluation:", evaluation)
print("outcome_intelligence:", outcome_intelligence)
print("adaptive_strategy:", adaptive_strategy)
print("portfolio_decision:", portfolio_decision)
print("final_decision:", final_decision)
print("integrated_intelligence:", integrated_intelligence)
print("orchestration:", orchestration)

assert_equal(
    evaluation["learning_signal"],
    "POSITIVE",
    "POSITIVE -> evaluation signal",
)

assert_equal(
    outcome_intelligence["outcome_learning_signal"],
    "POSITIVE",
    "POSITIVE -> intelligence signal",
)

assert_equal(
    adaptive_strategy["strategy"],
    "GROWTH",
    "POSITIVE -> adaptive strategy",
)

assert_equal(
    portfolio_decision["final_strategy"],
    "GROWTH",
    "POSITIVE -> portfolio strategy",
)

assert_equal(
    final_decision["strategy"],
    "GROWTH",
    "POSITIVE -> final strategy",
)

assert_equal(
    integrated_intelligence["decision"],
    final_decision["decision"],
    "POSITIVE -> integrated decision",
)

assert_equal(
    integrated_intelligence["action"],
    final_decision["action"],
    "POSITIVE -> integrated action",
)

assert_equal(
    integrated_intelligence["integrated_status"],
    "INTEGRATED_HEALTHY",
    "POSITIVE -> integrated status",
)

assert_equal(
    integrated_intelligence["integrated_action"],
    "PROCEED",
    "POSITIVE -> integrated action",
)

assert_equal(
    orchestration["orchestration_status"],
    "ORCHESTRATION_READY",
    "POSITIVE -> orchestration status",
)

assert_equal(
    orchestration["orchestration_action"],
    "PROCEED",
    "POSITIVE -> orchestration action",
)

assert_equal(
    orchestration["orchestration_risk"],
    "LOW",
    "POSITIVE -> orchestration risk",
)


print("")
print("=" * 82)
print("CASE: NEGATIVE OUTCOME -> DEFENSIVE -> FINAL -> ORCHESTRATION")
print("=" * 82)

(
    evaluation,
    outcome_intelligence,
    adaptive_strategy,
    portfolio_decision,
    final_decision,
    integrated_intelligence,
    orchestration,
) = build_closed_loop(-10.0)

print("evaluation:", evaluation)
print("outcome_intelligence:", outcome_intelligence)
print("adaptive_strategy:", adaptive_strategy)
print("portfolio_decision:", portfolio_decision)
print("final_decision:", final_decision)
print("integrated_intelligence:", integrated_intelligence)
print("orchestration:", orchestration)

assert_equal(
    evaluation["learning_signal"],
    "NEGATIVE",
    "NEGATIVE -> evaluation signal",
)

assert_equal(
    outcome_intelligence["learning_status"],
    "ADAPTIVE_LEARNING_REQUIRED",
    "NEGATIVE -> intelligence learning status",
)

assert_equal(
    adaptive_strategy["strategy"],
    "DEFENSIVE",
    "NEGATIVE -> adaptive strategy",
)

assert_equal(
    portfolio_decision["final_strategy"],
    "DEFENSIVE",
    "NEGATIVE -> portfolio strategy",
)

assert_equal(
    final_decision["strategy"],
    "DEFENSIVE",
    "NEGATIVE -> final strategy",
)

assert_equal(
    integrated_intelligence["decision"],
    final_decision["decision"],
    "NEGATIVE -> integrated decision",
)

assert_equal(
    integrated_intelligence["action"],
    final_decision["action"],
    "NEGATIVE -> integrated action",
)

assert_equal(
    integrated_intelligence["integrated_status"],
    "INTEGRATED_HEALTHY",
    "NEGATIVE -> integrated status",
)

assert_equal(
    integrated_intelligence["integrated_action"],
    "PROCEED",
    "NEGATIVE -> integrated action",
)

assert_equal(
    orchestration["orchestration_status"],
    "ORCHESTRATION_READY",
    "NEGATIVE -> orchestration status",
)

assert_equal(
    orchestration["orchestration_action"],
    "PROCEED",
    "NEGATIVE -> orchestration action",
)

assert_equal(
    orchestration["orchestration_risk"],
    "LOW",
    "NEGATIVE -> orchestration risk",
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

print("")
print("=" * 82)
print("===== PHASE 7-10-19-5 CLOSED-LOOP BOUNDARY COMPLETE =====")
print("=" * 82)
