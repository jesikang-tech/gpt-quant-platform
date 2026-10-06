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
