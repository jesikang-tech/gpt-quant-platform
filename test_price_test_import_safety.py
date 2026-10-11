"""Fail-closed regression tests for imports and DB/provider isolation."""
import os
from pathlib import Path
import subprocess
import sys
import pytest
from price_test_support import isolated_price_db, isolated_evaluation_api


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
    "test_step6_10_i5_audit_persistence_design",
    "test_step6_10_i8_audit_event_table_design",
    "test_step6_10_i9_audit_migration_safety_contract",
    "test_etf_ohlcv_persistence", "test_incremental_price_updater_contract", "test_incremental_price_updater_db_contract", "test_incremental_price_updater_update_contract", "test_price_collection_date_safety", "test_price_collection_operational_safety",
    'test_step6_history_snapshot_lifecycle_repository', 'test_step6_history_snapshot_retention_repository', 'test_step6_history_snapshot_referential_integrity',
    "test_step6_partial_evaluation_completion_contract", "test_step6_cleanup_candidate_repository",
    "test_ver11_snapshot_contract", "test_historical_replay_portfolio_contract",
    "test_historical_reality_test", "test_historical_replay_read_only", "test_historical_replay",
    "test_ver11_analysis_sort_contract", "test_close_only_reality_test",
    "test_ohlcv_backfill", "test_price_quality", "test_price_quality_boundary",
    "test_api_server",
    "test_historical_replay_api_contract", "test_ver11_analysis_api_contract",
    "test_platform_auth", "test_step6_10_g_canonical_signal_bridge_regression",
    "test_bulk_price_collector", "test_price_collector", "test_database",
    "test_provider", "test_collector", "test_insert_etf_info",
    "test_portfolio_optimization", "test_portfolio_explainability_api", "test_portfolio_chat_api",
    "test_dashboard_api", "test_dashboard_data", "test_dashboard_json",
    "test_intelligence_summary", "test_intelligence_universe", "test_multi_ranking",
    "test_ranking_prediction", "test_universe_ranking",
    "test_price_database", "test_ranking_history", "test_market_regime", "test_portfolio_advisor",
    "test_ranking_analytics", "test_recommendation", "test_step6_10_h8_repository_integrated_safety",
    "test_step6_history_snapshot_lifecycle_classification", "test_step6_retention_classification_contract",
    "test_step6_10_g_api_integration", "test_step6_10_g_collector_persistence",
    "test_phase8_7_runtime_outcome_decision_closed_loop_contract",
    "test_portfolio_history_persistence_contract",
    "test_step8_decision_intelligence_get_read_only_contract",
    "test_step8_decision_intelligence_post_persistence_contract",
    "_step7_10_18_q_api_integration_boundary_test",
    "_step7_10_20_23_api_runtime_outcome_closed_loop_boundary_contract_test",
    "_step7_10_20_24_outcome_history_portfolio_persistence_boundary_contract_test",
    "_step7_10_20_25_evaluation_waiting_boundary_contract_test",
    "_step7_10_20_26_api_waiting_boundary_contract_test",
    "test_step6_10_g_outcome_lifecycle", "test_step6_10_g_portfolio_outcome_integration",
    "test_step6_operational_lifecycle_readiness", "test_step6_same_date_evaluation_idempotency",
    "test_phase8_6_g_runtime_learning_readback_contract",
    "test_step7_10_18_s_outcome_history_readiness_projection_contract",
    "test_step6_transaction_persistence", "test_step6_snapshot_validation_persistence",
    "test_database_summary", "test_score_history", "test_ranking_snapshot", "test_score_detail",
    "test_step6_10_i33_audit_lifecycle_completeness_api_value_projection_boundary",
    "test_step6_10_i34_audit_events_api_value_projection_boundary",
    "test_step6_10_i35_audit_timeline_duplicate_row_preservation_boundary",

    "test_step6_10_i29_audit_timeline_deterministic_tie_break_ordering_boundary",
    "test_step6_10_i30_audit_timeline_default_limit_projection_boundary",
    "test_step6_10_i31_audit_lifecycle_completeness_limited_projection_boundary",
    "test_step6_10_i32_audit_lifecycle_completeness_filter_limit_intersection_boundary",

    "test_step6_10_i25_audit_read_api_identifier_value_boundary",
    "test_step6_10_i26_audit_timeline_details_projection_boundary",
    "test_step6_10_i27_audit_timeline_details_api_projection_boundary",
    "test_step6_10_i28_audit_timeline_limit_prefix_projection_boundary",

    "test_step6_10_i21_audit_lifecycle_read_api_boundary_contract",
    "test_step6_10_i22_audit_read_api_input_validation_boundary",
    "test_step6_10_i23_audit_lifecycle_read_api_response_schema_boundary",
    "test_step6_10_i24_audit_read_api_query_filter_intersection_boundary",

    "test_step6_10_i17_audit_event_read_boundary_contract",
    "test_step6_10_i18_audit_lifecycle_timeline_projection_boundary",
    "test_step6_10_i19_audit_lifecycle_completeness_boundary",
    "test_step6_10_i20_audit_lifecycle_completeness_boundary",

    "test_step6_10_i12_runtime_outcome_evaluation_audit_persistence",
    "test_step6_10_i13_runtime_adaptive_strategy_audit_persistence",
    "test_step6_10_i14_runtime_reassessment_audit_persistence",
    "test_step6_10_i15_end_to_end_audit_lifecycle_persistence",
    "test_step6_10_i16_runtime_reassessment_audit_persistence_contract",

    "test_phase8_6_a_runtime_evaluation_persistence",
    "test_phase8_6_b_runtime_evaluation_rollback",
    "test_phase8_6_c_runtime_evaluation_partial_audit",
    "test_phase8_6_d_runtime_evaluation_learning_propagation",
    "test_phase8_6_e_runtime_evaluation_idempotency",
    "test_phase8_6_f_runtime_readback_contract",

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
            import api_server
            original_secret = api_server.app.secret_key
            api_functions = (api_server.get_ai_decision_history,
                             api_server.get_ai_decision_outcome_history,
                             api_server.save_ai_decision_outcome_with_portfolio_transaction,
                             api_server.update_ai_decision_outcome_history,
                             api_server.save_ai_decision_audit_event)
            isolated_evaluation_api.__wrapped__(isolated, patches)
            conn = database.get_connection()
            try:
                assert Path(conn.execute("PRAGMA database_list").fetchone()[2]).resolve() == isolated.path
            finally:
                conn.close()
        finally:
            if generator is not None:
                generator.close()
    assert not isolated.path.exists()
    assert (config.DATABASE_PATH, database.DATABASE_PATH) == original_paths
    assert (sqlite3.connect, sqlite3.dbapi2.connect) == original_connections
    assert (socket.socket.connect, socket.socket.connect_ex,
            socket.create_connection, socket.getaddrinfo) == original_network

    assert api_server.app.secret_key == original_secret
    assert (api_server.get_ai_decision_history, api_server.get_ai_decision_outcome_history,
            api_server.save_ai_decision_outcome_with_portfolio_transaction,
            api_server.update_ai_decision_outcome_history,
            api_server.save_ai_decision_audit_event) == api_functions


@pytest.mark.parametrize("interrupt", [False, True])
def test_portfolio_auth_and_helper_restore_shared_state(isolated_price_db, tmp_path, interrupt):
    import api_server
    import config
    import database
    import repository
    from price_test_support import synthetic_portfolio_db, isolated_portfolio_api
    from testing_helpers import authenticated_client

    original = (api_server.app.secret_key, api_server.AUTH_CONFIG_PATH,
                config.DATABASE_PATH, database.DATABASE_PATH, repository.get_connection)
    data = synthetic_portfolio_db.__wrapped__(isolated_price_db)
    generator = isolated_portfolio_api.__wrapped__(data, tmp_path)
    try:
        context = next(generator)
        assert context.api.AUTH_CONFIG_PATH == context.auth_path
        assert context.auth_path.parent == tmp_path
        authenticated_client(context.api.app)
        assert context.api.app.secret_key == "test-auth-session-secret-key"
        if interrupt:
            with pytest.raises(RuntimeError, match="synthetic interruption"):
                generator.throw(RuntimeError("synthetic interruption"))
    finally:
        generator.close()
    assert (api_server.app.secret_key, api_server.AUTH_CONFIG_PATH,
            config.DATABASE_PATH, database.DATABASE_PATH, repository.get_connection) == original


@pytest.mark.parametrize("interrupt", [False, True])
def test_phase8_scope_restores_functions_and_closes_connections(isolated_price_db, interrupt):
    import sqlite3
    from contextlib import nullcontext
    from price_test_support import phase8_test_scope
    from testing_helpers import authenticated_client

    expected = pytest.raises(RuntimeError, match="synthetic interruption") if interrupt else nullcontext()
    with expected:
        with phase8_test_scope(isolated_price_db) as scope:
            from contextlib import closing
            with closing(scope.database.get_connection()) as conn:
                assert Path(conn.execute("PRAGMA database_list").fetchone()[2]).resolve() == isolated_price_db.path
            memory_conn = scope.memory()
            assert memory_conn.execute("PRAGMA database_list").fetchone()[2] == ""
            with pytest.raises(sqlite3.DatabaseError, match="not authorized"):
                memory_conn.execute("ATTACH DATABASE ? AS forbidden", (str(isolated_price_db.path.parent / "virtual-phase8.db"),))
            scope.patches.setattr(scope.config, "DATABASE_PATH", isolated_price_db.path.parent / "virtual-config.db")
            scope.patches.setattr(scope.database, "DATABASE_PATH", isolated_price_db.path.parent / "virtual-database.db")
            scope.patches.setattr(scope.repository, "get_connection", lambda: None)
            scope.patches.setattr(scope.repository, "save_ai_decision_portfolio_evaluation_transaction", lambda: None)
            scope.patches.setattr(scope.api, "evaluate_ai_decision_portfolio_snapshot", lambda: None)
            authenticated_client(scope.api.app)
            if interrupt:
                raise RuntimeError("synthetic interruption")


@pytest.mark.parametrize("interrupt", [False, True])
def test_audit_scope_blocks_fallback_and_restores_after_failure(isolated_price_db, interrupt):
    from contextlib import nullcontext
    import sqlite3
    from price_test_support import phase8_test_scope

    expected = pytest.raises(RuntimeError, match="synthetic audit interruption") if interrupt else nullcontext()
    with expected:
        with phase8_test_scope(isolated_price_db) as scope:
            for connect in (sqlite3.connect, sqlite3.dbapi2.connect):
                with pytest.raises(AssertionError, match="outside the isolated"):
                    connect(isolated_price_db.path.parent / "virtual-audit-forbidden.db")
            scope.repository.save_ai_decision_audit_event(
                "TEST_AUDIT", "2026-01-06T12:00:00+00:00", "synthetic_test",
                status="GENERATED", outcome_history_id=1)
            with pytest.raises(ValueError, match="event_time is required"):
                scope.repository.save_ai_decision_audit_event("TEST_FAILURE", "", "synthetic_test")
            conn = scope.database.get_connection()
            assert Path(conn.execute("PRAGMA database_list").fetchone()[2]).resolve() == isolated_price_db.path
            assert conn.execute("SELECT COUNT(*) FROM audit_event").fetchone()[0] == 1
            # Deliberately leave this handle open: the scope must close it on either exit.
            scope.patches.setattr(scope.config, "DATABASE_PATH", isolated_price_db.path.parent / "virtual-config.db")
            scope.patches.setattr(scope.database, "DATABASE_PATH", isolated_price_db.path.parent / "virtual-database.db")
            if interrupt:
                raise RuntimeError("synthetic audit interruption")


@pytest.mark.parametrize("failure", [None, "assertion", "sql"])
def test_audit_api_scope_restores_after_test_failure(isolated_price_db, failure):
    import sqlite3
    from contextlib import nullcontext
    from price_test_support import phase8_test_scope
    from testing_helpers import authenticated_client

    expected = (pytest.raises(AssertionError, match="synthetic assertion") if failure == "assertion"
                else pytest.raises(sqlite3.OperationalError, match="no such table") if failure == "sql"
                else nullcontext())
    with expected:
        with phase8_test_scope(isolated_price_db) as scope:
            original_auth = scope.api.AUTH_CONFIG_PATH
            client = authenticated_client(scope.api.app)
            count = len(scope.handles)
            response = client.get("/api/ai-decision/audit-events")
            assert response.status_code == 400
            assert len(scope.handles) > count  # Invalid input still opens a guarded repository connection.
            conn = sqlite3.connect(isolated_price_db.path)
            assert Path(conn.execute("PRAGMA database_list").fetchone()[2]).resolve() == isolated_price_db.path
            with pytest.raises(AssertionError, match="outside the isolated"):
                sqlite3.connect(isolated_price_db.path.parent / "virtual-api-forbidden.db")
            if failure == "assertion":
                raise AssertionError("synthetic assertion")
            if failure == "sql":
                conn.execute("SELECT * FROM synthetic_missing_table")
    assert scope.api.AUTH_CONFIG_PATH == original_auth


@pytest.mark.parametrize("interrupt", [False, True])
def test_isolated_db_cleans_own_files_on_generator_exit(tmp_path, interrupt):
    generator = None
    with pytest.MonkeyPatch.context() as patches:
        try:
            generator = isolated_price_db.__wrapped__(tmp_path, patches)
            db = next(generator)
            assert db.path.exists()
            if interrupt:
                with pytest.raises(RuntimeError, match="synthetic fixture failure"):
                    generator.throw(RuntimeError("synthetic fixture failure"))
        finally:
            if generator is not None:
                generator.close()
    assert not db.path.exists()
    assert all(not db.path.with_name(db.path.name + suffix).exists()
               for suffix in ("-journal", "-wal", "-shm"))


@pytest.mark.parametrize("module_name,builder_name,test_name", [
    ("test_step6_transaction_persistence", "build_test_db", "test_transaction_persistence"),
    ('test_step6_history_snapshot_lifecycle_repository', 'build_db', 'test_snapshot_lifecycle_repository'),
    ('test_step6_history_snapshot_retention_repository', 'build_db', 'test_snapshot_retention_repository'),
    ('test_step6_history_snapshot_referential_integrity', 'build_db', 'test_snapshot_referential_integrity'),
    ('test_step6_10_i5_audit_persistence_design', 'build_db', 'test_i5_audit_persistence_design'),
    ('test_step6_10_i8_audit_event_table_design', 'build_db', 'test_i8_audit_event_table_design'),
    ('test_step6_10_i9_audit_migration_safety_contract', 'build_existing_db', 'test_i9_audit_migration_safety_contract'),
    ("test_step6_snapshot_validation_persistence", "build_db", "test_snapshot_validation_persistence"),
])
@pytest.mark.parametrize("failure", ["assertion", "sql"])
def test_persistence_scope_closes_memory_on_failure(
        isolated_price_db, monkeypatch, module_name, builder_name, test_name, failure):
    import importlib
    import sqlite3
    import repository

    module = importlib.import_module(module_name)
    original_connection = repository.get_connection
    original_builder = getattr(module, builder_name)
    handles = []

    def fail_after_build(scope):
        conn = original_builder(scope)
        handles.append(conn)
        scope.patches.setattr(repository, "get_connection", lambda: conn)
        if failure == "assertion":
            raise AssertionError("synthetic persistence interruption")
        conn.execute("SELECT * FROM synthetic_missing_table")

    monkeypatch.setattr(module, builder_name, fail_after_build)
    error = AssertionError if failure == "assertion" else sqlite3.OperationalError
    message = "synthetic persistence interruption" if failure == "assertion" else "no such table"
    with pytest.raises(error, match=message):
        getattr(module, test_name)(isolated_price_db)
    assert repository.get_connection is original_connection
    assert len(handles) == 1
    with pytest.raises(sqlite3.ProgrammingError, match="closed"):
        handles[0].execute("SELECT 1")


@pytest.mark.parametrize("failure", [None, "assertion", "api"])
def test_readiness_projection_restores_state(isolated_price_db, monkeypatch, failure):
    import sqlite3
    from contextlib import nullcontext
    import api_server
    import test_step7_10_18_s_outcome_history_readiness_projection_contract as target

    original = (api_server.get_ai_decision_outcome_history,
                api_server.get_ai_decision_outcome_history_by_id,
                api_server.app.secret_key, api_server.AUTH_CONFIG_PATH,
                dict(api_server.app.config))
    original_make_row = target.make_row
    handles = []

    def checked_row(history_id, readiness):
        for connect in (sqlite3.connect, sqlite3.dbapi2.connect):
            with pytest.raises(AssertionError, match="outside the isolated"):
                connect(isolated_price_db.path.parent / "virtual-readiness-forbidden.db")
        conn = sqlite3.connect(isolated_price_db.path)
        handles.append(conn)
        if failure == "assertion":
            row = list(original_make_row(history_id, readiness))
            row[34] = "WRONG_READINESS"
            return tuple(row)
        if failure == "api":
            raise RuntimeError("synthetic readiness API failure")
        return original_make_row(history_id, readiness)

    monkeypatch.setattr(target, "make_row", checked_row)
    # Flask returns HTTP 500 for the injected API exception; the original
    # response-status assertion must fail rather than treating it as success.
    with pytest.raises(AssertionError) if failure else nullcontext():
        target.test_outcome_history_readiness_projection(isolated_price_db)
    assert (api_server.get_ai_decision_outcome_history,
            api_server.get_ai_decision_outcome_history_by_id,
            api_server.app.secret_key, api_server.AUTH_CONFIG_PATH,
            dict(api_server.app.config)) == original
    assert handles
    for conn in handles:
        with pytest.raises(sqlite3.ProgrammingError, match="closed"):
            conn.execute("SELECT 1")
    with api_server.app.test_client() as client:
        assert client.get("/api/ai-decision/outcome-history").status_code == 401


@pytest.mark.parametrize("module_name", [
    "test_platform_auth", "test_step6_10_g_canonical_signal_bridge_regression",
    "test_historical_replay_api_contract", "test_ver11_analysis_api_contract",
    "test_api_server",
    "test_ver11_snapshot_contract", "test_historical_replay_portfolio_contract",
    "test_historical_reality_test", "test_historical_replay_read_only", "test_historical_replay",
    "test_ver11_analysis_sort_contract", "test_close_only_reality_test",
    "test_ohlcv_backfill", "test_price_quality", "test_price_quality_boundary",
])
@pytest.mark.parametrize("failure", [None, "assertion", "api", "sql"])
def test_auth_module_fixture_restores_flask_state(isolated_price_db, module_name, failure):
    import importlib
    import sqlite3
    import api_server
    from core.platform_auth import save_auth_config, create_password_hash, configure_flask_auth
    from testing_helpers import authenticated_client

    module = importlib.import_module(module_name)
    original = (dict(api_server.app.config), api_server.AUTH_CONFIG_PATH,
                api_server.get_ai_decision_history, api_server.get_ai_decision_outcome_history,
                api_server.get_current_analysis_data, api_server.get_dashboard_api_data)
    with pytest.MonkeyPatch.context() as patches:
        generator = module._protected_flask_state.__wrapped__(isolated_price_db, patches)
        scope = next(generator)
        try:
            path = isolated_price_db.path.parent / "synthetic-auth.json"
            save_auth_config(create_password_hash("1234"), create_password_hash("1234567", admin=True), path)
            configure_flask_auth(api_server.app, path)
            patches.setattr(api_server, "AUTH_CONFIG_PATH", path)
            client = authenticated_client(api_server.app)
            for connect in (sqlite3.connect, sqlite3.dbapi2.connect):
                with pytest.raises(AssertionError, match="outside the isolated"):
                    connect(path.parent / "virtual-auth-forbidden.db")
            if failure == "assertion":
                with pytest.raises(AssertionError, match="synthetic auth interruption"):
                    generator.throw(AssertionError("synthetic auth interruption"))
            elif failure == "sql":
                conn = scope.memory()
                with pytest.raises(sqlite3.OperationalError, match="no such table") as caught:
                    conn.execute("SELECT * FROM synthetic_missing_table")
                with pytest.raises(sqlite3.OperationalError, match="no such table"):
                    generator.throw(caught.value)
            elif failure == "api":
                def fail_query(*args, **kwargs):
                    raise RuntimeError("synthetic auth API failure")
                if module_name in ("test_historical_replay_api_contract", "test_ver11_analysis_api_contract",
                                   "test_ver11_snapshot_contract", "test_historical_replay_portfolio_contract",
                                   "test_historical_reality_test", "test_historical_replay_read_only"):
                    scope.patches.setattr(api_server, "get_current_analysis_data", fail_query)
                    route = "/api/historical-replay" if "historical" in module_name else "/api/ver11-analysis"
                    response = (client.post("/api/ver11-analysis/snapshots?date=2026-09-04&period=3m")
                                if module_name == "test_ver11_snapshot_contract"
                                else client.get(route + "?date=2026-09-04&period=3m"))
                    assert response.status_code == 500
                    assert response.get_json()["message"] == "synthetic auth API failure"
                    with pytest.raises(RuntimeError, match="synthetic auth API failure"):
                        generator.throw(RuntimeError("synthetic auth API failure"))
                elif module_name == "test_api_server":
                    scope.patches.setattr(api_server, "get_dashboard_api_data", fail_query)
                    scope.patches.setattr(api_server.app, "testing", True)
                    with pytest.raises(RuntimeError, match="synthetic auth API failure") as caught:
                        client.get("/api/ranking")
                    with pytest.raises(RuntimeError, match="synthetic auth API failure"):
                        generator.throw(caught.value)
                else:
                    scope.patches.setattr(api_server, "get_ai_decision_history", fail_query)
                    scope.patches.setattr(api_server.app, "testing", True)
                    with pytest.raises(RuntimeError, match="synthetic auth API failure") as caught:
                        client.get("/api/ai-decision/adaptive-strategy")
                    with pytest.raises(RuntimeError, match="synthetic auth API failure"):
                        generator.throw(caught.value)
        finally:
            generator.close()
    assert (dict(api_server.app.config), api_server.AUTH_CONFIG_PATH,
            api_server.get_ai_decision_history, api_server.get_ai_decision_outcome_history,
                api_server.get_current_analysis_data, api_server.get_dashboard_api_data) == original
    with api_server.app.test_client() as client:
        assert client.get("/api/ranking").status_code == 401


@pytest.mark.parametrize("module_name", ['test_etf_ohlcv_persistence', 'test_incremental_price_updater_contract', 'test_incremental_price_updater_db_contract', 'test_incremental_price_updater_update_contract', 'test_price_collection_date_safety', 'test_price_collection_operational_safety'])
@pytest.mark.parametrize("failure", [None, "assertion", "sql"])
def test_collection_scope_restores_after_failure(isolated_price_db, module_name, failure):
    import importlib
    import sqlite3
    import FinanceDataReader as fdr
    import collector.incremental_price_updater as updater
    import repository
    import database
    import config

    target = importlib.import_module(module_name)
    original = (updater.get_connection, repository.get_connection, database.get_connection,
                config.DATABASE_PATH, database.DATABASE_PATH)
    generator = target._protected_collection.__wrapped__(isolated_price_db)
    scope = next(generator)
    try:
        conn = scope.memory()
        for connect in (sqlite3.connect, sqlite3.dbapi2.connect):
            with pytest.raises(AssertionError, match="outside the isolated"):
                connect(scope.db.path.parent / "virtual-collection-forbidden.db")
        with pytest.raises(AssertionError, match="External FDR"):
            fdr.StockListing("ETF/KR")
        scope.patches.setattr(updater, "get_connection", lambda: conn)
        if failure == "assertion":
            with pytest.raises(AssertionError, match="synthetic collection failure"):
                generator.throw(AssertionError("synthetic collection failure"))
        elif failure == "sql":
            with pytest.raises(sqlite3.OperationalError) as caught:
                conn.execute("SELECT * FROM synthetic_missing_table")
            with pytest.raises(sqlite3.OperationalError):
                generator.throw(caught.value)
    finally:
        generator.close()
    assert (updater.get_connection, repository.get_connection, database.get_connection,
            config.DATABASE_PATH, database.DATABASE_PATH) == original
    with pytest.raises(sqlite3.ProgrammingError, match="closed"):
        conn.execute("SELECT 1")


def test_only_exact_isolated_readonly_uri_is_allowed(isolated_price_db):
    import sqlite3

    uri = isolated_price_db.path.as_uri() + "?mode=ro"
    conn = sqlite3.connect(uri, uri=True)
    try:
        assert conn.execute("SELECT COUNT(*) FROM etf_prices").fetchone()[0] == 0
        with pytest.raises(sqlite3.OperationalError, match="readonly"):
            conn.execute("INSERT INTO etf_prices VALUES ('TEST', '2026-01-01', 100)")
        with pytest.raises(sqlite3.DatabaseError, match="not authorized"):
            conn.execute("ATTACH DATABASE ':memory:' AS forbidden")
    finally:
        conn.close()
    for forbidden in (isolated_price_db.path.as_uri() + "?mode=rw",
                      (isolated_price_db.path.parent / "virtual-uri.db").as_uri() + "?mode=ro"):
        with pytest.raises(AssertionError, match="outside the isolated"):
            sqlite3.connect(forbidden, uri=True)
    with pytest.raises(AssertionError, match="outside the isolated"):
        sqlite3.connect(uri)


@pytest.mark.parametrize("module_name,test_name,query_name", [
    ("test_step6_partial_evaluation_completion_contract", "test_partial_evaluation_completion",
     "evaluate_ai_decision_portfolio_snapshot"),
    ("test_step6_cleanup_candidate_repository", "test_cleanup_candidate_repository",
     "get_ai_decision_history_snapshot_cleanup_candidates"),
])
@pytest.mark.parametrize("failure", [None, "assertion", "sql"])
def test_partial_cleanup_scope_restores_after_failure(
        isolated_price_db, module_name, test_name, query_name, failure):
    import importlib
    import sqlite3
    from contextlib import nullcontext
    import repository

    target = importlib.import_module(module_name)
    original = (repository.get_connection, repository.get_ai_decision_history_snapshot_retention,
                getattr(repository, query_name))
    handles = []

    def checked_query(*args, **kwargs):
        with pytest.raises(AssertionError, match="outside the isolated"):
            sqlite3.connect(isolated_price_db.path.parent / "virtual-partial-cleanup.db")
        conn = sqlite3.connect(isolated_price_db.path)
        handles.append(conn)
        if failure == "assertion":
            raise AssertionError("synthetic partial cleanup failure")
        if failure == "sql":
            conn.execute("SELECT * FROM synthetic_missing_table")
        return original[2](*args, **kwargs)

    expected = (pytest.raises(AssertionError, match="synthetic partial cleanup failure")
                if failure == "assertion" else pytest.raises(sqlite3.OperationalError, match="no such table")
                if failure == "sql" else nullcontext())
    with pytest.MonkeyPatch.context() as patches:
        patches.setattr(repository, query_name, checked_query)
        with expected:
            getattr(target, test_name)(isolated_price_db)
    assert (repository.get_connection, repository.get_ai_decision_history_snapshot_retention,
            getattr(repository, query_name)) == original
    assert handles
    for conn in handles:
        with pytest.raises(sqlite3.ProgrammingError, match="closed"):
            conn.execute("SELECT 1")


@pytest.mark.parametrize("filename", ["replay # test.db", "reality.db"])
@pytest.mark.parametrize("failure", [None, "assertion", "sql"])
def test_custom_isolated_filename_cleanup(tmp_path, filename, failure):
    import sqlite3
    from price_test_support import _isolated_price_db

    with pytest.MonkeyPatch.context() as patches:
        generator = _isolated_price_db(tmp_path, patches, filename)
        db = next(generator)
        try:
            conn = sqlite3.connect(db.path.as_uri() + "?mode=ro", uri=True)
            try:
                with pytest.raises(sqlite3.OperationalError, match="readonly"):
                    conn.execute("DELETE FROM etf_prices")
            finally:
                conn.close()
            # Only synthetic sidecars belonging to this temporary DB.
            for suffix in ("-journal", "-wal", "-shm"):
                db.path.with_name(db.path.name + suffix).touch()
            if failure == "assertion":
                with pytest.raises(AssertionError, match="synthetic filename failure"):
                    generator.throw(AssertionError("synthetic filename failure"))
            elif failure == "sql":
                with pytest.raises(sqlite3.OperationalError, match="synthetic filename SQL failure"):
                    generator.throw(sqlite3.OperationalError("synthetic filename SQL failure"))
        finally:
            generator.close()
    assert not db.path.exists()
    assert all(not db.path.with_name(db.path.name + suffix).exists()
               for suffix in ("-journal", "-wal", "-shm"))


@pytest.mark.parametrize("filename", ["..", "../virtual-forbidden.db", "nested/virtual.db"])
def test_isolated_filename_cannot_escape_tmp_path(tmp_path, filename):
    from price_test_support import _isolated_price_db

    with pytest.MonkeyPatch.context() as patches:
        generator = _isolated_price_db(tmp_path, patches, filename)
        try:
            with pytest.raises(AssertionError, match="single leaf name"):
                next(generator)
        finally:
            generator.close()


@pytest.mark.parametrize("allow_readwrite_uri", [False, True])
def test_isolated_db_setup_sql_failure_closes_and_cleans(tmp_path, allow_readwrite_uri):
    import sqlite3
    from price_test_support import _isolated_price_db

    handles = []
    with pytest.MonkeyPatch.context() as patches:
        class SetupFailurePatches:
            def setattr(self, obj, name, value, **kwargs):
                patches.setattr(obj, name, value, **kwargs)
                if getattr(obj, "__name__", None) == "database" and name == "DATABASE_PATH":
                    def fail_init():
                        # This hook is installed only after DB/network guards.
                        conn = sqlite3.connect(value)
                        handles.append(conn)
                        conn.execute("CREATE TABLE synthetic_setup_table(x)")
                        conn.execute("SELECT * FROM synthetic_missing_setup_table")
                    patches.setattr(obj, "init_database", fail_init)
        generator = _isolated_price_db(tmp_path, SetupFailurePatches(), allow_readwrite_uri=allow_readwrite_uri)
        try:
            with pytest.raises(sqlite3.OperationalError, match="no such table"):
                next(generator)
        finally:
            generator.close()
    assert len(handles) == 1
    with pytest.raises(sqlite3.ProgrammingError, match="closed"):
        handles[0].execute("SELECT 1")
    path = tmp_path / "prices.db"
    assert all(not path.with_name(path.name + suffix).exists()
               for suffix in ("", "-journal", "-wal", "-shm"))


@pytest.mark.parametrize("test_name", [
    "test_historical_replay_respects_analysis_date_and_is_deterministic",
    "test_historical_replay_engine_ignores_future_prices",
])
@pytest.mark.parametrize("failure", [None, "assertion", "sql"])
def test_replay_connections_restore_after_failure(isolated_price_db, test_name, failure):
    import sqlite3
    import config
    import database
    import repository
    import api_server
    import test_historical_replay as target

    original = (config.DATABASE_PATH, database.DATABASE_PATH, database.get_connection,
                repository.get_connection, dict(api_server.app.config), api_server.AUTH_CONFIG_PATH)
    handles = []
    with pytest.MonkeyPatch.context() as patches:
        generator = target._protected_flask_state.__wrapped__(isolated_price_db, patches)
        scope = next(generator)
        real_connect = database.get_connection

        class Cursor:
            def __init__(self, cursor):
                self.cursor = cursor

            def executemany(self, *args, **kwargs):
                self.cursor.executemany(*args, **kwargs)
                if failure == "assertion":
                    raise AssertionError("synthetic replay interruption")
                if failure == "sql":
                    self.cursor.execute("SELECT * FROM synthetic_missing_table")

        class Connection:
            def __init__(self, connection):
                self.connection = connection

            def cursor(self):
                return Cursor(self.connection.cursor())

            def commit(self):
                return self.connection.commit()

            def close(self):
                return self.connection.close()

        def connect():
            conn = real_connect()
            handles.append(conn)
            return Connection(conn) if failure else conn

        scope.patches.setattr(database, "get_connection", connect)
        try:
            if failure:
                expected = AssertionError if failure == "assertion" else sqlite3.OperationalError
                with pytest.raises(expected, match="synthetic replay interruption|no such table"):
                    getattr(target, test_name)()
            else:
                getattr(target, test_name)()
            # Explicit closing must work before the scope's final cleanup.
            assert handles
            for conn in handles:
                with pytest.raises(sqlite3.ProgrammingError, match="closed"):
                    conn.execute("SELECT 1")
        finally:
            generator.close()
    assert (config.DATABASE_PATH, database.DATABASE_PATH, database.get_connection,
            repository.get_connection, dict(api_server.app.config), api_server.AUTH_CONFIG_PATH) == original


@pytest.mark.parametrize("module_name", [
    "test_ver11_analysis_sort_contract", "test_close_only_reality_test",
])
@pytest.mark.parametrize("failure", [None, "assertion", "sql"])
def test_sort_close_only_scope_blocks_fallback_and_restores(isolated_price_db, module_name, failure):
    import importlib
    import sqlite3
    import config
    import database
    import current_analysis as analysis
    import api_server

    module = importlib.import_module(module_name)
    names = ("_get_replay_connection", "_normalize_analysis_date", "_get_period_config",
             "get_all_etf_tickers", "_get_etf_name_map", "get_etf_prices", "calculate_return",
             "calculate_return_score", "calculate_trend_score", "calculate_slope_score",
             "calculate_uptrend_ratio", "_get_future_performance", "_get_reality_test")
    functions = tuple(getattr(analysis, name) for name in names)
    original = (config.DATABASE_PATH, database.DATABASE_PATH, dict(api_server.app.config),
                api_server.AUTH_CONFIG_PATH)
    handles = []
    with pytest.MonkeyPatch.context() as patches:
        generator = module._protected_flask_state.__wrapped__(isolated_price_db, patches)
        scope = next(generator)
        real_read = analysis._get_replay_connection

        def read():
            conn = real_read()
            handles.append(conn)
            assert Path(conn.execute("PRAGMA database_list").fetchone()[2]).resolve() == scope.db.path
            with pytest.raises(sqlite3.OperationalError, match="readonly"):
                conn.execute("DELETE FROM etf_prices")
            if failure == "assertion":
                raise AssertionError("synthetic close-only interruption")
            if failure == "sql":
                conn.execute("SELECT * FROM synthetic_missing_table")
            return conn

        scope.patches.setattr(analysis, "_get_replay_connection", read)
        try:
            # Reproduce a default-path fallback using a nonexistent synthetic path.
            virtual = scope.db.path.parent / "virtual-production" / "database" / "etf.db"
            accesses = list(scope.db.accesses)
            with pytest.MonkeyPatch.context() as fallback:
                fallback.setattr(config, "DATABASE_PATH", virtual)
                fallback.setattr(database, "DATABASE_PATH", virtual)
                with pytest.raises(AssertionError, match="outside the isolated"):
                    real_read()
                with pytest.raises(AssertionError, match="outside the isolated"):
                    database.get_connection()
                with pytest.raises(AssertionError, match="outside the isolated"):
                    sqlite3.dbapi2.connect(virtual)
            assert scope.db.accesses == accesses
            assert not virtual.exists()

            def run():
                if module_name == "test_ver11_analysis_sort_contract":
                    module.test_ver11_sort_is_applied_before_limit(scope.patches, "final_score", "FINAL")
                else:
                    market = module.close_market.__wrapped__(scope)
                    module.test_close_only_complete_window(market, "1m", 20, 5)

            if failure:
                expected = AssertionError if failure == "assertion" else sqlite3.OperationalError
                with pytest.raises(expected, match="synthetic close-only interruption|no such table"):
                    run()
            else:
                run()
            assert handles, "The real Close-only read path must be exercised"
        finally:
            generator.close()
    assert tuple(getattr(analysis, name) for name in names) == functions
    assert (config.DATABASE_PATH, database.DATABASE_PATH, dict(api_server.app.config),
            api_server.AUTH_CONFIG_PATH) == original
    for conn in handles:
        with pytest.raises(sqlite3.ProgrammingError, match="closed"):
            conn.execute("SELECT 1")


@pytest.mark.parametrize("enabled", [False, True])
def test_readwrite_uri_is_opt_in_and_exact(tmp_path, enabled):
    import sqlite3
    from price_test_support import _isolated_price_db

    with pytest.MonkeyPatch.context() as patches:
        generator = _isolated_price_db(tmp_path, patches, allow_readwrite_uri=enabled)
        db = next(generator)
        try:
            uri = db.path.as_uri() + "?mode=rw"
            for connect in (sqlite3.connect, sqlite3.dbapi2.connect):
                if enabled:
                    conn = connect(uri, uri=True)
                    try:
                        conn.execute("INSERT OR REPLACE INTO etf_prices VALUES ('TEST', '2026-01-01', 100)")
                        conn.commit()
                        with pytest.raises(sqlite3.DatabaseError, match="not authorized"):
                            conn.execute("ATTACH DATABASE ':memory:' AS forbidden")
                    finally:
                        conn.close()
                else:
                    with pytest.raises(AssertionError, match="outside the isolated"):
                        connect(uri, uri=True)
                for forbidden in (db.path.as_uri() + "?mode=rwc", uri + "&cache=shared",
                                  (tmp_path / "virtual-production.db").as_uri() + "?mode=rw"):
                    with pytest.raises(AssertionError, match="outside the isolated"):
                        connect(forbidden, uri=True)
                with pytest.raises(AssertionError, match="outside the isolated"):
                    connect(uri, uri=False)
            conn = sqlite3.connect(db.path.as_uri() + "?mode=ro", uri=True)
            try:
                with pytest.raises(sqlite3.OperationalError, match="readonly"):
                    conn.execute("DELETE FROM etf_prices")
            finally:
                conn.close()
        finally:
            generator.close()
    assert not db.path.exists()


@pytest.mark.parametrize("module_name,failure", [
    (name, failure)
    for name in ("test_ohlcv_backfill", "test_price_quality", "test_price_quality_boundary")
    for failure in (None, "assertion", "sql")
] + [("test_ohlcv_backfill", "init")])
def test_quality_backfill_full_cleanup_on_failure(tmp_path, module_name, failure):
    import importlib
    import sqlite3
    import socket

    module = importlib.import_module(module_name)  # Only inert test declarations.
    originals = (sqlite3.connect, sqlite3.dbapi2.connect, socket.socket.connect)
    path_originals = {}
    handles = []
    with pytest.MonkeyPatch.context() as patches:
        class PathTrackingPatches:
            def setattr(self, obj, name, value, **kwargs):
                if name == "DATABASE_PATH":
                    path_originals.setdefault(obj, getattr(obj, name))
                patches.setattr(obj, name, value, **kwargs)

        db_generator = module.isolated_price_db.__wrapped__(tmp_path, PathTrackingPatches())
        db = next(db_generator)
        scope_generator = module._protected_flask_state.__wrapped__(db, patches)
        scope = next(scope_generator)
        original_state = (dict(scope.api.app.config), scope.api.AUTH_CONFIG_PATH,
                          scope.database.init_database, scope.repository.get_connection)
        original_class = (module.module.OHLCVBackfill if module_name == "test_ohlcv_backfill" else None)
        try:
            def interrupt():
                if failure == "assertion":
                    raise AssertionError("synthetic quality interruption")
                conn = sqlite3.connect(db.path)
                handles.append(conn)
                conn.execute("CREATE TABLE IF NOT EXISTS synthetic_interruption(x)")
                conn.execute("SELECT * FROM synthetic_missing_table")

            def run():
                if module_name == "test_ohlcv_backfill":
                    if failure == "init":
                        scope.patches.setattr(scope.database, "init_database", interrupt)
                    data = module.setup.__wrapped__(tmp_path, patches, scope)
                    if failure in ("assertion", "sql"):
                        real = data[2].get_targets
                        def get_targets():
                            result = real()
                            interrupt()
                            return result
                        scope.patches.setattr(data[2], "get_targets", get_targets)
                    module.test_targets_ranges_and_legacy_preservation(data)
                    if failure is None:
                        module.test_no_initialization_on_import_or_missing_schema(tmp_path, scope.patches)
                else:
                    if failure:
                        real = module.check_price_quality
                        def check(*args, **kwargs):
                            result = real(*args, **kwargs)
                            interrupt()
                            return result
                        scope.patches.setattr(module, "check_price_quality", check)
                    if module_name == "test_price_quality":
                        path = module.quality_db.__wrapped__(scope)
                        module.test_price_quality_status(path, "MATCH", "MATCH")
                    else:
                        module.test_matching_prices_are_not_source_verified(tmp_path)

            if failure:
                expected = AssertionError if failure == "assertion" else sqlite3.OperationalError
                with pytest.raises(expected, match="synthetic quality interruption|no such table"):
                    run()
            else:
                run()
            handles.extend(scope.handles)
            for suffix in ("-journal", "-wal", "-shm"):
                db.path.with_name(db.path.name + suffix).touch()
        finally:
            try:
                scope_generator.close()
            finally:
                db_generator.close()
        assert (dict(scope.api.app.config), scope.api.AUTH_CONFIG_PATH,
                scope.database.init_database, scope.repository.get_connection) == original_state
        if original_class is not None:
            assert module.module.OHLCVBackfill is original_class
    assert (sqlite3.connect, sqlite3.dbapi2.connect, socket.socket.connect) == originals
    assert all(getattr(obj, "DATABASE_PATH") == value for obj, value in path_originals.items())
    assert all(not db.path.with_name(db.path.name + suffix).exists()
               for suffix in ("", "-journal", "-wal", "-shm"))
    assert handles
    for conn in handles:
        with pytest.raises(sqlite3.ProgrammingError, match="closed"):
            conn.execute("SELECT 1")
