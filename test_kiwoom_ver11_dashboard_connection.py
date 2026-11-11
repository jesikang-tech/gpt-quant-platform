"""Static contract for the isolated KIWOOM Ver1.1 dashboard panel.

No browser, HTTP, broker, or operating database access.
"""

from pathlib import Path


ROOT = Path(__file__).resolve().parent
HTML = ROOT / "templates" / "index.html"
JAVASCRIPT = ROOT / "static" / "dashboard.js"


def test_kiwoom_dashboard_input_elements_exist():
    html = HTML.read_text(encoding="utf-8")
    for element_id in (
        "kiwoom-ver11-panel",
        "kiwoom-ver11-ticker",
        "kiwoom-ver11-response",
        "kiwoom-ver11-run",
        "kiwoom-ver11-status",
        "kiwoom-ver11-result",
        "kiwoom-ver11-result-content",
    ):
        assert f'id="{element_id}"' in html


def test_kiwoom_dashboard_uses_explicit_offline_api():
    script = JAVASCRIPT.read_text(encoding="utf-8")
    assert "function initializeKiwoomVer11OfflinePanel()" in script
    assert 'fetch("/api/kiwoom-ver11-analysis"' in script
    assert 'method: "POST"' in script
    assert 'source: "KIWOOM"' in script
    assert 'api_id: "ka10086"' in script
    assert "response: suppliedResponse" in script
    assert "data.persistence !== false" in script
    assert "resultContent.replaceChildren(" in script


def test_existing_ver11_and_replay_controls_preserved():
    html = HTML.read_text(encoding="utf-8")
    script = JAVASCRIPT.read_text(encoding="utf-8")
    for element_id in (
        "ver11-analysis-run",
        "ver11-analysis-result",
        "historical-replay-button",
        "historical-replay-result",
        "ver11-snapshot-save",
    ):
        assert f'id="{element_id}"' in html
    assert "async function runVer11Analysis()" in script
    assert "async function runHistoricalReplay()" in script
    assert "/api/ver11-analysis?" in script
    assert "/api/historical-replay?" in script


def test_kiwoom_handler_does_not_write_or_collect_data():
    script = JAVASCRIPT.read_text(encoding="utf-8")
    handler = script.split(
        "function initializeKiwoomVer11OfflinePanel()", 1
    )[1]
    assert handler.count('fetch("/api/kiwoom-ver11-analysis"') == 1
    assert "/api/ver11-analysis/snapshots" not in handler
    assert "/api/historical-replay" not in handler
    assert "resultContent.innerHTML" not in handler


def test_kiwoom_replay_browser_contract():
    """Replay UI must use the existing authenticated, non-persistent API."""
    html = HTML.read_text(encoding="utf-8")
    script = JAVASCRIPT.read_text(encoding="utf-8")

    for marker in (
        'id="kiwoom-ver11-replay-panel"',
        'id="kiwoom-ver11-replay-prices"',
        'id="kiwoom-ver11-replay-limit"',
        'id="kiwoom-ver11-replay-run"',
        'id="kiwoom-ver11-replay-status"',
        'id="kiwoom-ver11-replay-result"',
        'id="kiwoom-ver11-replay-result-content"',
    ):
        assert marker in html

    for marker in (
        "function initializeKiwoomVer11ReplayPanel()",
        'getElementById("ver11-analysis-date")',
        'getElementById("ver11-analysis-period")',
        '"/api/kiwoom-ver11-replay"',
        'data.source !== "KIWOOM"',
        'data.input_origin !== "CALLER_SUPPLIED_UNVERIFIED"',
        "data.persistence !== false",
        "data.db_write !== false",
        "resultContent.textContent =",
        "initializeKiwoomVer11ReplayPanel",
    ):
        assert marker in script
