"""Explicit OHLCV field mapping for untrusted provider observations.

Pure data transformation. No provider certification or I/O.
"""

from dataclasses import dataclass

from .provider_contract import (
    RawPriceObservation,
    ProviderObservationRejected,
)


@dataclass(frozen=True)
class OhlcvFieldMapping:
    open_index: int
    high_index: int
    low_index: int
    close_index: int
    volume_index: int


def map_raw_ohlcv(observation, mapping):
    if type(observation) is not RawPriceObservation:
        raise ProviderObservationRejected("Invalid observation")

    if type(mapping) is not OhlcvFieldMapping:
        raise ProviderObservationRejected("Invalid OHLCV mapping")

    indices = (
        mapping.open_index,
        mapping.high_index,
        mapping.low_index,
        mapping.close_index,
        mapping.volume_index,
    )

    if any(type(index) is not int for index in indices):
        raise ProviderObservationRejected("Mapping indices must be integers")

    if set(indices) != set(range(5)):
        raise ProviderObservationRejected(
            "OHLCV mapping must be a permutation of five indices"
        )

    if type(observation.raw_fields) is not tuple:
        raise ProviderObservationRejected("Invalid raw fields")

    if len(observation.raw_fields) != 5:
        raise ProviderObservationRejected("Invalid raw field count")

    return {
        "Open": observation.raw_fields[mapping.open_index],
        "High": observation.raw_fields[mapping.high_index],
        "Low": observation.raw_fields[mapping.low_index],
        "Close": observation.raw_fields[mapping.close_index],
        "Volume": observation.raw_fields[mapping.volume_index],
    }
