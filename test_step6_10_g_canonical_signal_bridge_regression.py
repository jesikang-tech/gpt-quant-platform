"""
Step6-10-G canonical outcome-signal bridge regression.

This test deliberately compares the Step6-4 evaluator's canonical
signal with the signal reconstructed by the Adaptive Strategy API.
All repository calls are monkeypatched; no SQLite connection is used.
"""

import pytest

import api_server
from api_server import app
from core.ai_decision_outcome_evaluation import (
    AIDecisionOutcomeEvaluation,
)


EVALUATOR = AIDecisionOutcomeEvaluation()


def _history_rows():
    row = [None] * 10
    row[0] = "MAINTAIN"
    row[2] = 86.6
    row[3] = "A"
    row[9] = "2026-08-20 10:00:00"
    return [tuple(row)]


def _outcome_rows(score, adaptive_required):
    row = [None] * 29
    row[0] = 901
    row[15] = "EVALUATED"
    row[18] = score

    if score is None:
        row[19] = "N/A"
    else:
        row[19] = "F" if score < 60 else "C"
    row[24] = "ADAPTIVE_LEARNING_REQUIRED"
    row[25] = "ADAPTIVE_LEARNING"
    row[26] = int(adaptive_required)
    row[27] = int(adaptive_required)
    row[28] = (
        "REASSESSMENT_REQUIRED"
        if adaptive_required
        else "NOT_REQUIRED"
    )
    return [tuple(row)]


def _pending_outcome_rows():
    row = list(_outcome_rows(0.0, False)[0])
    row[15] = "PENDING"
    return [tuple(row)]


def _bridge_signal(monkeypatch, score, adaptive_required):
    monkeypatch.setattr(
        api_server,
        "get_ai_decision_history",
        lambda limit=10: _history_rows(),
    )
    monkeypatch.setattr(
        api_server,
        "get_ai_decision_outcome_history",
        lambda limit=50: _outcome_rows(score, adaptive_required),
    )

    response = app.test_client().get(
        "/api/ai-decision/adaptive-strategy"
    )

    assert response.status_code == 200
    return response.get_json()["strategy"]["outcome_learning_signal"]


@pytest.mark.parametrize(
    ("score", "expected_signal"),
    [
        (50.0, "NEGATIVE"),
        (59.9, "NEGATIVE"),
        (60.0, "STABLE"),
        (69.9, "STABLE"),
        (70.0, "STABLE"),
        (79.9, "STABLE"),
        (80.0, "POSITIVE"),
    ],
)
def test_evaluator_canonical_signal_boundaries(
    score,
    expected_signal,
):
    result = EVALUATOR.evaluate(
        outcome_snapshot={},
        actual_outcome={"outcome_score": score},
    )

    assert result["outcome_status"] == "EVALUATED"
    assert result["outcome_score"] == score
    assert result["learning_signal"] == expected_signal


def test_evaluator_pending_outcome_has_no_learning_signal():
    result = EVALUATOR.evaluate(
        outcome_snapshot={},
        actual_outcome={},
    )

    assert result["outcome_status"] == "PENDING"
    assert result["learning_signal"] == "NONE"


@pytest.mark.parametrize(
    ("score", "canonical_signal", "adaptive_required"),
    [
        (50.0, "NEGATIVE", True),
        (59.9, "NEGATIVE", True),
        (60.0, "STABLE", False),
        (69.9, "STABLE", False),
        (70.0, "STABLE", False),
        (79.9, "STABLE", False),
        (80.0, "POSITIVE", False),
    ],
)
def test_adaptive_strategy_bridge_preserves_canonical_signal(
    monkeypatch,
    score,
    canonical_signal,
    adaptive_required,
):
    """An evaluated history row must retain the evaluator's signal."""
    evaluation = EVALUATOR.evaluate(
        outcome_snapshot={},
        actual_outcome={"outcome_score": score},
    )
    bridge_signal = _bridge_signal(
        monkeypatch,
        score,
        adaptive_required,
    )

    assert evaluation["learning_signal"] == canonical_signal
    assert bridge_signal == evaluation["learning_signal"]


def test_adaptive_strategy_bridge_ignores_pending_outcomes(
    monkeypatch,
):
    monkeypatch.setattr(
        api_server,
        "get_ai_decision_history",
        lambda limit=10: _history_rows(),
    )
    monkeypatch.setattr(
        api_server,
        "get_ai_decision_outcome_history",
        lambda limit=50: _pending_outcome_rows(),
    )

    response = app.test_client().get(
        "/api/ai-decision/adaptive-strategy"
    )

    assert response.status_code == 200
    assert (
        response.get_json()["strategy"]["outcome_learning_signal"]
        == "NONE"
    )

def _balanced_history_rows():
    rows = []

    for decision_score, decision in (
        (83.0, "MAINTAIN"),
        (83.0, "MAINTAIN"),
        (79.0, "REVIEW"),
    ):
        row = [None] * 10
        row[0] = decision
        row[2] = decision_score
        row[3] = "A"
        row[9] = "2026-08-20 10:00:00"
        rows.append(tuple(row))

    return rows


def _adaptive_strategy_result(
    monkeypatch,
    score,
    adaptive_required,
):
    monkeypatch.setattr(
        api_server,
        "get_ai_decision_history",
        lambda limit=10: _balanced_history_rows(),
    )
    monkeypatch.setattr(
        api_server,
        "get_ai_decision_outcome_history",
        lambda limit=50: _outcome_rows(
            score,
            adaptive_required,
        ),
    )

    response = app.test_client().get(
        "/api/ai-decision/adaptive-strategy"
    )

    assert response.status_code == 200
    return response.get_json()["strategy"]


@pytest.mark.parametrize(
    "score",
    [70.0, 79.9],
)
def test_stable_outcome_does_not_promote_balanced_strategy(
    monkeypatch,
    score,
):
    result = _adaptive_strategy_result(
        monkeypatch,
        score,
        False,
    )

    assert result["outcome_learning_signal"] == "STABLE"
    assert result["strategy"] == "BALANCED"
    assert result["action"] == "MAINTAIN_BALANCE"


@pytest.mark.parametrize(
    "score",
    [50.0, 59.9],
)
def test_negative_outcome_forces_defensive_even_without_stored_flag(
    monkeypatch,
    score,
):
    result = _adaptive_strategy_result(
        monkeypatch,
        score,
        False,
    )

    assert result["outcome_learning_signal"] == "NEGATIVE"
    assert result["adaptive_learning_required"] is True
    assert result["strategy"] == "DEFENSIVE"
    assert result["action"] == "REDUCE_RISK"


def test_positive_outcome_can_promote_balanced_strategy(
    monkeypatch,
):
    result = _adaptive_strategy_result(
        monkeypatch,
        80.0,
        False,
    )

    assert result["outcome_learning_signal"] == "POSITIVE"
    assert result["outcome_learning_signal_strength"] >= 0.7
    assert result["strategy"] == "GROWTH"
    assert result["action"] == "INCREASE_RISK"

def _portfolio_bridge_outcome_intelligence(
    score,
    adaptive_required,
):
    row = list(
        _outcome_rows(
            score,
            adaptive_required,
        )[0]
    )

    if row[15] != "EVALUATED":
        return {
            "outcome_status": row[15],
            "outcome_learning_signal": "NONE",
            "outcome_learning_signal_strength": 0.0,
            "adaptive_learning_required": False,
        }

    outcome_score = row[18]
    stored_learning_required = bool(row[26])
    reassessment_required = bool(row[27])

    if outcome_score is None:
        signal = "NONE"
        strength = 0.0
    else:
        signal = (
            AIDecisionOutcomeEvaluation
            .canonical_learning_signal(
                float(outcome_score)
            )
        )
        strength = (
            AIDecisionOutcomeEvaluation
            .canonical_learning_signal_strength(
                float(outcome_score)
            )
        )

    effective_learning_required = (
        stored_learning_required
        or reassessment_required
        or signal == "NEGATIVE"
    )

    return {
        "outcome_status": row[15],
        "outcome_score": outcome_score,
        "outcome_grade": row[19],
        "outcome_learning_status": row[24],
        "feedback_state": row[25],
        "adaptive_learning_required":
            effective_learning_required,
        "reassessment_required": bool(row[27]),
        "reassessment_status": row[28],
        "outcome_learning_signal": signal,
        "outcome_learning_signal_strength": strength,
        "source_history_id": row[0],
    }


@pytest.mark.parametrize(
    ("score", "expected_signal", "expected_required"),
    [
        (50.0, "NEGATIVE", True),
        (59.9, "NEGATIVE", True),
        (60.0, "STABLE", False),
        (70.0, "STABLE", False),
        (79.9, "STABLE", False),
        (80.0, "POSITIVE", False),
    ],
)
def test_portfolio_bridge_uses_canonical_signal_policy(
    score,
    expected_signal,
    expected_required,
):
    result = _portfolio_bridge_outcome_intelligence(
        score,
        False,
    )

    assert result["outcome_learning_signal"] == expected_signal
    assert (
        result["adaptive_learning_required"]
        is expected_required
    )

    expected_strength = (
        AIDecisionOutcomeEvaluation
        .canonical_learning_signal_strength(
            score
        )
    )

    assert (
        result["outcome_learning_signal_strength"]
        == expected_strength
    )


def test_portfolio_bridge_null_score_is_not_negative():
    result = _portfolio_bridge_outcome_intelligence(
        None,
        False,
    )

    assert result["outcome_status"] == "EVALUATED"
    assert result["outcome_score"] is None
    assert result["outcome_learning_signal"] == "NONE"
    assert result["outcome_learning_signal_strength"] == 0.0
    assert result["adaptive_learning_required"] is False


def test_portfolio_bridge_negative_signal_overrides_missing_flag():
    result = _portfolio_bridge_outcome_intelligence(
        59.9,
        False,
    )

    assert result["outcome_learning_signal"] == "NEGATIVE"
    assert result["adaptive_learning_required"] is True


def test_portfolio_bridge_positive_signal_strength_matches_evaluator():
    result = _portfolio_bridge_outcome_intelligence(
        80.0,
        False,
    )

    assert result["outcome_learning_signal"] == "POSITIVE"
    assert (
        result["outcome_learning_signal_strength"]
        == EVALUATOR.canonical_learning_signal_strength(
            80.0
        )
    )

def test_portfolio_bridge_reassessment_required_forces_adaptive_learning(
    monkeypatch,
):
    row = list(_outcome_rows(80.0, False)[0])

    # GH boundary:
    # stored adaptive_learning_required = False
    # reassessment_required = True
    row[26] = 0
    row[27] = 1
    row[28] = "REASSESSMENT_REQUIRED"

    monkeypatch.setattr(
        api_server,
        "get_ai_decision_history",
        lambda limit=10: _balanced_history_rows(),
    )
    monkeypatch.setattr(
        api_server,
        "get_ai_decision_outcome_history",
        lambda limit=50: [tuple(row)],
    )

    response = app.test_client().get(
        "/api/ai-decision/adaptive-strategy"
    )

    assert response.status_code == 200

    strategy = response.get_json()["strategy"]

    assert strategy["outcome_learning_signal"] == "POSITIVE"
    assert strategy["adaptive_learning_required"] is True

    print(
        "GH reassessment_required -> adaptive_learning_required: PASS"
    )
