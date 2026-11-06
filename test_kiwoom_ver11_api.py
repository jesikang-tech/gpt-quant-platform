"""Authenticated offline KIWOOM Ver1.1 API contract tests."""

from datetime import date, timedelta

import pytest

from price_test_support import isolated_price_db, phase8_test_scope
from testing_helpers import authenticated_client


@pytest.fixture
def api_scope(isolated_price_db):
    with phase8_test_scope(isolated_price_db) as scope:
        yield scope.api


def _payload():
    start = date(2026, 8, 1)
    return {
        "source": "KIWOOM",
        "ticker": "069500",
        "date": (start + timedelta(days=64)).isoformat(),
        "period": "3m",
        "prices": [
            [
                (start + timedelta(days=i)).isoformat(),
                str(100 + i),
            ]
            for i in range(65)
        ],
    }


def test_unauthenticated_request_denied(api_scope):
    client = api_scope.app.test_client()
    response = client.post("/api/kiwoom-ver11-analysis", json=_payload())
    assert response.status_code == 401
    assert response.get_json()["success"] is False


def test_authenticated_offline_analysis(api_scope):
    client = authenticated_client(api_scope.app)
    response = client.post("/api/kiwoom-ver11-analysis", json=_payload())
    assert response.status_code == 200
    body = response.get_json()
    assert body["success"] is True
    assert body["input_origin"] == "CALLER_SUPPLIED_UNVERIFIED"
    assert body["persistence"] is False
    assert body["result"]["ticker"] == "069500"
    assert body["result"]["source"] == "KIWOOM"
    assert body["result"]["available"] is True
    assert body["result"]["db_write"] is False


@pytest.mark.parametrize("source", ["NAVER", "KIS", None, "kiwoom"])
def test_non_kiwoom_source_denied(api_scope, source):
    client = authenticated_client(api_scope.app)
    payload = _payload()
    payload["source"] = source
    response = client.post("/api/kiwoom-ver11-analysis", json=payload)
    assert response.status_code == 400
    assert response.get_json()["success"] is False


@pytest.mark.parametrize("bad_close", ["0", "-1", "NaN", "Infinity", "abc", 100])
def test_invalid_close_denied(api_scope, bad_close):
    client = authenticated_client(api_scope.app)
    payload = _payload()
    payload["prices"][0][1] = bad_close
    response = client.post("/api/kiwoom-ver11-analysis", json=payload)
    assert response.status_code == 400
    assert response.get_json()["success"] is False


def test_existing_ver11_api_remains_blocked(api_scope):
    client = authenticated_client(api_scope.app)
    response = client.get("/api/ver11-analysis")
    assert response.status_code == 400
    assert "Price provenance is unverified" in response.get_json()["message"]


def test_existing_snapshot_write_remains_blocked(api_scope):
    client = authenticated_client(api_scope.app)
    response = client.post(
        "/api/ver11-analysis/snapshots",
        json={"source": "KIWOOM"},
    )
    assert response.status_code == 400
    assert "Price provenance is unverified" in response.get_json()["message"]

def _kiwoom_daily_response_payload():
    start = date(2026, 8, 3)
    rows = []
    day = start
    while len(rows) < 65:
        if day.weekday() < 5:
            close = str(100 + len(rows))
            rows.append({
                "date": day.strftime("%Y%m%d"),
                "open_pric": close,
                "high_pric": close,
                "low_pric": close,
                "close_pric": close,
                "trde_qty": "1000",
            })
        day += timedelta(days=1)
    return {
        "source": "KIWOOM",
        "ticker": "069500",
        "date": rows[-1]["date"][:4] + "-" + rows[-1]["date"][4:6] + "-" + rows[-1]["date"][6:],
        "period": "3m",
        "api_id": "ka10086",
        "response": {"daly_stkpc": list(reversed(rows))},
    }


def test_kiwoom_daily_response_analysis_success(api_scope):
    client = authenticated_client(api_scope.app)
    response = client.post(
        "/api/kiwoom-ver11-analysis",
        json=_kiwoom_daily_response_payload(),
    )
    assert response.status_code == 200
    body = response.get_json()
    assert body["success"] is True
    assert body["input_origin"] == "CALLER_SUPPLIED_UNVERIFIED"
    assert body["persistence"] is False
    assert body["result"]["ticker"] == "069500"
    assert body["result"]["source"] == "KIWOOM"
    assert body["result"]["available"] is True
    assert body["result"]["db_write"] is False


def test_kiwoom_daily_response_invalid_close_denied(api_scope):
    client = authenticated_client(api_scope.app)
    payload = _kiwoom_daily_response_payload()
    payload["response"]["daly_stkpc"][0]["close_pric"] = "NaN"
    response = client.post("/api/kiwoom-ver11-analysis", json=payload)
    assert response.status_code == 400
    assert response.get_json()["success"] is False


def test_kiwoom_daily_response_conflicting_inputs_denied(api_scope):
    client = authenticated_client(api_scope.app)
    payload = _kiwoom_daily_response_payload()
    payload["prices"] = _payload()["prices"]
    response = client.post("/api/kiwoom-ver11-analysis", json=payload)
    assert response.status_code == 400
    assert response.get_json()["success"] is False


def test_kiwoom_daily_response_other_source_denied(api_scope):
    client = authenticated_client(api_scope.app)
    payload = _kiwoom_daily_response_payload()
    payload["source"] = "NAVER"
    response = client.post("/api/kiwoom-ver11-analysis", json=payload)
    assert response.status_code == 400
    assert response.get_json()["success"] is False
