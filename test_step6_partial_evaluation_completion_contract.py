import sqlite3

class _TestConnection:

    def __init__(self, connection):
        self._connection = connection

    def cursor(self):
        return self._connection.cursor()

    def commit(self):
        return self._connection.commit()

    def rollback(self):
        return self._connection.rollback()

    def close(self):
        return None

def build_db(scope, snapshot_rows, price_rows):
    conn = scope.memory()
    cursor = conn.cursor()
    cursor.execute('\n        CREATE TABLE ai_decision_portfolio_snapshot (\n            id INTEGER PRIMARY KEY AUTOINCREMENT,\n            history_id INTEGER NOT NULL,\n            ticker TEXT NOT NULL,\n            weight REAL,\n            reference_price REAL,\n            created_at TEXT,\n            reference_price_date TEXT\n        )\n        ')
    cursor.execute('\n        CREATE TABLE audit_event (\n            id INTEGER PRIMARY KEY AUTOINCREMENT,\n            audit_event_id TEXT NOT NULL UNIQUE,\n            event_type TEXT NOT NULL,\n            event_time TEXT NOT NULL,\n            source TEXT NOT NULL,\n            status TEXT,\n            decision_history_id INTEGER,\n            outcome_history_id INTEGER,\n            correlation_key TEXT NOT NULL,\n            details TEXT NOT NULL\n        )\n        ')
    cursor.execute('\n        CREATE TABLE etf_prices (\n            ticker TEXT NOT NULL,\n            date TEXT NOT NULL,\n            close_price REAL NOT NULL\n        )\n        ')
    cursor.execute('\n        CREATE TABLE ai_decision_outcome_history (\n            id INTEGER PRIMARY KEY AUTOINCREMENT,\n            outcome_status TEXT,\n            snapshot_status TEXT,\n            portfolio_return REAL,\n            portfolio_evaluation_date TEXT\n        )\n        ')
    cursor.execute('\n        INSERT INTO ai_decision_outcome_history(\n            id,\n            outcome_status,\n            snapshot_status,\n            portfolio_return,\n            portfolio_evaluation_date\n        )\n        VALUES (?, ?, ?, ?, ?)\n        ', (12, 'PENDING', 'COLLECTED', None, None))
    cursor.executemany('\n        INSERT INTO ai_decision_portfolio_snapshot\n        (\n            history_id,\n            ticker,\n            weight,\n            reference_price,\n            created_at,\n            reference_price_date\n        )\n        VALUES (?, ?, ?, ?, ?, ?)\n        ', snapshot_rows)
    cursor.executemany('\n        INSERT INTO etf_prices\n        (\n            ticker,\n            date,\n            close_price\n        )\n        VALUES (?, ?, ?)\n        ', price_rows)
    conn.commit()
    return conn

def run_case(scope, name, snapshot_rows, price_rows, expected_status, expected_outcome_status, expected_weight, expected_pending, expected_return):
    repository = scope.repository
    raw_conn = build_db(scope, snapshot_rows, price_rows)
    scope.patches.setattr(repository, 'get_connection', lambda: _TestConnection(raw_conn))
    try:
        result = repository.evaluate_ai_decision_portfolio_snapshot(history_id=12, evaluation_date='2026-08-21')
        assert result['evaluation_status'] == expected_status
        assert result['outcome_status'] == expected_outcome_status
        assert result.get('evaluated_weight') == expected_weight
        assert result.get('pending_positions') == expected_pending
        assert result.get('portfolio_return') == expected_return
        cursor = raw_conn.cursor()
        cursor.execute('\n            SELECT\n                portfolio_return,\n                portfolio_evaluation_date\n            FROM ai_decision_outcome_history\n            WHERE id = 12\n            ')
        stored = cursor.fetchone()
        if expected_return is None:
            assert stored[0] is None
            assert stored[1] is None
        else:
            assert stored[0] == expected_return
            assert stored[1] == '2026-08-21'
        print(f'{name}: PASS | status={expected_status} | weight={expected_weight} | pending={expected_pending} | return={expected_return}')
    finally:
        raw_conn.close()
from price_test_support import isolated_price_db, phase8_test_scope

def test_partial_evaluation_completion(isolated_price_db):
    with phase8_test_scope(isolated_price_db) as scope:
        repository = scope.repository
        print('=' * 60)
        print('Production Hardening - Partial Evaluation Completion Contract')
        print('=' * 60)
        run_case(scope, 'CASE 1 FULL EVALUATION', [(12, 'A', 40.0, 100.0, '2026-08-20T00:00:00', '2026-08-20'), (12, 'B', 30.0, 200.0, '2026-08-20T00:00:00', '2026-08-20'), (12, 'C', 20.0, 300.0, '2026-08-20T00:00:00', '2026-08-20'), (12, 'CASH', 10.0, None, '2026-08-20T00:00:00', None)], [('A', '2026-08-21', 110.0), ('B', '2026-08-21', 210.0), ('C', '2026-08-21', 315.0)], 'EVALUATED', 'EVALUATED', 100.0, 0, 6.5)
        run_case(scope, 'CASE 2 PARTIAL EVALUATION', [(12, 'A', 40.0, 100.0, '2026-08-20T00:00:00', '2026-08-20'), (12, 'B', 30.0, 200.0, '2026-08-20T00:00:00', '2026-08-20'), (12, 'C', 20.0, 300.0, '2026-08-20T00:00:00', '2026-08-20'), (12, 'CASH', 10.0, None, '2026-08-20T00:00:00', None)], [('A', '2026-08-21', 110.0), ('B', '2026-08-21', 210.0)], 'WAITING_FOR_OUTCOME', 'PENDING', 80.0, 1, None)
        run_case(scope, 'CASE 3 HEAVY PARTIAL EVALUATION', [(12, 'A', 40.0, 100.0, '2026-08-20T00:00:00', '2026-08-20'), (12, 'B', 30.0, 200.0, '2026-08-20T00:00:00', '2026-08-20'), (12, 'C', 20.0, 300.0, '2026-08-20T00:00:00', '2026-08-20'), (12, 'CASH', 10.0, None, '2026-08-20T00:00:00', None)], [('A', '2026-08-21', 110.0)], 'WAITING_FOR_OUTCOME', 'PENDING', 50.0, 2, None)
        print('')
        print('=' * 60)
        print('OVERALL RESULT: PASS')
        print('=' * 60)
