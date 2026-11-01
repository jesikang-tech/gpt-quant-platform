"""Offline compatibility checks for quality and existing deny-only boundaries."""

import pytest

from core.price_provenance_gate import PriceProvenanceRejected

from price_provider_validation.provider_contract import (
    prepare_raw_observation,
)
from price_provider_validation.provider_quality_entry import (
    assess_provider_observation_quality,
)
from price_provider_validation.price_quality_adapter import (
    prepare_provider_price_quality_input,
    assess_provider_price_quality,
)
from price_provider_validation.ohlcv_mapping import OhlcvFieldMapping
from price_provider_validation.trading_day_certification import (
    assess_trading_day_certification,
)
from price_provider_validation.provider_analysis_boundary import (
    assess_provider_analysis_boundary,
    invoke_provider_analysis,
)
from price_provider_validation.provider_evidence import (
    ProviderEvidenceDecision,
)


@pytest.mark.parametrize("provider", ["KIS", "KIWOOM"])
def test_quality_and_existing_analysis_boundary_remain_denied(provider):
    observation = prepare_raw_observation(
        provider,
        "005930",
        "2026-10-28",
        ("100", "110", "90", "105", "1000"),
    )

    quality = assess_provider_observation_quality(observation)

    assert quality.status == "DENIED"
    assert quality.structural_status == "CANDIDATE"
    assert quality.analysis_authorized is False
    assert quality.persistence_authorized is False

    quality_input = prepare_provider_price_quality_input(
        observation,
        OhlcvFieldMapping(0, 1, 2, 3, 4),
    )
    structural = assess_provider_price_quality(quality_input)
    trading_day = assess_trading_day_certification(structural)

    assert trading_day.status == "DENIED"
    assert trading_day.official_trading_day_verified is False
    assert trading_day.structural_status == quality.structural_status
    assert trading_day.structural_reason == quality.structural_reason
    assert (
        trading_day.structural_trading_day_eligible
        is quality.structural_trading_day_eligible
    )

    evidence = ProviderEvidenceDecision()
    boundary = assess_provider_analysis_boundary(
        observation,
        evidence,
        trading_day,
    )

    assert boundary.status == "BLOCKED"
    assert boundary.analysis_authorized is False
    assert boundary.dashboard_authorized is False
    assert boundary.snapshot_authorized is False
    assert boundary.persistence_authorized is False

    invoked = []

    def analysis_callback():
        invoked.append(True)

    with pytest.raises(PriceProvenanceRejected):
        invoke_provider_analysis(boundary, analysis_callback)

    assert invoked == []

def test_quality_and_kiwoom_persistence_remain_denied():
    """A structurally valid price must not authorize persistence."""
    from price_provider_validation.provider_persistence_entry import (
        invoke_provider_persistence,
    )
    from price_provider_validation.provider_usage_policy import (
        UsagePurpose,
        assess_provider_usage,
    )

    observation = prepare_raw_observation(
        "KIWOOM",
        "005930",
        "2026-10-30",
        ("100", "110", "90", "105", "1000"),
    )

    quality = assess_provider_observation_quality(observation)

    assert quality.structural_status == "CANDIDATE"
    assert quality.status == "DENIED"
    assert quality.persistence_authorized is False

    quality_input = prepare_provider_price_quality_input(
        observation,
        OhlcvFieldMapping(0, 1, 2, 3, 4),
    )
    structural = assess_provider_price_quality(quality_input)
    trading_day = assess_trading_day_certification(structural)

    assert trading_day.status == "DENIED"
    assert trading_day.official_trading_day_verified is False
    assert trading_day.structural_status == quality.structural_status
    assert trading_day.structural_reason == quality.structural_reason
    assert (
        trading_day.structural_trading_day_eligible
        is quality.structural_trading_day_eligible
    )

    usage = assess_provider_usage(
        "KIWOOM",
        UsagePurpose.PERSONAL_OWN_ASSET,
        official_reply_reviewed=True,
    )

    assert usage.api_execution_authorized is False
    assert usage.persistence_authorized is False

    evidence = ProviderEvidenceDecision(
        reason="SYNTHETIC_UNVERIFIED"
    )

    calls = []

    def persist_callback():
        calls.append("PERSISTED")

    try:
        with pytest.raises(PriceProvenanceRejected):
            invoke_provider_persistence(
                observation=observation,
                usage_decision=usage,
                evidence_decision=evidence,
                trading_day_decision=trading_day,
                persist_callback=persist_callback,
            )
    finally:
        assert calls == [], "Persistence callback must never execute"
