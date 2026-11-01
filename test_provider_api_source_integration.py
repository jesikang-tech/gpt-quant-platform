"""Fail-closed Flask API tests for explicit unverified price sources.

Uses the existing isolated price DB and Flask test scope.
No real provider, broker, or operational DB access is authorized.
"""

import pytest

from price_test_support import isolated_price_db, phase8_test_scope


@pytest.fixture
def protected_api(isolated_price_db):
    with phase8_test_scope(isolated_price_db) as scope:
        api = scope.api
        original_config = dict(api.app.config)
        original_auth_path = api.AUTH_CONFIG_PATH

        try:
            yield api
        finally:
            api.app.config.clear()
            api.app.config.update(original_config)
            api.AUTH_CONFIG_PATH = original_auth_path


@pytest.mark.parametrize("source", ["KIS", "KIWOOM", "NAVER"])
@pytest.mark.parametrize(
    "endpoint",
    [
        "/api/historical-replay",
        "/api/ver11-analysis",
    ],
)
def test_explicit_source_denied_before_analysis(
    protected_api, monkeypatch, source, endpoint
):
    from testing_helpers import authenticated_client

    calls = []

    def forbidden_analysis(*args, **kwargs):
        calls.append(("analysis", args, kwargs))
        raise AssertionError("Analysis must not execute")

    monkeypatch.setattr(
        protected_api,
        "get_current_analysis_data",
        forbidden_analysis,
    )

    client = authenticated_client(protected_api.app)
    response = client.get(endpoint, query_string={"source": source})

    assert response.status_code == 400
    assert response.get_json()["success"] is False
    assert calls == []


@pytest.mark.parametrize("source", ["KIS", "KIWOOM", "NAVER"])
def test_explicit_source_denied_before_snapshot_save(
    protected_api, monkeypatch, source
):
    from testing_helpers import authenticated_client

    calls = []

    def forbidden_analysis(*args, **kwargs):
        calls.append("analysis")
        raise AssertionError("Analysis must not execute")

    def forbidden_save(*args, **kwargs):
        calls.append("snapshot_save")
        raise AssertionError("Snapshot save must not execute")

    monkeypatch.setattr(
        protected_api,
        "get_current_analysis_data",
        forbidden_analysis,
    )
    monkeypatch.setattr(
        protected_api,
        "save_ver11_analysis_snapshot",
        forbidden_save,
    )

    client = authenticated_client(protected_api.app)

    response = client.post(
        "/api/ver11-analysis/snapshots",
        json={
            "source": source,
            "date": "2026-10-30",
            "period": "3m",
            "limit": 10,
        },
    )

    assert response.status_code == 400
    assert response.get_json()["success"] is False
    assert calls == []
