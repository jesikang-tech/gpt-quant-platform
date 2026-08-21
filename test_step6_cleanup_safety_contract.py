def cleanup_action_for_retention(retention):
    """
    Production Hardening Safety Contract.

    Retention classification never directly authorizes deletion.
    Every current retention state requires NO_AUTO_DELETE.
    """

    if retention in (
        "PROTECTED",
        "RETAIN_LONG_TERM",
        "RETAIN",
    ):
        return "NO_AUTO_DELETE"

    if retention == "REVIEW_REQUIRED":
        return "REVIEW_ONLY"

    return "NO_ACTION"


def run_case(
    name,
    retention,
    expected,
):
    actual = cleanup_action_for_retention(
        retention
    )

    assert actual == expected

    print(
        f"{name}: PASS | "
        f"retention={retention} | "
        f"action={actual}"
    )


print("=" * 60)
print(
    "Production Hardening - Cleanup Safety Contract"
)
print("=" * 60)


run_case(
    "CASE 1 PROTECTED",
    "PROTECTED",
    "NO_AUTO_DELETE",
)

run_case(
    "CASE 2 RETAIN LONG TERM",
    "RETAIN_LONG_TERM",
    "NO_AUTO_DELETE",
)

run_case(
    "CASE 3 RETAIN",
    "RETAIN",
    "NO_AUTO_DELETE",
)

run_case(
    "CASE 4 REVIEW REQUIRED",
    "REVIEW_REQUIRED",
    "REVIEW_ONLY",
)

run_case(
    "CASE 5 UNKNOWN",
    "UNKNOWN",
    "NO_ACTION",
)


print("")
print("=" * 60)
print("OVERALL RESULT: PASS")
print("=" * 60)
