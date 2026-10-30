"""Fail-first compatibility tests for isolated provider error handling."""

import pytest

from price_provider_validation.provider_contract import (
    ProviderObservationRejected,
)
from price_provider_validation.provider_evidence import (
    ProviderEvidenceRejected,
)
from price_provider_validation.price_quality_adapter import (
    ProviderPriceQualityInput,
    assess_provider_price_quality,
)


def test_existing_provider_rejections_remain_value_errors():
    assert issubclass(ProviderObservationRejected, ValueError)
    assert issubclass(ProviderEvidenceRejected, ValueError)


@pytest.mark.parametrize(
    "invalid_close",
    [None, True, "not-a-number", "NaN", "Infinity", "0"],
)
def test_provider_quality_boundary_normalizes_invalid_numeric_errors(
    invalid_close,
):
    quality_input = ProviderPriceQualityInput(
        provider="KIS",
        ticker="005930",
        observation_date="2026-10-29",
        ohlcv=("100", "110", "90", invalid_close, "1000"),
    )

    with pytest.raises(ProviderObservationRejected):
        assess_provider_price_quality(quality_input)


def test_provider_quality_boundary_keeps_structural_denial():
    quality_input = ProviderPriceQualityInput(
        provider="KIWOOM",
        ticker="005930",
        observation_date="2026-10-29",
        ohlcv=("100", "110", "90", "100", "1000"),
        analysis_authorized=True,
    )

    with pytest.raises(
        ProviderObservationRejected,
        match="Quality input authority escalation",
    ):
        assess_provider_price_quality(quality_input)
