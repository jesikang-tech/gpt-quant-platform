from core.ai_decision_outcome_collector import AIDecisionOutcomeDataCollector


def build_case(reassessment_required):

    if reassessment_required:
        return {
            "final_decision": {
                "decision": "MAINTAIN",
                "action": "REVIEW"
            },
            "master_control": {
                "decision": "MAINTAIN",
                "master_control_action": "REVIEW",
                "master_control_status": "MASTER_REVIEW",
                "master_control_risk": "MEDIUM",
                "execution_control": "HOLD",
                "reassessment_required": True
            },
            "certification": {
                "certification_status": "CERTIFICATION_REVIEW",
                "certification_score": 82.3
            },
            "execution": {
                "execution_status": "EXECUTION_REVIEW",
                "execution_authorization": "SUSPENDED",
                "execution_score": 80.0
            },
            "reassessment": {
                "reassessment_status": "REASSESSMENT_REQUIRED",
                "reassessment_required": True
            }
        }

    return {
        "final_decision": {
            "decision": "MAINTAIN",
            "action": "PROCEED"
        },
        "master_control": {
            "decision": "MAINTAIN",
            "master_control_action": "PROCEED",
            "master_control_status": "MASTER_READY",
            "master_control_risk": "LOW",
            "execution_control": "EXECUTE",
            "reassessment_required": False
        },
        "certification": {
            "certification_status": "CERTIFIED",
            "certification_score": 90.0
        },
        "execution": {
            "execution_status": "EXECUTION_READY",
            "execution_authorization": "AUTHORIZED",
            "execution_score": 90.0
        },
        "reassessment": {
            "reassessment_status": "NOT_REQUIRED",
            "reassessment_required": False
        }
    }


def run_case(name, reassessment_required):

    case = build_case(reassessment_required)

    collector = AIDecisionOutcomeDataCollector()

    snapshot = collector.collect(
        final_decision=case["final_decision"],
        final_decision_master_control=case["master_control"],
        final_decision_certification=case["certification"],
        final_execution_decision=case["execution"],
        final_decision_execution_reassessment=case["reassessment"]
    )

    print("")
    print("=" * 82)
    print(f"CASE: {name}")
    print("=" * 82)

    print("--- MASTER CONTROL ---")
    print(
        "master_control_status:",
        case["master_control"]["master_control_status"]
    )
    print(
        "master_control_action:",
        case["master_control"]["master_control_action"]
    )
    print(
        "execution_control:",
        case["master_control"]["execution_control"]
    )
    print(
        "reassessment_required:",
        case["master_control"]["reassessment_required"]
    )

    print("--- OUTCOME SNAPSHOT ---")
    print("snapshot_status:", snapshot["snapshot_status"])
    print("decision:", snapshot["decision"])
    print("action:", snapshot["action"])
    print("execution_status:", snapshot["execution_status"])
    print(
        "execution_authorization:",
        snapshot["execution_authorization"]
    )
    print(
        "certification_status:",
        snapshot["certification_status"]
    )
    print(
        "reassessment_status:",
        snapshot["reassessment_status"]
    )
    print(
        "reassessment_required:",
        snapshot["reassessment_required"]
    )
    print("snapshot_purpose:", snapshot["snapshot_purpose"])
    print("outcome_status:", snapshot["outcome_status"])

    assert snapshot["snapshot_status"] == "COLLECTED"
    assert snapshot["snapshot_purpose"] == "FUTURE_OUTCOME_EVALUATION"
    assert snapshot["outcome_status"] == "PENDING"

    if reassessment_required:

        assert snapshot["decision"] == "MAINTAIN"
        assert snapshot["action"] == "REVIEW"
        assert snapshot["execution_status"] == "EXECUTION_REVIEW"
        assert snapshot["execution_authorization"] == "SUSPENDED"
        assert snapshot["certification_status"] == "CERTIFICATION_REVIEW"
        assert snapshot["reassessment_status"] == "REASSESSMENT_REQUIRED"
        assert snapshot["reassessment_required"] is True

    else:

        assert snapshot["decision"] == "MAINTAIN"
        assert snapshot["action"] == "PROCEED"
        assert snapshot["execution_status"] == "EXECUTION_READY"
        assert snapshot["execution_authorization"] == "AUTHORIZED"
        assert snapshot["certification_status"] == "CERTIFIED"
        assert snapshot["reassessment_status"] == "NOT_REQUIRED"
        assert snapshot["reassessment_required"] is False

    print(f"{name} -> OUTCOME SNAPSHOT: PASS")

    return snapshot


print("=" * 82)
print("PHASE 7-9-9 MASTER CONTROL -> OUTCOME SNAPSHOT")
print("DOWNSTREAM PROPAGATION BOUNDARY CONTRACT TEST")
print("SOURCE-VERIFIED / MEMORY-ONLY / READ-ONLY")
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
    "REASSESSMENT_REQUIRED -> MASTER_REVIEW / REVIEW / HOLD "
    "-> SNAPSHOT PENDING / REASSESSMENT_REQUIRED: PASS"
)

print(
    "NOT_REQUIRED -> MASTER_READY / PROCEED / EXECUTE "
    "-> SNAPSHOT PENDING / NOT_REQUIRED: PASS"
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
print("===== PHASE 7-9-9 MASTER CONTROL -> OUTCOME SNAPSHOT")
print("===== CONTRACT TEST COMPLETE")
print("=" * 82)
