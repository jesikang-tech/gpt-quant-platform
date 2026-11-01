"""Synthetic fail-closed platform integration tests. No external I/O."""
from dataclasses import FrozenInstanceError, replace

import pytest

from price_provider_validation.provider_contract import prepare_raw_observation
from price_provider_validation.provider_evidence import ProviderEvidence
from price_provider_validation.trading_day_certification import (
    TradingDayCertificationDecision,
)
from price_provider_validation.provider_platform_integration import (
    ProviderPlatformIntegrationRejected,
    assess_provider_platform_integration,
)


def _inputs(provider="KIWOOM"):
    observation = prepare_raw_observation(
        provider, "005930", "2026-10-30",
        ("100", "110", "90", "105", "1000"),
    )
    evidence = ProviderEvidence(
        provider=provider,
        ticker="005930",
        observation_date="2026-10-30",
        acquired_at="2026-10-30T16:00:00+09:00",
        source_locator="synthetic://provider/daily",
        content_sha256="a" * 64,
    )
    trading_day = TradingDayCertificationDecision(
        structural_status="CANDIDATE",
        structural_reason="SYNTHETIC_CANDIDATE",
        structural_trading_day_eligible=True,
    )
    return observation, evidence, trading_day


@pytest.mark.parametrize("provider", ["KIS", "KIWOOM"])
def test_valid_synthetic_structure_remains_denied(provider):
    decision = assess_provider_platform_integration(*_inputs(provider))
    assert decision.provider == provider
    assert decision.ticker == "005930"
    assert decision.observation_date == "2026-10-30"
    assert decision.status == "DENIED"
    assert decision.evidence_status == "DENIED"
    assert decision.trading_day_status == "DENIED"
    for name in (
        "independently_verified",
        "api_execution_authorized",
        "analysis_authorized",
        "dashboard_authorized",
        "snapshot_authorized",
        "persistence_authorized",
        "redistribution_authorized",
        "database_rebuild_authorized",
        "live_api_execution_authorized",
        "broker_execution_authorized",
    ):
        assert getattr(decision, name) is False


@pytest.mark.parametrize(
    "field,value",
    [
        ("provider", "KIS"),
        ("ticker", "000660"),
        ("observation_date", "2026-10-29"),
    ],
)
def test_evidence_identity_mismatch_rejected(field, value):
    observation, evidence, trading_day = _inputs()
    evidence = replace(evidence, **{field: value})
    with pytest.raises(ProviderPlatformIntegrationRejected):
        assess_provider_platform_integration(
            observation, evidence, trading_day
        )


@pytest.mark.parametrize("target", ["observation", "evidence"])
def test_adjustment_relabel_rejected(target):
    observation, evidence, trading_day = _inputs()
    if target == "observation":
        observation = replace(observation, adjustment="ADJUSTED")
    else:
        evidence = replace(evidence, adjustment="UNADJUSTED")
    with pytest.raises(ProviderPlatformIntegrationRejected):
        assess_provider_platform_integration(
            observation, evidence, trading_day
        )


@pytest.mark.parametrize(
    "field,value",
    [
        ("status", "APPROVED"),
        ("official_trading_day_verified", True),
        ("analysis_authorized", True),
        ("persistence_authorized", True),
    ],
)
def test_forged_trading_day_authority_rejected(field, value):
    observation, evidence, trading_day = _inputs()
    trading_day = replace(trading_day, **{field: value})
    with pytest.raises(ProviderPlatformIntegrationRejected):
        assess_provider_platform_integration(
            observation, evidence, trading_day
        )


def test_invalid_observation_type_rejected():
    _, evidence, trading_day = _inputs()
    with pytest.raises(ProviderPlatformIntegrationRejected):
        assess_provider_platform_integration(
            object(), evidence, trading_day
        )


def test_invalid_evidence_type_rejected():
    observation, _, trading_day = _inputs()
    with pytest.raises(ProviderPlatformIntegrationRejected):
        assess_provider_platform_integration(
            observation, object(), trading_day
        )


def test_invalid_trading_day_type_rejected():
    observation, evidence, _ = _inputs()
    with pytest.raises(ProviderPlatformIntegrationRejected):
        assess_provider_platform_integration(
            observation, evidence, object()
        )


def test_decision_is_frozen():
    decision = assess_provider_platform_integration(*_inputs())
    with pytest.raises(FrozenInstanceError):
        decision.analysis_authorized = True
@pytest.mark.parametrize(
    "field,value",
    [
        ("status", "APPROVED"),
        ("independently_verified", True),
        ("analysis_authorized", True),
        ("persistence_authorized", True),
    ],
)
def test_forged_evidence_decision_rejected(monkeypatch, field, value):
    from price_provider_validation import provider_platform_integration as module
    from price_provider_validation.provider_evidence import (
        ProviderEvidenceDecision,
    )

    forged = ProviderEvidenceDecision(reason="SYNTHETIC")
    object.__setattr__(forged, field, value)

    monkeypatch.setattr(
        module,
        "assess_observation_evidence_binding",
        lambda observation, evidence: forged,
    )

    with pytest.raises(ProviderPlatformIntegrationRejected):
        module.assess_provider_platform_integration(*_inputs())

@pytest.mark.parametrize(
    "status,eligible",
    [
        ("CANDIDATE", False),
        ("BLOCKED", True),
        ("NON_TRADING", True),
        ("APPROVED", True),
    ],
)
def test_inconsistent_structural_trading_day_rejected(status, eligible):
    observation, evidence, trading_day = _inputs()
    trading_day = replace(
        trading_day,
        structural_status=status,
        structural_trading_day_eligible=eligible,
    )
    with pytest.raises(ProviderPlatformIntegrationRejected):
        assess_provider_platform_integration(
            observation, evidence, trading_day
        )

@pytest.mark.parametrize("provider", ["KIS", "KIWOOM"])
def test_platform_raw_bytes_matching_digest_remains_denied(provider):
    from hashlib import sha256
    from price_provider_validation.provider_platform_integration import (
        assess_provider_platform_raw_bytes_integration,
    )

    body = b"synthetic daily response bytes"
    observation, evidence, trading_day = _inputs(provider)
    evidence = replace(evidence, content_sha256=sha256(body).hexdigest())

    decision = assess_provider_platform_raw_bytes_integration(
        observation, evidence, trading_day, body
    )

    assert decision.status == "DENIED"
    assert decision.evidence_status == "DENIED"
    assert decision.analysis_authorized is False
    assert decision.dashboard_authorized is False
    assert decision.snapshot_authorized is False
    assert decision.persistence_authorized is False
    assert decision.live_api_execution_authorized is False
    assert decision.broker_execution_authorized is False


def test_platform_raw_bytes_modified_body_rejected():
    from hashlib import sha256
    from price_provider_validation.provider_platform_integration import (
        assess_provider_platform_raw_bytes_integration,
    )

    body = b"synthetic daily response bytes"
    observation, evidence, trading_day = _inputs()
    evidence = replace(evidence, content_sha256=sha256(body).hexdigest())

    with pytest.raises(ProviderPlatformIntegrationRejected):
        assess_provider_platform_raw_bytes_integration(
            observation, evidence, trading_day, body + b" modified"
        )


@pytest.mark.parametrize("invalid", ["text", bytearray(b"raw"), None, 123])
def test_platform_raw_bytes_non_bytes_rejected(invalid):
    from hashlib import sha256
    from price_provider_validation.provider_platform_integration import (
        assess_provider_platform_raw_bytes_integration,
    )

    body = b"synthetic daily response bytes"
    observation, evidence, trading_day = _inputs()
    evidence = replace(evidence, content_sha256=sha256(body).hexdigest())

    with pytest.raises(ProviderPlatformIntegrationRejected):
        assess_provider_platform_raw_bytes_integration(
            observation, evidence, trading_day, invalid
        )


@pytest.mark.parametrize(
    "field,value",
    [
        ("provider", "KIS"),
        ("ticker", "000660"),
        ("observation_date", "2026-10-29"),
    ],
)
def test_platform_raw_bytes_identity_mismatch_rejected(field, value):
    from hashlib import sha256
    from price_provider_validation.provider_platform_integration import (
        assess_provider_platform_raw_bytes_integration,
    )

    body = b"synthetic daily response bytes"
    observation, evidence, trading_day = _inputs()
    evidence = replace(
        evidence,
        content_sha256=sha256(body).hexdigest(),
        **{field: value},
    )

    with pytest.raises(ProviderPlatformIntegrationRejected):
        assess_provider_platform_raw_bytes_integration(
            observation, evidence, trading_day, body
        )


def test_platform_raw_bytes_adjustment_relabel_rejected():
    from hashlib import sha256
    from price_provider_validation.provider_platform_integration import (
        assess_provider_platform_raw_bytes_integration,
    )

    body = b"synthetic daily response bytes"
    observation, evidence, trading_day = _inputs()
    evidence = replace(
        evidence,
        content_sha256=sha256(body).hexdigest(),
        adjustment="ADJUSTED",
    )

    with pytest.raises(ProviderPlatformIntegrationRejected):
        assess_provider_platform_raw_bytes_integration(
            observation, evidence, trading_day, body
        )


@pytest.mark.parametrize(
    "field,value",
    [
        ("status", "APPROVED"),
        ("independently_verified", True),
        ("analysis_authorized", True),
        ("persistence_authorized", True),
    ],
)
def test_platform_raw_bytes_forged_authority_rejected(
    monkeypatch, field, value
):
    from hashlib import sha256
    from price_provider_validation import provider_platform_integration as module
    from price_provider_validation.provider_evidence import (
        ProviderEvidenceDecision,
    )

    body = b"synthetic daily response bytes"
    observation, evidence, trading_day = _inputs()
    evidence = replace(evidence, content_sha256=sha256(body).hexdigest())

    forged = ProviderEvidenceDecision(reason="SYNTHETIC")
    object.__setattr__(forged, field, value)

    original_binding = module.assess_observation_evidence_binding

    monkeypatch.setattr(
        module,
        "assess_observation_evidence_binding",
        original_binding,
    )

    monkeypatch.setattr(
        "price_provider_validation.provider_evidence.assess_raw_bytes_evidence_binding",
        lambda observation, evidence, raw_response: forged,
    )

    with pytest.raises(ProviderPlatformIntegrationRejected):
        module.assess_provider_platform_raw_bytes_integration(
            observation, evidence, trading_day, body
        )
