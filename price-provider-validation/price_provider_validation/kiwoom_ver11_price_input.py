"""Pure KIWOOM daily-response to Ver1.1 close-price adapter.

Caller-supplied responses only. No HTTP, database, broker, or persistence.
This applies the adopted KIWOOM reference convention without claiming
independent market-data certification.
"""

from decimal import Decimal, InvalidOperation

from .kiwoom_adapter import map_kiwoom_ohlcv
from .kiwoom_daily_batch import prepare_kiwoom_daily_batch
from .kiwoom_price_reference_policy import assess_kiwoom_price_reference_policy
from .ohlcv_mapping import OhlcvFieldMapping
from .provider_contract import ProviderObservationRejected


_DAILY_MAPPING = OhlcvFieldMapping(0, 1, 2, 3, 4)


def prepare_kiwoom_ver11_close_prices(
    api_id, ticker, response, *, requested_base_date
):
    """Return ascending (ISO date, positive Decimal close) tuples."""
    policy = assess_kiwoom_price_reference_policy()
    if (
        policy.provider != "KIWOOM"
        or policy.platform_version != "1.1"
        or policy.analysis_authorized is not True
        or policy.dashboard_authorized is not True
        or policy.api_execution_authorized is not False
        or policy.persistence_authorized is not False
    ):
        raise ProviderObservationRejected("KIWOOM_VER11_POLICY_DENIED")

    observations = prepare_kiwoom_daily_batch(
        api_id, ticker, response, requested_base_date=requested_base_date
    )
    prices = []

    for observation in observations:
        mapped = map_kiwoom_ohlcv(observation, _DAILY_MAPPING)
        raw_close = mapped["Close"]
        try:
            close = Decimal(raw_close)
        except (InvalidOperation, ValueError) as exc:
            raise ProviderObservationRejected("Invalid KIWOOM close") from exc

        if not close.is_finite() or close <= 0:
            raise ProviderObservationRejected("Invalid KIWOOM close")

        prices.append((observation.observation_date, close))

    return tuple(sorted(prices, key=lambda row: row[0]))
