"""Synthetic K15 acquisition-record consistency and denial tests."""
from dataclasses import FrozenInstanceError

import pytest

from price_provider_validation.provider_acquisition_evidence import (
    AcquisitionEvidenceRejected,
    AcquisitionRecord,
    assess_acquisition_record,
)
from price_provider_validation.provider_evidence import ProviderEvidence


API_CASES = (
    ("KIS", "inquire_daily_itemchartprice"),
    ("KIS", "inquire_daily_price"),
    ("KIWOOM", "ka10081"),
    ("KIWOOM", "ka10086"),
)


def evidence(provider):
    return ProviderEvidence(
        provider=provider,
        ticker="005930",
        observation_date="2026-10-28",
        acquired_at="2026-10-29T09:00:00+09:00",
        source_locator="synthetic:unverified",
        content_sha256="a" * 64,
        adjustment="UNKNOWN",
    )


def record(provider, api_id, **changes):
    values = dict(
        provider=provider,
        api_id=api_id,
        ticker="005930",
        observation_date="2026-10-28",
        content_sha256="a" * 64,
        acquisition_record_id="synthetic-record-001",
    )
    values.update(changes)
    return AcquisitionRecord(**values)


@pytest.mark.parametrize("provider,api_id", API_CASES)
def test_matching_declarations_remain_denied(provider, api_id):
    result = assess_acquisition_record(
        evidence(provider), record(provider, api_id)
    )
    assert result.provider == provider
    assert result.api_id == api_id
    assert result.status == "DENIED"
    assert result.reason == "ACQUISITION_SOURCE_NOT_INDEPENDENTLY_VERIFIED"
    for name in (
        "independently_verified",
        "analysis_authorized",
        "persistence_authorized",
        "live_api_execution_authorized",
        "broker_execution_authorized",
    ):
        assert getattr(result, name) is False


@pytest.mark.parametrize("provider,api_id", API_CASES)
@pytest.mark.parametrize("changes", (
    {"ticker": "000660"},
    {"observation_date": "2026-10-27"},
    {"content_sha256": "b" * 64},
))
def test_mismatched_record_rejected(provider, api_id, changes):
    with pytest.raises(AcquisitionEvidenceRejected):
        assess_acquisition_record(
            evidence(provider), record(provider, api_id, **changes)
        )


@pytest.mark.parametrize("provider,api_id", (
    ("KIS", "ka10081"),
    ("KIWOOM", "inquire_daily_price"),
    ("KIS", ""),
    ("KIWOOM", "unknown"),
))
def test_invalid_provider_api_pair_rejected(provider, api_id):
    with pytest.raises(AcquisitionEvidenceRejected):
        assess_acquisition_record(
            evidence(provider), record(provider, api_id)
        )


@pytest.mark.parametrize("bad", (None, "", " ", 123, True))
def test_invalid_record_identifier_rejected(bad):
    with pytest.raises(AcquisitionEvidenceRejected):
        assess_acquisition_record(
            evidence("KIS"),
            record("KIS", "inquire_daily_price", acquisition_record_id=bad),
        )


def test_provider_mismatch_rejected():
    with pytest.raises(AcquisitionEvidenceRejected):
        assess_acquisition_record(
            evidence("KIS"), record("KIWOOM", "ka10081")
        )


def test_invalid_record_type_rejected():
    with pytest.raises(AcquisitionEvidenceRejected):
        assess_acquisition_record(evidence("KIS"), object())


def test_invalid_evidence_type_rejected():
    with pytest.raises(AcquisitionEvidenceRejected):
        assess_acquisition_record(object(), record("KIS", "inquire_daily_price"))


def test_invalid_evidence_shape_rejected():
    bad = ProviderEvidence(
        provider="KIS",
        ticker="005930",
        observation_date="2026-10-28",
        acquired_at="not-a-timestamp",
        source_locator="synthetic",
        content_sha256="a" * 64,
    )
    with pytest.raises(AcquisitionEvidenceRejected):
        assess_acquisition_record(bad, record("KIS", "inquire_daily_price"))


def test_result_immutable():
    result = assess_acquisition_record(
        evidence("KIS"), record("KIS", "inquire_daily_price")
    )
    with pytest.raises(FrozenInstanceError):
        result.analysis_authorized = True
