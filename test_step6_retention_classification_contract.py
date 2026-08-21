from datetime import datetime, timedelta
from repository import get_connection


REVIEW_DAYS = 7


def classify_retention(
    lifecycle,
    age_days,
):
    if lifecycle == "ACTIVE_OUTCOME_TRACKING":
        return "PROTECTED"

    if lifecycle == "COMPLETED":
        return "RETAIN_LONG_TERM"

    if lifecycle in (
        "LEGACY_EVALUATED_CANDIDATE",
        "LEGACY_ORPHAN_CANDIDATE",
    ):
        if age_days < REVIEW_DAYS:
            return "RETAIN"

        return "REVIEW_REQUIRED"

    return "UNKNOWN"


def run_case(
    name,
    lifecycle,
    age_days,
    expected,
):
    actual = classify_retention(
        lifecycle,
        age_days,
    )

    assert actual == expected

    print(
        f"{name}: PASS | "
        f"lifecycle={lifecycle} | "
        f"age={age_days} | "
        f"retention={actual}"
    )


print("=" * 60)
print(
    "Production Hardening - Retention Classification Contract"
)
print("=" * 60)


run_case(
    "CASE 1 ACTIVE YOUNG",
    "ACTIVE_OUTCOME_TRACKING",
    1,
    "PROTECTED",
)

run_case(
    "CASE 2 ACTIVE OLD",
    "ACTIVE_OUTCOME_TRACKING",
    120,
    "PROTECTED",
)

run_case(
    "CASE 3 COMPLETED",
    "COMPLETED",
    45,
    "RETAIN_LONG_TERM",
)

run_case(
    "CASE 4 LEGACY EVALUATED YOUNG",
    "LEGACY_EVALUATED_CANDIDATE",
    5,
    "RETAIN",
)

run_case(
    "CASE 5 LEGACY EVALUATED OLD",
    "LEGACY_EVALUATED_CANDIDATE",
    30,
    "REVIEW_REQUIRED",
)

run_case(
    "CASE 6 LEGACY ORPHAN YOUNG",
    "LEGACY_ORPHAN_CANDIDATE",
    6,
    "RETAIN",
)

run_case(
    "CASE 7 LEGACY ORPHAN OLD",
    "LEGACY_ORPHAN_CANDIDATE",
    90,
    "REVIEW_REQUIRED",
)

run_case(
    "CASE 8 UNKNOWN",
    "UNKNOWN",
    10,
    "UNKNOWN",
)


print("")
print("--- CURRENT DATABASE RETENTION CLASSIFICATION ---")


def lifecycle(
    outcome_status,
    snapshot_count,
):
    if outcome_status == "PENDING":
        return (
            "ACTIVE_OUTCOME_TRACKING"
            if snapshot_count > 0
            else "LEGACY_ORPHAN_CANDIDATE"
        )

    if outcome_status == "EVALUATED":
        return (
            "COMPLETED"
            if snapshot_count > 0
            else "LEGACY_EVALUATED_CANDIDATE"
        )

    return "UNKNOWN"


conn = get_connection()
cursor = conn.cursor()

cursor.execute(
    """
    SELECT
        h.id,
        h.created_at,
        h.outcome_status,
        COUNT(s.id) AS snapshot_count
    FROM ai_decision_outcome_history h
    LEFT JOIN ai_decision_portfolio_snapshot s
        ON s.history_id = h.id
    GROUP BY
        h.id,
        h.created_at,
        h.outcome_status
    ORDER BY h.created_at ASC
    """
)

rows = cursor.fetchall()

now = datetime.now().astimezone()

for row in rows:
    history_id = row[0]
    created_at = row[1]
    outcome_status = row[2]
    snapshot_count = row[3]

    try:
        created = datetime.fromisoformat(
            created_at
        )

        if created.tzinfo is None:
            created = created.replace(
                tzinfo=now.tzinfo
            )

        age_days = (
            now - created
        ).total_seconds() / 86400.0

    except Exception:
        age_days = None

    current_lifecycle = lifecycle(
        outcome_status,
        snapshot_count,
    )

    retention = classify_retention(
        current_lifecycle,
        age_days
        if age_days is not None
        else 0,
    )

    print({
        "history_id": history_id,
        "age_days": (
            round(age_days, 3)
            if age_days is not None
            else None
        ),
        "lifecycle": current_lifecycle,
        "retention": retention,
    })


conn.close()

print("")
print("=" * 60)
print("OVERALL RESULT: PASS")
print("=" * 60)
