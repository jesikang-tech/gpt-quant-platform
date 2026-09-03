from pathlib import Path
import database

TEST_DB = Path(r".\database\g7_10_18_ready_fixture.db")
database.DATABASE_PATH = TEST_DB

import api_server

client = api_server.app.test_client()
response = client.get("/api/portfolio/decision-intelligence")

data = response.get_json()

print("API_RESPONSE_CONTRACT_DISCOVERY: PASS")
print("HTTP_STATUS:", response.status_code)
print("CONTENT_TYPE:", response.content_type)
print("TOP_LEVEL_KEYS:", len(data))
print("TOP_LEVEL_KEYS_LIST:")
for key in data.keys():
    print(" -", key)

print("")
print("===== FINAL EXECUTION CHAIN =====")

chain = [
    "final_decision",
    "final_decision_execution_control",
    "final_decision_execution_assurance",
    "final_decision_execution_monitoring",
    "final_decision_execution_feedback",
    "final_decision_execution_reassessment",
    "final_decision_lifecycle",
    "final_decision_lifecycle_governance_control",
    "final_decision_operational_intelligence",
    "final_decision_integrated_intelligence",
    "final_decision_orchestration",
    "final_execution_decision",
    "final_decision_certification",
    "final_decision_master_control",
]

for key in chain:
    value = data.get(key)
    print("")
    print("[" + key + "]")
    if isinstance(value, dict):
        for field in [
            "status",
            "decision",
            "action",
            "risk",
            "execution_status",
            "execution_authorization",
            "reassessment_required",
            "reassessment_status",
            "certification_status",
            "master_control_status",
            "master_control_action",
        ]:
            if field in value:
                print(field + ":", value[field])
    else:
        print("MISSING_OR_NON_DICT:", value)

print("")
print("=" * 82)
print("===== API RUNTIME SEMANTIC INTEGRATION CONTRACT =====")
print("=" * 82)

assert response.status_code == 200
assert response.is_json
assert isinstance(data, dict)

for key in chain:
    assert isinstance(data.get(key), dict), (
        f"API chain key missing or non-dict: {key}"
    )

execution = data["final_execution_decision"]
assert execution.get("execution_status") == "EXECUTION_READY"
assert execution.get("execution_authorization") == "AUTHORIZED"

certification = data["final_decision_certification"]
assert certification.get("certification_status") == "CERTIFIED"
assert certification.get("execution_status") == "EXECUTION_READY"
assert certification.get("execution_authorization") == "AUTHORIZED"

master = data["final_decision_master_control"]

master_invariants = {
    "certification_status": "CERTIFIED",
    "execution_status": "EXECUTION_READY",
    "execution_authorization": "AUTHORIZED",
    "execution_readiness": "READY",
    "decision_integrity": "INTACT",
    "governance_status": "APPROVED",
    "lifecycle_status": "HEALTHY",
    "operational_status": "OPERATIONALLY_HEALTHY",
    "orchestration_status": "ORCHESTRATION_READY",
    "integrated_status": "INTEGRATED_HEALTHY",
    "validation_status": "VALID",
    "master_control_status": "MASTER_READY",
    "master_control_action": "PROCEED",
    "execution_control": "EXECUTE",
    "reassessment_required": False,
}

for field, expected in master_invariants.items():
    assert master.get(field) == expected, (
        f"{field}: expected {expected!r}, "
        f"got {master.get(field)!r}"
    )

reassessment = data["final_decision_execution_reassessment"]
assert reassessment.get("reassessment_required") is False
assert reassessment.get("reassessment_status") == "NOT_REQUIRED"

print("HTTP 200 -> PASS")
print("JSON response -> PASS")
print("14 execution-chain objects -> PASS")
print("FINAL EXECUTION DECISION invariant -> PASS")
print("CERTIFICATION invariant -> PASS")
print("MASTER CONTROL invariant -> PASS")
print("REASSESSMENT invariant -> PASS")
print("")
print("===== PHASE 7-10-18-Q SEMANTIC INTEGRATION CONTRACT COMPLETE =====")
print("=" * 82)
