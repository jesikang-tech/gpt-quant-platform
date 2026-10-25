"""Fail-closed entry for new NAVER persistence operations.

This module grants no database or persistence authorization.
"""

from core.price_provenance_gate import invoke_naver_persistence


def persist_naver_observation(observation, persist_adapter):
    """Reject unverified NAVER persistence before invoking an adapter."""
    if not callable(persist_adapter):
        return invoke_naver_persistence(persist_adapter)

    def persist():
        return persist_adapter(observation)

    return invoke_naver_persistence(persist)
