"""Tests for pure NAVER raw observation boundary."""

import pytest

from core.naver_raw_observation import (
    NaverRawObservationRejected,
    authorize_naver_raw_observation,
    prepare_naver_raw_observation,
)


RAW_ROW = "20260916|9680|9715|9621|9676|252142"


def test_naver_raw_observation_preserves_exact_text():
    observation = prepare_naver_raw_observation("0008S0", RAW_ROW)

    assert observation.ticker == "0008S0"
    assert observation.observation_date == "2026-09-16"
    assert observation.raw_row == RAW_ROW

    assert observation.values == (
        "9680",
        "9715",
        "9621",
        "9676",
        "252142",
    )


def test_naver_raw_observation_keeps_unknown_adjustment():
    observation = prepare_naver_raw_observation("0008S0", RAW_ROW)

    assert observation.provider == "NAVER"
    assert observation.adjustment == "UNKNOWN"
    assert observation.provenance_verified is False
    assert observation.persistence_authorized is False


def test_naver_raw_observation_denies_persistence():
    observation = prepare_naver_raw_observation("0008S0", RAW_ROW)

    with pytest.raises(
        NaverRawObservationRejected,
        match="operational persistence prohibited",
    ):
        authorize_naver_raw_observation(observation)


@pytest.mark.parametrize(
    "ticker",
    ["", " 0008S0", "0008S0 ", None, 123],
)
def test_naver_raw_observation_rejects_invalid_ticker(ticker):
    with pytest.raises(NaverRawObservationRejected):
        prepare_naver_raw_observation(ticker, RAW_ROW)


@pytest.mark.parametrize(
    "raw_row",
    [
        "",
        "20260916|9680|9715|9621|9676",
        "20260916|9680|9715|9621|9676|bad",
        "20261316|9680|9715|9621|9676|252142",
    ],
)
def test_naver_raw_observation_rejects_invalid_row(raw_row):
    with pytest.raises(ValueError):
        prepare_naver_raw_observation("0008S0", raw_row)
