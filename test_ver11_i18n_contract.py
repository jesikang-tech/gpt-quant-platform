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

def test_ver11_snapshot_ui_contract():
    template = Path("templates/index.html").read_text(encoding="utf-8")
    source = Path("static/dashboard.js").read_text(encoding="utf-8")

    assert 'id="ver11-snapshot-save"' in template
    assert 'id="ver11-snapshot-history"' in template
    assert 'id="ver11-snapshot-history-panel"' in template
    assert 'id="ver11-snapshot-history-content"' in template

    required_translation_keys = (
        "ver11SnapshotSave",
        "ver11SnapshotHistory",
        "ver11SnapshotHistoryTitle",
        "ver11SnapshotSaved",
        "ver11SnapshotEmpty",
    )

    for key in required_translation_keys:
        assert source.count(f'"{key}"') >= 2

    assert 'document.getElementById("ver11-snapshot-save")' in source
    assert 'document.getElementById("ver11-snapshot-history")' in source
    assert 'document.getElementById("ver11-snapshot-history-panel")' in source
    assert 'document.getElementById("ver11-snapshot-history-content")' in source

def test_ver11_snapshot_save_behavior_contract():
    source = Path("static/dashboard.js").read_text(encoding="utf-8")

    assert 'document.getElementById("ver11-snapshot-save")' in source
    assert '"/api/ver11-analysis/snapshots"' in source
    assert 'method: "POST"' in source
    assert "JSON.stringify({" in source
    assert "date:" in source
    assert "period:" in source
    assert "sort:" in source
    assert "limit:" in source

    assert "snapshotSaveButton.disabled = false;" in source
    assert "snapshotSaveButton.disabled = true;" in source

def test_ver11_snapshot_history_behavior_contract():
    source = Path("static/dashboard.js").read_text(encoding="utf-8")

    assert 'fetch("/api/ver11-analysis/snapshots?limit=50")' in source
    assert 'fetch(`/api/ver11-analysis/snapshots/${snapshotId}`)' in source
    assert "renderVer11SnapshotHistory(" in source
    assert "renderVer11SnapshotDetail(" in source
    assert "snapshot.snapshot_payload" in source
    assert "snapshot.analysis_date" in source
    assert "snapshot.period" in source
    assert "snapshot.sort_by" in source
    assert "snapshot.display_limit" in source
    assert "snapshot.created_at" in source

def test_ver11_point_in_time_explain_reason_i18n_contract():
    source = Path("static/dashboard.js").read_text(encoding="utf-8")

    required_reason_keys = (
        "ver11ExplainRegimeBullishReason",
        "ver11ExplainRegimeNeutralReason",
        "ver11ExplainRegimeBearishReason",
        "ver11ExplainStrategyReason",
        "ver11ExplainPortfolioReason",
    )

    for key in required_reason_keys:
        assert source.count(f'"{key}"') >= 2

    assert "function formatVer11ExplainText(key, values = {})" in source
    assert "const localizedRegimeReason = formatVer11ExplainText(" in source
    assert "const localizedStrategyReason = formatVer11ExplainText(" in source
    assert "const localizedPortfolioReason = formatVer11ExplainText(" in source

    assert "${localizedRegimeReason}" in source
    assert "${localizedStrategyReason}" in source
    assert "${localizedPortfolioReason}" in source

    assert '${explanationRegime.reason || ""}' not in source
    assert '${explanationStrategy.reason || ""}' not in source
    assert '${explanationPortfolio.reason || ""}' not in source

def test_ver11_analysis_error_ui_contract():
    source = Path("static/dashboard.js").read_text(encoding="utf-8")

    assert "function renderVer11AnalysisError(error)" in source
    assert 'document.getElementById("ver11-analysis-result")' in source
    assert 'document.getElementById("ver11-analysis-result-meta")' in source
    assert 'document.getElementById("ver11-analysis-result-content")' in source
    assert 'getDashboardText("ver11AnalysisError")' in source
    assert "renderVer11AnalysisError(error);" in source

    # A failed request must not leave the previous successful result
    # visible as though it belonged to the newly requested date.
    assert 'resultContent.innerHTML = "";' in source
    assert "resultPanel.hidden = false;" in source

    # Both Korean and English dictionaries must define the message.
    assert source.count('"ver11AnalysisError"') >= 3

def test_ver11_snapshot_history_visibility_and_layout_contract():
    source = Path("static/dashboard.js").read_text(encoding="utf-8")
    style = Path("static/style.css").read_text(encoding="utf-8")

    # Snapshot history has seven columns and must not inherit only the
    # six-column Historical Replay width contract.
    assert 'class="historical-replay-table ver11-snapshot-history-table"' in source
    assert ".ver11-snapshot-history-table" in style

    # A successful history request must bring the newly opened panel
    # into view so the button does not appear to do nothing.
    assert "function focusVer11SnapshotHistoryPanel()" in source
    assert "panel.scrollIntoView(" in source
    assert "focusVer11SnapshotHistoryPanel();" in source

def test_ver11_snapshot_history_error_ui_contract():
    source = Path("static/dashboard.js").read_text(encoding="utf-8")

    assert "function renderVer11SnapshotHistoryError(error)" in source
    assert 'document.getElementById("ver11-snapshot-history-panel")' in source
    assert 'document.getElementById("ver11-snapshot-history-content")' in source
    assert 'getDashboardText("ver11SnapshotHistoryError")' in source
    assert "renderVer11SnapshotHistoryError(error);" in source

    # A failed history request must be visible to the user instead of
    # ending only in the browser console.
    assert "panel.hidden = false;" in source
    assert "focusVer11SnapshotHistoryPanel();" in source

    # Korean and English dictionaries must both define the message.
    assert source.count('"ver11SnapshotHistoryError"') >= 3

def test_ver11_snapshot_save_error_ui_contract():
    source = Path("static/dashboard.js").read_text(encoding="utf-8")

    # A failed save request must be visible to the user instead of
    # ending only in the browser console. Keep the current analysis
    # result intact and use the same alert-style feedback as save success.
    assert 'window.alert(getDashboardText("ver11SnapshotSaveError"));' in source

    # Korean and English dictionaries must both define the message.
    assert source.count('"ver11SnapshotSaveError"') >= 3


def test_ver11_snapshot_detail_error_ui_contract():
    source = Path("static/dashboard.js").read_text(encoding="utf-8")

    assert "function renderVer11SnapshotDetailError(error)" in source
    assert 'getDashboardText("ver11SnapshotDetailError")' in source
    assert "renderVer11SnapshotDetailError(error);" in source

    # A failed detail request must be visible in the Snapshot panel
    # instead of ending only in the browser console.
    assert source.count('"ver11SnapshotDetailError"') >= 3


def test_explainability_error_ui_contract():
    source = Path("static/dashboard.js").read_text(encoding="utf-8")

    assert 'getDashboardText("portfolioExplainabilityError")' in source
    assert 'getDashboardText("aiDecisionExplainabilityError")' in source

    # Both explainability loaders must surface failures in their existing
    # result panels instead of ending only in the browser console.
    assert source.count('"portfolioExplainabilityError"') >= 3
    assert source.count('"aiDecisionExplainabilityError"') >= 3
