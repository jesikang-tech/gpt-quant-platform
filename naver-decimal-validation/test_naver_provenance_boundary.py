"""Synthetic behavioral checks; run only in the isolated Actions job."""

import pytest

from core.naver_analysis_boundary import assess_naver_analysis_observation
from core.naver_analysis_response import build_naver_analysis_response
from core.naver_decimal_price_pipeline import prepare_naver_analysis_rows
from core.naver_raw_observation import prepare_naver_raw_observation
from core.price_provenance_gate import PriceProvenanceRejected


@pytest.mark.parametrize("adjustment", ["UNKNOWN", "ADJUSTED", "UNADJUSTED"])
def test_analysis_rows_reject_before_consuming_prices(adjustment):
    consumption_attempts = []

    def reject_consumption(operation):
        consumption_attempts.append(operation)
        pytest.fail(f"Unverified prices consumed via {operation}")

    class UnreadablePrices:
        __slots__ = ()

        def __getitem__(self, key):
            reject_consumption("__getitem__")

        def __iter__(self):
            reject_consumption("__iter__")

        def __next__(self):
            reject_consumption("__next__")

        def __len__(self):
            reject_consumption("__len__")

        def __getattribute__(self, name):
            reject_consumption(f"attribute:{name}")

        def __contains__(self, item):
            reject_consumption("__contains__")

        def __bool__(self):
            reject_consumption("__bool__")

        def __float__(self):
            reject_consumption("__float__")

        def __int__(self):
            reject_consumption("__int__")

        def __index__(self):
            reject_consumption("__index__")

        def __str__(self):
            reject_consumption("__str__")

        def __repr__(self):
            reject_consumption("__repr__")

    with pytest.raises(RuntimeError, match="UNVERIFIED_ANALYSIS_COMPATIBILITY_DENIED") as error:
        prepare_naver_analysis_rows(
            "069500", "2026-09-16", UnreadablePrices(),
            adjustment=adjustment,
        )
    assert isinstance(error.value.__cause__, PriceProvenanceRejected)
    # Also detect consumption if a consumer catches the sentinel's failure.
    assert consumption_attempts == []


def test_raw_observation_projects_only_blocked_metadata():
    observation = prepare_naver_raw_observation(
        "069500", "20260916|9680|9715|9621|9676|252142",
    )
    response = build_naver_analysis_response(
        assess_naver_analysis_observation(observation),
    )
    assert response == {
        "provider": "NAVER",
        "ticker": "069500",
        "observation_date": "2026-09-16",
        "status": "BLOCKED",
        "reason": "UNVERIFIED_ADJUSTMENT_AND_PROVENANCE",
        "analysis_authorized": False,
        "dashboard_authorized": False,
        "persistence_authorized": False,
    }
