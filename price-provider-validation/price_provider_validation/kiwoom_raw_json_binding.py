"""Offline Kiwoom raw JSON to observation evidence binding.

Only caller-supplied bytes are accepted. No HTTP, broker, DB or filesystem I/O.
Successful structural and digest checks never authenticate provenance or
authorize analysis, persistence, or adjustment classification.
"""
import json

from .kiwoom_daily_batch import prepare_kiwoom_daily_batch
from .provider_contract import ProviderObservationRejected
from .provider_evidence import (
    ProviderEvidenceRejected,
    assess_raw_bytes_evidence_binding,
)


MAX_RAW_JSON_BYTES = 2_000_000


def _unique_pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ProviderObservationRejected("Duplicate JSON key")
        result[key] = value
    return result


def _reject_constant(value):
    raise ProviderObservationRejected("Nonstandard JSON constant")


def bind_kiwoom_raw_json_observation(
    api_id,
    ticker,
    raw_response,
    evidence,
    *,
    requested_base_date,
    observation_date,
):
    """Reparse supplied raw bytes and bind one selected observation.

    This is an offline identity/digest consistency check, not proof that
    a broker delivered the bytes or that market data is certified.
    """
    if (
        type(raw_response) is not bytes
        or not 1 <= len(raw_response) <= MAX_RAW_JSON_BYTES
    ):
        raise ProviderObservationRejected("Invalid raw JSON byte size")

    try:
        text = raw_response.decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        raise ProviderObservationRejected("Invalid UTF-8 JSON") from exc

    if text.startswith("\ufeff"):
        raise ProviderObservationRejected("JSON BOM not permitted")

    try:
        response = json.loads(
            text,
            object_pairs_hook=_unique_pairs,
            parse_constant=_reject_constant,
        )
    except (ValueError, TypeError, RecursionError) as exc:
        raise ProviderObservationRejected("Invalid JSON response") from exc

    observations = prepare_kiwoom_daily_batch(
        api_id,
        ticker,
        response,
        requested_base_date=requested_base_date,
    )

    if type(observation_date) is not str:
        raise ProviderObservationRejected("Invalid selected observation date")

    selected = [
        row for row in observations
        if row.observation_date == observation_date
    ]

    if len(selected) != 1:
        raise ProviderObservationRejected("Selected observation not found")

    try:
        decision = assess_raw_bytes_evidence_binding(
            selected[0], evidence, raw_response
        )
    except ProviderEvidenceRejected:
        raise

    if (
        decision.status != "DENIED"
        or decision.independently_verified is not False
        or decision.analysis_authorized is not False
        or decision.persistence_authorized is not False
    ):
        raise ProviderObservationRejected("Evidence authority escalation")

    return selected[0], decision
