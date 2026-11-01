"""Offline daily observation-to-platform assessment bridge.

No API, network, database, persistence, broker, or authority grant.
"""
from .provider_daily_interface import prepare_provider_daily_observation
from .provider_platform_integration import assess_provider_platform_integration


def assess_provider_daily_bridge(
    provider, ticker, response_row, evidence, trading_day_decision, api_id=None
):
    """Reuse existing conversion and fail-closed platform assessment."""
    observation = prepare_provider_daily_observation(
        provider, ticker, response_row, api_id=api_id
    )
    return assess_provider_platform_integration(
        observation, evidence, trading_day_decision
    )
