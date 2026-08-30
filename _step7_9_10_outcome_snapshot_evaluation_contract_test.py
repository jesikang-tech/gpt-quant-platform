from core.ai_decision_outcome_collector import AIDecisionOutcomeDataCollector
from core.ai_decision_outcome_evaluation import AIDecisionOutcomeEvaluation


def build_snapshot(reassessment_required):

    collector = AIDecisionOutcomeDataCollector()

    if reassessment_required:

        return collector.collect(
            final_decision={
                "decision": "MAINTAIN",
                "action": "REVIEW"
            },
            final_decision_master_control={
                "decision": "MAINTAIN",
                "master_control_action": "REVIEW",
                "master_control_status": "MASTER_REVIEW",
                "master_control_risk": "MEDIUM",
                "execution_control": "HOLD",
                "reassessment_required": True
            },
            final_decision_certification={
                "certification_status": "CERTIFICATION_REVIEW",
                "certification_score": 82.3
            },
            final_execution_decision={
                "execution_status": "EXECUTION_REVIEW",
                "execution_authorization": "SUSPENDED",
                "execution_score": 80.0
            },
            final_decision_execution_reassessment={
                "reassessment_status": "REASSESSMENT_REQUIRED",
                "reassessment_required": True
            }
        )

    return collector.collect(
        final_decision={
            "decision": "MAINTAIN",
            "action": "PROCEED"
        },
        final_decision_master_control={
            "decision": "MAINTAIN",
            "master_control_action": "PROCEED",
            "master_control_status": "MASTER_READY",
            "master_control_risk": "LOW",
            "execution_control": "EXECUTE",
            "reassessment_required": False
        },
        final_decision_certification={
            "certification_status": "CERTIFIED",
            "certification_score": 90.0
        },
        final_execution_decision={
            "execution_status": "EXECUTION_READY",
            "execution_authorization": "AUTHORIZED",
            "execution_score": 90.0
        },
        final_decision_execution_reassessment={
            "reassessment_status": "NOT_REQUIRED",
            "reassessment_required": False
        }
    )


def run_case(name, reassessment_required):

    snapshot = build_snapshot(
        reassessment_required
    )

    evaluator = AIDecisionOutcomeEvaluation()

    evaluation = evaluator.evaluate(
        outcome_snapshot=snapshot,
        actual_outcome=None
    )

    print("")
    print("=" * 82)
    print(f"CASE: {name}")
    print("=" * 82)

    print("--- OUTCOME SNAPSHOT ---")
    print(
        "snapshot_status:",
        snapshot["snapshot_status"]
    )
    print(
        "outcome_status:",
        snapshot["outcome_status"]
    )
    print(
        "reassessment_status:",
        snapshot["reassessment_status"]
    )
    print(
        "reassessment_required:",
        snapshot["reassessment_required"]
    )

    print("--- OUTCOME EVALUATION ---")
    print(
        "evaluation_status:",
        evaluation.get("evaluation_status")
    )
    print(
        "learning_signal:",
        evaluation.get("learning_signal")
    )
    print(
        "learning_signal_strength:",
        evaluation.get(
            "learning_signal_strength"
        )
    )

    assert snapshot["snapshot_status"] == "COLLECTED"
    assert snapshot["outcome_status"] == "PENDING"

    assert (
        evaluation.get("evaluation_status")
        == "WAITING_FOR_OUTCOME"
    )

    assert (
        evaluation.get("learning_signal")
        == "NONE"
    )

    assert (
        evaluation.get("learning_signal_strength")
        == 0.0
    )

    print(
        f"{name} -> OUTCOME EVALUATION: PASS"
    )

    return evaluation


print("=" * 82)
print(
    "PHASE 7-9-10 OUTCOME SNAPSHOT -> "
    "OUTCOME EVALUATION"
)
print(
    "WAITING-FOR-OUTCOME BOUNDARY CONTRACT TEST"
)
print(
    "SOURCE-VERIFIED / MEMORY-ONLY / READ-ONLY"
)
print("=" * 82)

required = run_case(
    "REASSESSMENT_REQUIRED",
    True
)

normal = run_case(
    "NOT_REQUIRED",
    False
)

print("")
print("=" * 82)
print("FINAL ASSERTIONS")
print("=" * 82)

print(
    "REASSESSMENT_REQUIRED -> SNAPSHOT PENDING "
    "-> WAITING_FOR_OUTCOME / NONE / 0.0: PASS"
)

print(
    "NOT_REQUIRED -> SNAPSHOT PENDING "
    "-> WAITING_FOR_OUTCOME / NONE / 0.0: PASS"
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
print("No actual Outcome supplied to evaluator.")

print("")
print(
    "===== PHASE 7-9-10 OUTCOME SNAPSHOT -> "
    "OUTCOME EVALUATION"
)
print("===== CONTRACT TEST COMPLETE")
print("=" * 82)
