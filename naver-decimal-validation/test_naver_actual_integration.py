"""Static integration contracts for the isolated NAVER status boundary.

No application import, database access, network, or browser execution.
"""

from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parent
API = ROOT / "integration_sources" / "api_server.py"
DASHBOARD = ROOT / "integration_sources" / "dashboard.js"


def source(path):
    return path.read_text(encoding="utf-8")


def test_api_status_route_exists():
    api = source(API)
    assert '@app.route("/api/naver-validation-status", methods=["GET"])' in api
    assert "def naver_validation_status_api():" in api


def test_api_status_is_fail_closed():
    api = source(API)
    start = api.index('def naver_validation_status_api():')
    end = api.index('@app.route("/api/ver11-analysis")', start)
    block = api[start:end]

    assert '"status": "BLOCKED"' in block
    assert '"analysis_authorized": False' in block
    assert '"dashboard_authorized": False' in block
    assert '"persistence_authorized": False' in block

    for forbidden in (
        "get_current_analysis_data(",
        "_attach_point_in_time_portfolio(",
        "sqlite3",
        "etf.db",
    ):
        assert forbidden not in block


def test_dashboard_fetches_status():
    dashboard = source(DASHBOARD)
    assert '"/api/naver-validation-status"' in dashboard
    assert "renderNaverValidationStatus()" in dashboard


@pytest.mark.parametrize(
    "field",
    [
        "analysis_authorized",
        "dashboard_authorized",
        "persistence_authorized",
    ],
)
def test_dashboard_requires_explicit_denial(field):
    dashboard = source(DASHBOARD)
    assert f"status.{field} !== false" in dashboard


def test_dashboard_failure_message_is_fail_closed():
    dashboard = source(DASHBOARD)
    assert "NAVER 가격 데이터 검증 상태를 확인할 수 없습니다." in dashboard
    assert "검증 완료로 간주하지 마십시오." in dashboard


def test_existing_analysis_endpoint_remains():
    api = source(API)
    assert '@app.route("/api/ver11-analysis")' in api
    assert "data = _attach_point_in_time_portfolio(data)" in api

def test_naver_status_is_awaited_before_analysis_render():
    dashboard = source(DASHBOARD)
    start = dashboard.index("async function runVer11Analysis()")
    end = dashboard.index(
        "class DashboardAuthenticationRequiredError",
        start,
    )
    block = dashboard[start:end]

    status_pos = block.index("await renderNaverValidationStatus();")
    cache_pos = block.index("latestVer11AnalysisData = data;")
    render_pos = block.index("renderVer11AnalysisResult(data);")

    assert status_pos < cache_pos < render_pos
    assert "    renderNaverValidationStatus();" not in block


def test_naver_status_failure_remains_unverified():
    dashboard = source(DASHBOARD)
    start = dashboard.index(
        "async function renderNaverValidationStatus()"
    )
    end = dashboard.index(
        "function renderVer11AnalysisResult(data)",
        start,
    )
    block = dashboard[start:end]

    assert "catch (error)" in block
    assert "NAVER 가격 데이터 검증 상태를 확인할 수 없습니다." in block
    assert "검증 완료로 간주하지 마십시오." in block


def test_naver_status_does_not_authorize_analysis():
    dashboard = source(DASHBOARD)
    start = dashboard.index(
        "async function renderNaverValidationStatus()"
    )
    end = dashboard.index(
        "function renderVer11AnalysisResult(data)",
        start,
    )
    block = dashboard[start:end]

    assert "status.analysis_authorized !== false" in block
    assert "status.dashboard_authorized !== false" in block
    assert "status.persistence_authorized !== false" in block
    assert "status.status !== \"BLOCKED\"" in block
