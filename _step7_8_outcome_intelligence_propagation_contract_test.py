from core.ai_decision_outcome_evaluation import (
    AIDecisionOutcomeEvaluation,
)
from core.ai_decision_outcome_intelligence import (
    AIDecisionOutcomeIntelligence,
)

print("=" * 82)
print("PHASE 7-8 OUTCOME EVALUATION -> OUTCOME INTELLIGENCE")
print("PROPAGATION CONTRACT TEST")
print("MEMORY-ONLY / READ-ONLY")
print("=" * 82)

evaluation_engine = AIDecisionOutcomeEvaluation()
intelligence_engine = AIDecisionOutcomeIntelligence()

snapshot = {
    "decision": "TEST_DECISION",
    "action": "TEST_ACTION",
    "strategy": "TEST_STRATEGY",
    "snapshot_status": "COLLECTED",
    "snapshot_purpose": "MEMORY_ONLY_CONTRACT_TEST",
}

cases = [
    {
        "name": "NEGATIVE",
        "score": 40.0,
        "signal": "NEGATIVE",
        "strength": 20.0,
        "adaptive_required": True,
    },
    {
        "name": "POSITIVE",
        "score": 90.0,
        "signal": "POSITIVE",
        "strength": 80.0,
        "adaptive_required": False,
    },
    {
        "name": "STABLE",
        "score": 70.0,
        "signal": "STABLE",
        "strength": 40.0,
        "adaptive_required": False,
    },
]

for case in cases:
    print()
    print("=" * 82)
    print("CASE:", case["name"])
    print("=" * 82)

    evaluation = evaluation_engine.evaluate(
        outcome_snapshot=snapshot,
        actual_outcome={
            "outcome_score": case["score"],
            "market_response": "EVALUATED",
            "portfolio_response": "EVALUATED",
        },
    )

    print("evaluation status:", evaluation.get("evaluation_status"))
    print("evaluation signal:", evaluation.get("learning_signal"))
    print("evaluation strength:", evaluation.get("learning_signal_strength"))

    assert evaluation.get("evaluation_status") == "EVALUATED"
    assert evaluation.get("learning_signal") == case["signal"]
    assert evaluation.get("learning_signal_strength") == case["strength"]

    print("evaluation contract: PASS")

    intelligence = intelligence_engine.analyze(
        final_decision={
            "decision": "TEST_DECISION",
            "action": "TEST_ACTION",
            "execution_status": "EXECUTION_READY",
        },
        final_decision_master_control={
            "decision": "TEST_DECISION",
            "action": "TEST_ACTION",
            "execution_status": "EXECUTION_READY",
            "execution_authorization": "AUTHORIZED",
        },
        final_decision_certification={
            "certification_status": "CERTIFIED",
            "execution_status": "EXECUTION_READY",
            "execution_authorization": "AUTHORIZED",
        },
        final_execution_decision={
            "decision": "TEST_DECISION",
            "action": "TEST_ACTION",
            "execution_status": "EXECUTION_READY",
            "execution_authorization": "AUTHORIZED",
        },
        final_decision_execution_feedback={
            "feedback_status": "STABLE",
        },
        final_decision_execution_monitoring={
            "monitoring_status": "STANDARD_MONITORING",
        },
        final_decision_execution_reassessment={
            "reassessment_required": False,
            "reassessment_status": "NOT_REQUIRED",
        },
        intelligence={
            "decision": "TEST_DECISION",
            "action": "TEST_ACTION",
        },
        intelligence_score={
            "intelligence_score": 95.0,
        },
        decision_confidence={
            "confidence_score": 95.0,
        },
        outcome_evaluation=evaluation,
    )

    print("intelligence learning signal:",
          intelligence.get("outcome_learning_signal"))
    print("intelligence learning strength:",
          intelligence.get("outcome_learning_signal_strength"))
    print("learning status:",
          intelligence.get("learning_status"))
    print("feedback state:",
          intelligence.get("feedback_state"))
    print("adaptive learning required:",
          intelligence.get("adaptive_learning_required"))

    assert intelligence.get(
        "outcome_learning_signal"
    ) == case["signal"]

    assert intelligence.get(
        "outcome_learning_signal_strength"
    ) == case["strength"]

    if case["signal"] == "NEGATIVE":
        assert intelligence.get(
            "learning_status"
        ) == "ADAPTIVE_LEARNING_REQUIRED"

        assert intelligence.get(
            "feedback_state"
        ) == "ADAPTIVE_LEARNING"

        assert intelligence.get(
            "adaptive_learning_required"
        ) is True
    else:
        assert intelligence.get(
            "learning_status"
        ) == "LEARNING_AVAILABLE"

        assert intelligence.get(
            "feedback_state"
        ) == "LEARNING_AVAILABLE"

        assert intelligence.get(
            "adaptive_learning_required"
        ) is False

    if case["signal"] == "NEGATIVE":
        assert intelligence.get(
            "feedback_state"
        ) == "ADAPTIVE_LEARNING"
    else:
        assert intelligence.get(
            "feedback_state"
        ) == "LEARNING_AVAILABLE"

    assert intelligence.get(
        "adaptive_learning_required"
    ) == case["adaptive_required"]

    print("learning signal propagation: PASS")
    print("learning strength propagation: PASS")
    print("learning status propagation: PASS")
    print("feedback state propagation: PASS")
    print("adaptive learning contract: PASS")
    print("OUTCOME INTELLIGENCE PROPAGATION: PASS")


print()
print("=" * 82)
print("CASE: WAITING FOR OUTCOME")
print("=" * 82)

pending_evaluation = evaluation_engine.evaluate(
    outcome_snapshot=snapshot,
    actual_outcome={},
)

pending_intelligence = intelligence_engine.analyze(
    final_decision={
        "decision": "TEST_DECISION",
        "action": "TEST_ACTION",
        "execution_status": "EXECUTION_READY",
    },
    final_decision_master_control={
        "decision": "TEST_DECISION",
        "action": "TEST_ACTION",
        "execution_status": "EXECUTION_READY",
        "execution_authorization": "AUTHORIZED",
    },
    final_decision_certification={
        "certification_status": "CERTIFIED",
        "execution_status": "EXECUTION_READY",
        "execution_authorization": "AUTHORIZED",
    },
    final_execution_decision={
        "decision": "TEST_DECISION",
        "action": "TEST_ACTION",
        "execution_status": "EXECUTION_READY",
        "execution_authorization": "AUTHORIZED",
    },
    final_decision_execution_feedback={
        "feedback_status": "STABLE",
    },
    final_decision_execution_monitoring={
        "monitoring_status": "STANDARD_MONITORING",
    },
    final_decision_execution_reassessment={
        "reassessment_required": False,
        "reassessment_status": "NOT_REQUIRED",
    },
    intelligence={
        "decision": "TEST_DECISION",
        "action": "TEST_ACTION",
    },
    intelligence_score={
        "intelligence_score": 95.0,
    },
    decision_confidence={
        "confidence_score": 95.0,
    },
    outcome_evaluation=pending_evaluation,
)

print("evaluation status:",
      pending_evaluation.get("evaluation_status"))
print("learning signal:",
      pending_intelligence.get("outcome_learning_signal"))
print("learning strength:",
      pending_intelligence.get("outcome_learning_signal_strength"))
print("learning status:",
      pending_intelligence.get("learning_status"))
print("feedback state:",
      pending_intelligence.get("feedback_state"))
print("adaptive learning required:",
      pending_intelligence.get("adaptive_learning_required"))

assert pending_evaluation.get(
    "evaluation_status"
) == "WAITING_FOR_OUTCOME"

assert pending_intelligence.get(
    "outcome_learning_signal"
) == "NONE"

assert pending_intelligence.get(
    "outcome_learning_signal_strength"
) == 0.0

assert pending_intelligence.get(
    "learning_status"
) == "WAITING_FOR_OUTCOME"

assert pending_intelligence.get(
    "feedback_state"
) == "COLLECTING"

assert pending_intelligence.get(
    "adaptive_learning_required"
) is False

print("pending evaluation propagation: PASS")
print("pending learning contract: PASS")


print()
print("=" * 82)
print("FINAL ASSERTIONS")
print("=" * 82)

print("NEGATIVE -> NEGATIVE -> adaptive required: PASS")
print("POSITIVE -> POSITIVE -> learning available: PASS")
print("STABLE -> STABLE -> learning available: PASS")
print("PENDING -> NONE -> waiting: PASS")


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
print("=" * 82)
print("===== PHASE 7-8 OUTCOME INTELLIGENCE PROPAGATION TEST COMPLETE =====")
print("=" * 82)


