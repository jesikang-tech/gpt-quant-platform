"""Offline common entry point for documented daily response rows.

No network, broker, database, provenance certification, or authority grant.
"""

from .provider_contract import ProviderObservationRejected
from .kis_daily_response import prepare_kis_daily_observation
from .kiwoom_daily_response import prepare_kiwoom_daily_observation


def prepare_provider_daily_observation(
    provider, ticker, response_row, api_id=None
):
    """Delegate to an existing provider-specific daily row adapter."""
    if type(provider) is not str:
        raise ProviderObservationRejected("Invalid provider")

    if provider == "KIS":
        if api_id is not None:
            raise ProviderObservationRejected("KIS does not accept api_id")
        return prepare_kis_daily_observation(ticker, response_row)

    if provider == "KIWOOM":
        if type(api_id) is not str:
            raise ProviderObservationRejected("Kiwoom api_id required")
        return prepare_kiwoom_daily_observation(
            api_id, ticker, response_row
        )

    raise ProviderObservationRejected("Unsupported provider")
