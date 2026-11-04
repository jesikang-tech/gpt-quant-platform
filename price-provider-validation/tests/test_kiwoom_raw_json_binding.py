"""Synthetic tests for Kiwoom raw JSON observation/evidence binding."""
from dataclasses import replace
from hashlib import sha256
import json

import pytest

from price_provider_validation.kiwoom_raw_json_binding import (
    MAX_RAW_JSON_BYTES,
    bind_kiwoom_raw_json_observation,
)
from price_provider_validation.provider_contract import (
    ProviderObservationRejected,
)
from price_provider_validation.provider_evidence import (
    ProviderEvidence,
    ProviderEvidenceRejected,
)


def _body(api_id="ka10081", day="20261030"):
    row = {
        "open_pric": "+100",
        "high_pric": "+110",
        "low_pric": "+90",
        "trde_qty": "1000",
    }
    if api_id == "ka10081":
        row["dt"] = day
        row["cur_prc"] = "+105"
        field = "stk_dt_pole_chart_qry"
    else:
        row["date"] = day
        row["close_pric"] = "+105"
        field = "daly_stkpc"
    return json.dumps({field: [row]}).encode("utf-8")


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


def _bind(body, evidence=None, **changes):
    values = {
        "api_id": "ka10081",
        "ticker": "005930",
        "raw_response": body,
        "evidence": _evidence(body) if evidence is None else evidence,
        "requested_base_date": "2026-10-30",
        "observation_date": "2026-10-30",
    }
    values.update(changes)
    return bind_kiwoom_raw_json_observation(**values)


@pytest.mark.parametrize("api_id", ["ka10081", "ka10086"])
def test_valid_raw_json_binding_remains_denied(api_id):
    body = _body(api_id)
    observation, decision = _bind(body, api_id=api_id)

    assert observation.provider == "KIWOOM"
    assert observation.ticker == "005930"
    assert observation.observation_date == "2026-10-30"
    assert observation.adjustment == "UNKNOWN"
    assert decision.status == "DENIED"
    assert decision.independently_verified is False
    assert decision.analysis_authorized is False
    assert decision.persistence_authorized is False


@pytest.mark.parametrize(
    "body",
    [
        b"",
        b"not-json",
        b"\xff",
        b"\xef\xbb\xbf{}",
        b'{"stk_dt_pole_chart_qry":[]}',
        b'{"stk_dt_pole_chart_qry":[],"stk_dt_pole_chart_qry":[]}',
        b'{"stk_dt_pole_chart_qry":[{"dt":"20261030","dt":"20261030"}]}',
        b'{"stk_dt_pole_chart_qry":[NaN]}',
        b'{"stk_dt_pole_chart_qry":[Infinity]}',
    ],
)
def test_invalid_raw_json_rejected(body):
    with pytest.raises(ProviderObservationRejected):
        _bind(body)


@pytest.mark.parametrize("invalid", [None, "text", bytearray(b"{}"), 123])
def test_non_bytes_rejected(invalid):
    with pytest.raises(ProviderObservationRejected):
        _bind(invalid, evidence=_evidence(b"{}"))


def test_oversized_raw_json_rejected():
    with pytest.raises(ProviderObservationRejected):
        _bind(b" " * (MAX_RAW_JSON_BYTES + 1))


def test_selected_date_mismatch_rejected():
    with pytest.raises(ProviderObservationRejected, match="Selected observation not found"):
        _bind(_body(), observation_date="2026-10-29")


def test_evidence_date_mismatch_rejected():
    body = _body()
    with pytest.raises(ProviderEvidenceRejected, match="Observation date mismatch"):
        _bind(body, evidence=_evidence(body, observation_date="2026-10-29"))


def test_evidence_ticker_mismatch_rejected():
    body = _body()
    with pytest.raises(ProviderEvidenceRejected, match="Ticker mismatch"):
        _bind(body, evidence=_evidence(body, ticker="000660"))


def test_modified_raw_body_rejected():
    body = _body()
    evidence = _evidence(body)
    changed = body.replace(b"+105", b"+106")
    with pytest.raises(ProviderEvidenceRejected, match="SHA256 mismatch"):
        _bind(changed, evidence=evidence)


@pytest.mark.parametrize("adjustment", ["ADJUSTED", "UNADJUSTED"])
def test_unverified_adjustment_claim_rejected(adjustment):
    body = _body()
    evidence = replace(_evidence(body), adjustment=adjustment)

    with pytest.raises(ProviderEvidenceRejected, match="Unverified adjustment claim"):
        _bind(body, evidence=evidence)
