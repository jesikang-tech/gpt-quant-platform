"""Validate the copied real API without importing operational modules."""

from pathlib import Path

import pytest

from test_naver_api_route_execution import ROUTES, load_route


REAL_API = Path(__file__).parent / "integration_sources" / "api_server_original.py"


@pytest.mark.parametrize("route", ROUTES)
@pytest.mark.parametrize("source", ("NAVER", "UNKNOWN"))
def test_real_api_rejects_unverified_source_before_analysis(route, source):
    assert REAL_API.is_file()
    handler, calls = load_route(route, source=source, api_path=REAL_API)

    response, status = handler()

    assert status == 400
    assert response["success"] is False
    assert calls == []
