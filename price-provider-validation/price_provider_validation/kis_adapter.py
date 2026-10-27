"""KIS raw observation adapter scaffold.

No network, authentication, account, or price collection.
"""
from .provider_contract import prepare_raw_observation


def prepare_kis_observation(ticker, observation_date, raw_fields):
    return prepare_raw_observation(
        "KIS", ticker, observation_date, raw_fields
    )
