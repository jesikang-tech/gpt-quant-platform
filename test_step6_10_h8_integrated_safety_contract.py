def integrated_safety(
    lifecycle,
    age_days,
):
    if lifecycle == "ACTIVE_OUTCOME_TRACKING":
        retention = "PROTECTED"

    elif lifecycle == "COMPLETED":
        retention = "RETAIN_LONG_TERM"

    elif lifecycle in (
        "LEGACY_ORPHAN_CANDIDATE",
        "LEGACY_EVALUATED_CANDIDATE",
    ):
        if age_days < 7:
            retention = "RETAIN"
        else:
            retention = "REVIEW_REQUIRED"

    else:
        retention = "UNKNOWN"

    if retention == "REVIEW_REQUIRED":
        cleanup_candidate = True
        auto_delete = False
        action = "REVIEW_ONLY"

    elif retention in (
        "PROTECTED",
        "RETAIN_LONG_TERM",
        "RETAIN",
    ):
        cleanup_candidate = False
        auto_delete = False
        action = "NO_AUTO_DELETE"

    else:
        cleanup_candidate = False
        auto_delete = False
        action = "NO_ACTION"

    return {
        "lifecycle": lifecycle,
        "retention": retention,
        "cleanup_candidate": cleanup_candidate,
        "auto_delete": auto_delete,
        "cleanup_action": action,
    }


def run_case(
    name,
    lifecycle,
    age_days,
    expected_retention,
    expected_candidate,
    expected_auto_delete,
    expected_action,
):
    result = integrated_safety(
        lifecycle,
        age_days,
    )

    assert result["retention"] == expected_retention
    assert result["cleanup_candidate"] is expected_candidate
    assert result["auto_delete"] is expected_auto_delete
    assert result["cleanup_action"] == expected_action

    print(
        f"{name}: PASS | "
        f"lifecycle={lifecycle} | "
        f"age={age_days} | "
        f"retention={result['retention']} | "
        f"candidate={result['cleanup_candidate']} | "
        f"auto_delete={result['auto_delete']} | "
        f"action={result['cleanup_action']}"
    )


print("=" * 60)
print(
    "Step6-10-H-8 Lifecycle / Retention / Cleanup "
    "Integrated Safety Contract"
)
print("=" * 60)

run_case(
    "CASE 1 ACTIVE",
    "ACTIVE_OUTCOME_TRACKING",
    120,
    "PROTECTED",
    False,
    False,
    "NO_AUTO_DELETE",
)

run_case(
    "CASE 2 COMPLETED",
    "COMPLETED",
    120,
    "RETAIN_LONG_TERM",
    False,
    False,
    "NO_AUTO_DELETE",
)

run_case(
    "CASE 3 LEGACY YOUNG",
    "LEGACY_ORPHAN_CANDIDATE",
    6,
    "RETAIN",
    False,
    False,
    "NO_AUTO_DELETE",
)

run_case(
    "CASE 4 LEGACY OLD",
    "LEGACY_ORPHAN_CANDIDATE",
    30,
    "REVIEW_REQUIRED",
    True,
    False,
    "REVIEW_ONLY",
)

run_case(
    "CASE 5 LEGACY EVALUATED OLD",
    "LEGACY_EVALUATED_CANDIDATE",
    30,
    "REVIEW_REQUIRED",
    True,
    False,
    "REVIEW_ONLY",
)

run_case(
    "CASE 6 UNKNOWN",
    "UNKNOWN",
    30,
    "UNKNOWN",
    False,
    False,
    "NO_ACTION",
)

print("")
print("=" * 60)
print("OVERALL RESULT: PASS")
print("=" * 60)
