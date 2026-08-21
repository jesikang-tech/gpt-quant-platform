def classify_cleanup_candidate(retention):
    if retention == "REVIEW_REQUIRED":
        return {
            "cleanup_candidate": True,
            "auto_delete": False,
            "action": "REVIEW_ONLY",
        }

    if retention in (
        "PROTECTED",
        "RETAIN_LONG_TERM",
        "RETAIN",
    ):
        return {
            "cleanup_candidate": False,
            "auto_delete": False,
            "action": "NO_AUTO_DELETE",
        }

    return {
        "cleanup_candidate": False,
        "auto_delete": False,
        "action": "NO_ACTION",
    }


def run_case(
    name,
    retention,
    expected_candidate,
    expected_auto_delete,
    expected_action,
):
    result = classify_cleanup_candidate(retention)

    assert (
        result["cleanup_candidate"]
        is expected_candidate
    )

    assert (
        result["auto_delete"]
        is expected_auto_delete
    )

    assert result["action"] == expected_action

    print(
        f"{name}: PASS | "
        f"retention={retention} | "
        f"candidate={result['cleanup_candidate']} | "
        f"auto_delete={result['auto_delete']} | "
        f"action={result['action']}"
    )


print("=" * 60)
print(
    "Production Hardening - Cleanup Candidate Contract"
)
print("=" * 60)


run_case(
    "CASE 1 PROTECTED",
    "PROTECTED",
    False,
    False,
    "NO_AUTO_DELETE",
)

run_case(
    "CASE 2 RETAIN LONG TERM",
    "RETAIN_LONG_TERM",
    False,
    False,
    "NO_AUTO_DELETE",
)

run_case(
    "CASE 3 RETAIN",
    "RETAIN",
    False,
    False,
    "NO_AUTO_DELETE",
)

run_case(
    "CASE 4 REVIEW REQUIRED",
    "REVIEW_REQUIRED",
    True,
    False,
    "REVIEW_ONLY",
)

run_case(
    "CASE 5 UNKNOWN",
    "UNKNOWN",
    False,
    False,
    "NO_ACTION",
)


print("")
print("=" * 60)
print("OVERALL RESULT: PASS")
print("=" * 60)
