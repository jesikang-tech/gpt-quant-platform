"""Real POST persistence and audit linkage against synthetic isolated data."""
import pytest
from price_test_support import isolated_price_db, isolated_evaluation_api, synthetic_ranking_db


@pytest.mark.parametrize("waiting_contract", [False, True])
def test_collector_persistence(synthetic_ranking_db, isolated_evaluation_api, monkeypatch, waiting_contract):
    import json

    conn = isolated_evaluation_api.db.connect()
    try:
        with conn:
            conn.executemany("INSERT INTO etf_prices VALUES (?, ?, ?)",
                             [(ticker, synthetic_ranking_db.dates[-1], price)
                              for ticker, price in (("222222", 200), ("333333", 300))])
        before = conn.execute("SELECT COUNT(*) FROM ai_decision_outcome_history").fetchone()[0]
    finally:
        conn.close()
    api = isolated_evaluation_api.api
    snapshot_method = api.AIDecisionOutcomeDataCollector.collect
    intelligence_method = api.AIDecisionOutcomeIntelligence.analyze

    def waiting_snapshot(self, *args, **kwargs):
        result = snapshot_method(self, *args, **kwargs).copy()
        result.update(reassessment_required=False, reassessment_status="NOT_REQUIRED")
        return result

    def waiting_intelligence(self, *args, **kwargs):
        result = intelligence_method(self, *args, **kwargs).copy()
        result.update(learning_status="WAITING_FOR_OUTCOME", feedback_state="COLLECTING",
                      adaptive_learning_required=False, reassessment_required=False)
        return result

    # Only semantic inputs are controlled; all DB functions and audit writes stay real.
    with monkeypatch.context() as patches:
        if waiting_contract:
            patches.setattr(api.AIDecisionOutcomeDataCollector, "collect", waiting_snapshot)
            patches.setattr(api.AIDecisionOutcomeIntelligence, "analyze", waiting_intelligence)
        response = isolated_evaluation_api.client.post("/api/portfolio/decision-intelligence")
    assert api.AIDecisionOutcomeDataCollector.collect is snapshot_method
    assert api.AIDecisionOutcomeIntelligence.analyze is intelligence_method
    assert response.status_code == 200, response.get_json()
    data = response.get_json()
    assert data["success"] is True
    conn = isolated_evaluation_api.db.connect()
    try:
        rows = conn.execute("SELECT id, outcome_status, snapshot_status, snapshot_purpose, "
                            "learning_status, feedback_state, adaptive_learning_required, "
                            "reassessment_required, reassessment_status, created_at "
                            "FROM ai_decision_outcome_history ORDER BY id").fetchall()
        assert len(rows) == before + 1
        row = rows[-1]
        history_id = row[0]
        snapshot = data["ai_decision_outcome_snapshot"]
        evaluation = data["ai_decision_outcome_evaluation"]
        intelligence = data["ai_decision_outcome_intelligence"]
        assert row[1:4] == ("PENDING", "COLLECTED", "FUTURE_OUTCOME_EVALUATION")
        assert row[1] == evaluation["outcome_status"]
        assert row[4:9] == (intelligence["learning_status"], intelligence["feedback_state"],
                            int(intelligence["adaptive_learning_required"]),
                            int(snapshot["reassessment_required"]), snapshot["reassessment_status"])
        if waiting_contract:
            assert row[4:9] == ("WAITING_FOR_OUTCOME", "COLLECTING", 0, 0, "NOT_REQUIRED")
        assert row[9]
        portfolio = conn.execute("SELECT ticker, weight, reference_price, reference_price_date "
                                 "FROM ai_decision_portfolio_snapshot WHERE history_id=?",
                                 (history_id,)).fetchall()
        assert portfolio
        assert sum(item[1] for item in portfolio) == 100
        assert len({item[0] for item in portfolio}) == len(portfolio)
        for ticker, weight, price, day in portfolio:
            if ticker != "CASH":
                assert price is not None and day == synthetic_ranking_db.dates[-1]
        audits = conn.execute("SELECT event_type, status, correlation_key, details FROM audit_event "
                              "WHERE outcome_history_id=?", (history_id,)).fetchall()
        events = {event[0]: event for event in audits}
        assert {"SNAPSHOT_PERSISTED", "OUTCOME_PERSISTED"} <= set(events)
        assert events["SNAPSHOT_PERSISTED"][1] == "SUCCESS"
        assert events["OUTCOME_PERSISTED"][1] == "PENDING"
        assert all(event[2] == f"outcome:{history_id}" for event in audits)
        assert json.loads(events["SNAPSHOT_PERSISTED"][3])["snapshot_count"] == len(portfolio)
    finally:
        conn.close()
