"""Synthetic tests for the Kiwoom Ver1.1 daily reference bridge."""

from dataclasses import replace

import pytest

from price_provider_validation.kiwoom_price_reference_policy import (
    assess_kiwoom_ver11_daily_reference,
)
from price_provider_validation.provider_evidence import ProviderEvidence
from price_provider_validation.provider_platform_integration import (
    ProviderPlatformIntegrationRejected,
)
from price_provider_validation.trading_day_certification import (
    TradingDayCertificationDecision,
)


def _inputs(api_id):
    date_field = "dt" if api_id == "ka10081" else "date"
    close_field = "cur_prc" if api_id == "ka10081" else "close_pric"

    row = {
        date_field: "20261028",
        "open_pric": "100",
        "high_pric": "110",
        "low_pric": "90",
        close_field: "105",
        "trde_qty": "1000",
    }

    evidence = ProviderEvidence(
        provider="KIWOOM",
        ticker="005930",
        observation_date="2026-10-28",
        acquired_at="2026-10-28T16:00:00+09:00",
        source_locator="synthetic://kiwoom/ver11",
        content_sha256="a" * 64,
    )

    trading_day = TradingDayCertificationDecision(
        structural_status="CANDIDATE",
        structural_reason="SYNTHETIC_CANDIDATE",
        structural_trading_day_eligible=True,
    )

    return row, evidence, trading_day


@pytest.mark.parametrize("api_id", ["ka10081", "ka10086"])
def test_ver11_daily_reference_remains_denied(api_id):
    row, evidence, trading_day = _inputs(api_id)

    decision = assess_kiwoom_ver11_daily_reference(
        "005930", row, evidence, trading_day, api_id=api_id
    )

    assert decision.provider == "KIWOOM"
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
        "database_rebuild_authorized",
        "broker_execution_authorized",
    ):
        assert getattr(decision, field) is False


def test_unsupported_daily_api_rejected():
    row, evidence, trading_day = _inputs("ka10081")

    with pytest.raises(ValueError, match="UNSUPPORTED_KIWOOM_DAILY_API"):
        assess_kiwoom_ver11_daily_reference(
            "005930", row, evidence, trading_day, api_id="ka99999"
        )


@pytest.mark.parametrize("api_id", ["ka10081", "ka10086"])
def test_evidence_ticker_mismatch_rejected(api_id):
    row, evidence, trading_day = _inputs(api_id)
    evidence = replace(evidence, ticker="000660")

    with pytest.raises(ProviderPlatformIntegrationRejected):
        assess_kiwoom_ver11_daily_reference(
            "005930", row, evidence, trading_day, api_id=api_id
        )


@pytest.mark.parametrize("api_id", ["ka10081", "ka10086"])
def test_forged_trading_day_authority_rejected(api_id):
    row, evidence, trading_day = _inputs(api_id)
    trading_day = replace(trading_day, analysis_authorized=True)

    with pytest.raises(ProviderPlatformIntegrationRejected):
        assess_kiwoom_ver11_daily_reference(
            "005930", row, evidence, trading_day, api_id=api_id
        )
