"""Synthetic fail-closed KIS adjustment binding tests."""
from dataclasses import FrozenInstanceError
from hashlib import sha256
import json

import pytest

from price_provider_validation.kis_adjustment_binding import (
    KisAdjustmentBindingDecision,
    assess_kis_adjustment_raw_binding,
)
from price_provider_validation.provider_contract import ProviderObservationRejected
from price_provider_validation.provider_evidence import (
    ProviderEvidence,
    ProviderEvidenceRejected,
)


def _raw():
    return json.dumps(
        {"output2": [{
            "stck_bsop_date": "20261028",
            "stck_oprc": "100",
            "stck_hgpr": "110",
            "stck_lwpr": "90",
            "stck_clpr": "105",
            "acml_vol": "1000",
        }]},
        separators=(",", ":"),
    ).encode("utf-8")


def _evidence(raw, **changes):
    values = {
        "provider": "KIS",
        "ticker": "005930",
        "observation_date": "2026-10-28",
        "acquired_at": "2026-10-29T09:00:00+09:00",
        "source_locator": "synthetic:offline-kis",
        "content_sha256": sha256(raw).hexdigest(),
        "adjustment": "UNKNOWN",
    }
    values.update(changes)
    return ProviderEvidence(**values)


def _assess(value="0", **changes):
    raw = _raw()
    values = {
        "api_id": "inquire_daily_itemchartprice",
        "ticker": "005930",
        "parameter": "FID_ORG_ADJ_PRC",
        "value": value,
        "raw_response": raw,
        "evidence": _evidence(raw),
        "observation_date": "2026-10-28",
    }
    values.update(changes)
    return assess_kis_adjustment_raw_binding(**values)


@pytest.mark.parametrize(
    "value,expected",
    [("0", "ADJUSTED"), ("1", "UNADJUSTED")],
)
def test_request_policy_does_not_certify_response(value, expected):
    decision = _assess(value)
    assert decision.api_id == "inquire_daily_itemchartprice"
    assert decision.ticker == "005930"
    assert decision.observation_date == "2026-10-28"
    assert decision.requested_policy == expected
    assert decision.response_adjustment == "UNKNOWN"
    assert decision.corporate_action_verified is False
    assert decision.status == "DENIED"
    assert decision.independently_verified is False
    assert decision.analysis_authorized is False
    assert decision.persistence_authorized is False
    assert decision.database_rebuild_authorized is False


@pytest.mark.parametrize(
    "changes",
    [
        {"api_id": "inquire_daily_price"},
        {"parameter": "invalid"},
        {"value": "2"},
        {"value": 0},
    ],
)
def test_invalid_request_rejected(changes):
    with pytest.raises(ProviderObservationRejected):
        _assess(**changes)


def test_evidence_ticker_mismatch_rejected():
    raw = _raw()
    with pytest.raises(ProviderEvidenceRejected, match="Ticker mismatch"):
        _assess(evidence=_evidence(raw, ticker="000660"))


def test_evidence_date_mismatch_rejected():
    raw = _raw()
    with pytest.raises(ProviderEvidenceRejected, match="Observation date mismatch"):
        _assess(evidence=_evidence(raw, observation_date="2026-10-27"))


def test_modified_raw_response_rejected():
    raw = _raw()
    changed = raw.replace(b'"105"', b'"106"')
    with pytest.raises(ProviderEvidenceRejected, match="SHA256 mismatch"):
        _assess(raw_response=changed, evidence=_evidence(raw))


@pytest.mark.parametrize("adjustment", ["ADJUSTED", "UNADJUSTED"])
def test_unverified_adjustment_claim_rejected(adjustment):
    raw = _raw()
    with pytest.raises(ProviderEvidenceRejected, match="Unverified adjustment claim"):
        _assess(evidence=_evidence(raw, adjustment=adjustment))


def test_decision_is_immutable():
    decision = _assess()
    with pytest.raises(FrozenInstanceError):
        decision.analysis_authorized = True


def test_direct_construction_remains_denied():
    decision = KisAdjustmentBindingDecision(
        api_id="inquire_daily_itemchartprice",
        ticker="005930",
        observation_date="2026-10-28",
        requested_policy="ADJUSTED",
    )
    assert decision.response_adjustment == "UNKNOWN"
    assert decision.corporate_action_verified is False
    assert decision.status == "DENIED"
    assert decision.independently_verified is False
    assert decision.analysis_authorized is False
    assert decision.persistence_authorized is False
    assert decision.database_rebuild_authorized is False
