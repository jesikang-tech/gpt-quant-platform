from pathlib import Path


DASHBOARD_JS = Path("static/dashboard.js")


def _dashboard_source():
    return DASHBOARD_JS.read_text(encoding="utf-8")


def test_dashboard_refresh_intervals_are_tracked():
    source = _dashboard_source()

    assert "dashboardRefreshIntervalIds" in source
    assert "setInterval(loadDashboard, 10000)" in source
    assert "setInterval(loadPortfolioAdvisor, 10000)" in source
    assert "setInterval(loadMarketRegime, 10000)" in source


def test_logout_stops_dashboard_refresh_and_allows_restart():
    source = _dashboard_source()

    assert "function stopDashboard()" in source
    assert "clearInterval" in source
    assert "dashboardRefreshIntervalIds" in source
    assert "dashboardStarted = false" in source

    logout_start = source.index("async function logoutPlatform()")
    logout_end = source.index(
        "async function initializePlatformAuthentication()",
        logout_start,
    )
    logout_source = source[logout_start:logout_end]

    assert "stopDashboard();" in logout_source
