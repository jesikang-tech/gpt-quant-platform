from pathlib import Path


DASHBOARD_JS = Path("static/dashboard.js")


def _dashboard_source():
    return DASHBOARD_JS.read_text(encoding="utf-8-sig")


def test_historical_replay_uses_point_in_time_market_and_portfolio():
    source = _dashboard_source()

    assert 'data.market_regime' in source
    assert 'data.market_strategy' in source
    assert 'data.portfolio' in source


def test_historical_replay_renders_market_strategy_summary():
    source = _dashboard_source()

    assert 'Replay Market Regime' in source
    assert 'Replay Portfolio Mode' in source
    assert 'Replay Cash Target' in source


def test_historical_replay_renders_top3_and_cash_portfolio():
    source = _dashboard_source()

    assert 'Historical Replay - Portfolio' in source
    assert 'replayPortfolioRows' in source
    assert 'portfolioItem.weight' in source


def test_historical_replay_handles_empty_portfolio_explicitly():
    source = _dashboard_source()

    assert 'No replay portfolio available.' in source


def test_historical_replay_cash_null_score_is_not_rendered_as_zero():
    source = _dashboard_source()

    assert 'portfolioItem.score == null' in source


def test_historical_replay_uses_dashboard_translation_system():
    source = _dashboard_source()

    assert 'historicalReplayTitle' in source
    assert 'historicalReplayAnalysisDate' in source
    assert 'historicalReplayAnalysisPeriod' in source
    assert 'historicalReplayPortfolioTitle' in source
    assert 'historicalReplayRealityTitle' in source
    assert 'getDashboardText("historicalReplayPortfolioTitle")' in source


def test_historical_replay_rerenders_existing_result_on_language_change():
    source = _dashboard_source()

    assert 'latestHistoricalReplayData' in source
    assert 'renderHistoricalReplayResult' in source
    assert 'renderHistoricalReplayResult(latestHistoricalReplayData)' in source
