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


@pytest.fixture
def synthetic_ranking_db(isolated_price_db):
    """Synthetic rising, stable, falling and history-free ETF observations."""
    dates = ("2026-01-02", "2026-01-05", "2026-01-06")
    scores = {"111111": (60, 75, 90), "222222": (70, 70, 70),
              "333333": (80, 65, 50)}
    ranks = {"111111": (3, 2, 1), "222222": (2, 2, 2), "333333": (1, 3, 4)}
    conn = isolated_price_db.connect()
    try:
        with conn:
            for ticker in scores:
                conn.executemany(
                    "INSERT INTO etf_ranking_history(ticker, rank, final_score, ranking_date) "
                    "VALUES (?, ?, ?, ?)",
                    [(ticker, rank, score, day) for rank, score, day in
                     zip(ranks[ticker], scores[ticker], dates)],
                )
                conn.executemany(
                    "INSERT INTO etf_scores(ticker, return_score, trend_score, slope_score, "
                    "final_score, created_at) VALUES (?, ?, ?, ?, ?, ?)",
                    [(ticker, score / 2, score / 3, score / 6, score, day)
                     for score, day in zip(scores[ticker], dates)],
                )
            conn.execute(
                "INSERT INTO etf_scores(ticker, return_score, trend_score, slope_score, "
                "final_score, created_at) VALUES ('444444', 15, 10, 5, 30, ?)", (dates[-1],)
            )
            conn.execute("INSERT INTO etf_prices VALUES ('111111', ?, 100)", (dates[-1],))
        assert Path(conn.execute("PRAGMA database_list").fetchone()[2]).resolve() == isolated_price_db.path
    finally:
        conn.close()
    return SimpleNamespace(db=isolated_price_db, dates=dates, scores=scores, ranks=ranks)


@pytest.fixture
def synthetic_snapshot_db(isolated_price_db):
    """Lifecycle and retention states built only in the guarded temporary DB."""
    from datetime import datetime, timedelta, timezone
    from repository import save_ai_decision_portfolio_snapshot

    now = datetime.now(timezone.utc)
    cases = [
        ("PENDING", 4, 1, "ACTIVE_OUTCOME_TRACKING", "PROTECTED"),
        ("PENDING", 4, 120, "ACTIVE_OUTCOME_TRACKING", "PROTECTED"),
        ("EVALUATED", 4, 45, "COMPLETED", "RETAIN_LONG_TERM"),
        ("EVALUATED", 0, 5, "LEGACY_EVALUATED_CANDIDATE", "RETAIN"),
        ("EVALUATED", 0, 30, "LEGACY_EVALUATED_CANDIDATE", "REVIEW_REQUIRED"),
        ("PENDING", 0, 6, "LEGACY_ORPHAN_CANDIDATE", "RETAIN"),
        ("PENDING", 0, 90, "LEGACY_ORPHAN_CANDIDATE", "REVIEW_REQUIRED"),
        ("UNKNOWN", 0, 10, "UNKNOWN", "UNKNOWN"),
    ]
    expected = {}
    for status, count, age, lifecycle, retention in cases:
        created = (now - timedelta(days=age)).isoformat()
        conn = isolated_price_db.connect()
        try:
            with conn:
                cursor = conn.execute(
                    "INSERT INTO ai_decision_outcome_history(outcome_status, created_at) VALUES (?, ?)",
                    (status, created),
                )
                history_id = cursor.lastrowid
        finally:
            conn.close()
        if count:
            assert save_ai_decision_portfolio_snapshot(
                history_id, [{"ticker": ticker, "weight": 25,
                              "reference_price": 100, "reference_price_date": created[:10]}
                             for ticker in ("111111", "222222", "333333", "CASH")], created
            ) == count
        expected[history_id] = (lifecycle, retention, count)
    return SimpleNamespace(db=isolated_price_db, expected=expected)


@pytest.fixture
def synthetic_ready_api(synthetic_ranking_db, isolated_evaluation_api):
    """Strong stable synthetic history; all readiness engines remain real."""
    conn = isolated_evaluation_api.db.connect()
    try:
        with conn:
            conn.execute("UPDATE etf_scores SET return_score=95, trend_score=95, slope_score=95, final_score=95")
            conn.execute("UPDATE etf_ranking_history SET final_score=95, rank=CASE ticker WHEN '111111' THEN 1 WHEN '222222' THEN 2 ELSE 3 END")
            conn.executemany("INSERT INTO ai_decision_history(decision, action, decision_score, grade, "
                             "market_view, recommended_mode, top_etf, created_at) "
                             "VALUES ('MAINTAIN', 'PROCEED', ?, 'A', 'BULLISH', 'aggressive', '111111', ?)",
                             [(90 + day, f"2026-01-{day:02d}T10:00:00+00:00") for day in range(1, 11)])
            conn.execute("INSERT INTO ai_decision_outcome_history(outcome_status, outcome_score, "
                         "outcome_grade, learning_status, feedback_state, adaptive_learning_required, "
                         "reassessment_required, reassessment_status) VALUES "
                         "('EVALUATED', 95, 'A', 'LEARNING_AVAILABLE', 'COLLECTING', 0, 0, 'NOT_REQUIRED')")
    finally:
        conn.close()
    return isolated_evaluation_api


@pytest.fixture
def synthetic_waiting_portfolio(isolated_price_db):
    """Three ETF reference prices, deliberately no later evaluation prices."""
    from repository import save_ai_decision_outcome_with_portfolio_transaction

    reference_date = "2026-01-02"
    conn = isolated_price_db.connect()
    try:
        with conn:
            conn.executemany("INSERT INTO etf_prices VALUES (?, ?, ?)",
                             [(ticker, reference_date, price) for ticker, price in
                              (("111111", 100), ("222222", 200), ("333333", 300))])
    finally:
        conn.close()
    result = save_ai_decision_outcome_with_portfolio_transaction(
        history_kwargs={"decision": "MAINTAIN", "action": "PROCEED", "strategy": "MAINTAIN",
                        "outcome_status": "PENDING", "snapshot_status": "COLLECTED",
                        "snapshot_purpose": "FUTURE_OUTCOME_EVALUATION",
                        "learning_status": "WAITING_FOR_OUTCOME", "feedback_state": "COLLECTING",
                        "adaptive_learning_required": 0, "reassessment_required": 0,
                        "reassessment_status": "NOT_REQUIRED"},
        portfolio=[{"ticker": ticker, "weight": weight} for ticker, weight in
                   (("111111", 40), ("222222", 30), ("333333", 20), ("CASH", 10))],
        created_at=reference_date + "T12:00:00+00:00",
    )
    assert result["snapshot_count"] == 4
    return SimpleNamespace(db=isolated_price_db, history_id=result["history_id"])


@pytest.fixture
def synthetic_portfolio_db(isolated_price_db):
    """Original portfolio tickers with independent synthetic factor evidence."""
    factors = {"365040": (95, 90, 85), "306950": (80, 75, 70),
               "292160": (65, 60, 55)}
    scores = {"365040": 90.7, "306950": 90.4, "292160": 90.1}
    day = "2026-01-06"
    conn = isolated_price_db.connect()
    try:
        with conn:
            for rank, (ticker, values) in enumerate(factors.items(), 1):
                conn.execute("INSERT INTO etf_scores(ticker, return_score, trend_score, "
                             "slope_score, final_score, created_at) VALUES (?, ?, ?, ?, ?, ?)",
                             (ticker, *values, scores[ticker], day))
                conn.execute("INSERT INTO etf_ranking_history(ticker, rank, final_score, "
                             "ranking_date) VALUES (?, ?, ?, ?)",
                             (ticker, rank, scores[ticker], day))
                conn.execute("INSERT INTO etf_prices VALUES (?, ?, ?)", (ticker, day, 100))
            assert Path(conn.execute("PRAGMA database_list").fetchone()[2]).resolve() == isolated_price_db.path
    finally:
        conn.close()
    return SimpleNamespace(db=isolated_price_db, factors=factors, scores=scores, day=day)


@pytest.fixture
def isolated_portfolio_api(synthetic_portfolio_db, tmp_path):
    """Real authentication and API; restore shared Flask state even on failure."""
    import api_server
    from core.platform_auth import configure_flask_auth, create_password_hash, save_auth_config

    api = api_server
    original = (api.app.secret_key, api.AUTH_CONFIG_PATH)
    auth_path = tmp_path / "platform_auth.json"
    save_auth_config(create_password_hash("1234"),
                     create_password_hash("1234567", admin=True), auth_path)
    try:
        with pytest.MonkeyPatch.context() as patches:
            # Register the original value before configure_flask_auth mutates it.
            patches.setattr(api.app, "secret_key", api.app.secret_key)
            patches.setattr(api, "AUTH_CONFIG_PATH", auth_path)
            configure_flask_auth(api.app, auth_path)
            yield SimpleNamespace(api=api, client=api.app.test_client(),
                                  data=synthetic_portfolio_db, auth_path=auth_path)
    finally:
        assert (api.app.secret_key, api.AUTH_CONFIG_PATH) == original
