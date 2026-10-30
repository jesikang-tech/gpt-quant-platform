"""Offline synthetic contract tests for the common daily interface."""

import pytest

from price_provider_validation.provider_contract import (
    ProviderObservationRejected,
    RawPriceObservation,
)
from price_provider_validation.provider_daily_interface import (
    prepare_provider_daily_observation,
)


def _kis_row():
    return {
        "stck_bsop_date": "20261028",
        "stck_oprc": "100",
        "stck_hgpr": "110",
        "stck_lwpr": "90",
        "stck_clpr": "105",
        "acml_vol": "1000",
    }


def _kiwoom_row(api_id):
    date_field = "dt" if api_id == "ka10081" else "date"
    close_field = "cur_prc" if api_id == "ka10081" else "close_pric"
    return {
        date_field: "20261028",
        "open_pric": "100",
        "high_pric": "110",
        "low_pric": "90",
        close_field: "105",
        "trde_qty": "1000",
    }


@pytest.mark.parametrize(
    "provider,api_id,row",
    [
        ("KIS", None, _kis_row()),
        ("KIWOOM", "ka10081", _kiwoom_row("ka10081")),
        ("KIWOOM", "ka10086", _kiwoom_row("ka10086")),
    ],
)
def test_common_interface_preserves_existing_contract(
    provider, api_id, row
):
    observation = prepare_provider_daily_observation(
        provider, "005930", row, api_id=api_id
    )

    assert type(observation) is RawPriceObservation
    assert observation.provider == provider
    assert observation.ticker == "005930"
    assert observation.observation_date == "2026-10-28"
    assert observation.raw_fields == (
        "100", "110", "90", "105", "1000"
    )
    assert observation.adjustment == "UNKNOWN"


@pytest.mark.parametrize(
    "provider,api_id",
    [
        ("UNKNOWN", None),
        (None, None),
        (True, None),
        ("KIS", "ka10081"),
        ("KIWOOM", None),
        ("KIWOOM", ""),
        ("KIWOOM", "ka99999"),
    ],
)
def test_invalid_provider_or_api_selection_rejected(
    provider, api_id
):
    with pytest.raises(ProviderObservationRejected):
        prepare_provider_daily_observation(
            provider, "005930", {}, api_id=api_id
        )


@pytest.mark.parametrize(
    "provider,api_id,row",
    [
        ("KIS", None, {"stck_bsop_date": "20261028"}),
        ("KIWOOM", "ka10081", {"dt": "20261028"}),
        ("KIWOOM", "ka10086", {"date": "20261028"}),
    ],
)
def test_incomplete_response_row_rejected(
    provider, api_id, row
):
    with pytest.raises(ProviderObservationRejected):
        prepare_provider_daily_observation(
            provider, "005930", row, api_id=api_id
        )


def test_common_interface_preserves_unverified_raw_signs():
    row = _kiwoom_row("ka10086")
    row["open_pric"] = "+100"
    row["low_pric"] = "-90"

    observation = prepare_provider_daily_observation(
        "KIWOOM", "005930", row, api_id="ka10086"
    )

    assert observation.raw_fields == (
        "+100", "110", "-90", "105", "1000"
    )
    assert observation.adjustment == "UNKNOWN"
