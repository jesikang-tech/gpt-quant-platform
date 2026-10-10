from pathlib import Path


DASHBOARD_JS = Path("static/dashboard.js")


def _dashboard_source():
    return DASHBOARD_JS.read_text(encoding="utf-8")


def test_dashboard_refresh_intervals_are_tracked():
    source = _dashboard_source()

    assert "dashboardRefreshIntervalIds" in source
    assert "setInterval(() => runDashboardRefresh(loadDashboard), 10000)" in source
    assert "setInterval(() => runDashboardRefresh(loadPortfolioAdvisor), 10000)" in source
    assert "setInterval(() => runDashboardRefresh(loadMarketRegime), 10000)" in source


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


def test_dashboard_api_loaders_reject_unauthorized_responses():
    source = _dashboard_source()

    assert "async function requireDashboardApiResponse(response)" in source
    assert "response.status === 401" in source
    assert "response.ok" in source

    helper_start = source.index(
        "async function requireDashboardApiResponse(response)"
    )
    helper_end = source.index(
        "let dashboardStarted",
        helper_start,
    )
    helper_source = source[helper_start:helper_end]

    assert "stopDashboard();" in helper_source
    assert "hidePlatformAdminPanel();" in helper_source
    assert "setPlatformLogoutButtonVisible(false);" in helper_source
    assert 'setPlatformAuthMode("user");' in helper_source
    assert "showPlatformAuthOverlay();" in helper_source

    assert "requireDashboardApiResponse(response)" in source

    load_dashboard_start = source.index("function loadDashboard()")
    load_dashboard_end = source.index(
        "let platformAuthMode",
        load_dashboard_start,
    )
    load_dashboard_source = source[
        load_dashboard_start:load_dashboard_end
    ]

    assert load_dashboard_source.count(
        "requireDashboardApiResponse(response)"
    ) >= 3

    portfolio_start = source.index(
        "async function loadPortfolioAdvisor"
    )
    portfolio_end = source.index(
        "async function loadPortfolioHistory",
        portfolio_start,
    )
    portfolio_source = source[
        portfolio_start:portfolio_end
    ]

    assert "requireDashboardApiResponse(response)" in portfolio_source

    regime_start = source.index(
        "async function loadMarketRegime"
    )
    regime_source = source[regime_start:]

    assert "requireDashboardApiResponse(response)" in regime_source

def test_dashboard_authentication_error_is_handled_without_unhandled_rejection():
    source = Path("static/dashboard.js").read_text(encoding="utf-8")

    assert "class DashboardAuthenticationRequiredError extends Error" in source
    assert "function runDashboardRefresh(loader)" in source
    assert "error instanceof DashboardAuthenticationRequiredError" in source

    refresh_start = source.index("function refreshDashboardContent")
    start = source.index("function startDashboard", refresh_start)
    end = source.index("async function loadHistory", start)

    refresh_source = source[refresh_start:start]
    lifecycle_source = source[start:end]

    assert "refreshDashboardContent();" in lifecycle_source
    assert "runDashboardRefresh(loadDashboard);" in refresh_source
    assert "runDashboardRefresh(loadPortfolioAdvisor);" in refresh_source
    assert "runDashboardRefresh(loadMarketRegime);" in refresh_source
    assert "setInterval(() => runDashboardRefresh(loadDashboard), 10000)" in lifecycle_source
    assert "setInterval(() => runDashboardRefresh(loadPortfolioAdvisor), 10000)" in lifecycle_source
    assert "setInterval(() => runDashboardRefresh(loadMarketRegime), 10000)" in lifecycle_source

def test_dashboard_refresh_promise_and_history_use_auth_boundary():
    source = Path("static/dashboard.js").read_text(encoding="utf-8")

    dashboard_start = source.index("function loadDashboard")
    dashboard_end = source.index("let platformAuthMode", dashboard_start)
    dashboard_source = source[dashboard_start:dashboard_end]
    assert 'return fetch("/api/ranking")' in dashboard_source

    history_start = source.index("async function loadHistory")
    history_end = source.index("async function", history_start + 1)
    history_source = source[history_start:history_end]
    assert "await requireDashboardApiResponse(response)" in history_source


def test_logout_failure_is_visible_to_user():
    source = _dashboard_source()

    start = source.index("async function initializePlatformAuthentication()")
    end = source.index(
        'document.addEventListener(',
        start,
    )
    auth_source = source[start:end]

    assert 'getDashboardText("platformLogoutError")' in auth_source
    assert 'window.alert(' in auth_source

def test_dashboard_refresh_connection_status_lifecycle_contract():
    source = _dashboard_source()

    assert "dashboardRefreshFailures" in source
    assert "function setDashboardConnectionErrorVisible" in source
    assert "dashboardRefreshFailures.add(loader);" in source
    assert "dashboardRefreshFailures.delete(loader);" in source
    assert "dashboardRefreshFailures.size > 0" in source
    assert 'getDashboardText("dashboardConnectionError")' in source


def test_stop_dashboard_clears_connection_failure_state():
    source = _dashboard_source()

    start = source.index("function stopDashboard()")
    end = source.index("function runDashboardRefresh", start)
    stop_source = source[start:end]

    assert "dashboardRefreshFailures.clear();" in stop_source
    assert "setDashboardConnectionErrorVisible(false);" in stop_source
