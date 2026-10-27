"""KIWOOM raw observation adapter scaffold.

No network, authentication, account, or price collection.
"""
from .provider_contract import prepare_raw_observation


def prepare_kiwoom_observation(ticker, observation_date, raw_fields):
    return prepare_raw_observation(
        "KIWOOM", ticker, observation_date, raw_fields
    )
