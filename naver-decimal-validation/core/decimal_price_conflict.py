"""Pure Decimal-based price comparison contract.

No database, filesystem, network, or broker operations.
"""

from dataclasses import dataclass
from decimal import Decimal, InvalidOperation


class DecimalPriceConflictRejected(ValueError):
    pass


@dataclass(frozen=True)
class PriceEvidence:
    provider: str
    adjustment: str


@dataclass(frozen=True)
class DecimalPriceDecision:
    status: str
    existing_close: Decimal | None
    incoming_close: Decimal
    difference: Decimal | None


def _price(value, field):
    if isinstance(value, bool):
        raise DecimalPriceConflictRejected(f"Invalid {field}")

    if isinstance(value, float):
        raise DecimalPriceConflictRejected(
            f"Float not accepted for {field}"
        )

    if not isinstance(value, (Decimal, int, str)):
        raise DecimalPriceConflictRejected(f"Invalid {field}")

    try:
        result = Decimal(value)
    except (InvalidOperation, ValueError, TypeError, OverflowError) as exc:
        raise DecimalPriceConflictRejected(f"Invalid {field}") from exc

    if not result.is_finite() or result <= 0:
        raise DecimalPriceConflictRejected(f"Invalid {field}")

    return result


def _evidence(value, field):
    if not isinstance(value, PriceEvidence):
        raise DecimalPriceConflictRejected(
            f"Missing {field} evidence"
        )

    if (
        not isinstance(value.provider, str)
        or not value.provider
        or value.provider != value.provider.strip()
    ):
        raise DecimalPriceConflictRejected(
            f"Invalid {field} provider"
        )

    if (
        not isinstance(value.adjustment, str)
        or value.adjustment not in ("ADJUSTED", "UNADJUSTED")
    ):
        raise DecimalPriceConflictRejected(
            f"Invalid {field} adjustment"
        )

    return value


def classify_decimal_price(
    existing_close,
    incoming_close,
    *,
    existing_evidence,
    incoming_evidence,
):
    incoming = _price(incoming_close, "incoming close")
    new_evidence = _evidence(incoming_evidence, "incoming")

    if existing_close is None:
        if existing_evidence is not None:
            raise DecimalPriceConflictRejected(
                "Unexpected existing evidence"
            )

        return DecimalPriceDecision(
            status="NEW",
            existing_close=None,
            incoming_close=incoming,
            difference=None,
        )

    existing = _price(existing_close, "existing close")
    old_evidence = _evidence(existing_evidence, "existing")

    if old_evidence != new_evidence:
        raise DecimalPriceConflictRejected(
            "Price source evidence mismatch"
        )

    return DecimalPriceDecision(
        status="MATCH" if existing == incoming else "CONFLICT",
        existing_close=existing,
        incoming_close=incoming,
        difference=incoming - existing,
    )