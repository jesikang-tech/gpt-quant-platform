from pathlib import Path
import sqlite3

import api_server
import repository


TEST_DB = Path(r".\database\g7_10_18_integration_test.db")
HISTORY_ID = 46


def assert_equal(actual, expected, label):
    if actual != expected:
        raise AssertionError(
            f"{label}: expected={expected!r}, actual={actual!r}"
        )
    print(f"{label}: PASS")


def assert_true(value, label):
    if not value:
        raise AssertionError(
            f"{label}: expected=True, actual={value!r}"
        )
    print(f"{label}: PASS")


print("=" * 82)
print("PHASE 7-10-20-26")
print("API WAITING BOUNDARY")
print("PORTFOLIO OUTCOME EVALUATION -> OUTCOME LOOP")
print("SOURCE-VERIFIED / TEST-DB / NO FABRICATED OUTCOME")
print("=" * 82)


original_get_connection = repository.get_connection


def test_db_connection():
    return sqlite3.connect(
        TEST_DB,
        timeout=30
    )


repository.get_connection = test_db_connection

try:
    conn = sqlite3.connect(TEST_DB)

    try:
        history_before = conn.execute(
            """
            SELECT
                outcome_status,
                portfolio_return,
                portfolio_evaluation_date,
                adaptive_learning_required,
                reassessment_required
            FROM ai_decision_outcome_history
            WHERE id = ?
            """,
            (HISTORY_ID,),
        ).fetchone()

        assert_true(
            history_before is not None,
            "history 46 -> exists",
        )

        print("")
        print("=" * 82)
        print("CASE: PRE-EVALUATION PERSISTED STATE")
        print("=" * 82)

        assert_equal(
            history_before[0],
            "PENDING",
            "history -> pending before API evaluation",
        )

        assert_equal(
            history_before[1],
            None,
            "history -> no portfolio return before API evaluation",
        )

        assert_equal(
            history_before[2],
            None,
            "history -> no evaluation date before API evaluation",
        )

        print("")
        print("=" * 82)
        print("CASE: API WAITING EVALUATION")
        print("=" * 82)

        client = api_server.app.test_client()

        response = client.get(
            f"/api/ai-decision/portfolio-snapshot/{HISTORY_ID}/evaluate"
        )

        assert_equal(
            response.status_code,
            200,
            "API -> HTTP 200",
        )

        payload = response.get_json()

        assert_true(
            isinstance(payload, dict),
            "API -> JSON object",
        )

        assert_equal(
            payload.get("success"),
            True,
            "API -> success",
        )

        evaluation = payload.get("evaluation")

        assert_true(
            isinstance(evaluation, dict),
            "API -> evaluation object",
        )

        assert_equal(
            evaluation.get("evaluation_status"),
            "WAITING_FOR_OUTCOME",
            "API -> waiting for outcome",
        )

        assert_equal(
            evaluation.get("outcome_status"),
            "PENDING",
            "API -> pending outcome",
        )

        assert_equal(
            evaluation.get("portfolio_return"),
            None,
            "API -> no fabricated portfolio return",
        )

        assert_equal(
            evaluation.get("pending_positions"),
            3,
            "API -> three pending ETF positions",
        )

        assert_equal(
            evaluation.get("evaluated_weight"),
            10.0,
            "API -> only CASH evaluated",
        )

        print("")
        print("=" * 82)
        print("CASE: API OUTCOME LOOP MUST NOT ADVANCE")
        print("=" * 82)

        assert_equal(
            payload.get("outcome_evaluation"),
            None,
            "API -> no outcome evaluation while waiting",
        )

        assert_equal(
            payload.get("outcome_intelligence"),
            None,
            "API -> no outcome intelligence while waiting",
        )

        print("")
        print("=" * 82)
        print("CASE: PERSISTED STATE REMAINS UNCHANGED")
        print("=" * 82)

        history_after = conn.execute(
            """
            SELECT
                outcome_status,
                portfolio_return,
                portfolio_evaluation_date,
                adaptive_learning_required,
                reassessment_required
            FROM ai_decision_outcome_history
            WHERE id = ?
            """,
            (HISTORY_ID,),
        ).fetchone()

        assert_equal(
            history_after[0],
            history_before[0],
            "history -> outcome status unchanged",
        )

        assert_equal(
            history_after[1],
            history_before[1],
            "history -> portfolio return unchanged",
        )

        assert_equal(
            history_after[2],
            history_before[2],
            "history -> evaluation date unchanged",
        )

        assert_equal(
            history_after[3],
            history_before[3],
            "history -> adaptive learning flag unchanged",
        )

        assert_equal(
            history_after[4],
            history_before[4],
            "history -> reassessment flag unchanged",
        )

        print("")
        print("=" * 82)
        print("CASE: READ-ONLY PRICE BOUNDARY")
        print("=" * 82)

        coverage = conn.execute(
            """
            SELECT
                p.ticker,
                p.reference_price_date,
                MAX(e.date)
            FROM ai_decision_portfolio_snapshot p
            LEFT JOIN etf_prices e
                ON e.ticker = p.ticker
               AND e.date > p.reference_price_date
            WHERE p.history_id = ?
              AND p.ticker <> 'CASH'
            GROUP BY
                p.ticker,
                p.reference_price_date
            ORDER BY p.ticker
            """,
            (HISTORY_ID,),
        ).fetchall()

        assert_equal(
            len(coverage),
            3,
            "price boundary -> three ETF positions",
        )

        for ticker, reference_date, max_future_date in coverage:
            assert_equal(
                max_future_date,
                None,
                f"{ticker} -> no future price after reference date",
            )

        print("")
        print("=" * 82)
        print("===== PHASE 7-10-20-26 API WAITING BOUNDARY COMPLETE =====")
        print("=" * 82)

    finally:
        conn.close()

finally:
    repository.get_connection = original_get_connection
