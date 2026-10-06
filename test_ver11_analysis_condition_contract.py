from pathlib import Path


def test_ver11_analysis_condition_contract_uses_supported_periods():
    source = Path("current_analysis.py").read_text(encoding="utf-8")

    assert '"1m"' in source
    assert '"2m"' in source
    assert '"3m"' in source

    assert '"lookback_trading_days": 20' in source
    assert '"lookback_trading_days": 40' in source
    assert '"lookback_trading_days": 60' in source

    assert '"return_threshold": 5.0' in source
    assert '"return_threshold": 10.0' in source
    assert '"return_threshold": 15.0' in source


def test_ver11_analysis_condition_contract_rejects_unsupported_periods():
    source = Path("current_analysis.py").read_text(encoding="utf-8")

    assert 'raise ValueError("Invalid period. Use 1m, 2m, or 3m.")' in source


def test_ver11_analysis_condition_contract_preserves_analysis_date_boundary():
    source = Path("current_analysis.py").read_text(encoding="utf-8")

    assert "get_etf_prices(ticker, resolved_date)" in source
    assert '"analysis_date": resolved_date' in source
    assert '"market_data_date": resolved_date' in source


def test_ver11_analysis_condition_contract_preserves_reality_test_period():
    source = Path("current_analysis.py").read_text(encoding="utf-8")

    assert '_get_reality_test(row["ticker"], resolved_date, period)' in source


def test_ver11_analysis_condition_ui_control_state_contract():
    source = Path("templates/index.html").read_text(encoding="utf-8")

    assert 'id="ver11-analysis-run"' in source
    assert 'id="ver11-analysis-reset"' in source

    assert (
        '<button id="ver11-analysis-reset" type="button" disabled>'
        in source
    )

    assert source.count(
        '<label><input type="checkbox" disabled>'
    ) >= 2


def test_ver11_analysis_reset_behavior_contract():
    source = Path("static/dashboard.js").read_text(encoding="utf-8")

    assert 'document.getElementById("ver11-analysis-reset")' in source
    assert "resetButton.disabled = false" in source
    assert 'resetButton.addEventListener("click"' in source

    assert 'analysisDate.value = ""' in source
    assert 'analysisPeriod.value = "3m"' in source
    assert 'sortInput.value = "final_score"' in source
    assert 'countInput.value = "10"' in source
    assert "etfType.selectedIndex = 0" in source
    assert "market.selectedIndex = 0" in source

    assert 'document.getElementById("ver11-analysis-result")' in source
    assert "resultMeta.textContent = \"\"" in source
    assert "resultContent.innerHTML = \"\"" in source
    assert "resultPanel.hidden = true" in source

def test_ver11_sort_and_count_controls_are_enabled_contract():
    source = Path("templates/index.html").read_text(encoding="utf-8")

    assert '<select id="ver11-sort">' in source
    assert '<select id="ver11-count">' in source
    assert '<select id="ver11-sort" disabled>' not in source
    assert '<select id="ver11-count" disabled>' not in source


def test_ver11_unimplemented_filters_remain_disabled_contract():
    html = Path("templates/index.html").read_text(encoding="utf-8")
    js = Path("static/dashboard.js").read_text(encoding="utf-8")

    assert '<select id="ver11-etf-type" disabled>' in html
    assert '<select id="ver11-market" disabled>' in html
    assert 'disabled> <span id="ver11-watchlist-only">' in html
    assert 'disabled> <span id="ver11-holdings-only">' in html

    control_block = js.split(
        "const controlIds = [", 1
    )[1].split("];", 1)[0]

    assert '"ver11-etf-type"' not in control_block
    assert '"ver11-market"' not in control_block
