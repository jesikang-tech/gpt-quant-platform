from pathlib import Path


def test_ver11_ui_has_translation_contract():
    source = Path("static/dashboard.js").read_text(encoding="utf-8")

    required_keys = (
        "ver11ConditionTitle",
        "ver11ConditionSubtitle",
        "ver11AnalysisDate",
        "ver11AnalysisPeriod",
        "ver11Sort",
        "ver11Count",
        "ver11EtfType",
        "ver11Market",
        "ver11Run",
        "ver11Reset",
        "ver11ResultTitle",
        "ver11NoResults",
        "ver11TradingDays",
        "ver11SortLabel",
        "ver11Rank",
        "ver11EtfName",
        "ver11Return",
        "ver11UptrendRatio",
        "ver11AiScore",
        "ver11TrendScore",
        "ver11SlopeScore",
    )

    for key in required_keys:
        assert source.count(f'"{key}"') >= 2


def test_ver11_ui_language_application_contract():
    source = Path("static/dashboard.js").read_text(encoding="utf-8")

    assert 'document.getElementById("ver11-condition-title")' in source
    assert 'document.getElementById("ver11-condition-subtitle")' in source
    assert 'getDashboardText("ver11ConditionTitle")' in source
    assert 'getDashboardText("ver11ConditionSubtitle")' in source
    assert 'getDashboardText("ver11AnalysisDate")' in source
    assert 'getDashboardText("ver11AnalysisPeriod")' in source
    assert 'getDashboardText("ver11Run")' in source
    assert 'getDashboardText("ver11Reset")' in source


def test_ver11_result_uses_dashboard_translations():
    source = Path("static/dashboard.js").read_text(encoding="utf-8")

    assert 'getDashboardText("ver11NoResults")' in source
    assert 'getDashboardText("ver11TradingDays")' in source
    assert 'getDashboardText("ver11SortLabel")' in source
    assert 'getDashboardText("ver11Rank")' in source
    assert 'getDashboardText("ver11EtfName")' in source
    assert 'getDashboardText("ver11Return")' in source
    assert 'getDashboardText("ver11UptrendRatio")' in source
    assert 'getDashboardText("ver11AiScore")' in source


def test_ver11_old_placeholder_subtitle_is_removed():
    source = Path("templates/index.html").read_text(encoding="utf-8")

    assert "Ver.1.1 &#xC900;&#xBE44; &#xD654;&#xBA74;" not in source
    assert 'id="ver11-condition-title"' in source
    assert 'id="ver11-condition-subtitle"' in source


def test_ver11_result_language_rerender_state_contract():
    source = Path("static/dashboard.js").read_text(encoding="utf-8")

    assert "let latestVer11AnalysisData = null;" in source
    assert "latestVer11AnalysisData = data;" in source
    assert "latestVer11AnalysisData = null;" in source
    assert "if (latestVer11AnalysisData) {" in source
    assert "renderVer11AnalysisResult(latestVer11AnalysisData);" in source

def test_ver11_point_in_time_portfolio_ui_contract():
    source = Path("static/dashboard.js").read_text(encoding="utf-8")

    required_keys = (
        "ver11PortfolioTitle",
        "ver11MarketRegime",
        "ver11PortfolioMode",
        "ver11CashTarget",
        "ver11PortfolioTicker",
        "ver11PortfolioWeight",
        "ver11PortfolioScore",
        "ver11EmptyPortfolio",
    )

    for key in required_keys:
        assert source.count(f'"{key}"') >= 2

    assert "data.market_regime || {}" in source
    assert "data.market_strategy || {}" in source
    assert "Array.isArray(data.portfolio)" in source
    assert 'getDashboardText("ver11PortfolioTitle")' in source
    assert 'getDashboardText("ver11MarketRegime")' in source
    assert 'getDashboardText("ver11PortfolioMode")' in source
    assert 'getDashboardText("ver11CashTarget")' in source
    assert 'getDashboardText("ver11PortfolioTicker")' in source
    assert 'getDashboardText("ver11PortfolioWeight")' in source
    assert 'getDashboardText("ver11PortfolioScore")' in source

def test_ver11_point_in_time_explain_ui_contract():
    from pathlib import Path

    source = Path("static/dashboard.js").read_text(encoding="utf-8")

    required_translation_keys = (
        "ver11ExplainTitle",
        "ver11ExplainDate",
        "ver11ExplainPeriod",
        "ver11Confidence",
        "ver11AverageScore",
        "ver11MarketStrength",
        "ver11Recommendation",
        "ver11RebalanceAction",
        "ver11ReturnScore",
        "ver11OptimizationScore",
        "ver11RecommendationBuy",
        "ver11RecommendationHold",
        "ver11RecommendationReduce",
        "ver11RebalanceIncreaseEquity",
        "ver11RebalanceNoAction",
        "ver11RebalanceIncreaseCash",
    )

    for key in required_translation_keys:
        assert source.count(f'"{key}"') >= 2

    required_fields = (
        "point_in_time_explanation",
        "market_regime",
        "market_strategy",
        "portfolio",
        "cash_weight",
        "analysis_date",
        "reason",
    )

    for field in required_fields:
        assert field in source

    assert "point_in_time_explanation" in source
    assert "portfolio_mode" in source
    assert "cash_target" in source
    assert "recommendation" in source
    assert "rebalance_action" in source
    assert "optimization_score" in source
    assert 'getHistoricalReplayDisplayText("recommendation",' in source
    assert 'getHistoricalReplayDisplayText("rebalance",' in source
