"""Offline integration tests for the isolated KIWOOM Ver1.1 UAT app.

Uses Flask test_client only. No server, operating DB, credentials,
external provider, or broker calls.
"""

import pytest

from uat_boundary.app_factory import create_uat_app


_TEST_PASSWORD = "isolated-uat-test-only-password"
_TEST_SECRET = "isolated-uat-test-session-secret-000000000000"


@pytest.fixture
def client():
    app = create_uat_app(
        password=_TEST_PASSWORD,
        session_secret=_TEST_SECRET,
    )
    return app.test_client()


def _login(client):
    return client.post(
        "/api/auth/login",
        json={"password": _TEST_PASSWORD},
    )


def test_missing_uat_credentials_fail_closed():
    with pytest.raises(ValueError):
        create_uat_app(password="", session_secret=_TEST_SECRET)

    with pytest.raises(ValueError):
        create_uat_app(password=_TEST_PASSWORD, session_secret="short")


def test_dashboard_removes_external_cdn_and_sets_csp(client):
    response = client.get("/")

    assert response.status_code == 200
    assert b"cdn.jsdelivr.net" not in response.data
    assert b"/static/dashboard.js" in response.data

    csp = response.headers["Content-Security-Policy"]
    assert "default-src 'none'" in csp
    assert "connect-src 'self'" in csp
    assert "frame-ancestors 'none'" in csp


@pytest.mark.parametrize("path", [
    "/api/kiwoom-ver11-analysis",
    "/api/kiwoom-ver11-replay",
])
def test_kiwoom_routes_require_authentication(client, path):
    response = client.post(path, json={})
    assert response.status_code == 401


@pytest.mark.parametrize("path", [
    "/api/ranking",
    "/api/ver11-analysis",
    "/api/auth/admin-login",
    "/api/auth/user-password",
    "/api/historical-replay",
    "/api/unknown",
])
def test_operating_api_routes_are_blocked(client, path):
    assert _login(client).status_code == 200

    response = client.get(path)
    assert response.status_code == 403


def test_uat_login_status_and_logout(client):
    before = client.get("/api/auth/status")
    assert before.status_code == 200
    assert before.get_json()["authenticated"] is False

    bad = client.post(
        "/api/auth/login",
        json={"password": "incorrect"},
    )
    assert bad.status_code == 401

    login = _login(client)
    assert login.status_code == 200
    assert login.get_json()["success"] is True

    status = client.get("/api/auth/status")
    assert status.get_json()["authenticated"] is True

    logout = client.post("/api/auth/logout")
    assert logout.status_code == 200

    after = client.get("/api/auth/status")
    assert after.get_json()["authenticated"] is False


def test_kiwoom_analysis_uses_caller_supplied_prices(client):
    assert _login(client).status_code == 200

    response = client.post(
        "/api/kiwoom-ver11-analysis",
        json={
            "source": "KIWOOM",
            "ticker": "005930",
            "date": "2026-11-10",
            "period": "1m",
            "prices": [
                ["2026-11-09", "70000"],
                ["2026-11-10", "71000"],
            ],
        },
    )

    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert data["input_origin"] == "CALLER_SUPPLIED_UNVERIFIED"
    assert data["persistence"] is False
    assert data["result"]["available"] is False


def test_kiwoom_replay_uses_caller_supplied_prices(client):
    assert _login(client).status_code == 200

    response = client.post(
        "/api/kiwoom-ver11-replay",
        json={
            "source": "KIWOOM",
            "date": "2026-11-10",
            "period": "1m",
            "limit": 10,
            "ticker_prices": {
                "005930": [
                    ["2026-11-09", "70000"],
                    ["2026-11-10", "71000"],
                ],
            },
        },
    )

    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert data["source"] == "KIWOOM"
    assert data["persistence"] is False
    assert data["db_write"] is False


@pytest.mark.parametrize("path,payload", [
    (
        "/api/kiwoom-ver11-analysis",
        {"source": "NAVER", "ticker": "005930", "prices": []},
    ),
    (
        "/api/kiwoom-ver11-replay",
        {"source": "NAVER", "ticker_prices": {}},
    ),
])
def test_non_kiwoom_source_is_rejected(client, path, payload):
    assert _login(client).status_code == 200

    response = client.post(path, json=payload)
    assert response.status_code == 400
    assert response.get_json()["success"] is False
