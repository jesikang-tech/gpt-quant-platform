"""Synthetic Decimal/float boundary regression tests.

No provider requests, operational database access, or persistence authority.
"""

from decimal import Decimal

import pytest

from core.price_pair_contract import PricePairRejected, prepare_price_pair
from core.decimal_source_integration import prepare_decimal_source_record


def test_legacy_price_pair_rejects_decimal_input():
    with pytest.raises(PricePairRejected):
        prepare_price_pair(
            ticker="005930",
            observation_date="2026-10-01",
            close_price=Decimal("73123.456789"),
        )


def test_decimal_source_record_rejects_unverified_evidence():
    """Unverified NAVER provenance must never authorize a source record."""
    from core.decimal_source_integration import DecimalSourceRejected

    with pytest.raises(DecimalSourceRejected):
        prepare_decimal_source_record(
            ticker="005930",
            observation_date="2026-10-01",
            values={
                "Open": Decimal("73000"),
                "High": Decimal("73500"),
                "Low": Decimal("72900"),
                "Close": Decimal("73123.456789"),
                "Volume": Decimal("100000"),
            },
            provider="NAVER",
            adjustment="UNKNOWN",
        )
