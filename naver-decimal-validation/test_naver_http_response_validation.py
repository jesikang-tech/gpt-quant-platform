"""Offline synthetic tests for raw NAVER HTTP response validation."""

from dataclasses import FrozenInstanceError
from hashlib import sha256

import pytest

from core.naver_http_response_validation import (
    NaverHighBelowCloseByOneRow,
    NaverHttpResponseRejected,
    NaverZeroOhlcSpecialRow,
    validate_naver_http_response,
)
from core.naver_analysis_boundary import assess_naver_analysis_observation


def _response(*rows):
    items = "".join(f'<item data="{row}" />' for row in rows)
    return f"<?xml version='1.0' encoding='UTF-8'?><protocol><chartdata>{items}</chartdata></protocol>".encode()


def _validate(body):
    return validate_naver_http_response(body, sha256(body).hexdigest(), "0008S0")


def test_valid_response_preserves_raw_text_and_returns_immutable_observations():
    first = "20260916|09680|09715|09621|09676|0252142"
    second = "20260917|9676|9800|9650|9780|300000"
    observations = _validate(_response(first, second))

    assert isinstance(observations, tuple)
    assert tuple(item.raw_row for item in observations) == (first, second)
    assert observations[0].values == (
        "09680", "09715", "09621", "09676", "0252142",
    )
    assert observations[0].adjustment == "UNKNOWN"
    assert observations[0].provenance_verified is False
    assert observations[0].persistence_authorized is False
    with pytest.raises(FrozenInstanceError):
        observations[0].ticker = "changed"


def test_exact_zero_ohlc_special_row_is_classified_as_immutable_evidence():
    raw_row = "20180430|0|0|0|53000|0"
    special_row, = _validate(_response(raw_row))

    assert isinstance(special_row, NaverZeroOhlcSpecialRow)
    assert special_row.raw_row == raw_row
    assert special_row.values == ("0", "0", "0", "53000", "0")
    assert special_row.classification == "ZERO_OHLC_NON_TRADING_EVIDENCE"
    assert special_row.provenance_verified is False
    assert special_row.analysis_authorized is False
    assert special_row.persistence_authorized is False
    with pytest.raises(FrozenInstanceError):
        special_row.persistence_authorized = True


def test_mixed_normal_and_special_rows_preserve_their_distinct_types():
    normal = "20180427|52000|54000|51000|53000|1000"
    special = "20180502|0|0|0|53000|0"
    observations = _validate(_response(normal, special))

    assert not isinstance(observations[0], NaverZeroOhlcSpecialRow)
    assert isinstance(observations[1], NaverZeroOhlcSpecialRow)
    assert tuple(item.raw_row for item in observations) == (normal, special)


def test_exact_one_unit_high_close_violation_is_immutable_evidence():
    raw_row = "20260916|9680|9715|9621|9716|0252142"
    evidence, = _validate(_response(raw_row))

    assert isinstance(evidence, NaverHighBelowCloseByOneRow)
    assert evidence.observation.raw_row == raw_row
    assert evidence.raw_row == raw_row
    assert evidence.values == ("9680", "9715", "9621", "9716", "0252142")
    assert evidence.ticker == "0008S0"
    assert evidence.observation_date == "2026-09-16"
    assert evidence.provider == "NAVER"
    assert evidence.adjustment == "UNKNOWN"
    assert evidence.provenance_verified is False
    assert evidence.classification == "HIGH_BELOW_CLOSE_BY_ONE_UNVERIFIED"
    with pytest.raises(FrozenInstanceError):
        evidence.classification = "changed"


def test_mixed_normal_zero_special_and_one_unit_evidence_preserve_types():
    normal = "20180427|52000|54000|51000|53000|1000"
    zero_special = "20180430|0|0|0|53000|0"
    one_unit = "20180502|52000|54000|51000|54001|1000"

    observations = _validate(_response(normal, zero_special, one_unit))

    assert type(observations[0]) not in (
        NaverZeroOhlcSpecialRow, NaverHighBelowCloseByOneRow,
    )
    assert isinstance(observations[1], NaverZeroOhlcSpecialRow)
    assert isinstance(observations[2], NaverHighBelowCloseByOneRow)
    assert tuple(item.raw_row for item in observations) == (
        normal, zero_special, one_unit,
    )


def test_one_unit_evidence_has_no_analysis_or_persistence_authority():
    evidence, = _validate(
        _response("20260916|9680|9715|9621|9716|252142")
    )

    assert evidence.analysis_authorized is False
    assert evidence.persistence_authorized is False


def test_analysis_exact_type_gate_rejects_one_unit_evidence():
    evidence, = _validate(
        _response("20260916|9680|9715|9621|9716|252142")
    )

    with pytest.raises(ValueError, match="INVALID_NAVER_OBSERVATION"):
        assess_naver_analysis_observation(evidence)


@pytest.mark.parametrize(
    "row",
    [
        "20260916|9680|9715|9621|9717|252142",  # close is high + 2
        "20260916|9716|9715|9621|9716|252142",  # open is above high
        "20260916|9680|9715|9681|9716|252142",  # low is above open
        "20260916|9680|9715|9717|9716|252142",  # low is above close
        "20260916|0|9715|0|9716|252142",
        "20260916|-1|9715|9621|9716|252142",
        "20260916|9680|9715|9621|9716|-1",
    ],
)
def test_nearby_invalid_rows_are_not_one_unit_evidence(row):
    with pytest.raises(NaverHttpResponseRejected, match="Invalid NAVER OHLCV"):
        _validate(_response(row))


def test_hash_is_over_original_bytes_and_mismatch_is_rejected():
    body = _response("20260916|9680|9715|9621|9676|252142")
    changed_body = body.replace(b"9680", b"9681")

    with pytest.raises(NaverHttpResponseRejected, match="SHA-256 mismatch"):
        validate_naver_http_response(
            changed_body,
            sha256(body).hexdigest(),
            "0008S0",
        )


@pytest.mark.parametrize(
    "body",
    [
        b"<protocol><chartdata>",
        b"not xml",
    ],
)
def test_malformed_xml_is_rejected(body):
    with pytest.raises(NaverHttpResponseRejected, match="Malformed NAVER XML"):
        _validate(body)


@pytest.mark.parametrize(
    "row",
    [
        "20260916|9680|9715|9621|9676",
        "20260916|9680|9715|9621|bad|252142",
        "20260230|9680|9715|9621|9676|252142",
    ],
)
def test_invalid_ohlcv_is_rejected(row):
    with pytest.raises(NaverHttpResponseRejected, match="Invalid NAVER OHLCV"):
        _validate(_response(row))


@pytest.mark.parametrize(
    "row",
    [
        "20260916|0|9715|9621|9676|252142",
        "20260916|9680|0|9621|9676|252142",
        "20260916|9680|9715|0|9676|252142",
        "20260916|9680|9715|9621|0|252142",
        "20260916|9680|9715|9621|9676|-1",
        "20260916|9680|9675|9621|9676|252142",
        "20260916|9680|9679|9621|9676|252142",
        "20260916|9680|9715|9681|9676|252142",
        "20260916|9680|9715|9677|9676|252142",
    ],
)
def test_invalid_ohlcv_value_relationships_are_rejected(row):
    with pytest.raises(NaverHttpResponseRejected, match="Invalid NAVER OHLCV"):
        _validate(_response(row))


@pytest.mark.parametrize(
    "row",
    [
        "20180503|0|0|0|0|0",
        "20180503|0|0|0|53000|1",
        "20180503|0|0|1|53000|0",
        "20180503|0|1|0|53000|0",
        "20180503|1|0|0|53000|0",
    ],
)
def test_other_zero_value_combinations_are_not_special_rows(row):
    with pytest.raises(NaverHttpResponseRejected, match="Invalid NAVER OHLCV"):
        _validate(_response(row))


@pytest.mark.parametrize(
    "body",
    [
        b'<unexpected><chartdata><item data="20260916|9680|9715|9621|9676|252142" /></chartdata></unexpected>',
        b'<protocol><wrapper><chartdata><item data="20260916|9680|9715|9621|9676|252142" /></chartdata></wrapper></protocol>',
        b'<protocol><chartdata /><chartdata /></protocol>',
        b'<protocol><chartdata /><unexpected /></protocol>',
    ],
)
def test_invalid_naver_envelope_or_chartdata_structure_is_rejected(body):
    with pytest.raises(NaverHttpResponseRejected, match="envelope|chartdata"):
        _validate(body)


@pytest.mark.parametrize(
    "item",
    [
        '<item />',
        '<item data="20260916|9680|9715|9621|9676|252142" extra="value" />',
        '<item data="20260916|9680|9715|9621|9676|252142"><item data="20260917|9680|9715|9621|9676|252142" /></item>',
        '<wrapper><item data="20260916|9680|9715|9621|9676|252142" /></wrapper>',
    ],
)
def test_malformed_or_nested_item_elements_are_rejected(item):
    body = f"<protocol><chartdata>{item}</chartdata></protocol>".encode()

    with pytest.raises(NaverHttpResponseRejected, match="Malformed NAVER item"):
        _validate(body)


def test_duplicate_dates_are_rejected():
    body = _response(
        "20260916|9680|9715|9621|9676|252142",
        "20260916|9700|9750|9650|9720|200000",
    )

    with pytest.raises(NaverHttpResponseRejected, match="Duplicate"):
        _validate(body)


def test_unordered_dates_are_rejected():
    body = _response(
        "20260917|9676|9800|9650|9780|300000",
        "20260916|9680|9715|9621|9676|252142",
    )

    with pytest.raises(NaverHttpResponseRejected, match="Unordered"):
        _validate(body)


def test_response_without_ohlcv_items_is_rejected():
    with pytest.raises(NaverHttpResponseRejected, match="no OHLCV rows"):
        _validate(b"<protocol><chartdata /></protocol>")
