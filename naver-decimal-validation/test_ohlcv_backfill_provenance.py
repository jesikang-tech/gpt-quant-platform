"""Static regression for the legacy OHLCV backfill provenance boundary."""

import ast
from pathlib import Path


def test_legacy_backfill_requires_provenance_before_provider_fetch():
    source_path = (
        Path(__file__).resolve().parents[1]
        / "collector"
        / "ohlcv_backfill.py"
    )
    tree = ast.parse(source_path.read_text(encoding="utf-8"))

    backfill = next(
        node for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef)
        and node.name == "backfill_ticker"
    )

    calls = [
        node for node in ast.walk(backfill)
        if isinstance(node, ast.Call)
    ]

    provenance_calls = [
        node for node in calls
        if isinstance(node.func, ast.Name)
        and node.func.id == "require_persistence_authorization"
    ]

    assert provenance_calls, (
        "Legacy OHLCV backfill lacks a persistence provenance gate"
    )