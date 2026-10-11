"""Adaptive strategy API semantics through real queries on an isolated DB."""
import pytest
from price_test_support import isolated_price_db, isolated_evaluation_api


@pytest.mark.parametrize("status,score,grade,required,strategy,action,signal", [
    ("EVALUATED", 40, "F", 1, "DEFENSIVE", "REDUCE_RISK", "NEGATIVE"),
    ("EVALUATED", 87.5, "B", 0, "MAINTAIN", "MAINTAIN_ALLOCATION", "POSITIVE"),
    ("PENDING", 0, "N/A", 0, "MAINTAIN", "MAINTAIN_ALLOCATION", "NONE"),
])
def test_adaptive_strategy_api(isolated_evaluation_api, status, score, grade,
                               required, strategy, action, signal):
    conn = isolated_evaluation_api.db.connect()
    try:
        with conn:
            conn.execute("INSERT INTO ai_decision_history(decision, decision_score, grade, created_at) "
                         "VALUES ('MAINTAIN', 86.6, 'A', '2026-01-02T10:00:00+00:00')")
            conn.execute("INSERT INTO ai_decision_outcome_history(outcome_status, outcome_score, "
                         "outcome_grade, learning_status, feedback_state, adaptive_learning_required, "
                         "reassessment_required, reassessment_status) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                         (status, score, grade, "WAITING_FOR_OUTCOME" if status == "PENDING" else
                          "LEARNING_AVAILABLE", "COLLECTING", required, required,
                          "REASSESSMENT_REQUIRED" if required else "NOT_REQUIRED"))
    finally:
        conn.close()
    before = isolated_evaluation_api.db.path.read_bytes()
    response = isolated_evaluation_api.client.get("/api/ai-decision/adaptive-strategy")
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert data["strategy"]["strategy"] == strategy
    assert data["strategy"]["action"] == action
    assert data["strategy"]["outcome_learning_signal"] == signal
    assert data["strategy"]["adaptive_learning_required"] == bool(required)
    assert isolated_evaluation_api.db.path.read_bytes() == before
