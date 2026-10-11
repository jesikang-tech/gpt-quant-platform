import sqlite3

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
    cursor.execute('\n        CREATE TABLE ai_decision_outcome_history (\n            id INTEGER PRIMARY KEY AUTOINCREMENT,\n            outcome_status TEXT\n        )\n        ')
    cursor.execute('\n        CREATE TABLE ai_decision_portfolio_snapshot (\n            id INTEGER PRIMARY KEY AUTOINCREMENT,\n            history_id INTEGER NOT NULL\n        )\n        ')
    conn.commit()
    return conn
CASES = [('CASE 1 PENDING WITH SNAPSHOT', 'PENDING', True, 'ACTIVE_OUTCOME_TRACKING'), ('CASE 2 PENDING WITHOUT SNAPSHOT', 'PENDING', False, 'LEGACY_ORPHAN_CANDIDATE'), ('CASE 3 EVALUATED WITH SNAPSHOT', 'EVALUATED', True, 'COMPLETED'), ('CASE 4 EVALUATED WITHOUT SNAPSHOT', 'EVALUATED', False, 'LEGACY_EVALUATED_CANDIDATE'), ('CASE 5 UNKNOWN STATUS', 'UNKNOWN_STATUS', False, 'UNKNOWN')]
from price_test_support import isolated_price_db, phase8_test_scope

def test_snapshot_lifecycle_repository(isolated_price_db):
    with phase8_test_scope(isolated_price_db) as scope:
        repository = scope.repository
        print('=' * 60)
        print('Production Hardening - History Snapshot Lifecycle Repository Regression')
        print('=' * 60)
        for name, outcome_status, create_snapshot, expected_classification in CASES:
            raw_conn = build_db(scope)
            cursor = raw_conn.cursor()
            cursor.execute('\n            INSERT INTO ai_decision_outcome_history\n            (\n                outcome_status\n            )\n            VALUES (?)\n            ', (outcome_status,))
            history_id = cursor.lastrowid
            if create_snapshot:
                cursor.execute('\n                INSERT INTO ai_decision_portfolio_snapshot\n                (\n                    history_id\n                )\n                VALUES (?)\n                ', (history_id,))
            raw_conn.commit()
            scope.patches.setattr(repository, 'get_connection', lambda: _TestConnection(raw_conn))
            try:
                rows = repository.get_ai_decision_history_snapshot_lifecycle()
                assert len(rows) == 1
                row = rows[0]
                assert row['history_id'] == history_id
                assert row['outcome_status'] == outcome_status
                assert row['snapshot_count'] == (1 if create_snapshot else 0)
                assert row['classification'] == expected_classification
                print(f"{name}: PASS | {outcome_status} | snapshot_count={row['snapshot_count']} | {row['classification']}")
            finally:
                raw_conn.close()
        print('')
        print('=' * 60)
        print('OVERALL RESULT: PASS')
        print('=' * 60)
