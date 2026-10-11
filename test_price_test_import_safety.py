"""Fail-closed regression tests for imports and DB/provider isolation."""
import os
from pathlib import Path
import subprocess
import sys
import pytest
from price_test_support import isolated_price_db


def test_imports_do_not_open_databases_or_collect_data(tmp_path):
    script = """
import importlib, socket, sqlite3, sys

attempts = []

def deny(*args, **kwargs):
    attempts.append("patched access")
    raise AssertionError("DB/network access during import")

# Audit events also cover direct SQLite construction in this fresh process.
def audit(event, args):
    if event in ("sqlite3.connect", "socket.connect", "socket.getaddrinfo"):
        attempts.append(event)
        raise AssertionError("DB/network audit event during import: " + event)

sys.addaudithook(audit)
sqlite3.connect = deny
sqlite3.dbapi2.connect = deny
socket.socket.connect = deny
socket.socket.connect_ex = deny
socket.create_connection = deny
socket.getaddrinfo = deny
import FinanceDataReader
assert FinanceDataReader.__file__, "Real FinanceDataReader was not imported"
FinanceDataReader.DataReader = deny
FinanceDataReader.StockListing = deny
for name in (
    "test_bulk_price_collector", "test_price_collector", "test_database",
    "test_provider", "test_collector", "test_insert_etf_info",
    "test_dashboard_api", "test_dashboard_data", "test_dashboard_json",
    "test_intelligence_summary", "test_intelligence_universe", "test_multi_ranking",
    "test_ranking_prediction", "test_universe_ranking",
    "test_step6_10_g_outcome_lifecycle", "test_step6_10_g_portfolio_outcome_integration",
    "test_step6_operational_lifecycle_readiness", "test_step6_same_date_evaluation_idempotency",
    "test_phase8_6_g_runtime_learning_readback_contract",
    "collector.bulk_price_collector", "collector.price_collector",
    "collector.etf_collector", "repository", "database", "providers.fdr_provider",
):
    importlib.import_module(name)
assert not attempts, attempts
print("REAL_FDR_IMPORT_SAFE")
"""
    result = subprocess.run([sys.executable, "-B", "-c", script],
                            cwd=tmp_path,
                            env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1",
                                     PYTHONPATH=str(Path(__file__).resolve().parent)),
                            capture_output=True, text=True, timeout=30)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "REAL_FDR_IMPORT_SAFE" in result.stdout


@pytest.mark.parametrize("entrypoint", ["connect", "dbapi2"])
def test_virtual_path_is_rejected_before_open(isolated_price_db, entrypoint):
    import sqlite3

    path = isolated_price_db.path.parent / "nonexistent-forbidden" / "virtual.db"
    connect = sqlite3.connect if entrypoint == "connect" else sqlite3.dbapi2.connect
    before = len(isolated_price_db.accesses)
    with pytest.raises(AssertionError, match="outside the isolated"):
        connect(path)
    assert len(isolated_price_db.accesses) == before


def test_live_fdr_is_blocked(isolated_price_db):
    import FinanceDataReader as fdr

    for call in (lambda: fdr.DataReader("111111", "2026-01-01", "2026-01-05"),
                 lambda: fdr.StockListing("ETF/KR")):
        with pytest.raises(AssertionError, match="External FDR"):
            call()


@pytest.mark.parametrize("entrypoint", ["connect", "dbapi2"])
def test_attach_is_denied(isolated_price_db, entrypoint):
    import sqlite3

    connect = sqlite3.connect if entrypoint == "connect" else sqlite3.dbapi2.connect
    target = isolated_price_db.path.parent / "virtual-attach.db"
    conn = connect(isolated_price_db.path)
    try:
        with pytest.raises(sqlite3.DatabaseError, match="not authorized"):
            conn.execute("ATTACH DATABASE ? AS forbidden", (str(target),))
        assert not target.exists()
        assert [row[1] for row in conn.execute("PRAGMA database_list")] == ["main"]
    finally:
        conn.close()


@pytest.mark.parametrize("entrypoint", ["connect", "connect_ex", "create_connection", "getaddrinfo"])
def test_network_entrypoints_are_blocked(isolated_price_db, entrypoint):
    import socket

    with pytest.raises(AssertionError, match="Network access"):
        if entrypoint in ("connect", "connect_ex"):
            with socket.socket() as sock:
                getattr(sock, entrypoint)(("192.0.2.1", 443))
        elif entrypoint == "create_connection":
            socket.create_connection(("192.0.2.1", 443))
        else:
            socket.getaddrinfo("192.0.2.1", 443)



def test_isolation_fixture_restores_paths_and_guards(tmp_path):
    import config
    import database
    import socket
    import sqlite3

    original_paths = (config.DATABASE_PATH, database.DATABASE_PATH)
    original_connections = (sqlite3.connect, sqlite3.dbapi2.connect)
    original_network = (socket.socket.connect, socket.socket.connect_ex,
                        socket.create_connection, socket.getaddrinfo)
    generator = None
    with pytest.MonkeyPatch.context() as patches:
        try:
            generator = isolated_price_db.__wrapped__(tmp_path, patches)
            isolated = next(generator)
            assert config.DATABASE_PATH == database.DATABASE_PATH == isolated.path
            conn = database.get_connection()
            try:
                assert Path(conn.execute("PRAGMA database_list").fetchone()[2]).resolve() == isolated.path
            finally:
                conn.close()
        finally:
            if generator is not None:
                generator.close()
    assert (config.DATABASE_PATH, database.DATABASE_PATH) == original_paths
    assert (sqlite3.connect, sqlite3.dbapi2.connect) == original_connections
    assert (socket.socket.connect, socket.socket.connect_ex,
            socket.create_connection, socket.getaddrinfo) == original_network
