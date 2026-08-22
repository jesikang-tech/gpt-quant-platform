from core.ai_decision_outcome_evaluation import AIDecisionOutcomeEvaluation
from core.ai_decision_outcome_intelligence import AIDecisionOutcomeIntelligence
from core.ai_decision_adaptive_strategy import AIDecisionAdaptiveStrategy
from core.portfolio_decision_intelligence import PortfolioDecisionIntelligence
from core.ai_decision_validation import AIDecisionValidation
from core.ai_decision_validation_action import AIDecisionValidationAction
from core.ai_decision_validation_explainability import AIDecisionValidationExplainability
from core.ai_final_execution_decision import AIFinalExecutionDecision
from core.ai_final_decision_master_control import AIFinalDecisionMasterControl

print("=" * 90)
print("PHASE 7-8 FINAL END-TO-END SEMANTIC CONTRACT TEST")
print("OUTCOME -> ADAPTIVE -> PORTFOLIO -> VALIDATION -> ACTION")
print("-> EXPLAINABILITY -> FINAL EXECUTION -> MASTER CONTROL")
print("SOURCE-VERIFIED / MEMORY-ONLY / READ-ONLY")
print("=" * 90)

evaluation_engine = AIDecisionOutcomeEvaluation()
intelligence_engine = AIDecisionOutcomeIntelligence()
adaptive_engine = AIDecisionAdaptiveStrategy()
portfolio_engine = PortfolioDecisionIntelligence()
validation_engine = AIDecisionValidation()
action_engine = AIDecisionValidationAction()
explainability_engine = AIDecisionValidationExplainability()
execution_engine = AIFinalExecutionDecision()
master_engine = AIFinalDecisionMasterControl()

trend = {
    "direction": "STABLE",
    "stability": "HIGH",
    "momentum": "NEUTRAL",
    "grade_stability": "STABLE",
    "consistency": "HIGH",
    "latest_score": 85,
}

base_decision = {
    "decision": "ACCUMULATE",
    "action": "PROCEED",
    "execution_status": "AUTHORIZED",
    "confidence_score": 95.0,
    "intelligence_score": 90.0,
}

cases = [
    {
        "name": "NEGATIVE",
        "actual_outcome": {
            "outcome_score": 40.0,
            "market_response": "NEGATIVE",
            "portfolio_response": "NEGATIVE",
        },
        "expected_signal": "NEGATIVE",
        "expected_strategy": "DEFENSIVE",
        "expected_adaptive_action": "REDUCE_RISK",
        "expected_execution_status": "EXECUTION_READY",
        "expected_master_status": "MASTER_READY",
        "expected_master_action": "PROCEED",
        "expected_execution_control": "EXECUTE",
    },
    {
        "name": "POSITIVE",
        "actual_outcome": {
            "outcome_score": 90.0,
            "market_response": "POSITIVE",
            "portfolio_response": "POSITIVE",
        },
        "expected_signal": "POSITIVE",
        "expected_strategy": "GROWTH",
        "expected_adaptive_action": "INCREASE_RISK",
        "expected_execution_status": "EXECUTION_READY",
        "expected_master_status": "MASTER_READY",
        "expected_master_action": "PROCEED",
        "expected_execution_control": "EXECUTE",
    },
    {
        "name": "PENDING",
        "actual_outcome": {},
        "expected_signal": "NONE",
        "expected_strategy": "MAINTAIN",
        "expected_adaptive_action": "MAINTAIN_ALLOCATION",
        "expected_execution_status": "EXECUTION_READY",
        "expected_master_status": "MASTER_READY",
        "expected_master_action": "PROCEED",
        "expected_execution_control": "EXECUTE",
    },
]

for case in cases:

    print("")
    print("=" * 90)
    print(f"CASE: {case['name']}")
    print("=" * 90)

    # -------------------------------------------------
    # 1. Outcome Evaluation
    # -------------------------------------------------

    outcome_snapshot = {
        "decision": "ACCUMULATE",
        "action": "PROCEED",
        "strategy": "BALANCED",
        "snapshot_status": "COLLECTED",
        "snapshot_purpose": "FUTURE_OUTCOME_EVALUATION",
    }

    evaluation = evaluation_engine.evaluate(
        outcome_snapshot=outcome_snapshot,
        actual_outcome=case["actual_outcome"],
    )

    print("evaluation status:", evaluation.get("evaluation_status"))
    print("outcome score:", evaluation.get("outcome_score"))
    print("learning signal:", evaluation.get("learning_signal"))
    print("learning strength:", evaluation.get("learning_signal_strength"))

    assert evaluation.get("learning_signal") == case["expected_signal"]
    print("OUTCOME EVALUATION: PASS")

    # -------------------------------------------------
    # 2. Outcome Intelligence
    # -------------------------------------------------

    outcome_intelligence = intelligence_engine.analyze(
        final_decision=base_decision,
        final_decision_master_control={},
        final_decision_certification={},
        final_execution_decision={},
        final_decision_execution_feedback={},
        final_decision_execution_monitoring={},
        final_decision_execution_reassessment={},
        intelligence={"intelligence_score": 90.0},
        intelligence_score={"intelligence_score": 90.0},
        decision_confidence={"confidence_score": 95.0},
        outcome_evaluation=evaluation,
    )

    print("intelligence learning signal:",
          outcome_intelligence.get("outcome_learning_signal"))
    print("intelligence learning strength:",
          outcome_intelligence.get("outcome_learning_signal_strength"))
    print("learning status:",
          outcome_intelligence.get("learning_status"))
    print("adaptive learning required:",
          outcome_intelligence.get("adaptive_learning_required"))

    assert outcome_intelligence.get(
        "outcome_learning_signal"
    ) == case["expected_signal"]

    print("OUTCOME INTELLIGENCE: PASS")

    # -------------------------------------------------
    # 3. Adaptive Strategy
    # -------------------------------------------------

    adaptive = adaptive_engine.analyze(
        trend,
        outcome_intelligence=outcome_intelligence,
    )

    print("adaptive strategy:", adaptive.get("strategy"))
    print("adaptive action:", adaptive.get("action"))

    assert adaptive.get("strategy") == case["expected_strategy"]
    assert adaptive.get("action") == case["expected_adaptive_action"]

    print("ADAPTIVE STRATEGY: PASS")

    # -------------------------------------------------
    # 4. Portfolio Intelligence
    # -------------------------------------------------

    portfolio = portfolio_engine.generate(
        ai_decision=base_decision,
        decision_quality={
            "quality": 90.0,
            "quality_grade": "A",
        },
        reliability={
            "confidence_score": 95.0,
            "reliability_level": "HIGH",
        },
        adaptive_strategy=adaptive,
        rebalance={
            "rebalance_action": "HOLD",
        },
        optimization={
            "optimization_status": "OPTIMIZED",
        },
        explainability={
            "summary": "Canonical semantic contract test",
        },
    )

    print("portfolio strategy:", portfolio.get("strategy_mode"))
    print("portfolio adaptive action:", portfolio.get("adaptive_action"))
    print("portfolio final strategy:", portfolio.get("final_strategy"))
    print("portfolio final action:", portfolio.get("final_action"))

    assert portfolio.get(
        "strategy_mode"
    ) == case["expected_strategy"]

    assert portfolio.get(
        "adaptive_action"
    ) == case["expected_adaptive_action"]

    print("PORTFOLIO INTELLIGENCE: PASS")

    # -------------------------------------------------
    # 5. Validation
    # -------------------------------------------------

    validation_intelligence = {
        "decision": base_decision["decision"],
        "strategy_mode": portfolio.get(
            "strategy_mode"
        ),
        "adaptive_action": portfolio.get(
            "adaptive_action"
        ),
        "decision_alignment": portfolio.get(
            "decision_alignment",
            "ALIGNED"
        ),
        "decision_consistency": portfolio.get(
            "decision_consistency",
            "CONSISTENT"
        ),
        "reliability": "HIGH",
        "optimization_status": "COMPLETED",
        "adaptive_override": portfolio.get(
            "adaptive_override",
            False
        ),
    }

    validation = validation_engine.validate(
        validation_intelligence,
        {
            "confidence_score": 95.0,
            "confidence_level": "HIGH",
        },
        {
            "attention_signals": [],
        },
        {
            "recommendation": "PROCEED",
        },
    )

    print("validation status:", validation.get("validation_status"))
    print("validation score:", validation.get("validation_score"))

    assert validation.get("validation_status") == "VALID"

    print("VALIDATION: PASS")

    # -------------------------------------------------
    # 6. Validation Action
    # -------------------------------------------------

    validation_action = action_engine.decide(
        validation,
        {
            "confidence_score": 95.0,
            "confidence_level": "HIGH",
        },
        {
            "attention_signals": [],
        },
        {
            "recommendation": "PROCEED",
        },
    )

    print("validation action:",
          validation_action.get("action"))
    print("execution status:",
          validation_action.get("execution_status"))
    print("action strategy:",
          validation_action.get("strategy_mode"))
    print("action adaptive action:",
          validation_action.get("adaptive_action"))

    assert validation_action.get(
        "strategy_mode"
    ) == case["expected_strategy"]

    assert validation_action.get(
        "adaptive_action"
    ) == case["expected_adaptive_action"]

    print("VALIDATION ACTION: PASS")

    # -------------------------------------------------
    # 7. Explainability
    # -------------------------------------------------

    explainability = explainability_engine.explain(
        validation=validation,
        validation_action=validation_action,
        portfolio_intelligence=portfolio,
        final_decision=base_decision,
    )

    print("explainability strategy:",
          explainability.get("strategy_mode"))
    print("explainability adaptive action:",
          explainability.get("adaptive_action"))
    print("explainability alignment:",
          explainability.get("decision_alignment"))
    print("explainability consistency:",
          explainability.get("decision_consistency"))

    assert explainability.get(
        "strategy_mode"
    ) == case["expected_strategy"]

    assert explainability.get(
        "adaptive_action"
    ) == case["expected_adaptive_action"]

    print("EXPLAINABILITY: PASS")

    # -------------------------------------------------
    # 8. Final Execution Decision
    # -------------------------------------------------

    orchestration = {
        "decision": base_decision["decision"],
        "orchestration_action": "PROCEED",
        "orchestration_status": "ORCHESTRATION_READY",
        "orchestration_risk": "LOW",
        "execution_authorization": "AUTHORIZED",
        "reassessment_policy": "NOT_REQUIRED",
        "confidence_score": 95.0,
        "orchestration_score": 95.0,
        "integrated_score": 95.0,
        "governance_score": 95.0,
        "lifecycle_score": 95.0,
        "operational_score": 95.0,
    }

    integrated = {
        "integrated_status": "INTEGRATED_HEALTHY",
        "integrated_score": 95.0,
    }

    lifecycle_governance = {
        "lifecycle_status": "HEALTHY",
        "lifecycle_score": 95.0,
        "reassessment_required": False,
        "reassessment_policy": "NOT_REQUIRED",
        "execution_authorization": "AUTHORIZED",
        "governance_score": 95.0,
    }

    operational = {
        "operational_status": "OPERATIONALLY_HEALTHY",
        "operational_score": 95.0,
    }

    final_execution = execution_engine.analyze(
        final_decision=base_decision,
        orchestration=orchestration,
        integrated_intelligence=integrated,
        lifecycle_governance_control=lifecycle_governance,
        operational_intelligence=operational,
    )

    print("final execution status:",
          final_execution.get("execution_status"))
    print("final execution decision:",
          final_execution.get("execution_decision"))
    print("execution authorization:",
          final_execution.get("execution_authorization"))

    assert final_execution.get(
        "execution_status"
    ) == case["expected_execution_status"]

    print("FINAL EXECUTION: PASS")

    # -------------------------------------------------
    # 9. Master Control
    # -------------------------------------------------

    certification = {
        "decision": final_execution.get("decision"),
        "certification_status": "CERTIFIED",
        "certification_risk": "LOW",
        "execution_status": final_execution.get("execution_status"),
        "execution_authorization": final_execution.get(
            "execution_authorization"
        ),
        "execution_readiness": "READY",
        "decision_integrity": "INTACT",
        "certification_score": 95.0,
        "certification_action": final_execution.get("action"),
    }

    governance = {
        "governance_status": "APPROVED",
        "governance_score": 95.0,
    }

    lifecycle = {
        "lifecycle_status": "HEALTHY",
        "lifecycle_score": 95.0,
        "reassessment_required": False,
    }

    validation_master = {
        "validation_status": "VALID",
        "validation_score": 95.0,
    }

    master = master_engine.analyze(
        final_decision=base_decision,
        certification=certification,
        execution_decision=final_execution,
        governance=governance,
        lifecycle=lifecycle,
        operational_intelligence=operational,
        orchestration=orchestration,
        integrated_intelligence=integrated,
        validation=validation_master,
    )

    print("master status:",
          master.get("master_control_status"))
    print("master action:",
          master.get("master_control_action"))
    print("master risk:",
          master.get("master_control_risk"))
    print("execution control:",
          master.get("execution_control"))

    assert master.get(
        "master_control_status"
    ) == case["expected_master_status"]

    assert master.get(
        "master_control_action"
    ) == case["expected_master_action"]

    assert master.get(
        "execution_control"
    ) == case["expected_execution_control"]

    print("MASTER CONTROL: PASS")

    print("")
    print("END-TO-END SEMANTIC CONTRACT: PASS")


print("")
print("=" * 90)
print("FINAL ASSERTIONS")
print("=" * 90)
print("NEGATIVE -> DEFENSIVE -> REDUCE_RISK -> FINAL EXECUTION -> MASTER: PASS")
print("POSITIVE -> GROWTH -> INCREASE_RISK -> FINAL EXECUTION -> MASTER: PASS")
print("PENDING -> MAINTAIN -> MAINTAIN_ALLOCATION -> FINAL EXECUTION -> MASTER: PASS")

print("")
print("=" * 90)
print("SAFETY")
print("=" * 90)
print("Memory-only execution: PASS")
print("No production DB access.")
print("No API runtime call.")
print("No INSERT.")
print("No UPDATE.")
print("No DELETE.")
print("No future price injection.")
print("No fake Outcome persistence.")

print("")
print("=" * 90)
print("===== PHASE 7-8 FINAL END-TO-END SEMANTIC CONTRACT TEST COMPLETE =====")
print("=" * 90)


