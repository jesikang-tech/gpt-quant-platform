import sqlite3
from pathlib import Path

import database

from repository import evaluate_ai_decision_portfolio_snapshot


TEST_DB = Path(r".\database\g7_10_18_integration_test.db")
database.DATABASE_PATH = TEST_DB


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
print("PHASE 7-10-20-25")
print("PORTFOLIO OUTCOME EVALUATION WAITING BOUNDARY")
print("REAL PRICE COVERAGE END -> NO FABRICATED OUTCOME")
print("SOURCE-VERIFIED / TEST-DB / EVALUATION BOUNDARY")
print("=" * 82)


conn = sqlite3.connect(TEST_DB)

try:
    history = conn.execute(
        """
        SELECT
            id,
            outcome_status,
            portfolio_return,
            portfolio_evaluation_date
        FROM ai_decision_outcome_history
        WHERE id = 46
        """
    ).fetchone()

    assert_true(
        history is not None,
        "history 46 -> exists",
    )

    history_id, history_status, history_return, history_date = history

    print("")
    print("=" * 82)
    print("CASE: PRE-EVALUATION PERSISTED STATE")
    print("=" * 82)

    assert_equal(
        history_status,
        "PENDING",
        "history -> pending before evaluation",
    )

    assert_equal(
        history_return,
        None,
        "history -> no portfolio return before evaluation",
    )

    assert_equal(
        history_date,
        None,
        "history -> no evaluation date before evaluation",
    )

    print("")
    print("=" * 82)
    print("CASE: REAL PRICE COVERAGE BOUNDARY")
    print("=" * 82)

    rows = conn.execute(
        """
        SELECT
            ticker,
            reference_price_date
        FROM ai_decision_portfolio_snapshot
        WHERE history_id = ?
          AND ticker != 'CASH'
        ORDER BY id
        """,
        (history_id,),
    ).fetchall()

    assert_equal(
        len(rows),
        3,
        "portfolio -> three ETF positions",
    )

    for ticker, reference_date in rows:
        latest = conn.execute(
            """
            SELECT MAX(date)
            FROM etf_prices
            WHERE ticker = ?
            """,
            (ticker,),
        ).fetchone()[0]

        assert_equal(
            latest,
            reference_date,
            f"{ticker} -> price coverage ends at reference date",
        )

    print("")
    print("=" * 82)
    print("CASE: EVALUATION WAITING CONTRACT")
    print("=" * 82)

    result = evaluate_ai_decision_portfolio_snapshot(
        history_id=history_id
    )

    assert_equal(
        result.get("evaluation_status"),
        "WAITING_FOR_OUTCOME",
        "evaluation -> waiting for outcome",
    )

    assert_equal(
        result.get("outcome_status"),
        "PENDING",
        "evaluation -> pending outcome",
    )

    assert_equal(
        result.get("portfolio_return"),
        None,
        "evaluation -> no portfolio return",
    )

    assert_equal(
        result.get("evaluated_weight"),
        10.0,
        "evaluation -> only CASH evaluated",
    )

    assert_equal(
        result.get("pending_positions"),
        3,
        "evaluation -> three pending ETF positions",
    )

    print("")
    print("=" * 82)
    print("CASE: POSITION STATUS INTEGRITY")
    print("=" * 82)

    positions = result.get("positions")

    assert_true(
        isinstance(positions, list),
        "evaluation -> positions list",
    )

    assert_equal(
        len(positions),
        4,
        "evaluation -> four positions",
    )

    etf_positions = [
        position
        for position in positions
        if position.get("ticker") != "CASH"
    ]

    cash_positions = [
        position
        for position in positions
        if position.get("ticker") == "CASH"
    ]

    assert_equal(
        len(etf_positions),
        3,
        "positions -> three ETF positions",
    )

    assert_equal(
        len(cash_positions),
        1,
        "positions -> one CASH position",
    )

    for position in etf_positions:
        assert_equal(
            position.get("status"),
            "WAITING_FOR_OUTCOME",
            f"{position.get('ticker')} -> waiting",
        )

        assert_equal(
            position.get("evaluation_price"),
            None,
            f"{position.get('ticker')} -> no fabricated evaluation price",
        )

        assert_equal(
            position.get("return_pct"),
            None,
            f"{position.get('ticker')} -> no fabricated return",
        )

    cash = cash_positions[0]

    assert_equal(
        cash.get("status"),
        "EVALUATED",
        "CASH -> evaluated",
    )

    assert_equal(
        cash.get("return_pct"),
        0.0,
        "CASH -> zero return",
    )

    print("")
    print("=" * 82)
    print("CASE: NO FABRICATED PORTFOLIO OUTCOME")
    print("=" * 82)

    assert_equal(
        result.get("portfolio_return"),
        None,
        "no future price -> no fabricated portfolio return",
    )

    assert_equal(
        result.get("outcome_status"),
        "PENDING",
        "no future price -> outcome remains pending",
    )

    print("")
    print("=" * 82)
    print("CASE: PERSISTED HISTORY REMAINS PENDING")
    print("=" * 82)

    persisted = conn.execute(
        """
        SELECT
            outcome_status,
            portfolio_return,
            portfolio_evaluation_date
        FROM ai_decision_outcome_history
        WHERE id = ?
        """,
        (history_id,),
    ).fetchone()

    assert_equal(
        persisted[0],
        "PENDING",
        "history -> remains pending after waiting evaluation",
    )

    assert_equal(
        persisted[1],
        None,
        "history -> return remains null",
    )

    assert_equal(
        persisted[2],
        None,
        "history -> evaluation date remains null",
    )

    print("")
    print("=" * 82)
    print("===== PHASE 7-10-20-25 EVALUATION WAITING BOUNDARY COMPLETE =====")
    print("=" * 82)

finally:
    conn.close()
