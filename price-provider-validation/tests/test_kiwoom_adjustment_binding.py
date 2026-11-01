"""Offline tests for Kiwoom adjustment-request and raw JSON binding."""
from dataclasses import FrozenInstanceError, replace
from hashlib import sha256
import json

import pytest

from price_provider_validation.kiwoom_adjustment_binding import (
    KiwoomAdjustmentBindingDecision,
    assess_kiwoom_adjustment_raw_binding,
)
from price_provider_validation.provider_contract import (
    ProviderObservationRejected,
)
from price_provider_validation.provider_evidence import (
    ProviderEvidence,
    ProviderEvidenceRejected,
)


def _raw_body():
    response = {
        "stk_dt_pole_chart_qry": [
            {
                "dt": "20261030",
                "open_pric": "+100",
                "high_pric": "+110",
                "low_pric": "+90",
                "cur_prc": "+105",
                "trde_qty": "1000",
            }
        ]
    }
    return json.dumps(response).encode("utf-8")


def _evidence(body, **changes):
    values = {
        "provider": "KIWOOM",
        "ticker": "005930",
        "observation_date": "2026-10-30",
        "acquired_at": "2026-10-31T09:00:00+09:00",
        "source_locator": "synthetic-offline",
        "content_sha256": sha256(body).hexdigest(),
        "adjustment": "UNKNOWN",
    }
    values.update(changes)
    return ProviderEvidence(**values)


def _assess(value="0", **changes):
    body = _raw_body()
    values = {
        "api_id": "ka10081",
        "ticker": "005930",
        "parameter": "upd_stkpc_tp",
        "value": value,
        "raw_response": body,
        "evidence": _evidence(body),
        "requested_base_date": "2026-10-30",
        "observation_date": "2026-10-30",
    }
    values.update(changes)
    return assess_kiwoom_adjustment_raw_binding(**values)


@pytest.mark.parametrize(
    "value,expected_policy",
    [
        ("0", "UNADJUSTED"),
        ("1", "ADJUSTED"),
    ],
)
def test_valid_request_policy_never_certifies_response(value, expected_policy):
    decision = _assess(value)
    assert decision.api_id == "ka10081"
    assert decision.ticker == "005930"
    assert decision.observation_date == "2026-10-30"
    assert decision.requested_policy == expected_policy
    assert decision.response_adjustment == "UNKNOWN"
    assert decision.status == "DENIED"
    assert decision.independently_verified is False
    assert decision.analysis_authorized is False
    assert decision.persistence_authorized is False
    assert decision.database_rebuild_authorized is False


@pytest.mark.parametrize(
    "changes",
    [
        {"api_id": "ka10086"},
        {"api_id": "invalid"},
        {"parameter": "FID_ORG_ADJ_PRC"},
        {"parameter": "invalid"},
        {"value": "2"},
        {"value": ""},
        {"value": 0},
    ],
)
def test_unsupported_request_rejected(changes):
    with pytest.raises(ProviderObservationRejected):
        _assess(**changes)


def test_evidence_ticker_mismatch_rejected():
    body = _raw_body()
    with pytest.raises(ProviderEvidenceRejected, match="Ticker mismatch"):
        _assess(evidence=_evidence(body, ticker="000660"))


def test_evidence_date_mismatch_rejected():
    body = _raw_body()
    with pytest.raises(ProviderEvidenceRejected, match="Observation date mismatch"):
        _assess(evidence=_evidence(body, observation_date="2026-10-29"))


def test_modified_raw_response_rejected():
    body = _raw_body()
    changed = body.replace(b"+105", b"+106")
    with pytest.raises(ProviderEvidenceRejected, match="SHA256 mismatch"):
        _assess(raw_response=changed, evidence=_evidence(body))


@pytest.mark.parametrize("adjustment", ["ADJUSTED", "UNADJUSTED"])
def test_evidence_adjustment_claim_does_not_certify_response(adjustment):
    body = _raw_body()
    decision = _assess(
        "1",
        evidence=_evidence(body, adjustment=adjustment),
    )
    assert decision.response_adjustment == "UNKNOWN"
    assert decision.independently_verified is False
    assert decision.analysis_authorized is False


def test_decision_authority_fields_cannot_be_modified():
    decision = _assess("1")
    with pytest.raises(FrozenInstanceError):
        decision.analysis_authorized = True


def test_direct_decision_construction_remains_denied():
    decision = KiwoomAdjustmentBindingDecision(
        api_id="ka10081",
        ticker="005930",
        observation_date="2026-10-30",
        requested_policy="ADJUSTED",
    )
    assert decision.status == "DENIED"
    assert decision.response_adjustment == "UNKNOWN"
    assert decision.independently_verified is False
    assert decision.analysis_authorized is False
    assert decision.persistence_authorized is False
    assert decision.database_rebuild_authorized is False
