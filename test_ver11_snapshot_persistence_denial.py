"""Direct snapshot persistence must fail before database access."""

import pytest

import repository
from core.price_provenance_gate import PriceProvenanceRejected


def test_unverified_snapshot_save_denied_before_database_connection(monkeypatch):
    calls = []

    def forbidden_connection():
        calls.append("database_connection")
        raise AssertionError("Database connection must not occur")

    monkeypatch.setattr(repository, "get_connection", forbidden_connection)

    with pytest.raises(
        PriceProvenanceRejected,
        match="Price provenance is unverified",
    ):
        repository.save_ver11_analysis_snapshot(
            analysis_date="2026-10-01",
            period="3m",
            sort_by="final_score",
            display_limit=10,
            snapshot_payload={"synthetic": True},
        )

    assert calls == []
