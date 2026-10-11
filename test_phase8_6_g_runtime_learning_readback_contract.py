"""Learning readback contract using the isolated lifecycle harness."""
from price_test_support import isolated_evaluation_api, isolated_price_db


def test_runtime_learning_readback(isolated_evaluation_api):
    from test_step6_10_g_outcome_lifecycle import run_case

    print("=" * 60)
    print(
        "Phase8-6-G Runtime Learning/Adaptive Read-Back Contract"
    )
    print("=" * 60)

    print("")
    print("CASE 1 POSITIVE DOWNSTREAM LEARNING BASELINE")

    run_case(
        isolated_evaluation_api,
        "CASE 1 POSITIVE",
        10.0,
        100.0,
        "A",
        "POSITIVE",
        "LEARNING_AVAILABLE",
        "LEARNING_AVAILABLE",
        False,
        False,
        "NOT_REQUIRED",
    )

    print("")
    print("CASE 2 NEGATIVE DOWNSTREAM LEARNING BASELINE")

    run_case(
        isolated_evaluation_api,
        "CASE 2 NEGATIVE",
        -10.0,
        0.0,
        "F",
        "NEGATIVE",
        "ADAPTIVE_LEARNING_REQUIRED",
        "ADAPTIVE_LEARNING",
        True,
        True,
        "REASSESSMENT_REQUIRED",
    )

    print("")
    print("=" * 60)
    print("OVERALL RESULT: PASS")
    print("=" * 60)
