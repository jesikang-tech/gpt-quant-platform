import pytest

from current_analysis import _get_period_config


def test_get_period_config_1m():
    config = _get_period_config("1m")

    assert config["lookback_trading_days"] == 20
    assert config["return_threshold"] == 5.0


def test_get_period_config_2m():
    config = _get_period_config("2m")

    assert config["lookback_trading_days"] == 40
    assert config["return_threshold"] == 10.0


def test_get_period_config_3m():
    config = _get_period_config("3m")

    assert config["lookback_trading_days"] == 60
    assert config["return_threshold"] == 15.0


@pytest.mark.parametrize("period", ["6m", "12m", "invalid"])
def test_get_period_config_rejects_unsupported_period(period):
    with pytest.raises(ValueError, match="Invalid period"):
        _get_period_config(period)


def test_get_period_config_returns_expected_keys():
    config = _get_period_config("3m")

    assert set(config.keys()) == {
        "lookback_trading_days",
        "return_threshold",
    }
