"""Untrusted provider evidence contract. No I/O or authorization."""
from dataclasses import dataclass, field
from datetime import date, datetime
from .provider_contract import SUPPORTED_PROVIDERS


class ProviderEvidenceRejected(ValueError):
    pass


@dataclass(frozen=True)
class ProviderEvidence:
    provider: str
    ticker: str
    observation_date: str
    acquired_at: str
    source_locator: str
    content_sha256: str
    adjustment: str = "UNKNOWN"


@dataclass(frozen=True)
class ProviderEvidenceDecision:
    reason: str
    status: str = field(default="DENIED", init=False)
    independently_verified: bool = field(default=False, init=False)
    analysis_authorized: bool = field(default=False, init=False)
    persistence_authorized: bool = field(default=False, init=False)


def assess_provider_evidence(evidence):
    if type(evidence) is not ProviderEvidence:
        raise ProviderEvidenceRejected("Invalid evidence type")
    if type(evidence.provider) is not str or evidence.provider not in SUPPORTED_PROVIDERS:
        raise ProviderEvidenceRejected("Unsupported provider")
    for name in ("ticker", "observation_date", "acquired_at", "source_locator", "content_sha256"):
        value = getattr(evidence, name)
        if type(value) is not str or not value or value != value.strip():
            raise ProviderEvidenceRejected("Invalid " + name)
    try:
        parsed_date = date.fromisoformat(evidence.observation_date)
    except ValueError as exc:
        raise ProviderEvidenceRejected("Invalid observation date") from exc
    if parsed_date.isoformat() != evidence.observation_date:
        raise ProviderEvidenceRejected("Noncanonical observation date")
    if type(evidence.adjustment) is not str or evidence.adjustment not in ("UNKNOWN", "ADJUSTED", "UNADJUSTED"):
        raise ProviderEvidenceRejected("Invalid adjustment")
    try:
        parsed = datetime.fromisoformat(evidence.acquired_at)
    except ValueError as exc:
        raise ProviderEvidenceRejected("Invalid acquisition timestamp") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ProviderEvidenceRejected("Timezone required")
    digest = evidence.content_sha256
    if len(digest) != 64 or any(c not in "0123456789abcdef" for c in digest):
        raise ProviderEvidenceRejected("Invalid SHA256 format")
    return ProviderEvidenceDecision(reason="INDEPENDENT_PROVIDER_PROVENANCE_NOT_VERIFIED")
