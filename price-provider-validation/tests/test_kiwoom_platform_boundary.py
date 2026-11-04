"""Synthetic KIWOOM boundary tests; no external I/O."""

from dataclasses import FrozenInstanceError, replace

import pytest

from price_provider_validation.provider_contract import (
    prepare_raw_observation,
)
from price_provider_validation.provider_evidence import ProviderEvidence
from price_provider_validation.trading_day_certification import (
    TradingDayCertificationDecision,
)
from price_provider_validation.kiwoom_platform_boundary import (
    KiwoomPlatformBoundaryDecision,
    KiwoomPlatformBoundaryRejected,
    assess_kiwoom_platform_boundary,
    invoke_kiwoom_platform_analysis,
)


def _inputs(provider="KIWOOM"):
    observation = prepare_raw_observation(
        provider,
        "005930",
        "2026-10-30",
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


def test_synthetic_kiwoom_remains_denied():
    decision = assess_kiwoom_platform_boundary(*_inputs())
    assert decision.provider == "KIWOOM"
    assert decision.ticker == "005930"
    assert decision.status == "DENIED"
    for name in (
        "analysis_authorized",
        "dashboard_authorized",
        "snapshot_authorized",
        "persistence_authorized",
    ):
        assert getattr(decision, name) is False


def test_other_provider_rejected():
    with pytest.raises(KiwoomPlatformBoundaryRejected):
        assess_kiwoom_platform_boundary(*_inputs("KIS"))


@pytest.mark.parametrize("index", [0, 1, 2])
def test_invalid_input_type_rejected(index):
    values = list(_inputs())
    values[index] = object()
    with pytest.raises(KiwoomPlatformBoundaryRejected):
        assess_kiwoom_platform_boundary(*values)


@pytest.mark.parametrize(
    "field,value",
    [
        ("status", "APPROVED"),
        ("analysis_authorized", True),
        ("dashboard_authorized", True),
        ("snapshot_authorized", True),
        ("persistence_authorized", True),
        ("provider", "KIS"),
    ],
)
def test_forged_boundary_rejected_before_callback(field, value):
    decision = assess_kiwoom_platform_boundary(*_inputs())
    forged = replace(decision)
    object.__setattr__(forged, field, value)
    calls = []
    with pytest.raises(KiwoomPlatformBoundaryRejected):
        invoke_kiwoom_platform_analysis(
            forged, lambda: calls.append("EXECUTED")
        )
    assert calls == []


def test_analysis_callback_never_executed():
    decision = assess_kiwoom_platform_boundary(*_inputs())
    calls = []
    with pytest.raises(ValueError):
        invoke_kiwoom_platform_analysis(
            decision, lambda: calls.append("EXECUTED")
        )
    assert calls == []


def test_repeated_denial_never_executes_callback():
    decision = assess_kiwoom_platform_boundary(*_inputs())
    calls = []
    for _ in range(3):
        with pytest.raises(ValueError):
            invoke_kiwoom_platform_analysis(
                decision, lambda: calls.append("EXECUTED")
            )
    assert calls == []


def test_boundary_decision_is_immutable():
    decision = assess_kiwoom_platform_boundary(*_inputs())
    with pytest.raises(FrozenInstanceError):
        decision.analysis_authorized = True


def test_invalid_callback_rejected():
    decision = assess_kiwoom_platform_boundary(*_inputs())
    with pytest.raises(KiwoomPlatformBoundaryRejected):
        invoke_kiwoom_platform_analysis(decision, None)


def test_invalid_decision_rejected():
    with pytest.raises(KiwoomPlatformBoundaryRejected):
        invoke_kiwoom_platform_analysis(object(), lambda: None)
