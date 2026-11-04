"""Prevent uncertified provider imports in legacy price analysis modules."""

import ast
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[2]

@pytest.mark.parametrize("module_name", ("current_analysis.py", "repository.py"))
def test_legacy_analysis_has_no_direct_provider_import(module_name):
    """Keep existing ETF readers separate from uncertified provider adapters."""
    tree = ast.parse((ROOT / module_name).read_text(encoding="utf-8"))

    forbidden_modules = {
        "price_provider_validation",
        "kis_adapter",
        "kiwoom_adapter",
        "provider_analysis_boundary",
    }

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names = [alias.name for alias in node.names]
        elif isinstance(node, ast.ImportFrom):
            names = [node.module or ""]
        else:
            continue

        for name in names:
            parts = set(name.split("."))
            assert not (parts & forbidden_modules), (
                f"{module_name}: unexpected provider import {name}"
            )
