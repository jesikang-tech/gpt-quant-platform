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

def test_historical_replay_localizes_display_only_values():
    source = _dashboard_source()

    assert 'getHistoricalReplayDisplayText' in source
    assert 'historicalReplayRegimeBullish' in source
    assert 'historicalReplayRegimeNeutral' in source
    assert 'historicalReplayRegimeBearish' in source
    assert 'getDashboardText("aggressive")' in source
    assert 'getDashboardText("balanced")' in source
    assert 'getDashboardText("conservative")' in source
    assert 'historicalReplayStatusPass' in source
    assert 'historicalReplayStatusFail' in source
    assert 'historicalReplayStatusPending' in source
    assert 'historicalReplayCash' in source
    assert 'historicalReplayDaySuffix' in source

def test_historical_replay_null_hit_day_is_not_rendered_as_zero():
    source = _dashboard_source()

    assert "reality.close_first_hit_day == null" in source
    assert "reality.high_first_hit_day == null" in source


def test_historical_replay_renders_localized_unavailable_reasons():
    source = _dashboard_source()

    assert 'historicalReplayReasonMissingBaseline' in source
    assert 'historicalReplayReasonInvalidBaseline' in source
    assert 'historicalReplayReasonIncompleteHighCoverage' in source
    assert 'historicalReplayReasonIncompleteCloseCoverage' in source
    assert 'reality.close_unavailable_reason || reality.unavailable_reason' in source
    assert 'reality.high_unavailable_reason || reality.unavailable_reason' in source
    assert 'reality.close_status == null && closeUnavailableReason' in source
    assert 'reality.high_status == null && highUnavailableReason' in source
    assert '"reason",' in source
    assert '${closeStatusText}' in source
    assert '${highStatusText}' in source
