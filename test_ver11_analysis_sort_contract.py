import pytest

import current_analysis


@pytest.mark.parametrize(
    "sort_by,expected_ticker",
    [
        ("final_score", "FINAL"),
        ("return", "RETURN"),
        ("trend_score", "TREND"),
        ("slope_score", "SLOPE"),
    ],
)
def test_ver11_sort_is_applied_before_limit(monkeypatch, sort_by, expected_ticker):
    tickers = ["FINAL", "RETURN", "TREND", "SLOPE"]

    score_map = {
        "FINAL": (80.0, 70.0, 70.0),
        "RETURN": (100.0, 0.0, 0.0),
        "TREND": (0.0, 100.0, 0.0),
        "SLOPE": (0.0, 0.0, 100.0),
    }

    active_ticker = {"value": None}

    monkeypatch.setattr(
        current_analysis,
        "_normalize_analysis_date",
        lambda analysis_date: "2026-09-04",
    )
    monkeypatch.setattr(
        current_analysis,
        "_get_period_config",
        lambda period: {
            "lookback_trading_days": 2,
            "return_threshold": -999.0,
        },
    )
    monkeypatch.setattr(
        current_analysis,
        "get_all_etf_tickers",
        lambda: tickers,
    )
    monkeypatch.setattr(
        current_analysis,
        "_get_etf_name_map",
        lambda: {ticker: ticker for ticker in tickers},
    )

    def fake_get_etf_prices(ticker, analysis_date):
        active_ticker["value"] = ticker
        return [
            ("2026-09-03", 100.0),
            ("2026-09-04", 101.0),
        ]

    monkeypatch.setattr(
        current_analysis,
        "get_etf_prices",
        fake_get_etf_prices,
    )
    monkeypatch.setattr(
        current_analysis,
        "calculate_return",
        lambda first, last: {
            "FINAL": 10.0,
            "RETURN": 100.0,
            "TREND": 20.0,
            "SLOPE": 30.0,
        }[active_ticker["value"]],
    )
    monkeypatch.setattr(
        current_analysis,
        "calculate_return_score",
        lambda value: score_map[active_ticker["value"]][0],
    )
    monkeypatch.setattr(
        current_analysis,
        "calculate_trend_score",
        lambda prices: score_map[active_ticker["value"]][1],
    )
    monkeypatch.setattr(
        current_analysis,
        "calculate_slope_score",
        lambda prices: score_map[active_ticker["value"]][2],
    )
    monkeypatch.setattr(
        current_analysis,
        "calculate_uptrend_ratio",
        lambda prices: 100.0,
    )
    monkeypatch.setattr(
        current_analysis,
        "_get_future_performance",
        lambda ticker, analysis_date: (None, None, None),
    )
    monkeypatch.setattr(
        current_analysis,
        "_get_reality_test",
        lambda ticker, analysis_date, period: {},
    )

    result = current_analysis.get_current_analysis_data(
        limit=1,
        analysis_date="2026-09-04",
        period="1m",
        sort_by=sort_by,
    )

    assert result["current_score_top"][0]["ticker"] == expected_ticker


def test_ver11_sort_evidence_ui_contract():
    from pathlib import Path

    source = Path("static/dashboard.js").read_text(encoding="utf-8")

    assert 'trend_score: "\\uCD94\\uC138 \\uC810\\uC218"' in source
    assert 'slope_score: "\\uAE30\\uC6B8\\uAE30 \\uC810\\uC218"' in source
    assert '`\\uC815\\uB82C: ${sortLabel} \\u2193`' in source

    assert 'sortBy === "trend_score" || sortBy === "slope_score"' in source
    assert "Number(item[sortBy])" in source

    assert (
        'sortBy === "trend_score"'
        in source
    )
    assert (
        '? `<th scope="col">\\uCD94\\uC138 \\uC810\\uC218</th>`'
        in source
    )
    assert (
        'sortBy === "slope_score"'
        in source
    )
    assert (
        '? `<th scope="col">\\uAE30\\uC6B8\\uAE30 \\uC810\\uC218</th>`'
        in source
    )


def test_ver11_default_sort_preserves_legacy_return_score_tiebreak(monkeypatch):
    tickers = ["HIGH_RETURN", "HIGH_RETURN_SCORE"]
    active_ticker = {"value": None}

    monkeypatch.setattr(
        current_analysis,
        "_normalize_analysis_date",
        lambda analysis_date: "2026-09-04",
    )
    monkeypatch.setattr(
        current_analysis,
        "_get_period_config",
        lambda period: {
            "lookback_trading_days": 2,
            "return_threshold": -999.0,
        },
    )
    monkeypatch.setattr(
        current_analysis,
        "get_all_etf_tickers",
        lambda: tickers,
    )
    monkeypatch.setattr(
        current_analysis,
        "_get_etf_name_map",
        lambda: {ticker: ticker for ticker in tickers},
    )

    def fake_get_etf_prices(ticker, analysis_date):
        active_ticker["value"] = ticker
        return [
            ("2026-09-03", 100.0),
            ("2026-09-04", 101.0),
        ]

    monkeypatch.setattr(
        current_analysis,
        "get_etf_prices",
        fake_get_etf_prices,
    )
    monkeypatch.setattr(
        current_analysis,
        "calculate_return",
        lambda first, last: {
            "HIGH_RETURN": 100.0,
            "HIGH_RETURN_SCORE": 10.0,
        }[active_ticker["value"]],
    )
    monkeypatch.setattr(
        current_analysis,
        "calculate_return_score",
        lambda value: {
            "HIGH_RETURN": 50.0,
            "HIGH_RETURN_SCORE": 80.0,
        }[active_ticker["value"]],
    )
    monkeypatch.setattr(
        current_analysis,
        "calculate_trend_score",
        lambda prices: {
            "HIGH_RETURN": 80.0,
            "HIGH_RETURN_SCORE": 60.0,
        }[active_ticker["value"]],
    )
    monkeypatch.setattr(
        current_analysis,
        "calculate_slope_score",
        lambda prices: {
            "HIGH_RETURN": 80.0,
            "HIGH_RETURN_SCORE": 60.0,
        }[active_ticker["value"]],
    )
    monkeypatch.setattr(
        current_analysis,
        "calculate_uptrend_ratio",
        lambda prices: 100.0,
    )
    monkeypatch.setattr(
        current_analysis,
        "_get_future_performance",
        lambda ticker, analysis_date: (None, None, None),
    )
    monkeypatch.setattr(
        current_analysis,
        "_get_reality_test",
        lambda ticker, analysis_date, period: {},
    )

    result = current_analysis.get_current_analysis_data(
        limit=1,
        analysis_date="2026-09-04",
        period="1m",
        sort_by="final_score",
    )

    assert (
        result["current_score_top"][0]["ticker"]
        == "HIGH_RETURN_SCORE"
    )
