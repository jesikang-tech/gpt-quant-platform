from pathlib import Path
import database

TEST_DB = Path(r".\database\g7_10_18_integration_test.db")
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
