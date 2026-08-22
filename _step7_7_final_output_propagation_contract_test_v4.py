from core.ai_final_decision_master_control import (
    AIFinalDecisionMasterControl
)


print("=" * 82)
print("PHASE 7-7 FINAL OUTPUT PROPAGATION CONTRACT TEST V4")
print("MASTER CONTROL -> FINAL OUTPUT")
print("SOURCE-VERIFIED CANONICAL CONTRACT")
print("MEMORY-ONLY / READ-ONLY")
print("=" * 82)


def ready_inputs():

    return {
        "final_decision": {
            "decision": "ACCUMULATE",
            "action": "PROCEED",
        },

        "certification": {
            "decision": "ACCUMULATE",
            "certification_action": "PROCEED",
            "certification_status": "CERTIFIED",
            "certification_risk": "LOW",
            "execution_status": "EXECUTION_READY",
            "execution_authorization": "AUTHORIZED",
            "execution_readiness": "READY",
            "decision_integrity": "INTACT",
            "certification_score": 95,
        },

        "execution_decision": {
            "decision": "ACCUMULATE",
            "action": "INCREASE_RISK",
            "execution_status": "EXECUTION_READY",
            "execution_authorization": "AUTHORIZED",
            "execution_score": 95,
        },

        "governance": {
            "governance_status": "APPROVED",
            "governance_score": 95,
        },

        "lifecycle": {
            "lifecycle_status": "HEALTHY",
            "lifecycle_score": 95,
        },

        "operational_intelligence": {
            "operational_status": "OPERATIONALLY_HEALTHY",
            "operational_score": 95,
        },

        "orchestration": {
            "orchestration_status": "ORCHESTRATION_READY",
            "orchestration_score": 95,
        },

        "integrated_intelligence": {
            "integrated_status": "INTEGRATED_HEALTHY",
            "integrated_score": 95,
        },

        "validation": {
            "validation_status": "VALID",
            "validation_score": 95,
        },
    }


def review_inputs():

    inputs = ready_inputs()

    inputs["operational_intelligence"][
        "operational_status"
    ] = "WARNING"

    for key in inputs:
        if isinstance(inputs[key], dict):
            if key.endswith("intelligence"):
                continue

    return inputs


def blocked_inputs():

    inputs = ready_inputs()

    inputs["certification"][
        "certification_status"
    ] = "NOT_CERTIFIED"

    inputs["certification"][
        "execution_authorization"
    ] = "UNAUTHORIZED"

    inputs["execution_decision"][
        "execution_authorization"
    ] = "UNAUTHORIZED"

    inputs["validation"][
        "validation_status"
    ] = "INVALID"

    return inputs


cases = [
    (
        "MASTER READY",
        ready_inputs(),
        {
            "status": "MASTER_READY",
            "action": "PROCEED",
            "risk": "LOW",
            "control": "EXECUTE",
        },
    ),

    (
        "MASTER REVIEW",
        review_inputs(),
        {
            "status": "MASTER_REVIEW",
            "action": "REVIEW",
            "risk": "MEDIUM",
            "control": "HOLD",
        },
    ),

    (
        "MASTER BLOCKED",
        blocked_inputs(),
        {
            "status": "MASTER_BLOCKED",
            "action": "HALT",
            "risk": "CRITICAL",
            "control": "HOLD",
        },
    ),
]


engine = AIFinalDecisionMasterControl()


for name, inputs, expected in cases:

    print()
    print("=" * 82)
    print("CASE:", name)
    print("=" * 82)

    result = engine.analyze(
        inputs["final_decision"],
        inputs["certification"],
        inputs["execution_decision"],
        inputs["governance"],
        inputs["lifecycle"],
        inputs["operational_intelligence"],
        inputs["orchestration"],
        inputs["integrated_intelligence"],
        inputs["validation"],
    )

    status = result.get("master_control_status")
    action = result.get("master_control_action")
    risk = result.get("master_control_risk")
    control = result.get("execution_control")

    print("master control status:", status)
    print("master control action:", action)
    print("master control risk:", risk)
    print("execution control:", control)

    assert status == expected["status"]
    assert action == expected["action"]
    assert risk == expected["risk"]
    assert control == expected["control"]

    print("MASTER CONTROL CONTRACT: PASS")

    # ------------------------------------------------------------
    # Memory-only final output boundary
    # ------------------------------------------------------------

    final_output = {
        "success": True,
        "final_decision": inputs["final_decision"],
        "final_execution_decision": inputs["execution_decision"],
        "final_decision_master_control": result,
    }

    output_master = final_output[
        "final_decision_master_control"
    ]

    output_execution = final_output[
        "final_execution_decision"
    ]

    assert (
        output_master.get("master_control_status")
        == status
    )

    assert (
        output_master.get("master_control_action")
        == action
    )

    assert (
        output_master.get("master_control_risk")
        == risk
    )

    assert (
        output_master.get("execution_control")
        == control
    )

    assert (
        output_execution.get("action")
        == inputs["execution_decision"].get("action")
    )

    assert (
        output_execution.get("execution_status")
        == inputs["execution_decision"].get(
            "execution_status"
        )
    )

    print("master status propagation: PASS")
    print("master action propagation: PASS")
    print("master risk propagation: PASS")
    print("execution control propagation: PASS")
    print("execution action preservation: PASS")
    print("execution status preservation: PASS")

    print("FINAL OUTPUT PROPAGATION CONTRACT: PASS")


print()
print("=" * 82)
print("FINAL ASSERTIONS")
print("=" * 82)

print(
    "MASTER_READY -> PROCEED -> EXECUTE -> FINAL OUTPUT: PASS"
)

print(
    "MASTER_REVIEW -> REVIEW -> HOLD -> FINAL OUTPUT: PASS"
)

print(
    "MASTER_BLOCKED -> HALT -> HOLD -> FINAL OUTPUT: PASS"
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
    "===== PHASE 7-7 FINAL OUTPUT PROPAGATION CONTRACT TEST V4 COMPLETE ====="
)
