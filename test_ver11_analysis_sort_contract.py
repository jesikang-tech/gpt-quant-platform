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

    assert 'trend_score: getDashboardText("ver11TrendScore")' in source
    assert 'slope_score: getDashboardText("ver11SlopeScore")' in source
    assert '`${getDashboardText("ver11SortLabel")}: ${sortLabel} \\u2193`' in source

    assert 'sortBy === "trend_score" || sortBy === "slope_score"' in source
    assert "Number(item[sortBy])" in source

    assert (
        'sortBy === "trend_score"'
        in source
    )
    assert (
        '? `<th scope="col">${getDashboardText("ver11TrendScore")}</th>`'
        in source
    )
    assert (
        'sortBy === "slope_score"'
        in source
    )
    assert (
        '? `<th scope="col">${getDashboardText("ver11SlopeScore")}</th>`'
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

def test_ver11_market_regime_scores_are_fixed_final_score_top10(monkeypatch):
    tickers = [f"ETF{i:02d}" for i in range(12)]
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
        lambda first, last: float(active_ticker["value"][3:]),
    )
    monkeypatch.setattr(
        current_analysis,
        "calculate_return_score",
        lambda value: 100.0 - value,
    )
    monkeypatch.setattr(
        current_analysis,
        "calculate_trend_score",
        lambda prices: 50.0,
    )
    monkeypatch.setattr(
        current_analysis,
        "calculate_slope_score",
        lambda prices: 50.0,
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
        sort_by="return",
    )

    assert result["current_score_top"][0]["ticker"] == "ETF11"
    assert [row["ticker"] for row in result["market_regime_scores"]] == [
        f"ETF{i:02d}" for i in range(10)
    ]

def test_ver11_market_regime_scores_are_deterministic_across_display_sort(monkeypatch):
    tickers = ["BBB", "AAA", "CCC"]
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
            "AAA": 20.0,
            "BBB": 30.0,
            "CCC": 10.0,
        }[active_ticker["value"]],
    )
    monkeypatch.setattr(
        current_analysis,
        "calculate_return_score",
        lambda value: 100.0,
    )
    monkeypatch.setattr(
        current_analysis,
        "calculate_trend_score",
        lambda prices: 50.0,
    )
    monkeypatch.setattr(
        current_analysis,
        "calculate_slope_score",
        lambda prices: 50.0,
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

    final_score_result = current_analysis.get_current_analysis_data(
        limit=3,
        analysis_date="2026-09-04",
        period="1m",
        sort_by="final_score",
    )
    return_result = current_analysis.get_current_analysis_data(
        limit=3,
        analysis_date="2026-09-04",
        period="1m",
        sort_by="return",
    )

    expected = ["AAA", "BBB", "CCC"]

    assert [
        row["ticker"]
        for row in final_score_result["market_regime_scores"]
    ] == expected
    assert [
        row["ticker"]
        for row in return_result["market_regime_scores"]
    ] == expected
