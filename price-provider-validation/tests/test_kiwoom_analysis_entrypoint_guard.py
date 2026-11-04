"""Offline KIWOOM platform entrypoint regression tests."""

import inspect

import pytest

from core import price_provenance_gate


def install_denial(monkeypatch):
    calls = []

    def assess(*, provider, adjustment):
        calls.append(("assess", provider, adjustment))
        return object()

    def require(decision):
        calls.append(("require",))
        raise ValueError("KIWOOM_NOT_AUTHORIZED")

    monkeypatch.setattr(
        price_provenance_gate,
        "assess_price_provenance",
        assess,
    )
    monkeypatch.setattr(
        price_provenance_gate,
        "require_analysis_authorization",
        require,
    )
    return calls


def test_current_analysis_denied_before_data_access(monkeypatch):
    import current_analysis

    calls = install_denial(monkeypatch)

    def forbidden(*args, **kwargs):
        raise AssertionError("DATA_ACCESS_MUST_NOT_RUN")

    monkeypatch.setattr(
        current_analysis,
        "_normalize_analysis_date",
        forbidden,
    )

    with pytest.raises(ValueError, match="KIWOOM_NOT_AUTHORIZED"):
        current_analysis.get_current_analysis_data(
            provider="KIWOOM",
        )

    assert calls == [
        ("assess", "KIWOOM", "UNKNOWN"),
        ("require",),
    ]


def test_historical_replay_denied_before_initialization(monkeypatch):
    import historical_replay

    calls = install_denial(monkeypatch)

    def forbidden(*args, **kwargs):
        raise AssertionError("INITIALIZATION_MUST_NOT_RUN")

    monkeypatch.setattr(
        historical_replay.HistoricalReplayEngine,
        "_validate_analysis_date",
        staticmethod(forbidden),
    )

    with pytest.raises(ValueError, match="KIWOOM_NOT_AUTHORIZED"):
        historical_replay.HistoricalReplayEngine(
            "2026-10-30",
            provider="KIWOOM",
        )

    assert calls == [
        ("assess", "KIWOOM", "UNKNOWN"),
        ("require",),
    ]


@pytest.mark.parametrize(
    "provider",
    ["KIS", "NAVER", "", 123, False],
)
def test_current_analysis_rejects_unsupported_provider(provider):
    import current_analysis

    with pytest.raises(
        ValueError,
        match="Unsupported explicit price provider",
    ):
        current_analysis.get_current_analysis_data(
            provider=provider,
        )


@pytest.mark.parametrize(
    "provider",
    ["KIS", "NAVER", "", 123, False],
)
def test_replay_rejects_unsupported_provider(provider):
    import historical_replay

    with pytest.raises(
        ValueError,
        match="Unsupported explicit price provider",
    ):
        historical_replay.HistoricalReplayEngine(
            "2026-10-30",
            provider=provider,
        )


def test_default_provider_parameters_preserved():
    import current_analysis
    import historical_replay

    current_signature = inspect.signature(
        current_analysis.get_current_analysis_data
    )
    replay_signature = inspect.signature(
        historical_replay.HistoricalReplayEngine
    )

    assert current_signature.parameters["provider"].default is None
    assert replay_signature.parameters["provider"].default is None
