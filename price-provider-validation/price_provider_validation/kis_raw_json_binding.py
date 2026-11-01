"""Offline KIS raw JSON observation/evidence binding.

Caller-supplied bytes only. No HTTP, broker, DB, or filesystem I/O.
Structural/digest consistency never establishes provenance or authorization.
"""
import json

from .kis_daily_response import (
    kis_daily_array_field,
    prepare_kis_daily_observation,
)
from .provider_contract import ProviderObservationRejected
from .provider_evidence import assess_raw_bytes_evidence_binding


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


def bind_kis_raw_json_observation(
    ticker,
    raw_response,
    evidence,
    *,
    observation_date,
):
    """Select one KIS output2 row and verify supplied-byte digest binding."""
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

    if type(response) is not dict:
        raise ProviderObservationRejected("Invalid KIS response container")

    rows = response.get(kis_daily_array_field())
    if type(rows) is not list or not rows:
        raise ProviderObservationRejected("Invalid KIS daily array")

    if type(observation_date) is not str:
        raise ProviderObservationRejected("Invalid selected observation date")

    observations = [
        prepare_kis_daily_observation(ticker, row)
        for row in rows
    ]

    selected = [
        observation for observation in observations
        if observation.observation_date == observation_date
    ]

    if len(selected) != 1:
        raise ProviderObservationRejected("Selected observation not unique")

    decision = assess_raw_bytes_evidence_binding(
        selected[0], evidence, raw_response
    )

    if (
        decision.status != "DENIED"
        or decision.independently_verified is not False
        or decision.analysis_authorized is not False
        or decision.persistence_authorized is not False
    ):
        raise ProviderObservationRejected("Evidence authority escalation")

    return selected[0], decision
