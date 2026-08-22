from core.ai_decision_outcome_intelligence import AIDecisionOutcomeIntelligence
from core.ai_decision_adaptive_strategy import AIDecisionAdaptiveStrategy
from core.portfolio_decision_intelligence import PortfolioDecisionIntelligence
from core.ai_decision_validation import AIDecisionValidation
from core.ai_decision_validation_action import AIDecisionValidationAction
from core.ai_final_execution_decision import AIFinalExecutionDecision
from core.ai_final_decision_execution_control import (
    AIFinalDecisionExecutionControl
)
from core.ai_final_decision_master_control import (
    AIFinalDecisionMasterControl
)

print("=" * 82)
print("PHASE 7-6 END-TO-END SEMANTIC CONTRACT TEST")
print("OUTCOME -> ADAPTIVE -> PORTFOLIO -> VALIDATION")
print("-> EXECUTION -> CONTROL -> MASTER CONTROL")
print("MEMORY-ONLY / READ-ONLY")
print("=" * 82)


cases = [
    {
        "name": "NEGATIVE",
        "signal": "NEGATIVE",
        "strength": 0.2,
        "expected_strategy": "DEFENSIVE",
        "expected_adaptive_action": "REDUCE_RISK",
        "expected_portfolio_action":
            "Reduce equity exposure and strengthen defensive allocation",
    },
    {
        "name": "POSITIVE",
        "signal": "POSITIVE",
        "strength": 0.8,
        "expected_strategy": "GROWTH",
        "expected_adaptive_action": "INCREASE_RISK",
        "expected_portfolio_action":
            "Increase growth exposure while maintaining risk controls",
    },
    {
        "name": "PENDING",
        "signal": "NONE",
        "strength": 0.0,
        "expected_strategy": "MAINTAIN",
        "expected_adaptive_action": "MAINTAIN_ALLOCATION",
        "expected_portfolio_action":
            "Maintain balanced allocation and monitor market conditions",
    },
]


intelligence_engine = AIDecisionOutcomeIntelligence()
adaptive_engine = AIDecisionAdaptiveStrategy()
portfolio_engine = PortfolioDecisionIntelligence()
validation_engine = AIDecisionValidation()
validation_action_engine = AIDecisionValidationAction()
execution_engine = AIFinalExecutionDecision()
control_engine = AIFinalDecisionExecutionControl()
master_engine = AIFinalDecisionMasterControl()


for case in cases:

    print()
    print("=" * 82)
    print("CASE:", case["name"])
    print("=" * 82)

    # ------------------------------------------------------------
    # 1. Canonical Outcome Intelligence
    # ------------------------------------------------------------

    outcome_evaluation = {
        "outcome_status": (
            "EVALUATED"
            if case["name"] != "PENDING"
            else "WAITING_FOR_OUTCOME"
        ),
        "learning_signal": case["signal"],
        "learning_signal_strength": case["strength"],
        "adaptive_learning_required": (
            case["signal"] == "NEGATIVE"
        ),
    }

    intelligence = intelligence_engine.analyze(
        final_decision={
            "decision": (
                "DEFENSIVE"
                if case["name"] == "NEGATIVE"
                else (
                    "ACCUMULATE"
                    if case["name"] == "POSITIVE"
                    else "MAINTAIN"
                )
            ),
            "action": "PROCEED",
            "execution_status": "EXECUTION_READY",
        },
        intelligence={
            "decision": "PROCEED",
            "decision_consistency_score": 95,
        },
        intelligence_score={
            "intelligence_score": 95,
        },
        decision_confidence={
            "confidence_score": 95,
        },
        outcome_evaluation=outcome_evaluation,
    )

    signal = intelligence.get("outcome_learning_signal")
    strength = intelligence.get("outcome_learning_signal_strength")
    learning_required = intelligence.get(
        "adaptive_learning_required"
    )

    print("learning signal:", signal)
    print("learning strength:", strength)
    print("adaptive learning required:", learning_required)

    assert signal == case["signal"]
    assert strength == case["strength"]

    print("outcome intelligence contract: PASS")

    # ------------------------------------------------------------
    # 2. Adaptive Strategy
    # ------------------------------------------------------------

    # ------------------------------------------------------------
    # Canonical trend input by semantic case
    # ------------------------------------------------------------

    if case["name"] == "NEGATIVE":
        adaptive_trend = {
            "direction": "STABLE",
            "stability": "HIGH",
            "momentum": "NEUTRAL",
            "grade_stability": "STABLE",
            "consistency": "HIGH",
            "latest_score": 85,
        }

    elif case["name"] == "POSITIVE":
        # Deliberately produce BALANCED first.
        # POSITIVE outcome learning must then promote
        # BALANCED -> GROWTH.
        adaptive_trend = {
            "direction": "STABLE",
            "stability": "MEDIUM",
            "momentum": "NEUTRAL",
            "grade_stability": "STABLE",
            "consistency": "MEDIUM",
            "latest_score": 85,
        }

    else:
        # PENDING must preserve the normal MAINTAIN posture.
        adaptive_trend = {
            "direction": "STABLE",
            "stability": "HIGH",
            "momentum": "NEUTRAL",
            "grade_stability": "STABLE",
            "consistency": "HIGH",
            "latest_score": 85,
        }

    adaptive = adaptive_engine.analyze(
        trend=adaptive_trend,
        outcome_intelligence=intelligence,
    )

    strategy = adaptive.get(
        "strategy",
        adaptive.get("strategy_mode")
    )

    adaptive_action = adaptive.get("action")

    print("adaptive strategy:", strategy)
    print("adaptive action:", adaptive_action)

    assert strategy == case["expected_strategy"]
    assert adaptive_action == case["expected_adaptive_action"]

    print("adaptive strategy contract: PASS")

    # ------------------------------------------------------------
    # 3. Portfolio Intelligence
    # ------------------------------------------------------------

    portfolio = portfolio_engine.generate(
        ai_decision={
            "decision": (
                "DEFENSIVE"
                if case["name"] == "NEGATIVE"
                else (
                    "ACCUMULATE"
                    if case["name"] == "POSITIVE"
                    else "MAINTAIN"
                )
            ),
            "market_view": "NEUTRAL",
            "confidence": 95,
        },
        decision_quality={
            "quality_level": "HIGH",
            "recent_trend": "STABLE",
        },
        reliability={
            "confidence": 95,
            "reliability_level": "HIGH",
        },
        adaptive_strategy=adaptive,
        rebalance={
            "rebalance_action": "HOLD",
        },
        optimization={
            "optimization_status": "READY",
        },
        explainability={
            "summary": "Controlled E2E contract test",
        },
    )

    strategy_mode = portfolio.get("strategy_mode")
    portfolio_final_action = portfolio.get("final_action")

    print("portfolio strategy:", strategy_mode)
    print("portfolio adaptive action:",
          portfolio.get("adaptive_action"))
    print("portfolio final strategy:",
          portfolio.get("final_strategy"))
    print("portfolio final action:",
          portfolio_final_action)

    assert strategy_mode == case["expected_strategy"]
    assert portfolio.get("adaptive_action") == \
        case["expected_adaptive_action"]
    assert portfolio.get("final_strategy") == \
        case["expected_strategy"]
    assert portfolio_final_action == \
        case["expected_portfolio_action"]

    print("portfolio bridge contract: PASS")

    # ------------------------------------------------------------
    # 4. Validation
    # ------------------------------------------------------------

    validation = validation_engine.validate(
        {
            "decision": portfolio.get("final_strategy"),
            "strategy_mode": portfolio.get("strategy_mode"),
            "adaptive_action": portfolio.get(
                "adaptive_action"
            ),
            "decision_alignment": portfolio.get(
                "decision_alignment"
            ),
            "decision_consistency": "CONSISTENT",
            "reliability": "HIGH",
            "optimization_status": "READY",
        },
        {
            "confidence_score": 95,
            "confidence_level": "HIGH",
        },
        {
            "assessment_status": "ACCEPTABLE",
        },
        {},
    )

    print("validation status:",
          validation.get("validation"))

    print("validation adaptive action:",
          validation.get("adaptive_action"))

    assert validation.get("adaptive_action") == \
        case["expected_adaptive_action"]

    print("validation propagation: PASS")

    # ------------------------------------------------------------
    # 5. Validation Action
    # ------------------------------------------------------------

    validation_action = validation_action_engine.decide(
        validation,
        {
            "confidence_score": 95,
            "confidence_level": "HIGH",
        },
        {
            "assessment_status": "ACCEPTABLE",
        },
        {},
    )

    executable_action = validation_action.get("action")

    print("validation executable action:",
          executable_action)

    assert executable_action == \
        case["expected_adaptive_action"]

    print("executable action contract: PASS")

    # ------------------------------------------------------------
    # 6. Final Execution Decision
    # ------------------------------------------------------------

    final_decision = {
        "decision": portfolio.get("final_strategy"),
        "action": executable_action,
        "confidence_score": 95,
    }

    orchestration = {
        "decision": portfolio.get("final_strategy"),
        "orchestration_action": executable_action,
        "orchestration_status": "ORCHESTRATION_READY",
        "orchestration_risk": "LOW",
        "execution_authorization": "AUTHORIZED",
        "reassessment_policy": "NOT_REQUIRED",
        "confidence_score": 95,
        "orchestration_score": 95,
        "integrated_score": 95,
        "governance_score": 95,
        "lifecycle_score": 95,
        "operational_score": 95,
    }

    integrated_intelligence = {
        "decision": portfolio.get("final_strategy"),
        "action": executable_action,
        "execution_authorization": "AUTHORIZED",
        "integrated_score": 95,
        "integrated_risk": "LOW",
        "confidence_score": 95,
    }

    lifecycle_governance_control = {
        "execution_authorization": "AUTHORIZED",
        "reassessment_policy": "NOT_REQUIRED",
        "governance_score": 95,
        "operational_risk": "LOW",
    }

    operational_intelligence = {
        "operational_score": 95,
        "intelligence_risk": "LOW",
    }

    execution = execution_engine.analyze(
        final_decision,
        orchestration,
        integrated_intelligence,
        lifecycle_governance_control,
        operational_intelligence,
    )

    print("final execution action:",
          execution.get("action"))

    print("execution decision:",
          execution.get("execution_decision"))

    print("execution status:",
          execution.get("execution_status"))

    assert execution.get("action") == \
        case["expected_adaptive_action"]

    assert execution.get("execution_decision") == \
        case["expected_adaptive_action"]

    assert execution.get("execution_status") == \
        "EXECUTION_READY"

    print("final execution decision contract: PASS")

    # ------------------------------------------------------------
    # 7. Execution Control
    # ------------------------------------------------------------

    execution_control = control_engine.control(
        {
            "decision": portfolio.get("final_strategy"),
            "action": executable_action,
            "execution_status": "EXECUTION_READY",
            "confidence_score": 95,
            "validation_status": "VALID",
            "validation_score": 95,
        },
        {
            "decision": portfolio.get("final_strategy"),
            "action": executable_action,
            "execution_status": "EXECUTION_READY",
            "governance_status": "APPROVED",
            "governance_score": 95,
            "integrity_status": "INTACT",
            "execution_readiness": "READY",
            "risk_governance": "ACCEPTABLE",
            "override_status": "NONE",
            "confidence_score": 95,
            "validation_status": "VALID",
            "validation_score": 95,
            "monitoring_policy": "STANDARD",
        },
    )

    print("control action:",
          execution_control.get("control_action"))

    print("control status:",
          execution_control.get("control_status"))

    assert execution_control.get("action") == \
        case["expected_adaptive_action"]

    assert execution_control.get("control_action") == \
        "MONITOR"

    assert execution_control.get("control_status") == \
        "AUTHORIZED_WITH_MONITORING"

    print("execution control contract: PASS")

    # ------------------------------------------------------------
    # 8. Master Control
    # ------------------------------------------------------------

    master = master_engine.analyze(
        {
            "decision": "PROCEED",
            "action": "PROCEED",
        },
        {
            "certification_status": "CERTIFIED",
            "certification_action": "PROCEED",
            "certification_risk": "LOW",
            "execution_status": "EXECUTION_READY",
            "execution_authorization": "AUTHORIZED",
            "execution_readiness": "READY",
            "decision_integrity": "INTACT",
            "certification_score": 97,
        },
        {
            "decision": "PROCEED",
            "action": "PROCEED",
            "execution_status": "EXECUTION_READY",
            "execution_authorization": "AUTHORIZED",
            "execution_score": 95,
        },
        {
            "governance_status": "APPROVED",
            "governance_score": 96,
        },
        {
            "lifecycle_status": "HEALTHY",
            "lifecycle_score": 94,
            "reassessment_required": False,
        },
        {
            "operational_status": "OPERATIONALLY_HEALTHY",
            "operational_score": 93,
        },
        {
            "orchestration_status": "ORCHESTRATION_READY",
            "orchestration_score": 92,
        },
        {
            "integrated_status": "INTEGRATED_HEALTHY",
            "integrated_score": 91,
        },
        {
            "validation_status": "VALID",
            "validation_score": 90,
        },
    )

    print("master control status:",
          master.get("master_control_status"))

    print("master control action:",
          master.get("master_control_action"))

    print("master control risk:",
          master.get("master_control_risk"))

    print("master execution control:",
          master.get("execution_control"))

    assert master.get("master_control_status") == \
        "MASTER_READY"

    assert master.get("master_control_action") == \
        "PROCEED"

    assert master.get("execution_control") == \
        "EXECUTE"

    print("master control contract: PASS")

    # ------------------------------------------------------------
    # CASE COMPLETE
    # ------------------------------------------------------------

    print()
    print(
        "E2E CONTRACT:",
        "PASS"
    )


print()
print("=" * 82)
print("FINAL ASSERTIONS")
print("=" * 82)

print(
    "NEGATIVE -> DEFENSIVE -> REDUCE_RISK -> MASTER_READY: PASS"
)

print(
    "POSITIVE -> GROWTH -> INCREASE_RISK -> MASTER_READY: PASS"
)

print(
    "PENDING -> MAINTAIN -> MAINTAIN_ALLOCATION -> MASTER_READY: PASS"
)

print()
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

print()
print(
    "===== PHASE 7-6 END-TO-END SEMANTIC CONTRACT TEST COMPLETE ====="
)



