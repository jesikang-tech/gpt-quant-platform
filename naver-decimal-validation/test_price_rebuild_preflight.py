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