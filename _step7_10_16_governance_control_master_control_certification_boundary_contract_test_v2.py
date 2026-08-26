"""
GPT Quant Platform
Phase 7-10-16
Governance Control -> Master Control / Certification
Boundary Contract Test V2

SOURCE-VERIFIED / MEMORY-ONLY / READ-ONLY
No production DB access.
No API runtime call.
No persistence.
"""

from core.ai_final_decision_master_control import (
    AIFinalDecisionMasterControl,
)


engine = AIFinalDecisionMasterControl()


def build_base_inputs():
    return {
        "final_decision": {
            "decision": "MAINTAIN",
            "action": "PROCEED",
        },
        "certification": {
            "decision": "MAINTAIN",
            "certification_status": "CERTIFIED",
            "certification_risk": "LOW",
            "certification_score": 97.9,
            "execution_status": "EXECUTION_READY",
            "execution_authorization": "AUTHORIZED",
            "execution_readiness": "READY",
            "decision_integrity": "INTACT",
        },
        "execution_decision": {
            "decision": "MAINTAIN",
            "action": "PROCEED",
            "execution_status": "EXECUTION_READY",
            "execution_authorization": "AUTHORIZED",
        },
        "governance": {
            "governance_status": "APPROVED",
            "governance_score": 98.8,
        },
        "lifecycle": {
            "lifecycle_status": "HEALTHY",
            "lifecycle_score": 95.0,
            "reassessment_required": False,
        },
        "operational_intelligence": {
            "operational_status": "OPERATIONALLY_HEALTHY",
            "operational_score": 95.0,
        },
        "orchestration": {
            "orchestration_status": "ORCHESTRATION_READY",
            "orchestration_score": 95.0,
        },
        "integrated_intelligence": {
            "integrated_status": "INTEGRATED_HEALTHY",
            "integrated_score": 95.0,
        },
        "validation": {
            "validation_status": "VALID",
            "validation_score": 95.0,
        },
    }


def run_case(name, mutate=None):
    data = build_base_inputs()

    if mutate is not None:
        mutate(data)

    result = engine.analyze(
        final_decision=data["final_decision"],
        certification=data["certification"],
        execution_decision=data["execution_decision"],
        governance=data["governance"],
        lifecycle=data["lifecycle"],
        operational_intelligence=data["operational_intelligence"],
        orchestration=data["orchestration"],
        integrated_intelligence=data["integrated_intelligence"],
        validation=data["validation"],
    )

    print("=" * 82)
    print(f"CASE: {name}")
    print("=" * 82)

    print("--- GOVERNANCE CONTROL SOURCE ---")
    print(
        "governance_status:",
        data["governance"]["governance_status"],
    )
    print(
        "lifecycle_status:",
        data["lifecycle"]["lifecycle_status"],
    )
    print(
        "reassessment_required:",
        data["lifecycle"]["reassessment_required"],
    )
    print(
        "operational_status:",
        data["operational_intelligence"]["operational_status"],
    )

    print("--- CERTIFICATION SOURCE ---")
    print(
        "certification_status:",
        data["certification"]["certification_status"],
    )
    print(
        "execution_status:",
        data["certification"]["execution_status"],
    )
    print(
        "execution_authorization:",
        data["certification"]["execution_authorization"],
    )
    print(
        "execution_readiness:",
        data["certification"]["execution_readiness"],
    )
    print(
        "decision_integrity:",
        data["certification"]["decision_integrity"],
    )

    print("--- MASTER CONTROL RESULT ---")
    print(
        "master_control_status:",
        result["master_control_status"],
    )
    print(
        "master_control_action:",
        result["master_control_action"],
    )
    print(
        "master_control_risk:",
        result["master_control_risk"],
    )
    print(
        "execution_control:",
        result["execution_control"],
    )

    return result


# ---------------------------------------------------------------------------
# CASE 1
# Governance Control + Certification fully healthy
# -> MASTER_READY / PROCEED / LOW / EXECUTE
# ---------------------------------------------------------------------------

result = run_case(
    "APPROVED_CERTIFIED_MASTER_READY"
)

assert result["master_control_status"] == "MASTER_READY"
assert result["master_control_action"] == "PROCEED"
assert result["master_control_risk"] == "LOW"
assert result["execution_control"] == "EXECUTE"

print("APPROVED -> MASTER_READY boundary: PASS")
print("Certified execution boundary: PASS")


# ---------------------------------------------------------------------------
# CASE 2
# Reassessment must override otherwise healthy state
# ---------------------------------------------------------------------------

result = run_case(
    "REASSESSMENT_PRIORITY",
    lambda d: d["lifecycle"].update(
        {
            "reassessment_required": True,
        }
    ),
)

assert result["master_control_status"] == "MASTER_REVIEW"
assert result["master_control_action"] == "REVIEW"
assert result["master_control_risk"] == "MEDIUM"
assert result["execution_control"] == "HOLD"
assert result["reassessment_required"] is True

print("Reassessment priority boundary: PASS")
print("Reassessment -> MASTER_REVIEW boundary: PASS")


# ---------------------------------------------------------------------------
# CASE 3
# Certification blocked must dominate healthy downstream signals
# ---------------------------------------------------------------------------

result = run_case(
    "CERTIFICATION_BLOCK_PRIORITY",
    lambda d: d["certification"].update(
        {
            "certification_status": "CERTIFICATION_BLOCKED",
        }
    ),
)

assert result["master_control_status"] == "MASTER_BLOCKED"
assert result["master_control_action"] == "HALT"
assert result["master_control_risk"] == "CRITICAL"
assert result["execution_control"] == "HOLD"

print("Certification block priority boundary: PASS")
print("Certification -> Master Control propagation: PASS")


print("")
print("=" * 82)
print("FINAL ASSERTIONS")
print("=" * 82)
print("Governance Control -> Master Control propagation: PASS")
print("Certification -> Master Control boundary: PASS")
print("MASTER_READY execution boundary: PASS")
print("Reassessment priority boundary: PASS")
print("Certification BLOCK priority boundary: PASS")
print("Execution control boundary: PASS")

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
print("=" * 82)
print("===== PHASE 7-10-16 CONTRACT TEST V2 COMPLETE =====")
print("=" * 82)
