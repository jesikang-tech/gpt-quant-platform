"""Synthetic tests for the NAVER rebuild adapter."""

from dataclasses import FrozenInstanceError, replace
from decimal import Decimal
from hashlib import sha256

import pytest

from price_rebuild_adapter import (
    BoundSyntheticRebuildRows,
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
