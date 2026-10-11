"""Opt-in test isolation, not a general SQLite security boundary.

Direct sqlite3.Connection construction and previously cached connect aliases are
not intercepted by this fixture. Connections returned here deny SQL ATTACH;
callers can remove that authorizer, so only trusted test code should use them.
"""
from pathlib import Path
from types import SimpleNamespace
import sqlite3
import socket
import pytest


@pytest.fixture
def isolated_price_db(tmp_path, monkeypatch):
    path = (tmp_path / "prices.db").resolve()
    original_connect = sqlite3.connect
    accesses = []

    def guarded_connect(database, *args, **kwargs):
        if str(database).startswith("file:") or Path(database).resolve() != path:
            raise AssertionError("SQLite access outside the isolated test DB")
        accesses.append(path)
        conn = original_connect(database, *args, **kwargs)
        conn.set_authorizer(
            lambda action, *unused: sqlite3.SQLITE_DENY
            if action == sqlite3.SQLITE_ATTACH else sqlite3.SQLITE_OK
        )
        return conn

    monkeypatch.setattr(sqlite3, "connect", guarded_connect)
    monkeypatch.setattr(sqlite3.dbapi2, "connect", guarded_connect)

    def deny_network(*args, **kwargs):
        raise AssertionError("Network access is forbidden in automatic tests")

    monkeypatch.setattr(socket.socket, "connect", deny_network)
    monkeypatch.setattr(socket.socket, "connect_ex", deny_network)
    monkeypatch.setattr(socket, "create_connection", deny_network)
    monkeypatch.setattr(socket, "getaddrinfo", deny_network)
    import config
    import database
    import FinanceDataReader as fdr

    def deny_external(*args, **kwargs):
        raise AssertionError("External FDR requests are forbidden in automatic tests")

    monkeypatch.setattr(fdr, "DataReader", deny_external)
    monkeypatch.setattr(fdr, "StockListing", deny_external)
    monkeypatch.setattr(config, "DATABASE_PATH", path)
    monkeypatch.setattr(database, "DATABASE_PATH", path)
    database.init_database()
    yield SimpleNamespace(path=path, connect=database.get_connection, accesses=accesses)
    assert accesses and all(access == path for access in accesses)


@pytest.fixture
def isolated_evaluation_api(isolated_price_db, monkeypatch):
    """All repository connections remain guarded; audit persistence stays real."""
    import json
    import api_server
    from testing_helpers import authenticated_client

    monkeypatch.setattr(api_server.app, "secret_key", "isolated-evaluation-session")
    client = authenticated_client(api_server.app)

    def audit_count():
        conn = isolated_price_db.connect()
        try:
            return conn.execute("SELECT COUNT(*) FROM audit_event").fetchone()[0]
        finally:
            conn.close()

    def assert_audit(before, signal):
        conn = isolated_price_db.connect()
        try:
            rows = conn.execute(
                "SELECT event_type, source, status, outcome_history_id, "
                "correlation_key, details FROM audit_event ORDER BY id"
            ).fetchall()
            assert len(rows) == before + 1
            event = rows[-1]
            assert event[:5] == ("LEARNING_SIGNAL_GENERATED",
                                "portfolio_outcome_evaluation", "GENERATED", 12, "outcome:12")
            details = json.loads(event[5])
            assert details["learning_signal"] == signal
            assert details["adaptive_learning_required"] == (signal == "NEGATIVE")
            assert details["reassessment_required"] == (signal == "NEGATIVE")
        finally:
            conn.close()

    return SimpleNamespace(api=api_server, client=client, audit_count=audit_count,
                           assert_audit=assert_audit, db=isolated_price_db)
