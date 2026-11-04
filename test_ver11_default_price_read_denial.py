"""Default Ver1.1 analysis paths must deny unverified prices before DB access."""

import pytest

import current_analysis
import historical_replay
from core.price_provenance_gate import PriceProvenanceRejected


def test_default_current_analysis_denied_before_database_access(monkeypatch):
    calls = []

    def forbidden_connection(*args, **kwargs):
        calls.append("database_connection")
        raise AssertionError("Database access must not occur")

    monkeypatch.setattr(
        current_analysis,
        "get_connection",
        forbidden_connection,
        raising=False,
    )

    with pytest.raises(PriceProvenanceRejected):
        current_analysis.get_current_analysis_data(
            analysis_date="2026-10-01",
            period="3m",
        )

    assert calls == []


def test_default_historical_replay_denied_before_database_access(monkeypatch):
    calls = []

    def forbidden_connection(*args, **kwargs):
        calls.append("database_connection")
        raise AssertionError("Database access must not occur")

    monkeypatch.setattr(
        historical_replay,
        "get_connection",
        forbidden_connection,
    )

    with pytest.raises(PriceProvenanceRejected):
        historical_replay.HistoricalReplayEngine(
            "2026-10-01"
        )

    assert calls == []
