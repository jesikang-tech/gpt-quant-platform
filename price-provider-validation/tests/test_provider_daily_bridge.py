"""Synthetic offline tests for the common provider daily bridge."""
from dataclasses import replace

import pytest

from price_provider_validation.provider_contract import ProviderObservationRejected
from price_provider_validation.provider_evidence import ProviderEvidence
from price_provider_validation.trading_day_certification import (
    TradingDayCertificationDecision,
)
from price_provider_validation.provider_platform_integration import (
    ProviderPlatformIntegrationRejected,
)
from price_provider_validation.provider_daily_bridge import (
    assess_provider_daily_bridge,
)


def _row(provider):
    if provider == "KIS":
        return {
            "stck_bsop_date": "20261028",
            "stck_oprc": "100",
            "stck_hgpr": "110",
            "stck_lwpr": "90",
            "stck_clpr": "105",
            "acml_vol": "1000",
        }
    return {
        "dt": "20261028",
        "open_pric": "100",
        "high_pric": "110",
        "low_pric": "90",
        "cur_prc": "105",
        "trde_qty": "1000",
    }


def _inputs(provider):
    evidence = ProviderEvidence(
        provider=provider,
        ticker="005930",
        observation_date="2026-10-28",
        acquired_at="2026-10-28T16:00:00+09:00",
        source_locator="synthetic://provider/daily",
        content_sha256="a" * 64,
    )
    trading_day = TradingDayCertificationDecision(
        structural_status="CANDIDATE",
        structural_reason="SYNTHETIC_CANDIDATE",
        structural_trading_day_eligible=True,
    )
    api_id = "ka10081" if provider == "KIWOOM" else None
    return (
        provider, "005930", _row(provider),
        evidence, trading_day, api_id
    )


@pytest.mark.parametrize("provider", ["KIS", "KIWOOM"])
def test_synthetic_daily_bridge_remains_denied(provider):
    decision = assess_provider_daily_bridge(*_inputs(provider))
    assert decision.provider == provider
    assert decision.ticker == "005930"
    assert decision.observation_date == "2026-10-28"
    assert decision.status == "DENIED"
    assert decision.evidence_status == "DENIED"
    assert decision.trading_day_status == "DENIED"
    for field in (
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
        assert getattr(decision, field) is False


@pytest.mark.parametrize("provider", ["KIS", "KIWOOM"])
def test_evidence_ticker_mismatch_rejected(provider):
    args = list(_inputs(provider))
    args[3] = replace(args[3], ticker="000660")
    with pytest.raises(ProviderPlatformIntegrationRejected):
        assess_provider_daily_bridge(*args)


@pytest.mark.parametrize("provider", ["KIS", "KIWOOM"])
def test_forged_trading_day_authority_rejected(provider):
    args = list(_inputs(provider))
    args[4] = replace(args[4], analysis_authorized=True)
    with pytest.raises(ProviderPlatformIntegrationRejected):
        assess_provider_daily_bridge(*args)


@pytest.mark.parametrize("provider", ["KIS", "KIWOOM"])
def test_incomplete_daily_row_rejected(provider):
    args = list(_inputs(provider))
    args[2] = {}
    with pytest.raises(ProviderObservationRejected):
        assess_provider_daily_bridge(*args)
