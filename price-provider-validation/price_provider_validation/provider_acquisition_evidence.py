"""Offline acquisition-record consistency; never provider authentication.

Caller-supplied records are untrusted even when they agree.
No network, broker, database, filesystem I/O, or authority grant.
"""
from dataclasses import dataclass, field

from .provider_evidence import (
    ProviderEvidence,
    ProviderEvidenceRejected,
    assess_provider_evidence,
)


class AcquisitionEvidenceRejected(ValueError):
    pass


@dataclass(frozen=True)
class AcquisitionRecord:
    provider: str
    api_id: str
    ticker: str
    observation_date: str
    content_sha256: str
    acquisition_record_id: str


@dataclass(frozen=True)
class AcquisitionAssessment:
    provider: str
    api_id: str
    reason: str = field(
        default="ACQUISITION_SOURCE_NOT_INDEPENDENTLY_VERIFIED",
        init=False,
    )
    status: str = field(default="DENIED", init=False)
    independently_verified: bool = field(default=False, init=False)
    analysis_authorized: bool = field(default=False, init=False)
    persistence_authorized: bool = field(default=False, init=False)
    live_api_execution_authorized: bool = field(default=False, init=False)
    broker_execution_authorized: bool = field(default=False, init=False)


_API_IDS = {
    "KIS": frozenset((
        "inquire_daily_itemchartprice",
        "inquire_daily_price",
    )),
    "KIWOOM": frozenset(("ka10081", "ka10086")),
}


def assess_acquisition_record(evidence, record):
    """Check declared identity consistency, not external authenticity."""
    if type(evidence) is not ProviderEvidence:
        raise AcquisitionEvidenceRejected("Invalid provider evidence type")
    if type(record) is not AcquisitionRecord:
        raise AcquisitionEvidenceRejected("Invalid acquisition record type")

    try:
        evidence_decision = assess_provider_evidence(evidence)
    except ProviderEvidenceRejected as exc:
        raise AcquisitionEvidenceRejected("Invalid provider evidence") from exc

    if (
        evidence_decision.status != "DENIED"
        or evidence_decision.independently_verified is not False
        or evidence_decision.analysis_authorized is not False
        or evidence_decision.persistence_authorized is not False
    ):
        raise AcquisitionEvidenceRejected("Provider evidence authority escalation")

    if type(record.provider) is not str or record.provider != evidence.provider:
        raise AcquisitionEvidenceRejected("Provider mismatch")

    if type(record.api_id) is not str or record.api_id not in _API_IDS[record.provider]:
        raise AcquisitionEvidenceRejected("Unsupported API identifier")

    for name in ("ticker", "observation_date", "content_sha256"):
        value = getattr(record, name)
        if type(value) is not str or value != getattr(evidence, name):
            raise AcquisitionEvidenceRejected("Acquisition " + name + " mismatch")

    if (
        type(record.acquisition_record_id) is not str
        or not record.acquisition_record_id
        or record.acquisition_record_id != record.acquisition_record_id.strip()
    ):
        raise AcquisitionEvidenceRejected("Invalid acquisition record identifier")

    return AcquisitionAssessment(
        provider=record.provider,
        api_id=record.api_id,
    )
