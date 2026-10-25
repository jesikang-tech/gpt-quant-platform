"""Fail-closed tests for the new NAVER persistence entry."""

import pytest

from core.price_provenance_gate import PriceProvenanceRejected
from core.naver_persistence_entry import persist_naver_observation


@pytest.mark.parametrize("observation", [
    None,
    object(),
    {"provider": "NAVER", "persistence_authorized": True},
])
def test_naver_entry_rejects_before_adapter(observation):
    calls = []

    def forbidden_adapter(value):
        calls.append(value)
        raise AssertionError("Persistence adapter must not execute")

    with pytest.raises(PriceProvenanceRejected):
        persist_naver_observation(observation, forbidden_adapter)

    assert calls == []


@pytest.mark.parametrize("adapter", [None, object(), "write"])
def test_naver_entry_rejects_invalid_adapter(adapter):
    with pytest.raises(PriceProvenanceRejected):
        persist_naver_observation(object(), adapter)


def test_naver_entry_rejects_forged_approval_object():
    class ForgedObservation:
        provider = "NAVER"
        provenance_verified = True
        persistence_authorized = True

    calls = []

    def forbidden_adapter(value):
        calls.append(value)

    with pytest.raises(PriceProvenanceRejected):
        persist_naver_observation(ForgedObservation(), forbidden_adapter)

    assert calls == []
