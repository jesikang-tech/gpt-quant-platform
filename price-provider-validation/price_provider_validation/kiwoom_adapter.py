"""KIWOOM raw observation adapter scaffold.

No network, authentication, account, or price collection.
"""
from .provider_contract import prepare_raw_observation


def prepare_kiwoom_observation(ticker, observation_date, raw_fields):
    return prepare_raw_observation(
        "KIWOOM", ticker, observation_date, raw_fields
    )

from .ohlcv_mapping import map_raw_ohlcv
from .provider_contract import ProviderObservationRejected, RawPriceObservation


def map_kiwoom_ohlcv(observation, mapping):
    if type(observation) is not RawPriceObservation or observation.provider != "KIWOOM":
        raise ProviderObservationRejected("Provider mismatch")
    return map_raw_ohlcv(observation, mapping)
