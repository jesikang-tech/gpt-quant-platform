"""HTTP contract tests for isolated NAVER analysis routes.

No operational API import, database, network or server startup.
"""

import pytest
from flask import Flask, jsonify, request

from test_naver_api_route_execution import load_route


ROUTES = (
    ("historical_replay_api", "/api/historical-replay", "GET"),
    ("ver11_analysis_api", "/api/ver11-analysis", "GET"),
    (
        "save_ver11_analysis_snapshot_api",
        "/api/ver11-analysis/snapshots",
        "POST",
    ),
)


@pytest.mark.parametrize("name,path,method", ROUTES)
@pytest.mark.parametrize("source", ("NAVER", "UNKNOWN"))
def test_http_rejects_unverified_source(name, path, method, source):
    app = Flask(__name__)
    handler, calls = load_route(name, source=source)

    # Rebind the extracted function to Flask request and response objects.
    handler.__globals__["request"] = request
    handler.__globals__["jsonify"] = jsonify

    app.add_url_rule(
        path,
        endpoint=name,
        view_func=handler,
        methods=[method],
    )

    with app.test_client() as client:
        if method == "POST":
            response = client.post(path, json={"source": source})
        else:
            response = client.get(path, query_string={"source": source})

    assert response.status_code == 400
    assert response.is_json
    assert response.get_json()["success"] is False
    assert calls == []
