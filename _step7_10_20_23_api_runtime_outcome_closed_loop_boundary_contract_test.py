from pathlib import Path

import database

TEST_DB = Path(r".\database\g7_10_18_integration_test.db")
database.DATABASE_PATH = TEST_DB

import api_server


def assert_equal(actual, expected, label):
    if actual != expected:
        raise AssertionError(
            f"{label}: expected={expected!r}, actual={actual!r}"
        )
    print(f"{label}: PASS")


print("=" * 82)
print("PHASE 7-10-20-23")
print("API RUNTIME MASTER CONTROL -> OUTCOME CLOSED LOOP")
print("BOUNDARY CONTRACT TEST V1")
print("SOURCE-VERIFIED / TEST-DB / READ-ONLY")
print("=" * 82)


client = api_server.app.test_client()
response = client.get("/api/portfolio/decision-intelligence")
data = response.get_json()

print("")
print("=" * 82)
print("CASE: API RUNTIME CONTRACT")
print("=" * 82)

assert_equal(response.status_code, 200, "API -> HTTP 200")
assert_equal(response.is_json, True, "API -> JSON response")
assert_equal(isinstance(data, dict), True, "API -> dictionary response")


print("")
print("=" * 82)
print("CASE: OUTCOME RUNTIME OBJECTS")
print("=" * 82)

snapshot = data.get("ai_decision_outcome_snapshot")
evaluation = data.get("ai_decision_outcome_evaluation")
intelligence = data.get("ai_decision_outcome_intelligence")

assert_equal(
    isinstance(snapshot, dict),
    True,
    "snapshot -> dictionary",
)

assert_equal(
    isinstance(evaluation, dict),
    True,
    "evaluation -> dictionary",
)

assert_equal(
    isinstance(intelligence, dict),
    True,
    "intelligence -> dictionary",
)


print("")
print("=" * 82)
print("CASE: MASTER CONTROL -> OUTCOME SNAPSHOT")
print("=" * 82)

master = data["final_decision_master_control"]

assert_equal(
    master.get("master_control_status"),
    "MASTER_READY",
    "master -> ready",
)

assert_equal(
    master.get("master_control_action"),
    "PROCEED",
    "master -> proceed",
)

assert_equal(
    master.get("execution_status"),
    "EXECUTION_READY",
    "master -> execution ready",
)

assert_equal(
    master.get("execution_authorization"),
    "AUTHORIZED",
    "master -> authorized",
)

assert_equal(
    snapshot.get("snapshot_status"),
    "COLLECTED",
    "master -> collected snapshot",
)

assert_equal(
    snapshot.get("snapshot_purpose"),
    "FUTURE_OUTCOME_EVALUATION",
    "snapshot -> future outcome purpose",
)

assert_equal(
    snapshot.get("outcome_status"),
    "PENDING",
    "snapshot -> pending outcome",
)


print("")
print("=" * 82)
print("CASE: OUTCOME SNAPSHOT -> EVALUATION")
print("=" * 82)

assert_equal(
    evaluation.get("evaluation_status"),
    "WAITING_FOR_OUTCOME",
    "evaluation -> waiting",
)

assert_equal(
    evaluation.get("actual_outcome_available"),
    False,
    "evaluation -> actual outcome unavailable",
)

assert_equal(
    evaluation.get("outcome_status"),
    "PENDING",
    "evaluation -> pending outcome",
)

assert_equal(
    evaluation.get("outcome_score"),
    0.0,
    "evaluation -> no outcome score",
)

assert_equal(
    evaluation.get("learning_signal"),
    "NONE",
    "evaluation -> no learning signal",
)

assert_equal(
    evaluation.get("learning_signal_strength"),
    0.0,
    "evaluation -> zero learning strength",
)


print("")
print("=" * 82)
print("CASE: EVALUATION -> OUTCOME INTELLIGENCE")
print("=" * 82)

assert_equal(
    intelligence.get("outcome_status"),
    "PENDING",
    "intelligence -> pending outcome",
)

assert_equal(
    intelligence.get("learning_status"),
    "WAITING_FOR_OUTCOME",
    "intelligence -> waiting for outcome",
)

assert_equal(
    intelligence.get("outcome_learning_status"),
    "WAITING_FOR_OUTCOME",
    "intelligence -> learning waiting",
)

assert_equal(
    intelligence.get("outcome_learning_signal"),
    "NONE",
    "intelligence -> no learning signal",
)

assert_equal(
    intelligence.get("outcome_learning_signal_strength"),
    0.0,
    "intelligence -> zero learning strength",
)

assert_equal(
    intelligence.get("adaptive_learning_required"),
    False,
    "intelligence -> no adaptive learning",
)

assert_equal(
    intelligence.get("feedback_state"),
    "COLLECTING",
    "intelligence -> collecting feedback",
)


print("")
print("=" * 82)
print("CASE: OUTCOME -> REASSESSMENT SAFETY")
print("=" * 82)

assert_equal(
    intelligence.get("reassessment_required"),
    False,
    "pending outcome -> no reassessment",
)

assert_equal(
    intelligence.get("reassessment_status"),
    "NOT_REQUIRED",
    "pending outcome -> reassessment not required",
)

assert_equal(
    snapshot.get("reassessment_required"),
    False,
    "snapshot -> reassessment false",
)

assert_equal(
    snapshot.get("reassessment_status"),
    "NOT_REQUIRED",
    "snapshot -> reassessment not required",
)


print("")
print("=" * 82)
print("CASE: IDENTITY PROPAGATION")
print("=" * 82)

for field in [
    "decision",
    "action",
    "strategy",
]:
    assert_equal(
        evaluation.get(field),
        snapshot.get(field),
        f"snapshot -> evaluation -> {field}",
    )

    assert_equal(
        intelligence.get(field),
        snapshot.get(field),
        f"snapshot -> intelligence -> {field}",
    )


print("")
print("=" * 82)
print("CASE: MASTER CONTROL IDENTITY PRESERVED")
print("=" * 82)

assert_equal(
    snapshot.get("decision"),
    master.get("decision"),
    "master -> snapshot decision",
)

assert_equal(
    snapshot.get("action"),
    master.get("action"),
    "master -> snapshot action",
)


assert_equal(
    intelligence.get("master_control_status"),
    master.get("master_control_status"),
    "master -> intelligence status",
)


print("")
print("=" * 82)
print("CASE: NO FABRICATED OUTCOME / LEARNING")
print("=" * 82)

assert_equal(
    evaluation.get("actual_outcome_available"),
    False,
    "no actual outcome -> preserved",
)

assert_equal(
    evaluation.get("learning_signal"),
    "NONE",
    "no outcome -> no fabricated learning signal",
)

assert_equal(
    evaluation.get("learning_signal_strength"),
    0.0,
    "no outcome -> no fabricated learning strength",
)

assert_equal(
    intelligence.get("adaptive_learning_required"),
    False,
    "no outcome -> no fabricated adaptive learning",
)

assert_equal(
    intelligence.get("outcome_learning_signal"),
    "NONE",
    "no outcome -> intelligence signal remains none",
)


print("")
print("=" * 82)
print("===== PHASE 7-10-20-23 API RUNTIME CLOSED LOOP BOUNDARY COMPLETE =====")
print("=" * 82)
