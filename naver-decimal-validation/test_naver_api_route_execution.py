"""Execute isolated API route functions without importing operational modules."""

import ast
from pathlib import Path
from types import SimpleNamespace

import pytest

from core.price_provenance_gate import PriceProvenanceRejected


API = Path(__file__).parent / "integration_sources" / "api_server.py"

ROUTES = (
    "historical_replay_api",
    "ver11_analysis_api",
    "save_ver11_analysis_snapshot_api",
)


def load_route(name, *, source):
    tree = ast.parse(API.read_text(encoding="utf-8"))
    functions = [
        node for node in tree.body
        if isinstance(node, ast.FunctionDef) and node.name == name
    ]
    assert len(functions) == 1

    function = functions[0]
    function.decorator_list = []

    calls = []

    def forbidden_analysis(*args, **kwargs):
        calls.append("analysis")
        raise AssertionError("Analysis must not run")

    def forbidden_save(*args, **kwargs):
        calls.append("save")
        raise AssertionError("Snapshot save must not run")

    request = SimpleNamespace(
        args={"source": source},
        get_json=lambda silent=False: {"source": source},
    )

    namespace = {
        "request": request,
        "jsonify": lambda value: value,
        "get_current_analysis_data": forbidden_analysis,
        "_attach_point_in_time_portfolio": forbidden_analysis,
        "_build_ver11_snapshot_payload": forbidden_analysis,
        "save_ver11_analysis_snapshot": forbidden_save,
    }

    module = ast.Module(body=[function], type_ignores=[])
    ast.fix_missing_locations(module)

    exec(compile(module, str(API), "exec"), namespace)

    return namespace[name], calls


@pytest.mark.parametrize("route", ROUTES)
def test_unverified_naver_rejected_before_analysis(route):
    handler, calls = load_route(route, source="NAVER")
    response, status = handler()

    assert status == 400
    assert response["success"] is False
    assert calls == []


@pytest.mark.parametrize("route", ROUTES)
def test_unknown_source_rejected_before_analysis(route):
    handler, calls = load_route(route, source="UNKNOWN")
    response, status = handler()

    assert status == 400
    assert response["success"] is False
    assert calls == []


@pytest.mark.parametrize("route", ROUTES)
def test_legacy_request_reaches_existing_analysis(route):
    handler, calls = load_route(route, source=None)

    handler()

    assert calls == ["analysis"]
