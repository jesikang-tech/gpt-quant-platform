import sqlite3
from datetime import datetime, timedelta

class _TestConnection:

    def __init__(self, connection):
        self._connection = connection

    def cursor(self):
        return self._connection.cursor()

    def close(self):
        return None

def build_db(scope):
    conn = scope.memory()
    cursor = conn.cursor()
    cursor.execute('\n        CREATE TABLE ai_decision_outcome_history (\n            id INTEGER PRIMARY KEY AUTOINCREMENT,\n            created_at TEXT,\n            outcome_status TEXT\n        )\n        ')
    cursor.execute('\n        CREATE TABLE ai_decision_portfolio_snapshot (\n            id INTEGER PRIMARY KEY AUTOINCREMENT,\n            history_id INTEGER NOT NULL\n        )\n        ')
    conn.commit()
    return conn
CASES = [('CASE 1 PENDING WITH SNAPSHOT', 'PENDING', True, 1, 'PROTECTED'), ('CASE 2 EVALUATED WITH SNAPSHOT', 'EVALUATED', True, 1, 'RETAIN_LONG_TERM'), ('CASE 3 RECENT PENDING ORPHAN', 'PENDING', False, 1, 'RETAIN'), ('CASE 4 RECENT EVALUATED LEGACY', 'EVALUATED', False, 1, 'RETAIN'), ('CASE 5 OLD PENDING ORPHAN', 'PENDING', False, 8, 'REVIEW_REQUIRED'), ('CASE 6 OLD EVALUATED LEGACY', 'EVALUATED', False, 8, 'REVIEW_REQUIRED')]
from price_test_support import isolated_price_db, phase8_test_scope

def test_snapshot_retention_repository(isolated_price_db):
    with phase8_test_scope(isolated_price_db) as scope:
        repository = scope.repository
        now = datetime.now().astimezone()
        print('=' * 60)
        print('Production Hardening - History Snapshot Retention Repository Regression')
        print('=' * 60)
        for name, outcome_status, create_snapshot, age_days, expected_retention in CASES:
            raw_conn = build_db(scope)
            cursor = raw_conn.cursor()
            created_at = (now - timedelta(days=age_days)).isoformat()
            cursor.execute('\n            INSERT INTO ai_decision_outcome_history\n            (\n                created_at,\n                outcome_status\n            )\n            VALUES (?, ?)\n            ', (created_at, outcome_status))
            history_id = cursor.lastrowid
            if create_snapshot:
                cursor.execute('\n                INSERT INTO ai_decision_portfolio_snapshot\n                (\n                    history_id\n                )\n                VALUES (?)\n                ', (history_id,))
            raw_conn.commit()
            scope.patches.setattr(repository, 'get_connection', lambda: _TestConnection(raw_conn))
            try:
                rows = repository.get_ai_decision_history_snapshot_retention()
                assert len(rows) == 1
                row = rows[0]
                assert row['history_id'] == history_id
                assert row['outcome_status'] == outcome_status
                assert row['snapshot_count'] == (1 if create_snapshot else 0)
                assert row['retention'] == expected_retention
                print(f"{name}: PASS | {row['lifecycle']} | retention={row['retention']}")
            finally:
                raw_conn.close()
        print('')
        print('=' * 60)
        print('OVERALL RESULT: PASS')
        print('=' * 60)
