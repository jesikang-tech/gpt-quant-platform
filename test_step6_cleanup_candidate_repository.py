EXPECTED = {1: (False, False, 'NO_AUTO_DELETE'), 2: (False, False, 'NO_AUTO_DELETE'), 3: (False, False, 'NO_AUTO_DELETE'), 4: (True, False, 'REVIEW_ONLY'), 5: (False, False, 'NO_AUTO_DELETE'), 6: (False, False, 'NO_ACTION')}
from price_test_support import isolated_price_db, phase8_test_scope

def test_cleanup_candidate_repository(isolated_price_db):
    with phase8_test_scope(isolated_price_db) as scope:
        repository = scope.repository
        print('=' * 60)
        print('Production Hardening - Cleanup Candidate Repository Regression')
        print('=' * 60)
        retention_rows = [{'history_id': 1, 'lifecycle': 'ACTIVE_OUTCOME_TRACKING', 'retention': 'PROTECTED'}, {'history_id': 2, 'lifecycle': 'COMPLETED', 'retention': 'RETAIN_LONG_TERM'}, {'history_id': 3, 'lifecycle': 'LEGACY_EVALUATED_CANDIDATE', 'retention': 'RETAIN'}, {'history_id': 4, 'lifecycle': 'LEGACY_ORPHAN_CANDIDATE', 'retention': 'REVIEW_REQUIRED'}, {'history_id': 5, 'lifecycle': 'LEGACY_EVALUATED_CANDIDATE', 'retention': 'RETAIN'}, {'history_id': 6, 'lifecycle': 'UNKNOWN', 'retention': 'UNKNOWN'}]
        scope.patches.setattr(repository, 'get_ai_decision_history_snapshot_retention', lambda: retention_rows)
        rows = repository.get_ai_decision_history_snapshot_cleanup_candidates()
        assert len(rows) == len(EXPECTED)
        actual = {row['history_id']: (row['cleanup_candidate'], row['auto_delete'], row['cleanup_action']) for row in rows}
        assert actual == EXPECTED
        for row in rows:
            print(f"HISTORY {row['history_id']}: PASS | {row['lifecycle']} | {row['retention']} | candidate={row['cleanup_candidate']} | auto_delete={row['auto_delete']} | {row['cleanup_action']}")
        print('')
        print('=' * 60)
        print('OVERALL RESULT: PASS')
        print('=' * 60)
