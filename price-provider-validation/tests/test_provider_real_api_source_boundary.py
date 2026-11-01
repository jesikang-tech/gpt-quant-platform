"""Verify existing real API source rejection without operational imports."""

import ast
from pathlib import Path
from types import SimpleNamespace

import pytest


ROOT = Path(__file__).resolve().parents[2]
API = ROOT / "api_server.py"

ROUTES = (
    "historical_replay_api",
    "ver11_analysis_api",
    "save_ver11_analysis_snapshot_api",
)


def _load_route(name, source):
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
        raise AssertionError("Operational analysis must not execute")

    def forbidden_save(*args, **kwargs):
        calls.append("save")
        raise AssertionError("Operational persistence must not execute")

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
@pytest.mark.parametrize("source", ("KIS", "KIWOOM", "NAVER", "UNKNOWN"))
def test_unverified_external_source_rejected_before_analysis(route, source):
    handler, calls = _load_route(route, source)
    response, status = handler()

    assert status == 400
    assert response["success"] is False
    assert calls == []


@pytest.mark.parametrize("route", ROUTES)
def test_existing_unspecified_source_path_is_preserved(route):
    handler, calls = _load_route(route, None)

    handler()

    assert calls == ["analysis"]
