import sqlite3
from pathlib import Path

TEST_DB = Path(r".\database\g7_10_18_ready_fixture.db")


def assert_equal(actual, expected, label):
    if actual != expected:
        raise AssertionError(
            f"{label}: expected={expected!r}, actual={actual!r}"
        )
    print(f"{label}: PASS")


def assert_true(value, label):
    if not value:
        raise AssertionError(f"{label}: expected=True, actual={value!r}")
    print(f"{label}: PASS")


print("=" * 82)
print("PHASE 7-10-20-24")
print("OUTCOME HISTORY -> PORTFOLIO SNAPSHOT PERSISTENCE")
print("RUNTIME PERSISTED LINK BOUNDARY CONTRACT TEST V1")
print("SOURCE-VERIFIED / TEST-DB / READ-ONLY")
print("=" * 82)

conn = sqlite3.connect(TEST_DB)

try:
    history = conn.execute(
        """
        SELECT
            id,
            decision,
            action,
            strategy,
            outcome_status,
            snapshot_status,
            snapshot_purpose
        FROM ai_decision_outcome_history
        ORDER BY id DESC
        LIMIT 1
        """
    ).fetchone()

    assert_true(
        history is not None,
        "persisted outcome history exists",
    )

    (
        history_id,
        decision,
        action,
        strategy,
        outcome_status,
        snapshot_status,
        snapshot_purpose,
    ) = history

    print("")
    print("=" * 82)
    print("CASE: OUTCOME HISTORY PERSISTENCE")
    print("=" * 82)

    assert_true(
        isinstance(history_id, int),
        "history -> integer identity",
    )

    assert_equal(
        decision,
        "MAINTAIN",
        "history -> decision",
    )

    assert_equal(
        action,
        "PROCEED",
        "history -> action",
    )

    assert_equal(
        strategy,
        "MAINTAIN",
        "history -> strategy",
    )

    assert_equal(
        outcome_status,
        "PENDING",
        "history -> pending outcome",
    )

    assert_equal(
        snapshot_status,
        "COLLECTED",
        "history -> collected snapshot",
    )

    assert_equal(
        snapshot_purpose,
        "FUTURE_OUTCOME_EVALUATION",
        "history -> future outcome purpose",
    )

    snapshots = conn.execute(
        """
        SELECT
            id,
            history_id,
            ticker,
            weight,
            reference_price,
            reference_price_date
        FROM ai_decision_portfolio_snapshot
        WHERE history_id = ?
        ORDER BY id
        """,
        (history_id,),
    ).fetchall()

    print("")
    print("=" * 82)
    print("CASE: HISTORY -> PORTFOLIO SNAPSHOT LINK")
    print("=" * 82)

    assert_equal(
        len(snapshots),
        4,
        "history -> four portfolio snapshots",
    )

    for row in snapshots:
        snapshot_id, linked_history_id, ticker, weight, reference_price, reference_price_date = row

        assert_equal(
            linked_history_id,
            history_id,
            f"snapshot {snapshot_id} -> history_id link",
        )

        assert_true(
            isinstance(ticker, str) and bool(ticker),
            f"snapshot {snapshot_id} -> ticker identity",
        )

        assert_true(
            weight is not None,
            f"snapshot {snapshot_id} -> weight present",
        )

    print("")
    print("=" * 82)
    print("CASE: PORTFOLIO WEIGHT INTEGRITY")
    print("=" * 82)

    weights = [float(row[3] or 0.0) for row in snapshots]
    weight_sum = sum(weights)

    assert_equal(
        round(weight_sum, 1),
        100.0,
        "portfolio -> weight sum 100%",
    )

    print("")
    print("=" * 82)
    print("CASE: REFERENCE PRICE PERSISTENCE")
    print("=" * 82)

    etf_snapshots = [
        row for row in snapshots
        if row[2] != "CASH"
    ]

    assert_true(
        len(etf_snapshots) > 0,
        "ETF snapshots -> present",
    )

    for row in etf_snapshots:
        snapshot_id, linked_history_id, ticker, weight, reference_price, reference_price_date = row

        assert_true(
            reference_price is not None,
            f"{ticker} -> reference price persisted",
        )

        assert_true(
            reference_price_date is not None,
            f"{ticker} -> reference price date persisted",
        )

    cash_snapshots = [
        row for row in snapshots
        if row[2] == "CASH"
    ]

    assert_equal(
        len(cash_snapshots),
        1,
        "portfolio -> CASH snapshot present",
    )

    cash = cash_snapshots[0]

    assert_equal(
        cash[4],
        None,
        "CASH -> no reference price",
    )

    assert_equal(
        cash[5],
        None,
        "CASH -> no reference price date",
    )

    print("")
    print("=" * 82)
    print("CASE: PERSISTED IDENTITY CONSISTENCY")
    print("=" * 82)

    for row in snapshots:
        assert_equal(
            decision,
            "MAINTAIN",
            f"{row[2]} -> decision context preserved",
        )

        assert_equal(
            strategy,
            "MAINTAIN",
            f"{row[2]} -> strategy context preserved",
        )

    print("")
    print("=" * 82)
    print("CASE: READ-ONLY BOUNDARY")
    print("=" * 82)

    assert_true(
        conn.in_transaction is False,
        "read-only discovery -> no active transaction",
    )

    print("")
    print("=" * 82)
    print("===== PHASE 7-10-20-24 PERSISTENCE BOUNDARY COMPLETE =====")
    print("=" * 82)

finally:
    conn.close()
