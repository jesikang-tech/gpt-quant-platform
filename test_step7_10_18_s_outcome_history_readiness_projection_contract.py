import api_server


client = api_server.app.test_client()


def make_row(history_id, readiness):
    row = [None] * 38

    row[0] = history_id
    row[1] = "MAINTAIN"
    row[2] = "PROCEED"
    row[3] = "MAINTAIN"

    row[4] = 93.2
    row[5] = 89.6
    row[6] = 100.0
    row[7] = 98.8
    row[8] = 97.6
    row[9] = 99.7
    row[10] = 98.3
    row[11] = 97.6
    row[12] = 97.9

    row[13] = "NEUTRAL"
    row[14] = "LOW"
    row[15] = "PENDING"
    row[16] = "COLLECTED"
    row[17] = "FUTURE_OUTCOME_EVALUATION"
    row[18] = 0.0
    row[19] = "N/A"
    row[20] = "PENDING"
    row[21] = "PENDING"
    row[22] = "PENDING"
    row[23] = "PENDING"
    row[24] = "WAITING_FOR_OUTCOME"
    row[25] = "COLLECTING"
    row[26] = 0
    row[27] = 0
    row[28] = "NOT_REQUIRED"
    row[29] = "2026-08-20T14:00:00+09:00"
    row[30] = None
    row[31] = None

    row[32] = "EXECUTION_READY"
    row[33] = "AUTHORIZED"
    row[34] = readiness
    row[35] = "CERTIFIED"
    row[36] = "STANDARD_MONITORING"
    row[37] = "STABLE"

    return tuple(row)


print("=" * 70)
print("PHASE 7-10-18-S")
print("OUTCOME HISTORY API READINESS PROJECTION CONTRACT")
print("=" * 70)


original_list = api_server.get_ai_decision_outcome_history
original_by_id = api_server.get_ai_decision_outcome_history_by_id

try:
    print()
    print("=== CASE 1: LIST API READY PROJECTION ===")

    api_server.get_ai_decision_outcome_history = (
        lambda limit=10: [make_row(1001, "READY")]
    )

    response = client.get(
        "/api/ai-decision/outcome-history"
    )

    assert response.status_code == 200
    payload = response.get_json()

    assert payload["success"] is True
    assert len(payload["history"]) == 1

    item = payload["history"][0]

    assert item["id"] == 1001
    assert item["execution_status"] == "EXECUTION_READY"
    assert item["execution_authorization"] == "AUTHORIZED"
    assert item["execution_readiness"] == "READY"
    assert item["certification_status"] == "CERTIFIED"
    assert item["monitoring_status"] == "STANDARD_MONITORING"
    assert item["feedback_status"] == "STABLE"

    print("LIST API READY projection: PASS")


    print()
    print("=== CASE 2: LIST API NOT_READY PROJECTION ===")

    api_server.get_ai_decision_outcome_history = (
        lambda limit=10: [make_row(1002, "NOT_READY")]
    )

    response = client.get(
        "/api/ai-decision/outcome-history"
    )

    assert response.status_code == 200
    payload = response.get_json()

    item = payload["history"][0]

    assert item["id"] == 1002
    assert item["execution_status"] == "EXECUTION_READY"
    assert item["execution_authorization"] == "AUTHORIZED"
    assert item["execution_readiness"] == "NOT_READY"
    assert item["certification_status"] == "CERTIFIED"

    print("LIST API NOT_READY projection: PASS")


    print()
    print("=== CASE 3: BY-ID API READY PROJECTION ===")

    api_server.get_ai_decision_outcome_history_by_id = (
        lambda history_id: make_row(history_id, "READY")
    )

    response = client.get(
        "/api/ai-decision/outcome-history/2001"
    )

    assert response.status_code == 200
    payload = response.get_json()

    assert payload["success"] is True

    item = payload["history"]

    assert item["id"] == 2001
    assert item["execution_status"] == "EXECUTION_READY"
    assert item["execution_authorization"] == "AUTHORIZED"
    assert item["execution_readiness"] == "READY"
    assert item["certification_status"] == "CERTIFIED"
    assert item["monitoring_status"] == "STANDARD_MONITORING"
    assert item["feedback_status"] == "STABLE"

    print("BY-ID API READY projection: PASS")


    print()
    print("=== CASE 4: BY-ID API NOT_READY PROJECTION ===")

    api_server.get_ai_decision_outcome_history_by_id = (
        lambda history_id: make_row(history_id, "NOT_READY")
    )

    response = client.get(
        "/api/ai-decision/outcome-history/2002"
    )

    assert response.status_code == 200
    payload = response.get_json()

    assert payload["success"] is True

    item = payload["history"]

    assert item["id"] == 2002
    assert item["execution_status"] == "EXECUTION_READY"
    assert item["execution_authorization"] == "AUTHORIZED"
    assert item["execution_readiness"] == "NOT_READY"
    assert item["certification_status"] == "CERTIFIED"
    assert item["monitoring_status"] == "STANDARD_MONITORING"
    assert item["feedback_status"] == "STABLE"

    print("BY-ID API NOT_READY projection: PASS")


    print()
    print("=== CASE 5: FIELD ORDER / PROJECTION BOUNDARY ===")

    api_server.get_ai_decision_outcome_history = (
        lambda limit=10: [make_row(3001, "READY")]
    )

    response = client.get(
        "/api/ai-decision/outcome-history"
    )

    item = response.get_json()["history"][0]

    assert (
        item["execution_status"],
        item["execution_authorization"],
        item["execution_readiness"],
        item["certification_status"],
        item["monitoring_status"],
        item["feedback_status"],
    ) == (
        "EXECUTION_READY",
        "AUTHORIZED",
        "READY",
        "CERTIFIED",
        "STANDARD_MONITORING",
        "STABLE",
    )

    print("FIELD ORDER / PROJECTION boundary: PASS")


    print()
    print("=== PRODUCTION DB SAFETY ===")
    print("All API repository calls were mocked.")
    print("Production database mutation: NONE")


    print()
    print("=" * 70)
    print("OVERALL RESULT: PASS")
    print("=" * 70)

finally:
    api_server.get_ai_decision_outcome_history = original_list
    api_server.get_ai_decision_outcome_history_by_id = original_by_id
