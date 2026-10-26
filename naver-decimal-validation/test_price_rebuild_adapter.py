"""Synthetic tests for the NAVER rebuild adapter."""

from dataclasses import FrozenInstanceError, replace
from decimal import Decimal
from hashlib import sha256
from copy import copy, deepcopy
import sqlite3

import pytest

from price_rebuild_adapter import (
    BoundSyntheticRebuildRows,
    SyntheticRebuildRequest,
    SyntheticRebuildBatch,
    prepare_synthetic_rebuild_batch,
    prepare_bound_synthetic_rebuild_rows,
    prepare_synthetic_rebuild_rows,
    prepare_real_rebuild_rows,
    reject_unverified_rebuild,
)
from price_rebuild_preflight import RebuildPreflight
from core.naver_source_evidence import (
    AcquisitionContext, ClaimedProvider, EvidenceReference,
    NaverSourceEvidence, ObservationIdentity,
)
from core.naver_persistence_entry import persist_naver_observation
from core.price_provenance_gate import PriceProvenanceRejected


VALUES = {
    "Open": "100.125",
    "High": "110.500",
    "Low": "90.000",
    "Close": "105.375",
    "Volume": "1000",
}


def _prepare(**overrides):
    kwargs = {
        "adjustment": "UNADJUSTED",
        "synthetic_fixture": True,
    }
    kwargs.update(overrides)
    return prepare_synthetic_rebuild_rows(
        "005930",
        "2026-01-02",
        VALUES,
        **kwargs,
    )


def test_price_ohlcv_identity_and_decimal_precision():
    result = _prepare()

    assert result.ticker == "005930"
    assert result.price_row[0:2] == result.ohlcv_row[0:2]
    assert result.price_row[2] == result.ohlcv_row[5]
    assert result.price_row[2] == Decimal("105.375")
    assert result.ohlcv_row[3] == Decimal("110.500")
    assert result.verification_status == "SYNTHETIC_ONLY"
    assert result.persistence_authorized is False


@pytest.mark.parametrize("adjustment", ["ADJUSTED", "UNADJUSTED"])
def test_explicit_synthetic_adjustment(adjustment):
    result = _prepare(adjustment=adjustment)
    assert result.persistence_authorized is False


@pytest.mark.parametrize("declaration", [False, None, "true", 1])
def test_missing_or_invalid_synthetic_declaration_rejected(declaration):
    with pytest.raises(ValueError, match="synthetic fixture"):
        _prepare(synthetic_fixture=declaration)


@pytest.mark.parametrize("adjustment", ["UNKNOWN", "", None])
def test_unknown_adjustment_rejected(adjustment):
    with pytest.raises(ValueError, match="synthetic adjustment"):
        _prepare(adjustment=adjustment)


def test_unverified_preflight_always_denied():
    preflight = RebuildPreflight(
        ticker="005930",
        total_rows=6,
        normal_rows=4,
        zero_ohlc_rows=1,
        high_below_close_rows=1,
        price_candidates=4,
        ohlcv_candidates=4,
    )

    with pytest.raises(ValueError, match="UNVERIFIED_NAVER_REBUILD_DENIED"):
        reject_unverified_rebuild(preflight)


def test_invalid_preflight_type_rejected():
    with pytest.raises(ValueError, match="RebuildPreflight required"):
        reject_unverified_rebuild(object())


def test_preflight_authority_escalation_rejected():
    preflight = RebuildPreflight(
        ticker="005930",
        total_rows=1,
        normal_rows=1,
        zero_ohlc_rows=0,
        high_below_close_rows=0,
        price_candidates=1,
        ohlcv_candidates=1,
        persistence_authorized=True,
    )

    with pytest.raises(ValueError, match="Invalid preflight authority"):
        reject_unverified_rebuild(preflight)


def test_result_is_immutable():
    result = _prepare()

    with pytest.raises(FrozenInstanceError):
        result.persistence_authorized = True

def test_real_rebuild_entrypoint_denies_unverified_preflight():
    preflight = RebuildPreflight(
        ticker="005930",
        total_rows=1,
        normal_rows=1,
        zero_ohlc_rows=0,
        high_below_close_rows=0,
        price_candidates=1,
        ohlcv_candidates=1,
    )

    with pytest.raises(
        ValueError,
        match="UNVERIFIED_NAVER_REBUILD_DENIED",
    ):
        prepare_real_rebuild_rows(preflight)


def _bound_inputs(rows=("20260102|100|110|90|105|1000",)):
    raw = ('<protocol><chartdata>' + ''.join(
        f'<item data="{row}" />' for row in rows
    ) + '</chartdata></protocol>').encode("utf-8")
    digest = sha256(raw).hexdigest()
    identity = ObservationIdentity("SYNTHETIC", "2026-01-02", digest)
    evidence = NaverSourceEvidence(
        ClaimedProvider("NAVER"),
        AcquisitionContext("SYNTHETIC_FIXTURE", "2026-01-03T00:00:00Z", "synthetic://response"),
        identity,
        (EvidenceReference("fixture", "SYNTHETIC_RESPONSE", "NAVER", "TEST_ONLY",
                           "synthetic://response", digest),),
    )
    return raw, evidence


def _bound(raw, evidence, **overrides):
    arguments = dict(expected_observation=evidence.observation,
                     adjustment="UNADJUSTED", synthetic_fixture=True)
    arguments.update(overrides)
    return prepare_bound_synthetic_rebuild_rows(raw, evidence, **arguments)


def test_bound_synthetic_pair_preserves_evidence_and_exact_values():
    raw, evidence = _bound_inputs((
        "20260102|100|110|90|105|1000", "20260105|200|210|190|205|2000",
    ))
    result = _bound(raw, evidence, revision_id="synthetic-revision-1")
    assert result.evidence is evidence
    assert result.observation is evidence.observation
    assert result.source_sha256 == sha256(raw).hexdigest()
    assert result.provider == "NAVER"
    assert result.adjustment == "UNADJUSTED"
    assert result.revision_id == "synthetic-revision-1"
    assert result.verification_status == result.rows.verification_status == "SYNTHETIC_ONLY"
    assert result.rows.price_row == ("SYNTHETIC", "2026-01-02", Decimal("105"))
    assert result.rows.ohlcv_row == (
        "SYNTHETIC", "2026-01-02", Decimal("100"), Decimal("110"),
        Decimal("90"), Decimal("105"), Decimal("1000"),
    )
    assert result.rows.price_row[2] is result.rows.ohlcv_row[5]
    assert result.rows.persistence_authorized is False


def test_bound_result_and_nested_evidence_are_immutable():
    raw, evidence = _bound_inputs()
    result = _bound(raw, evidence)
    for target, name, value in (
        (result, "adjustment", "ADJUSTED"), (result.rows, "ticker", "OTHER"),
        (result.evidence, "caller_claims_verified", True),
        (result.observation, "content_sha256", "0" * 64),
    ):
        with pytest.raises(FrozenInstanceError):
            setattr(target, name, value)


@pytest.mark.parametrize("changes", [
    {"ticker": "OTHER"}, {"observation_date": "2026-01-05"},
    {"content_sha256": "0" * 64},
])
def test_bound_expected_evidence_identity_mismatch_rejected(changes):
    raw, evidence = _bound_inputs()
    with pytest.raises(ValueError, match="Evidence observation identity mismatch"):
        _bound(raw, evidence, expected_observation=replace(evidence.observation, **changes))


def test_bound_modified_bytes_rejected():
    raw, evidence = _bound_inputs()
    with pytest.raises(ValueError, match="SHA-256 mismatch"):
        _bound(raw.replace(b"105", b"106"), evidence)


@pytest.mark.parametrize("digest", ["bad", "g" * 64])
def test_bound_malformed_hash_rejected(digest):
    raw, evidence = _bound_inputs()
    evidence = replace(evidence, observation=replace(evidence.observation, content_sha256=digest))
    with pytest.raises(ValueError, match="Invalid expected SHA-256"):
        _bound(raw, evidence)


def test_bound_missing_matching_observation_rejected():
    raw, evidence = _bound_inputs(("20260105|100|110|90|105|1000",))
    with pytest.raises(ValueError, match="Exactly one matching observation"):
        _bound(raw, evidence)


def test_bound_duplicate_matching_observation_rejected_by_http_validator():
    row = "20260102|100|110|90|105|1000"
    raw, evidence = _bound_inputs((row, row))
    with pytest.raises(ValueError, match="Duplicate NAVER observation date"):
        _bound(raw, evidence)


@pytest.mark.parametrize("row", [
    "20260102|0|0|0|105|0", "20260102|100|104|90|105|1000",
])
def test_bound_special_rows_rejected(row):
    raw, evidence = _bound_inputs((row,))
    with pytest.raises(ValueError, match="Special observation"):
        _bound(raw, evidence)


def test_bound_conflicting_provider_reference_rejected():
    raw, evidence = _bound_inputs()
    evidence = replace(evidence, references=(replace(evidence.references[0], asserted_provider="OTHER"),))
    with pytest.raises(ValueError, match="Conflicting provider evidence"):
        _bound(raw, evidence)


def test_bound_consistent_non_naver_provider_rejected():
    raw, evidence = _bound_inputs()
    evidence = replace(evidence, claimed_provider=ClaimedProvider("OTHER"),
                       references=(replace(evidence.references[0], asserted_provider="OTHER"),))
    with pytest.raises(ValueError, match="NAVER provider declaration"):
        _bound(raw, evidence)


@pytest.mark.parametrize("adjustment", ["UNKNOWN", "", None, "VERIFIED"])
def test_bound_invalid_adjustment_declaration_rejected(adjustment):
    raw, evidence = _bound_inputs()
    with pytest.raises(ValueError, match="synthetic adjustment"):
        _bound(raw, evidence, adjustment=adjustment)


@pytest.mark.parametrize("revision", ["", " ", " revision", "revision ", 1, True])
def test_bound_invalid_revision_rejected(revision):
    raw, evidence = _bound_inputs()
    with pytest.raises(ValueError, match="Invalid revision identifier"):
        _bound(raw, evidence, revision_id=revision)


@pytest.mark.parametrize("adjustment", ["ADJUSTED", "UNADJUSTED"])
def test_bound_unknown_revision_and_declared_adjustment_remain_unverified(adjustment):
    raw, evidence = _bound_inputs()
    result = _bound(raw, evidence, adjustment=adjustment)
    assert result.revision_id is None
    assert result.adjustment == adjustment
    assert result.provenance_verified is False


@pytest.mark.parametrize("column,value", [(0, "OTHER"), (1, "2026-01-05")])
def test_bound_pair_identity_mismatch_rejected(monkeypatch, column, value):
    import price_rebuild_adapter as adapter
    raw, evidence = _bound_inputs()
    original = adapter.prepare_synthetic_rebuild_rows

    def wrong_identity(*args, **kwargs):
        rows = original(*args, **kwargs)
        price, ohlcv = list(rows.price_row), list(rows.ohlcv_row)
        price[column] = ohlcv[column] = value
        return replace(rows, price_row=tuple(price), ohlcv_row=tuple(ohlcv))

    with monkeypatch.context() as patch:
        patch.setattr(adapter, "prepare_synthetic_rebuild_rows", wrong_identity)
        with pytest.raises(ValueError, match="Prepared pair observation identity mismatch"):
            _bound(raw, evidence)


def test_bound_pair_close_mismatch_rejected(monkeypatch):
    import price_rebuild_adapter as adapter
    raw, evidence = _bound_inputs()
    original = adapter.prepare_synthetic_rebuild_rows

    def wrong_close(*args, **kwargs):
        rows = original(*args, **kwargs)
        return replace(rows, price_row=(*rows.price_row[:2], Decimal("106")))

    with monkeypatch.context() as patch:
        patch.setattr(adapter, "prepare_synthetic_rebuild_rows", wrong_close)
        with pytest.raises(ValueError, match="Decimal close mismatch"):
            _bound(raw, evidence)


@pytest.mark.parametrize("name", [
    "provenance_verified", "analysis_authorized", "persistence_authorized",
    "rebuild_authorized", "execution_authorized", "verification_status",
])
def test_bound_authority_and_status_cannot_be_overridden(name):
    raw, evidence = _bound_inputs()
    result = _bound(raw, evidence)
    value = "APPROVED" if name == "verification_status" else True
    assert getattr(result, name) == ("SYNTHETIC_ONLY" if name == "verification_status" else False)
    with pytest.raises(TypeError):
        BoundSyntheticRebuildRows(result.rows, evidence, result.adjustment, None, **{name: value})
    with pytest.raises(FrozenInstanceError):
        setattr(result, name, value)
    with pytest.raises(TypeError):
        replace(result, **{name: value})


def test_bound_caller_verification_claim_rejected():
    raw, evidence = _bound_inputs()
    with pytest.raises(ValueError, match="Caller verification claim"):
        _bound(raw, replace(evidence, caller_claims_verified=True))


def test_bound_nested_row_authority_rejected():
    raw, evidence = _bound_inputs()
    result = _bound(raw, evidence)
    with pytest.raises(ValueError, match="Nested row authority"):
        replace(result, rows=replace(result.rows, persistence_authorized=True))


@pytest.mark.parametrize("declaration", [False, None, "true", 1])
def test_bound_requires_explicit_synthetic_fixture(declaration):
    raw, evidence = _bound_inputs()
    with pytest.raises(ValueError, match="synthetic fixture"):
        _bound(raw, evidence, synthetic_fixture=declaration)


def _batch_request(ticker, day, *, revision_id=None, adjustment="UNADJUSTED"):
    raw, evidence = _bound_inputs((f"{day.replace('-', '')}|100|110|90|105|1000",))
    evidence = replace(evidence, observation=replace(
        evidence.observation, ticker=ticker, observation_date=day,
    ))
    return SyntheticRebuildRequest(raw, evidence, evidence.observation, adjustment, revision_id)


def _batch_requests():
    return (
        _batch_request("BBB", "2026-01-05", revision_id="revision-b"),
        _batch_request("AAA", "2026-01-05", adjustment="ADJUSTED"),
        _batch_request("AAA", "2026-01-02", revision_id="revision-a"),
    )


def _request_keys(requests):
    return [(item.expected_observation.ticker, item.expected_observation.observation_date)
            for item in requests]


def test_batch_multiple_tickers_dates_order_and_evidence_preservation():
    requests = _batch_requests()
    result = prepare_synthetic_rebuild_batch(
        requests, expected_keys=_request_keys(requests), synthetic_fixture=True,
    )
    keys = [(pair.observation.ticker, pair.observation.observation_date) for pair in result.pairs]
    assert keys == [("AAA", "2026-01-02"), ("AAA", "2026-01-05"), ("BBB", "2026-01-05")]
    assert result.coverage.status == "COMPLETE_UNVERIFIED"
    assert result.coverage.expected_count == result.coverage.observed_count == 3
    assert result.verification_status == "SYNTHETIC_ONLY"
    originals = dict(zip(_request_keys(requests), requests))
    for key, pair in zip(keys, result.pairs):
        request = originals[key]
        assert pair.evidence is request.evidence
        assert pair.source_sha256 == sha256(request.raw_response).hexdigest()
        assert pair.adjustment == request.adjustment
        assert pair.revision_id == request.revision_id
        assert pair.rows.price_row[:2] == pair.rows.ohlcv_row[:2] == key
        assert pair.rows.price_row[2] is pair.rows.ohlcv_row[5]
        assert pair.rows.price_row[2] == Decimal("105")
        assert pair.persistence_authorized is False


def test_batch_input_permutation_produces_identical_complete_result():
    requests = _batch_requests()
    first = prepare_synthetic_rebuild_batch(
        requests, expected_keys=_request_keys(requests), synthetic_fixture=True,
    )
    second = prepare_synthetic_rebuild_batch(
        list(reversed(requests)), expected_keys=list(reversed(_request_keys(requests))),
        synthetic_fixture=True,
    )
    assert first == second


def test_batch_duplicate_requests_rejected_without_revision_merging():
    request = _batch_requests()[0]
    with pytest.raises(ValueError, match="Duplicate observed key"):
        prepare_synthetic_rebuild_batch(
            [request, replace(request, revision_id="other-revision")],
            expected_keys=_request_keys([request]), synthetic_fixture=True,
        )


@pytest.mark.parametrize("missing", [True, False], ids=["missing", "unexpected"])
def test_batch_incomplete_expected_coverage_rejected(missing):
    requests = _batch_requests()
    expected = _request_keys(requests)
    expected = expected + [("CCC", "2026-01-02")] if missing else expected[:-1]
    with pytest.raises(ValueError, match="Incomplete synthetic rebuild coverage"):
        prepare_synthetic_rebuild_batch(requests, expected_keys=expected, synthetic_fixture=True)


def test_batch_later_invalid_request_raises_without_returning_partial_result():
    requests = _batch_requests()
    bad = replace(requests[1], raw_response=requests[1].raw_response + b" ")
    marker = object()
    returned = marker
    with pytest.raises(ValueError, match="SHA-256 mismatch"):
        returned = prepare_synthetic_rebuild_batch(
            [requests[0], bad], expected_keys=_request_keys(requests[:2]), synthetic_fixture=True,
        )
    assert returned is marker


def test_batch_special_request_is_rejected_not_omitted():
    raw, evidence = _bound_inputs(("20260102|0|0|0|105|0",))
    request = SyntheticRebuildRequest(raw, evidence, evidence.observation, "UNADJUSTED")
    with pytest.raises(ValueError, match="Special observation"):
        prepare_synthetic_rebuild_batch(
            [request], expected_keys=_request_keys([request]), synthetic_fixture=True,
        )


def test_batch_existing_pair_error_propagates_unchanged():
    request = replace(_batch_requests()[0], adjustment="UNKNOWN")
    with pytest.raises(ValueError, match="Explicit synthetic adjustment required"):
        prepare_synthetic_rebuild_batch(
            [request], expected_keys=_request_keys([request]), synthetic_fixture=True,
        )


@pytest.mark.parametrize("requests", [[], (), None, {}, "requests"])
def test_batch_requires_nonempty_explicit_requests(requests):
    with pytest.raises(ValueError, match="Nonempty explicit request collection"):
        prepare_synthetic_rebuild_batch(requests, expected_keys=[], synthetic_fixture=True)


def test_batch_rejects_wrong_request_type():
    with pytest.raises(ValueError, match="SyntheticRebuildRequest required"):
        prepare_synthetic_rebuild_batch([{}], expected_keys=[], synthetic_fixture=True)


@pytest.mark.parametrize("declaration", [False, None, "true", 1])
def test_batch_requires_exact_synthetic_fixture(declaration):
    requests = _batch_requests()
    with pytest.raises(ValueError, match="synthetic fixture"):
        prepare_synthetic_rebuild_batch(
            requests, expected_keys=_request_keys(requests), synthetic_fixture=declaration,
        )


def test_batch_and_nested_results_are_immutable():
    requests = _batch_requests()
    result = prepare_synthetic_rebuild_batch(
        requests, expected_keys=_request_keys(requests), synthetic_fixture=True,
    )
    assert type(result.pairs) is tuple
    assert type(result.coverage.missing_keys) is tuple
    for target, name, value in (
        (result, "pairs", ()), (result.coverage, "status", "APPROVED"),
        (result.pairs[0], "revision_id", "latest"),
        (result.pairs[0].rows, "price_row", ()),
        (result.pairs[0].evidence, "caller_claims_verified", True),
        (requests[0], "adjustment", "ADJUSTED"),
    ):
        with pytest.raises(FrozenInstanceError):
            setattr(target, name, value)


@pytest.mark.parametrize("name", [
    "provenance_verified", "analysis_authorized", "persistence_authorized",
    "rebuild_authorized", "execution_authorized", "verification_status",
])
def test_batch_authority_and_status_are_fixed_and_non_overridable(name):
    requests = _batch_requests()
    result = prepare_synthetic_rebuild_batch(
        requests, expected_keys=_request_keys(requests), synthetic_fixture=True,
    )
    value = "APPROVED" if name == "verification_status" else True
    assert getattr(result, name) == ("SYNTHETIC_ONLY" if name == "verification_status" else False)
    with pytest.raises(TypeError):
        SyntheticRebuildBatch(result.pairs, result.coverage, **{name: value})
    with pytest.raises(FrozenInstanceError):
        setattr(result, name, value)
    with pytest.raises(TypeError):
        replace(result, **{name: value})


@pytest.fixture
def batch_without_database(monkeypatch):
    database_calls = []

    def forbidden_connection(*args, **kwargs):
        database_calls.append((args, kwargs))
        raise AssertionError("Synthetic batch denial must not open a database")

    with monkeypatch.context() as patch:
        patch.setattr(sqlite3, "connect", forbidden_connection)
        patch.setattr(sqlite3.dbapi2, "connect", forbidden_connection)
        patch.setattr(sqlite3, "Connection", forbidden_connection)
        requests = _batch_requests()
        batch = prepare_synthetic_rebuild_batch(
            requests, expected_keys=_request_keys(requests), synthetic_fixture=True,
        )
        assert database_calls == []
        yield batch, database_calls


def _assert_batch_remains_synthetic(batch):
    assert batch.verification_status == "SYNTHETIC_ONLY"
    assert batch.coverage.status == "COMPLETE_UNVERIFIED"
    for result in (batch, batch.coverage, *batch.pairs):
        for name in (
            "provenance_verified", "analysis_authorized", "persistence_authorized",
            "rebuild_authorized", "execution_authorized",
        ):
            assert getattr(result, name) is False


@pytest.mark.parametrize("copier", [copy, deepcopy], ids=["shallow", "deep"])
def test_ordinary_batch_copy_preserves_synthetic_invariants(batch_without_database, copier):
    original, database_calls = batch_without_database
    copied = copier(original)
    assert copied is not original
    assert copied == original
    assert copied.coverage == original.coverage
    assert type(copied.pairs) is tuple
    for before, after in zip(original.pairs, copied.pairs):
        assert after.observation == before.observation
        assert after.evidence == before.evidence
        assert after.source_sha256 == before.source_sha256
        assert after.provider == before.provider
        assert after.adjustment == before.adjustment
        assert after.revision_id == before.revision_id
        assert after.rows.price_row == before.rows.price_row
        assert after.rows.ohlcv_row == before.rows.ohlcv_row
    _assert_batch_remains_synthetic(original)
    _assert_batch_remains_synthetic(copied)
    assert database_calls == []


@pytest.mark.parametrize("variant", ["original", "shallow", "deep"])
def test_original_and_copied_batches_cannot_enter_real_rebuild(batch_without_database, variant):
    original, database_calls = batch_without_database
    batch = copy(original) if variant == "shallow" else deepcopy(original) if variant == "deep" else original
    not_returned = object()
    result = not_returned
    # This API accepts only RebuildPreflight, not a synthetic batch certificate.
    with pytest.raises(ValueError, match="^RebuildPreflight required$"):
        result = prepare_real_rebuild_rows(batch)
    assert result is not_returned
    _assert_batch_remains_synthetic(batch)
    _assert_batch_remains_synthetic(original)
    assert database_calls == []


@pytest.mark.parametrize("variant", ["original", "shallow", "deep"])
def test_original_and_copied_batches_rejected_before_persistence_adapter(
    batch_without_database, variant,
):
    original, database_calls = batch_without_database
    batch = copy(original) if variant == "shallow" else deepcopy(original) if variant == "deep" else original
    adapter_calls = []

    def forbidden_adapter(observation):
        adapter_calls.append(observation)
        raise AssertionError("Persistence adapter must not execute")

    not_returned = object()
    result = not_returned
    # The public persistence boundary accepts an observation object and adapter;
    # supplying a batch does not make it a supported operational data format.
    with pytest.raises(PriceProvenanceRejected, match="persistence is prohibited"):
        result = persist_naver_observation(batch, forbidden_adapter)
    assert result is not_returned
    assert adapter_calls == []
    assert database_calls == []
    _assert_batch_remains_synthetic(batch)
    _assert_batch_remains_synthetic(original)
