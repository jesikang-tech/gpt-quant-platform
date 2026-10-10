"""Regression tests for disabled development price writes."""

from unittest.mock import patch

import pytest

import price_loader


@pytest.mark.parametrize(
    "function_name",
    [
        "load_price_data",
        "update_price_database",
    ],
)
def test_development_price_write_is_blocked(function_name):
    sample = [
        {
            "ticker": "069500",
            "date": "2026-07-20",
            "close_price": 10000,
        }
    ]

    with (
        patch(
            "price_loader.save_etf_price",
            create=True,
        ) as save_mock,
        patch(
            "price_loader.get_all_price_data",
            create=True,
        ) as read_mock,
    ):
        with pytest.raises(
            RuntimeError,
            match="Development price writes are disabled",
        ):
            getattr(price_loader, function_name)(sample)

        save_mock.assert_not_called()
        read_mock.assert_not_called()


def test_sample_price_data_remains_readable():
    sample = price_loader.get_sample_price_data()

    assert len(sample) == 7
    assert sample[0]["ticker"] == "069500"
    assert sample[0]["close_price"] == 10000
    assert sample[-1]["close_price"] == 11600
