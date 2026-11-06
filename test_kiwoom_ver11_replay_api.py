"""Authenticated KIWOOM historical replay API contract tests."""

from datetime import date, timedelta

import pytest

from price_test_support import isolated_price_db, phase8_test_scope


@pytest.fixture
def api_scope(isolated_price_db):
    with phase8_test_scope(isolated_price_db) as scope:
        yield scope.api


def _payload():
    start = date(2026, 8, 1)
    prices = [
        [(start + timedelta(days=i)).isoformat(), str(100 + i)]
        for i in range(65)
    ]
    return {
        "source": "KIWOOM",
        "ticker_prices": {"069500": prices},
        "date": "2026-10-04",
        "period": "3m",
        "limit": 10,
    }


def test_unauthenticated_replay_denied(api_scope):
    response = api_scope.app.test_client().post(
        "/api/kiwoom-ver11-replay", json=_payload()
    )
    assert response.status_code == 401


def test_authenticated_replay_returns_offline_result(api_scope):
    from testing_helpers import authenticated_client

    client = authenticated_client(api_scope.app)
    response = client.post("/api/kiwoom-ver11-replay", json=_payload())
    assert response.status_code == 200
    body = response.get_json()
    assert body["success"] is True
    assert body["source"] == "KIWOOM"
    assert body["input_origin"] == "CALLER_SUPPLIED_UNVERIFIED"
    assert body["persistence"] is False
    assert body["db_write"] is False
    assert body["analysis_date"] == "2026-10-04"


@pytest.mark.parametrize("bad_source", ["NAVER", "KIS", None, "kiwoom"])
def test_other_sources_rejected(api_scope, bad_source):
    from testing_helpers import authenticated_client

    client = authenticated_client(api_scope.app)
    payload = _payload()
    payload["source"] = bad_source
    response = client.post("/api/kiwoom-ver11-replay", json=payload)
    assert response.status_code == 400


@pytest.mark.parametrize("bad_close", ["0", "-1", "NaN", "Infinity", "abc", 100])
def test_invalid_close_rejected(api_scope, bad_close):
    from testing_helpers import authenticated_client

    client = authenticated_client(api_scope.app)
    payload = _payload()
    payload["ticker_prices"]["069500"][0][1] = bad_close
    response = client.post("/api/kiwoom-ver11-replay", json=payload)
    assert response.status_code == 400


def test_existing_historical_replay_remains_blocked(api_scope):
    from testing_helpers import authenticated_client

    client = authenticated_client(api_scope.app)
    response = client.get("/api/historical-replay")
    assert response.status_code == 400