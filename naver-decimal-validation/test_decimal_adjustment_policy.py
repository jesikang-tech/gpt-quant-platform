"""Synthetic label/comparison policy; no NAVER semantics or authority implied."""

from decimal import Context, Decimal, Inexact, Rounded, ROUND_HALF_EVEN, localcontext

import pytest

from core.decimal_price_conflict import (
    DecimalPriceConflictRejected,
    PriceEvidence,
    classify_decimal_price,
)
from core.naver_decimal_price_pipeline import prepare_naver_price_rows


@pytest.mark.parametrize("adjustment", ["ADJUSTED", "UNADJUSTED"])
@pytest.mark.parametrize(
    "incoming,status,difference",
    [("100.1250", "MATCH", "0"), ("100.1251", "CONFLICT", "0.0001")],
)
def test_matching_labels_use_exact_decimal_comparison(
    adjustment, incoming, status, difference,
):
    evidence = PriceEvidence("NAVER", adjustment)
    with localcontext(Context(prec=40, rounding=ROUND_HALF_EVEN)):
        result = classify_decimal_price(
            "100.125", incoming,
            existing_evidence=evidence, incoming_evidence=evidence,
        )
    assert result.status == status
    assert result.existing_close == Decimal("100.125")
    assert result.incoming_close == Decimal(incoming)
    assert result.difference == Decimal(difference)


@pytest.mark.parametrize("adjustment", ["ADJUSTED", "UNADJUSTED"])
def test_new_price_requires_no_existing_evidence(adjustment):
    result = classify_decimal_price(
        None, "100.125", existing_evidence=None,
        incoming_evidence=PriceEvidence("NAVER", adjustment),
    )
    assert result.status == "NEW"
    assert result.existing_close is None
    assert result.incoming_close == Decimal("100.125")
    assert result.difference is None


def test_provider_mismatch_rejected_even_when_prices_match():
    with pytest.raises(DecimalPriceConflictRejected, match="Price source evidence mismatch"):
        classify_decimal_price(
            "100", "100",
            existing_evidence=PriceEvidence("SYNTHETIC_OTHER", "ADJUSTED"),
            incoming_evidence=PriceEvidence("NAVER", "ADJUSTED"),
        )


@pytest.mark.parametrize(
    "existing,incoming", [("ADJUSTED", "UNADJUSTED"), ("UNADJUSTED", "ADJUSTED")],
)
def test_adjustment_basis_mismatch_rejected_even_when_prices_match(existing, incoming):
    with pytest.raises(DecimalPriceConflictRejected, match="Price source evidence mismatch"):
        classify_decimal_price(
            "100", "100",
            existing_evidence=PriceEvidence("NAVER", existing),
            incoming_evidence=PriceEvidence("NAVER", incoming),
        )


@pytest.mark.parametrize(
    "precision,expected_difference,rounded",
    [(8, "1.2345679E+29", True),
     (80, "123456789012345678901234567889.123456789", False)],
)
def test_long_operands_preserved_but_difference_obeys_decimal_context(
    precision, expected_difference, rounded,
):
    incoming = Decimal("123456789012345678901234567890.123456789")
    evidence = PriceEvidence("NAVER", "UNADJUSTED")
    with localcontext(Context(prec=precision, rounding=ROUND_HALF_EVEN)) as context:
        context.clear_flags()
        result = classify_decimal_price(
            Decimal("1"), incoming,
            existing_evidence=evidence, incoming_evidence=evidence,
        )
        assert context.flags[Inexact] is rounded
        assert context.flags[Rounded] is rounded
    assert result.status == "CONFLICT"
    assert result.existing_close == Decimal("1")
    assert result.incoming_close.as_tuple() == incoming.as_tuple()
    assert result.difference == Decimal(expected_difference)


def test_changing_only_adjustment_label_does_not_transform_ohlcv():
    values = {
        "Open": "100.125", "High": "110.500", "Low": "90.000",
        "Close": "105.375", "Volume": "1000",
    }
    original = dict(values)
    adjusted = prepare_naver_price_rows(
        "SYNTHETIC", "2026-01-02", values, adjustment="ADJUSTED",
    )
    unadjusted = prepare_naver_price_rows(
        "SYNTHETIC", "2026-01-02", values, adjustment="UNADJUSTED",
    )
    assert adjusted == unadjusted
    assert adjusted[1][2:] == tuple(Decimal(values[key]) for key in (
        "Open", "High", "Low", "Close", "Volume",
    ))
    assert values == original
