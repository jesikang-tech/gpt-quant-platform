"""Offline NAVER rebuild adapter with explicit synthetic-only boundary.

No network, database, filesystem access, or persistence authorization.
"""

from dataclasses import dataclass, field
from decimal import Decimal

from core.naver_decimal_price_pipeline import prepare_naver_price_rows
from core.naver_http_response_validation import validate_naver_http_response
from core.naver_raw_observation import NaverRawObservation
from core.naver_source_evidence import (
    NaverSourceEvidence,
    ObservationIdentity,
    assess_naver_source_evidence,
)
from price_rebuild_preflight import RebuildPreflight


@dataclass(frozen=True)
class SyntheticRebuildRows:
    ticker: str
    price_row: tuple
    ohlcv_row: tuple
    verification_status: str = "SYNTHETIC_ONLY"
    persistence_authorized: bool = False


def prepare_synthetic_rebuild_rows(
    ticker,
    observation_date,
    values,
    *,
    adjustment,
    synthetic_fixture,
):
    """Prepare matching PRICE/OHLCV rows for declared synthetic data only."""

    if synthetic_fixture is not True:
        raise ValueError("Explicit synthetic fixture declaration required")

    if adjustment not in ("ADJUSTED", "UNADJUSTED"):
        raise ValueError("Explicit synthetic adjustment required")

    price_row, ohlcv_row = prepare_naver_price_rows(
        ticker,
        observation_date,
        values,
        adjustment=adjustment,
    )

    if price_row[0] != ohlcv_row[0]:
        raise ValueError("PRICE/OHLCV ticker mismatch")

    if price_row[1] != ohlcv_row[1]:
        raise ValueError("PRICE/OHLCV date mismatch")

    if type(price_row[2]) is not Decimal:
        raise ValueError("Decimal close required")

    if price_row[2] != ohlcv_row[5]:
        raise ValueError("PRICE/OHLCV close mismatch")

    return SyntheticRebuildRows(
        ticker=ticker,
        price_row=price_row,
        ohlcv_row=ohlcv_row,
    )


@dataclass(frozen=True)
class BoundSyntheticRebuildRows:
    rows: SyntheticRebuildRows
    evidence: NaverSourceEvidence
    adjustment: str
    revision_id: str | None
    verification_status: str = field(default="SYNTHETIC_ONLY", init=False)
    provenance_verified: bool = field(default=False, init=False)
    analysis_authorized: bool = field(default=False, init=False)
    persistence_authorized: bool = field(default=False, init=False)
    rebuild_authorized: bool = field(default=False, init=False)
    execution_authorized: bool = field(default=False, init=False)

    @property
    def observation(self):
        return self.evidence.observation

    @property
    def source_sha256(self):
        return self.observation.content_sha256

    @property
    def provider(self):
        return self.evidence.claimed_provider.name

    def __post_init__(self):
        if type(self.rows) is not SyntheticRebuildRows:
            raise ValueError("SyntheticRebuildRows required")
        if (self.rows.verification_status != "SYNTHETIC_ONLY"
                or self.rows.persistence_authorized is not False):
            raise ValueError("Nested row authority escalation prohibited")
        if type(self.evidence) is not NaverSourceEvidence:
            raise ValueError("NaverSourceEvidence required")
        if type(self.observation) is not ObservationIdentity:
            raise ValueError("ObservationIdentity required")
        if self.adjustment not in ("ADJUSTED", "UNADJUSTED"):
            raise ValueError("Explicit synthetic adjustment required")
        if self.revision_id is not None and (
            type(self.revision_id) is not str or not self.revision_id
            or self.revision_id != self.revision_id.strip()
        ):
            raise ValueError("Invalid revision identifier")
        price, ohlcv = self.rows.price_row, self.rows.ohlcv_row
        if type(price) is not tuple or len(price) != 3 or type(ohlcv) is not tuple or len(ohlcv) != 7:
            raise ValueError("Invalid prepared pair shape")
        identity = (self.observation.ticker, self.observation.observation_date)
        if self.rows.ticker != identity[0] or price[:2] != identity or ohlcv[:2] != identity:
            raise ValueError("Prepared pair observation identity mismatch")
        if type(price[2]) is not Decimal or type(ohlcv[5]) is not Decimal or price[2] != ohlcv[5]:
            raise ValueError("Prepared pair Decimal close mismatch")


def prepare_bound_synthetic_rebuild_rows(
    raw_response,
    evidence,
    *,
    expected_observation,
    adjustment,
    revision_id=None,
    synthetic_fixture,
):
    """Bind synthetic rows to supplied response bytes, not authenticated trust.

    The hash covers original response bytes; ticker/date selects one row from
    that response. Adjustment and revision remain declarations. In particular,
    the raw observation's UNKNOWN basis is never promoted to verified evidence.
    No acquisition, filesystem/database access, or authorization is performed.
    """
    if synthetic_fixture is not True:
        raise ValueError("Explicit synthetic fixture declaration required")
    assess_naver_source_evidence(evidence)
    if evidence.caller_claims_verified is not False:
        raise ValueError("Caller verification claim cannot grant provenance")
    if type(expected_observation) is not ObservationIdentity:
        raise ValueError("Expected ObservationIdentity required")
    if expected_observation != evidence.observation:
        raise ValueError("Evidence observation identity mismatch")
    if evidence.claimed_provider.name != "NAVER":
        raise ValueError("NAVER provider declaration required")
    if type(adjustment) is not str or adjustment not in ("ADJUSTED", "UNADJUSTED"):
        raise ValueError("Explicit synthetic adjustment required")
    if revision_id is not None and (
        type(revision_id) is not str or not revision_id or revision_id != revision_id.strip()
    ):
        raise ValueError("Invalid revision identifier")

    observations = validate_naver_http_response(
        raw_response, expected_observation.content_sha256, expected_observation.ticker,
    )
    matches = tuple(item for item in observations if (
        item.ticker == expected_observation.ticker
        and item.observation_date == expected_observation.observation_date
    ))
    if len(matches) != 1:
        raise ValueError("Exactly one matching observation required")
    selected = matches[0]
    if type(selected) is not NaverRawObservation:
        raise ValueError("Special observation cannot prepare numeric pairs")
    values = dict(zip(("Open", "High", "Low", "Close", "Volume"), selected.values))
    rows = prepare_synthetic_rebuild_rows(
        selected.ticker, selected.observation_date, values,
        adjustment=adjustment, synthetic_fixture=synthetic_fixture,
    )
    return BoundSyntheticRebuildRows(rows, evidence, adjustment, revision_id)


def reject_unverified_rebuild(preflight):
    """Never convert unverified real observations into database rows."""

    if type(preflight) is not RebuildPreflight:
        raise ValueError("RebuildPreflight required")

    if (
        preflight.verification_status != "UNVERIFIED"
        or preflight.persistence_authorized is not False
    ):
        raise ValueError("Invalid preflight authority state")

    raise ValueError(
        "UNVERIFIED_NAVER_REBUILD_DENIED: "
        "trusted provenance and adjustment basis are required"
    )

def prepare_real_rebuild_rows(preflight):
    """Fail closed for real NAVER observations until trust is verified."""

    reject_unverified_rebuild(preflight)
