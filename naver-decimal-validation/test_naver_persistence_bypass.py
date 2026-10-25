"""Static regression checks for tracked NAVER persistence boundaries."""

import ast
from pathlib import Path


def _tracked_source(name):
    root = Path(__file__).resolve().parent
    return (root / "core" / name).read_text(encoding="utf-8")


def test_naver_persistence_entry_uses_provenance_gate():
    tree = ast.parse(_tracked_source("naver_persistence_entry.py"))

    imports = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom)
    ]

    assert any(
        node.module == "core.price_provenance_gate"
        and any(
            alias.name == "invoke_naver_persistence"
            for alias in node.names
        )
        for node in imports
    )


def test_naver_persistence_entry_has_no_direct_storage():
    tree = ast.parse(_tracked_source("naver_persistence_entry.py"))

    forbidden_names = {
        "get_connection",
        "sqlite3",
        "save_etf_price",
        "save_etf_ohlcv_price",
        "executemany",
    }

    for node in ast.walk(tree):
        if isinstance(node, ast.Name):
            assert node.id not in forbidden_names
        if isinstance(node, ast.Attribute):
            assert node.attr not in forbidden_names

    source = _tracked_source("naver_persistence_entry.py")

    assert "INSERT INTO" not in source
    assert "INSERT OR REPLACE" not in source
    assert "UPDATE etf_" not in source
    assert "DELETE FROM etf_" not in source


def test_naver_price_preparation_has_no_direct_storage():
    tree = ast.parse(_tracked_source("naver_decimal_price_pipeline.py"))

    forbidden_names = {
        "get_connection",
        "sqlite3",
        "save_etf_price",
        "save_etf_ohlcv_price",
        "executemany",
    }

    for node in ast.walk(tree):
        if isinstance(node, ast.Name):
            assert node.id not in forbidden_names
        if isinstance(node, ast.Attribute):
            assert node.attr not in forbidden_names


def test_naver_raw_observation_has_no_direct_storage():
    tree = ast.parse(_tracked_source("naver_raw_observation.py"))

    forbidden_names = {
        "get_connection",
        "sqlite3",
        "save_etf_price",
        "save_etf_ohlcv_price",
        "executemany",
    }

    for node in ast.walk(tree):
        if isinstance(node, ast.Name):
            assert node.id not in forbidden_names
        if isinstance(node, ast.Attribute):
            assert node.attr not in forbidden_names
