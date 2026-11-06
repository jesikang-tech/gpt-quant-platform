"""Fail-closed Kiwoom Ver1.1 ranking API provenance contract."""

from price_test_support import isolated_price_db, phase8_test_scope
from testing_helpers import authenticated_client


def test_unverified_ranking_api_denied_before_dashboard_read(
    isolated_price_db,
    monkeypatch,
):
    with phase8_test_scope(isolated_price_db) as scope:
        api = scope.api
        calls = []

        def forbidden_dashboard(*args, **kwargs):
            calls.append("dashboard_read")
            raise AssertionError("Dashboard read must not occur")

        monkeypatch.setattr(
            api,
            "get_dashboard_api_data",
            forbidden_dashboard,
        )

        client = authenticated_client(api.app)
        response = client.get("/api/ranking")

        assert response.status_code == 400

        payload = response.get_json()

        assert payload["success"] is False
        assert "Price provenance is unverified" in payload["message"]
        assert calls == []
