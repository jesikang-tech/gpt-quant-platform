from api_server import app
import api_server


client = app.test_client()


def make_history():
    row = [None] * 10
    row[0] = "MAINTAIN"
    row[2] = 86.6
    row[3] = "A"
    row[9] = "2026-08-20 10:00:00"
    return [tuple(row)]


def make_outcome(
    history_id,
    status,
    score,
    grade,
    learning_status,
    feedback_state,
    adaptive_required,
    reassessment_required,
    reassessment_status,
):
    row = [None] * 29
    row[0] = history_id
    row[15] = status
    row[18] = score
    row[19] = grade
    row[24] = learning_status
    row[25] = feedback_state
    row[26] = adaptive_required
    row[27] = reassessment_required
    row[28] = reassessment_status
    return [tuple(row)]


def run_case(
    name,
    outcome_rows,
    expected_strategy,
    expected_action,
    expected_signal,
    expected_learning_required,
):
    api_server.get_ai_decision_history = lambda limit=10: make_history()
    api_server.get_ai_decision_outcome_history = (
        lambda limit=50: outcome_rows
    )

    response = client.get(
        "/api/ai-decision/adaptive-strategy"
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["success"] is True
    assert data["strategy"]["strategy"] == expected_strategy
    assert data["strategy"]["action"] == expected_action
    assert (
        data["strategy"]["outcome_learning_signal"]
        == expected_signal
    )
    assert (
        data["strategy"]["adaptive_learning_required"]
        == expected_learning_required
    )

    print(
        f"{name}: PASS | "
        f"{expected_strategy} / "
        f"{expected_action} / "
        f"{expected_signal}"
    )


print("=" * 60)
print(
    "Step6-10-G API Integration Semantic Regression Test"
)
print("=" * 60)


run_case(
    "CASE 1 NEGATIVE",
    make_outcome(
        901,
        "EVALUATED",
        40.0,
        "F",
        "LEARNING_AVAILABLE",
        "COLLECTING",
        1,
        1,
        "REASSESSMENT_REQUIRED",
    ),
    "DEFENSIVE",
    "REDUCE_RISK",
    "NEGATIVE",
    True,
)


run_case(
    "CASE 2 POSITIVE",
    make_outcome(
        902,
        "EVALUATED",
        87.5,
        "B",
        "LEARNING_AVAILABLE",
        "COLLECTING",
        0,
        0,
        "NOT_REQUIRED",
    ),
    "MAINTAIN",
    "MAINTAIN_ALLOCATION",
    "POSITIVE",
    False,
)


run_case(
    "CASE 3 PENDING",
    make_outcome(
        903,
        "PENDING",
        0.0,
        "N/A",
        "WAITING_FOR_OUTCOME",
        "COLLECTING",
        0,
        0,
        "NOT_REQUIRED",
    ),
    "MAINTAIN",
    "MAINTAIN_ALLOCATION",
    "NONE",
    False,
)


print("")
print("=" * 60)
print("OVERALL RESULT: PASS")
print("=" * 60)
