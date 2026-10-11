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

def build_db(scope):
    conn = scope.memory()
    cursor = conn.cursor()
    cursor.execute('\n        CREATE TABLE ai_decision_outcome_history (\n            id INTEGER PRIMARY KEY AUTOINCREMENT,\n            decision TEXT,\n            action TEXT,\n            strategy TEXT\n        )\n        ')
    cursor.execute('\n        CREATE TABLE etf_prices (\n            ticker TEXT NOT NULL,\n            date TEXT NOT NULL,\n            close_price REAL NOT NULL\n        )\n        ')
    cursor.executemany('\n        INSERT INTO etf_prices\n        (\n            ticker,\n            date,\n            close_price\n        )\n        VALUES (?, ?, ?)\n        ', [('306950', '2026-08-20', 67560.0)])
    cursor.execute('\n        CREATE TABLE ai_decision_portfolio_snapshot (\n            id INTEGER PRIMARY KEY AUTOINCREMENT,\n            history_id INTEGER NOT NULL,\n            ticker TEXT NOT NULL,\n            weight REAL,\n            reference_price REAL,\n            created_at TEXT,\n            reference_price_date TEXT\n        )\n        ')
    conn.commit()
    return conn

def valid_portfolio():
    return [{'ticker': '306950', 'weight': 90.0, 'reference_price': 67560.0, 'reference_price_date': '2026-08-20'}, {'ticker': 'CASH', 'weight': 10.0}]

def run_case(scope, name, history_id, create_history, expected_success, expected_error):
    repository = scope.repository
    raw_conn = build_db(scope)
    cursor = raw_conn.cursor()
    if create_history:
        cursor.execute('\n            INSERT INTO ai_decision_outcome_history\n            (\n                decision,\n                action,\n                strategy\n            )\n            VALUES (?, ?, ?)\n            ', ('MAINTAIN', 'PROCEED', 'MAINTAIN'))
        raw_conn.commit()
    scope.patches.setattr(repository, 'get_connection', lambda: _TestConnection(raw_conn))
    try:
        try:
            result = repository.save_ai_decision_portfolio_snapshot(history_id=history_id, portfolio=valid_portfolio(), created_at='2026-08-20T14:30:00+09:00')
            if not expected_success:
                raise AssertionError(f'Expected rejection: {expected_error}')
            assert result == 2
            cursor.execute('\n                SELECT COUNT(*)\n                FROM ai_decision_portfolio_snapshot\n                WHERE history_id = ?\n                ', (history_id,))
            snapshot_count = cursor.fetchone()[0]
            assert snapshot_count == 2
            print(f'{name}: PASS | snapshot_count={snapshot_count}')
        except ValueError as exc:
            if expected_success:
                raise
            assert str(exc) == expected_error
            cursor.execute('\n                SELECT COUNT(*)\n                FROM ai_decision_portfolio_snapshot\n                ')
            snapshot_count = cursor.fetchone()[0]
            assert snapshot_count == 0
            print(f'{name}: PASS | rejected={expected_error} | snapshot_count=0')
    finally:
        raw_conn.close()
from price_test_support import isolated_price_db, phase8_test_scope

def test_snapshot_referential_integrity(isolated_price_db):
    with phase8_test_scope(isolated_price_db) as scope:
        repository = scope.repository
        print('=' * 60)
        print('Production Hardening - History Snapshot Referential Integrity Contract')
        print('=' * 60)
        run_case(scope, 'CASE 1 EXISTING HISTORY', history_id=1, create_history=True, expected_success=True, expected_error=None)
        run_case(scope, 'CASE 2 MISSING HISTORY', history_id=999, create_history=False, expected_success=False, expected_error='HISTORY_NOT_FOUND')
        print('')
        print('=' * 60)
        print('OVERALL RESULT: PASS')
        print('=' * 60)
