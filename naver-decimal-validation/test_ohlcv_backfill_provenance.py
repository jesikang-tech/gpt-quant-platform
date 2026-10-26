"""Static and database-free behavioral regressions for OHLCV provenance."""

import ast
import importlib.util
from pathlib import Path

import pytest

from core.price_provenance_gate import (
    PriceProvenanceDecision,
    PriceProvenanceRejected,
    assess_price_provenance,
    require_persistence_authorization,
)


def _source_path():
    # Support both the repository layout and the Actions staging directory.
    directory = Path(__file__).resolve().parent
    for root in (directory, directory.parent):
        candidate = root / "collector" / "ohlcv_backfill.py"
        if candidate.is_file():
            return candidate
    raise AssertionError("OHLCV backfill source was not staged")


def test_legacy_backfill_requires_provenance_before_provider_fetch():
    source_path = _source_path()
    tree = ast.parse(source_path.read_text(encoding="utf-8"))

    backfill = next(
        node for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef)
        and node.name == "backfill_ticker"
    )

    calls = [
        node for node in ast.walk(backfill)
        if isinstance(node, ast.Call)
    ]

    provenance_calls = [
        node for node in calls
        if isinstance(node.func, ast.Name)
        and node.func.id == "require_persistence_authorization"
    ]

    assert provenance_calls, (
        "Legacy OHLCV backfill lacks a persistence provenance gate"
    )


class RecordingProvider:
    def __init__(self):
        self.calls = 0

    def get_price(self, *args, **kwargs):
        self.calls += 1
        raise AssertionError("Provider fetch is forbidden")


@pytest.fixture
def guarded_backfill(monkeypatch, tmp_path):
    # Load the real source without executing collector package initialization.
    spec = importlib.util.spec_from_file_location(
        "ohlcv_backfill_provenance_subject", _source_path()
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    provider = RecordingProvider()
    service = module.OHLCVBackfill(tmp_path / "never-opened.db", provider)
    connection_calls = []

    def forbidden_connection():
        connection_calls.append(True)
        raise AssertionError("Database connection is forbidden")

    monkeypatch.setattr(service, "_connection", forbidden_connection)
    return module, service, provider, connection_calls


def _assert_denied(result, provider, connection_calls):
    assert result["status"] == "FAILED"
    assert result["rows_written"] == 0
    assert result["rows_skipped"] == 0
    assert result["error"].startswith("PriceProvenanceRejected:")
    assert "provenance is unverified" in result["error"]
    assert "persistence is prohibited" in result["error"]
    assert provider.calls == 0
    assert len(connection_calls) == 0


def test_unverified_backfill_rejects_before_connection_or_fetch(guarded_backfill):
    _, service, provider, connections = guarded_backfill
    result = service.backfill_ticker("A")
    assert result["ticker"] == "A"
    _assert_denied(result, provider, connections)


def test_explicit_tickers_fail_independently_with_aggregate_counts(guarded_backfill):
    _, service, provider, connections = guarded_backfill
    result = service.backfill(["A", "B", "A", "C"])
    assert result["attempted"] == result["failed"] == 3
    assert result["succeeded"] == result["skipped"] == 0
    assert [item["ticker"] for item in result["results"]] == ["A", "B", "C"]
    for item in result["results"]:
        _assert_denied(item, provider, connections)


def test_caller_and_provider_authorization_claims_do_not_grant_trust(
    guarded_backfill, monkeypatch,
):
    _, service, provider, connections = guarded_backfill
    claimed = PriceProvenanceDecision(status="APPROVED", persistence_authorized=True)
    # Caller-attached metadata is not an authorization interface.
    for target in (service, provider):
        for name, value in (
            ("persistence_authorized", True),
            ("provenance_verified", True),
            ("provenance_decision", claimed),
            ("adjustment", "VERIFIED"),
        ):
            monkeypatch.setattr(target, name, value, raising=False)
    decision = assess_price_provenance(provider="NAVER", adjustment="VERIFIED")
    assert decision.persistence_authorized is False
    with pytest.raises(PriceProvenanceRejected, match="persistence is prohibited"):
        require_persistence_authorization(decision)
    _assert_denied(service.backfill_ticker("A"), provider, connections)


@pytest.fixture
def guarded_discovery(guarded_backfill, monkeypatch):
    module, service, provider, connections = guarded_backfill
    discovery_calls = []

    def forbidden_discovery():
        discovery_calls.append(True)
        raise AssertionError("Automatic target discovery is forbidden")

    monkeypatch.setattr(service, "get_targets", forbidden_discovery)
    return module, service, provider, connections, discovery_calls


@pytest.mark.parametrize("explicit_none", [False, True], ids=["omitted", "none"])
@pytest.mark.parametrize("evidence", ["unverified", "claims", "forged"])
def test_auto_discovery_rejects_before_any_access(
    guarded_discovery, monkeypatch, explicit_none, evidence,
):
    module, service, provider, connections, discoveries = guarded_discovery
    assert module.require_persistence_authorization is require_persistence_authorization
    if evidence in ("claims", "forged"):
        forged = PriceProvenanceDecision(
            status="APPROVED", reason="CALLER_ASSERTED_VERIFIED",
            analysis_authorized=True, portfolio_authorized=True,
            dashboard_authorized=True, snapshot_authorized=True,
            persistence_authorized=True,
        )
        if evidence == "claims":
            for target in (service, provider):
                for name, value in (
                    ("persistence_authorized", True),
                    ("provenance_verified", True),
                    ("provenance_decision", forged),
                    ("adjustment", "VERIFIED"),
                ):
                    monkeypatch.setattr(target, name, value, raising=False)
        else:
            # Supply hostile evidence without replacing the real enforcement gate.
            monkeypatch.setattr(module, "assess_price_provenance", lambda: forged)

    with pytest.raises(PriceProvenanceRejected) as rejected:
        if explicit_none:
            service.backfill(None)
        else:
            service.backfill()

    assert "provenance is unverified" in str(rejected.value)
    assert "persistence is prohibited" in str(rejected.value)
    assert discoveries == []
    assert connections == []
    assert provider.calls == 0


def test_explicit_batch_never_discovers_and_preserves_independent_failures(
    guarded_discovery,
):
    _, service, provider, connections, discoveries = guarded_discovery
    summary = service.backfill(["A", "B", "A"])
    assert summary["attempted"] == summary["failed"] == 2
    assert summary["succeeded"] == summary["skipped"] == 0
    assert [item["ticker"] for item in summary["results"]] == ["A", "B"]
    assert summary["results"][0] is not summary["results"][1]
    for result in summary["results"]:
        _assert_denied(result, provider, connections)
    assert discoveries == []


def test_empty_explicit_batch_performs_no_access(guarded_discovery):
    _, service, provider, connections, discoveries = guarded_discovery
    assert service.backfill([]) == {
        "attempted": 0, "succeeded": 0, "failed": 0, "skipped": 0,
        "results": [],
    }
    assert discoveries == []
    assert connections == []
    assert provider.calls == 0


def test_forged_approval_is_rejected_by_real_gate_in_backfill(
    guarded_backfill, monkeypatch,
):
    module, service, provider, connections = guarded_backfill
    forged = PriceProvenanceDecision(
        status="APPROVED", reason="CALLER_ASSERTED_VERIFIED",
        analysis_authorized=True, portfolio_authorized=True,
        dashboard_authorized=True, snapshot_authorized=True,
        persistence_authorized=True,
    )
    assert module.require_persistence_authorization is require_persistence_authorization
    with pytest.raises(PriceProvenanceRejected, match="persistence is prohibited"):
        require_persistence_authorization(forged)
    # Inject hostile assessment output; the real enforcement gate stays intact.
    monkeypatch.setattr(module, "assess_price_provenance", lambda: forged)
    _assert_denied(service.backfill_ticker("A"), provider, connections)
