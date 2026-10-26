"""Synthetic tests for the offline NAVER rebuild preflight."""

from dataclasses import FrozenInstanceError, replace

import pytest

from core.naver_http_response_validation import validate_naver_http_response
from price_rebuild_preflight import assess_rebuild_candidates


TICKER = "005930"

ROWS = (
    "20260102|100|110|90|105|1000",
    "20260105|101|111|91|106|1001",
    "20260106|102|112|92|107|1002",
    "20260107|103|113|93|108|1003",
    "20260108|0|0|0|105|0",
    "20260109|100|104|90|105|1000",
)


def _observations(rows=ROWS):
    from hashlib import sha256

    payload = (
        '<protocol><chartdata>'
        + "".join(f'<item data="{row}" />' for row in rows)
        + '</chartdata></protocol>'
    ).encode("utf-8")

    return validate_naver_http_response(
        payload,
        sha256(payload).hexdigest(),
        TICKER,
    )


def test_classifies_normal_and_special_rows():
    result = assess_rebuild_candidates(TICKER, _observations())

    assert result.ticker == TICKER
    assert result.total_rows == 6
    assert result.normal_rows == 4
    assert result.zero_ohlc_rows == 1
    assert result.high_below_close_rows == 1
    assert result.price_candidates == 4
    assert result.ohlcv_candidates == 4
    assert result.verification_status == "UNVERIFIED"
    assert result.persistence_authorized is False


def test_empty_collection_remains_denied():
    result = assess_rebuild_candidates(TICKER, ())
    assert result.total_rows == 0
    assert result.price_candidates == 0
    assert result.persistence_authorized is False


@pytest.mark.parametrize("index", [0, 4, 5], ids=["normal", "zero_ohlc", "one_unit"])
@pytest.mark.parametrize("collection_type", [tuple, list])
def test_assembled_duplicate_observations_rejected(index, collection_type):
    observation = _observations()[index]
    assembled = collection_type((observation, observation))
    with pytest.raises(ValueError, match="Duplicate NAVER observation date"):
        assess_rebuild_candidates(TICKER, assembled)


def test_nonadjacent_assembled_duplicate_rejected():
    observations = _observations()
    with pytest.raises(ValueError, match="Duplicate NAVER observation date"):
        assess_rebuild_candidates(TICKER, (*observations, observations[0]))


def test_conflicting_observations_with_same_key_rejected():
    # Each response is valid alone; combining responses must not duplicate a key.
    first = _observations((ROWS[0],))[0]
    conflicting = _observations(("20260102|100|110|90|106|1000",))[0]
    with pytest.raises(ValueError, match="Duplicate NAVER observation date"):
        assess_rebuild_candidates(TICKER, (first, conflicting))


@pytest.mark.parametrize("collection_type", [tuple, list])
def test_assembled_unordered_observations_rejected(collection_type):
    observations = _observations()
    assembled = collection_type((observations[1], observations[0]))
    with pytest.raises(ValueError, match="Unordered NAVER observation dates"):
        assess_rebuild_candidates(TICKER, assembled)


def test_increasing_dates_with_gaps_preserve_counts_and_denial():
    # No weekday/holiday inference: only supplied ordering and identity matter.
    observations = _observations()
    result = assess_rebuild_candidates(
        TICKER, [observations[0], observations[3], observations[4], observations[5]],
    )
    assert result.total_rows == 4
    assert result.normal_rows == result.price_candidates == result.ohlcv_candidates == 2
    assert result.zero_ohlc_rows == result.high_below_close_rows == 1
    assert result.verification_status == "UNVERIFIED"
    assert result.persistence_authorized is False


def test_ticker_mismatch_rejected():
    with pytest.raises(ValueError, match="ticker mismatch"):
        assess_rebuild_candidates("000660", _observations())


@pytest.mark.parametrize("ticker", ["", None, 5930])
def test_invalid_ticker_rejected(ticker):
    with pytest.raises(ValueError, match="Valid ticker"):
        assess_rebuild_candidates(ticker, ())


@pytest.mark.parametrize("collection", [None, "invalid", {}])
def test_invalid_collection_rejected(collection):
    with pytest.raises(ValueError, match="collection"):
        assess_rebuild_candidates(TICKER, collection)


def test_unsupported_observation_rejected():
    with pytest.raises(ValueError):
        assess_rebuild_candidates(TICKER, (object(),))


@pytest.mark.parametrize(
    "field,value",
    [
        ("provenance_verified", True),
        ("adjustment", "ADJUSTED"),
        ("persistence_authorized", True),
    ],
)
def test_authority_escalation_rejected(field, value):
    observation = _observations()[0]
    modified = replace(observation, **{field: value})

    with pytest.raises(ValueError):
        assess_rebuild_candidates(TICKER, (modified,))


def test_result_is_immutable():
    result = assess_rebuild_candidates(TICKER, ())

    with pytest.raises(FrozenInstanceError):
        result.persistence_authorized = True
