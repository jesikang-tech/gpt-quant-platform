"""Synthetic tests for the offline NAVER rebuild preflight."""

from dataclasses import FrozenInstanceError, replace

import pytest

from core.naver_http_response_validation import validate_naver_http_response
from price_rebuild_preflight import (
    RebuildKeyCoverage,
    assess_rebuild_candidates,
    assess_rebuild_key_coverage,
)


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


KEY_A = ("005930", "2026-01-02")
KEY_B = ("005930", "2026-01-05")
KEY_C = ("000660", "2026-01-02")
AUTHORITY_FIELDS = (
    "provenance_verified", "analysis_authorized", "persistence_authorized",
    "rebuild_authorized", "execution_authorized",
)


@pytest.mark.parametrize("inventory_type", [tuple, list])
def test_key_coverage_exact_is_complete_but_unauthorized(inventory_type):
    expected = inventory_type((KEY_B, KEY_A))
    observed = inventory_type((KEY_A, KEY_B))
    result = assess_rebuild_key_coverage(expected_keys=expected, observed_keys=observed)
    assert result.status == "COMPLETE_UNVERIFIED"
    assert result.expected_count == result.observed_count == 2
    assert result.missing_keys == result.unexpected_keys == ()
    assert all(getattr(result, name) is False for name in AUTHORITY_FIELDS)
    assert list(expected) == [KEY_B, KEY_A]
    assert list(observed) == [KEY_A, KEY_B]


@pytest.mark.parametrize(
    "expected,observed,missing,unexpected",
    [((KEY_A, KEY_B), (KEY_A,), (KEY_B,), ()),
     ((KEY_A,), (KEY_A, KEY_C), (), (KEY_C,)),
     ((KEY_A, KEY_B), (KEY_A, KEY_C), (KEY_B,), (KEY_C,)),
     ((KEY_A,), (), (KEY_A,), ())],
    ids=["missing", "unexpected", "both", "empty_observed"],
)
def test_key_coverage_differences_are_blocked(expected, observed, missing, unexpected):
    result = assess_rebuild_key_coverage(expected_keys=expected, observed_keys=observed)
    assert result.status == "BLOCKED"
    assert result.expected_count == len(expected)
    assert result.observed_count == len(observed)
    assert result.missing_keys == missing
    assert result.unexpected_keys == unexpected
    assert all(getattr(result, name) is False for name in AUTHORITY_FIELDS)


@pytest.mark.parametrize("side", ["expected", "observed"])
def test_key_coverage_duplicate_inventory_rejected(side):
    arguments = {"expected_keys": [KEY_A], "observed_keys": [KEY_A]}
    arguments[f"{side}_keys"] = [KEY_A, KEY_B, list(KEY_A)]
    with pytest.raises(ValueError, match=f"Duplicate {side} key"):
        assess_rebuild_key_coverage(**arguments)


@pytest.mark.parametrize("empty", [(), []])
def test_key_coverage_empty_expected_rejected(empty):
    with pytest.raises(ValueError, match="nonempty"):
        assess_rebuild_key_coverage(expected_keys=empty, observed_keys=[])


@pytest.mark.parametrize("side", ["expected", "observed"])
@pytest.mark.parametrize("inventory", [None, {}, "invalid", {KEY_A}])
def test_key_coverage_malformed_inventory_rejected(side, inventory):
    arguments = {"expected_keys": [KEY_A], "observed_keys": [KEY_A]}
    arguments[f"{side}_keys"] = inventory
    with pytest.raises(ValueError, match="inventory"):
        assess_rebuild_key_coverage(**arguments)


@pytest.mark.parametrize("side", ["expected", "observed"])
@pytest.mark.parametrize("key", [
    None, "005930", (), ("005930",), ("005930", "2026-01-02", "extra"),
    ("", "2026-01-02"), (" ", "2026-01-02"), (" 005930", "2026-01-02"),
    ("005930 ", "2026-01-02"), (5930, "2026-01-02"),
    ("005930", None), ("005930", "2026-02-30"),
    ("005930", "20260102"), ("005930", "2026-1-2"),
])
def test_key_coverage_invalid_ticker_date_or_key_rejected(side, key):
    arguments = {"expected_keys": [KEY_A], "observed_keys": [KEY_A]}
    arguments[f"{side}_keys"] = [key]
    with pytest.raises(ValueError):
        assess_rebuild_key_coverage(**arguments)


def test_key_coverage_differences_have_deterministic_order():
    extra = ("ZZZ", "2026-01-03")
    result = assess_rebuild_key_coverage(
        expected_keys=[KEY_B, KEY_A], observed_keys=[extra, KEY_C],
    )
    reverse = assess_rebuild_key_coverage(
        expected_keys=[KEY_A, KEY_B], observed_keys=[KEY_C, extra],
    )
    assert result == reverse
    assert result.missing_keys == (KEY_A, KEY_B)
    assert result.unexpected_keys == (KEY_C, extra)


def test_key_coverage_result_is_immutable():
    result = assess_rebuild_key_coverage(expected_keys=[KEY_A], observed_keys=[KEY_A])
    for name, value in (("status", "APPROVED"), ("missing_keys", (KEY_B,))):
        with pytest.raises(FrozenInstanceError):
            setattr(result, name, value)


@pytest.mark.parametrize("name", AUTHORITY_FIELDS)
def test_key_coverage_authority_cannot_be_forged(name):
    result = assess_rebuild_key_coverage(expected_keys=[KEY_A], observed_keys=[KEY_A])
    with pytest.raises(TypeError):
        RebuildKeyCoverage(
            status="COMPLETE_UNVERIFIED", expected_count=1, observed_count=1,
            missing_keys=(), unexpected_keys=(), **{name: True},
        )
    with pytest.raises(FrozenInstanceError):
        setattr(result, name, True)
    with pytest.raises(TypeError, match=f"field {name} is declared with init=False"):
        replace(result, **{name: True})


def test_key_coverage_inventory_scopes_are_not_silently_filtered():
    observations = _observations()
    source_keys = [(item.ticker, item.observation_date) for item in observations]
    # Existing fixture: four normal rows, followed by two classified special rows.
    prepared_keys = source_keys[:4]
    assert assess_rebuild_key_coverage(
        expected_keys=source_keys, observed_keys=source_keys,
    ).status == "COMPLETE_UNVERIFIED"
    assert assess_rebuild_key_coverage(
        expected_keys=prepared_keys, observed_keys=prepared_keys,
    ).status == "COMPLETE_UNVERIFIED"
    mixed = assess_rebuild_key_coverage(expected_keys=source_keys, observed_keys=prepared_keys)
    assert mixed.status == "BLOCKED"
    assert mixed.missing_keys == tuple(source_keys[4:])
    assert mixed.unexpected_keys == ()
