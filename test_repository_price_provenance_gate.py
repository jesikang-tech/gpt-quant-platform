"""Database-free regression tests for the real repository persistence gate."""

import importlib.util
from pathlib import Path
import sqlite3
import sys
from types import ModuleType

import pytest

from core.price_provenance_gate import (
    PriceProvenanceRejected,
    assess_price_provenance,
    require_persistence_authorization,
)


@pytest.fixture
def guarded_repository(monkeypatch, tmp_path):
    root = Path(__file__).resolve().parent
    attempts = []

    def forbidden_connection(*args, **kwargs):
        attempts.append((args, kwargs))
        raise AssertionError("Database connection or persistence attempted")

    def load_source(name, filename):
        spec = importlib.util.spec_from_file_location(name, root / filename)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    with monkeypatch.context() as patch:
        # Avoid config.py's import-time directory creation and operational path.
        config = ModuleType("config")
        config.DATABASE_PATH = tmp_path / "never-opened.db"
        patch.setitem(sys.modules, "config", config)
        patch.setattr(sqlite3, "connect", forbidden_connection)
        patch.setattr(sqlite3.dbapi2, "connect", forbidden_connection)
        patch.setattr(sqlite3, "Connection", forbidden_connection)
        database = load_source("repository_gate_database_subject", "database.py")
        patch.setattr(database, "get_connection", forbidden_connection)
        patch.setitem(sys.modules, "database", database)
        repository = load_source("repository_gate_subject", "repository.py")
        patch.setattr(repository, "get_connection", forbidden_connection)
        assert repository.assess_price_provenance is assess_price_provenance
        assert repository.require_persistence_authorization is require_persistence_authorization
        assert attempts == []
        yield repository, attempts


def test_save_etf_price_rejects_before_database_access(guarded_repository):
    repository, attempts = guarded_repository
    with pytest.raises(PriceProvenanceRejected) as rejected:
        repository.save_etf_price("SYNTHETIC", "2026-01-02", 100.0)
    assert str(rejected.value) == (
        "Price provenance is unverified; persistence is prohibited"
    )
    # No connection can be obtained, so no cursor, SQL, or commit is reachable.
    assert attempts == []


def test_save_etf_ohlcv_price_rejects_before_database_access(guarded_repository):
    repository, attempts = guarded_repository
    with pytest.raises(PriceProvenanceRejected) as rejected:
        repository.save_etf_ohlcv_price(
            "SYNTHETIC", "2026-01-02", 99.0, 101.0, 98.0, 100.0, 10.0,
        )
    assert str(rejected.value) == (
        "Price provenance is unverified; persistence is prohibited"
    )
    assert attempts == []
