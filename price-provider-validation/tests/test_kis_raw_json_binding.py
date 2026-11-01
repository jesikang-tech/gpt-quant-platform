"""Synthetic fail-closed tests for offline KIS raw JSON binding."""
from dataclasses import replace
from hashlib import sha256
import json

import pytest

from price_provider_validation.kis_raw_json_binding import (
    MAX_RAW_JSON_BYTES,
    bind_kis_raw_json_observation,
)
from price_provider_validation.provider_contract import ProviderObservationRejected
from price_provider_validation.provider_evidence import (
    ProviderEvidence,
    ProviderEvidenceRejected,
)


def _row(date="20261028"):
    return {
        "stck_bsop_date": date,
        "stck_oprc": "100",
        "stck_hgpr": "110",
        "stck_lwpr": "90",
        "stck_clpr": "105",
        "acml_vol": "1000",
    }


def _raw(rows=None):
    return json.dumps(
        {"output2": [_row()] if rows is None else rows},
        separators=(",", ":"),
    ).encode("utf-8")


def _evidence(raw, **changes):
    evidence = ProviderEvidence(
        provider="KIS",
        ticker="005930",
        observation_date="2026-10-28",
        acquired_at="2026-10-29T09:00:00+09:00",
        source_locator="synthetic:offline-kis",
        content_sha256=sha256(raw).hexdigest(),
    )
    return replace(evidence, **changes)


def _bind(raw, evidence=None, **kwargs):
    return bind_kis_raw_json_observation(
        "005930",
        raw,
        _evidence(raw) if evidence is None else evidence,
        observation_date=kwargs.get("observation_date", "2026-10-28"),
    )


def test_selected_row_preserved_but_never_authorized():
    raw = _raw([_row("20261027"), _row()])
    observation, decision = _bind(raw)

    assert observation.provider == "KIS"
    assert observation.observation_date == "2026-10-28"
    assert observation.raw_fields == ("100", "110", "90", "105", "1000")
    assert observation.adjustment == "UNKNOWN"
    assert decision.status == "DENIED"
    assert decision.independently_verified is False
    assert decision.analysis_authorized is False
    assert decision.persistence_authorized is False


@pytest.mark.parametrize(
    "raw",
    [
        b"",
        b"\xff",
        b"\xef\xbb\xbf{}",
        b'{"output2":[]}',
        b'{"output2":{}}',
        b'{"output2":null}',
        b'{"output2":[{}]}',
        b'{"output2":[{"stck_bsop_date":"20261028"}]}',
        b'{"output2":[],"output2":[]}',
        b'{"output2":[NaN]}',
        b"[]",
        b"null",
        "not-bytes",
        b"x" * (MAX_RAW_JSON_BYTES + 1),
    ],
)
def test_invalid_raw_response_rejected(raw):
    with pytest.raises(ProviderObservationRejected):
        _bind(raw)


def test_duplicate_selected_date_rejected():
    raw = _raw([_row(), _row()])
    with pytest.raises(ProviderObservationRejected):
        _bind(raw)


def test_missing_selected_date_rejected():
    raw = _raw([_row("20261027")])
    with pytest.raises(ProviderObservationRejected):
        _bind(raw)


@pytest.mark.parametrize(
    "changes",
    [
        {"provider": "KIWOOM"},
        {"ticker": "000660"},
        {"observation_date": "2026-10-27"},
        {"adjustment": "ADJUSTED"},
        {"content_sha256": "0" * 64},
    ],
)
def test_evidence_mismatch_rejected(changes):
    raw = _raw()
    with pytest.raises(ProviderEvidenceRejected):
        _bind(raw, _evidence(raw, **changes))


def test_raw_digest_change_rejected():
    original = _raw()
    modified = _raw([dict(_row(), stck_clpr="106")])

    with pytest.raises(ProviderEvidenceRejected):
        _bind(modified, _evidence(original))


def test_invalid_selected_date_type_rejected():
    raw = _raw()
    with pytest.raises(ProviderObservationRejected):
        _bind(raw, observation_date=20261028)


def test_no_implicit_adjustment_or_authorization():
    raw = _raw()
    observation, decision = _bind(raw)

    assert observation.adjustment == "UNKNOWN"
    assert decision.status == "DENIED"
    assert decision.independently_verified is False
