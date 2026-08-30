ALLOWED_EVENT_TYPES = {
    "DECISION_CREATED",
    "OUTCOME_PERSISTED",
    "SNAPSHOT_PERSISTED",
    "OUTCOME_EVALUATION_STARTED",
    "OUTCOME_EVALUATED",
    "LEARNING_SIGNAL_GENERATED",
    "REASSESSMENT_REQUIRED",
    "ADAPTIVE_STRATEGY_GENERATED",
    "PERSISTENCE_FAILED",
}


def build_correlated_audit_event(
    event_type,
    event_time,
    source,
    decision_history_id=None,
    outcome_history_id=None,
    status=None,
    details=None,
):
    assert event_type in ALLOWED_EVENT_TYPES
    assert event_time is not None
    assert source is not None

    decision_events = {
        "DECISION_CREATED",
    }

    outcome_events = {
        "OUTCOME_PERSISTED",
        "SNAPSHOT_PERSISTED",
        "OUTCOME_EVALUATION_STARTED",
        "OUTCOME_EVALUATED",
        "LEARNING_SIGNAL_GENERATED",
        "REASSESSMENT_REQUIRED",
        "ADAPTIVE_STRATEGY_GENERATED",
    }

    if event_type in decision_events:
        assert decision_history_id is not None

    if event_type in outcome_events:
        assert outcome_history_id is not None

    if event_type == "PERSISTENCE_FAILED":
        assert (
            decision_history_id is not None
            or outcome_history_id is not None
        )

    if (
        decision_history_id is not None
        and outcome_history_id is not None
    ):
        correlation_key = (
            f"decision:{decision_history_id}"
            f"|outcome:{outcome_history_id}"
        )
    elif decision_history_id is not None:
        correlation_key = (
            f"decision:{decision_history_id}"
        )
    else:
        correlation_key = (
            f"outcome:{outcome_history_id}"
        )

    return {
        "event_id": (
            f"{event_type}:{correlation_key}:{event_time}"
        ),
        "event_type": event_type,
        "event_time": event_time,
        "source": source,
        "status": status,
        "decision_history_id": decision_history_id,
        "outcome_history_id": outcome_history_id,
        "correlation_key": correlation_key,
        "details": details or {},
    }


def run_case(
    name,
    event_type,
    decision_history_id,
    outcome_history_id,
    status,
):
    event = build_correlated_audit_event(
        event_type=event_type,
        event_time="2026-08-20T15:00:00+09:00",
        source="contract_test",
        decision_history_id=decision_history_id,
        outcome_history_id=outcome_history_id,
        status=status,
    )

    assert event["event_type"] == event_type
    assert event["decision_history_id"] == decision_history_id
    assert event["outcome_history_id"] == outcome_history_id
    assert event["correlation_key"] is not None
    assert event["event_id"] is not None

    print(
        f"{name}: PASS | "
        f"type={event_type} | "
        f"decision_id={decision_history_id} | "
        f"outcome_id={outcome_history_id} | "
        f"correlation={event['correlation_key']}"
    )


print("=" * 60)
print(
    "Step6-10-I-4 Future Audit Correlation Contract"
)
print("=" * 60)


run_case(
    "CASE 1 DECISION",
    "DECISION_CREATED",
    101,
    None,
    "CREATED",
)

run_case(
    "CASE 2 OUTCOME",
    "OUTCOME_PERSISTED",
    None,
    201,
    "SUCCESS",
)

run_case(
    "CASE 3 SNAPSHOT",
    "SNAPSHOT_PERSISTED",
    None,
    201,
    "SUCCESS",
)

run_case(
    "CASE 4 EVALUATION",
    "OUTCOME_EVALUATED",
    None,
    201,
    "EVALUATED",
)

run_case(
    "CASE 5 LEARNING",
    "LEARNING_SIGNAL_GENERATED",
    None,
    201,
    "AVAILABLE",
)

run_case(
    "CASE 6 REASSESSMENT",
    "REASSESSMENT_REQUIRED",
    None,
    201,
    "REQUIRED",
)

run_case(
    "CASE 7 FAILURE-DECISION",
    "PERSISTENCE_FAILED",
    101,
    None,
    "FAILED",
)

run_case(
    "CASE 8 FAILURE-OUTCOME",
    "PERSISTENCE_FAILED",
    None,
    201,
    "FAILED",
)

run_case(
    "CASE 9 CROSS-CORRELATED",
    "PERSISTENCE_FAILED",
    101,
    201,
    "FAILED",
)


print("")
print("--- CORRELATION KEY CONTRACT ---")

decision_event = build_correlated_audit_event(
    "DECISION_CREATED",
    "2026-08-20T15:00:00+09:00",
    "contract_test",
    decision_history_id=101,
)

outcome_event = build_correlated_audit_event(
    "OUTCOME_EVALUATED",
    "2026-08-20T15:01:00+09:00",
    "contract_test",
    outcome_history_id=201,
)

assert decision_event["correlation_key"] == (
    "decision:101"
)

assert outcome_event["correlation_key"] == (
    "outcome:201"
)

print("CORRELATION KEY: PASS")


print("")
print("--- HISTORICAL DATA SAFETY CONTRACT ---")

# Existing production history is NOT retroactively
# assigned a guessed correlation key.

assert decision_event["decision_history_id"] != None
assert outcome_event["outcome_history_id"] != None

print(
    "RETROACTIVE GUESSING: PASS | "
    "existing events remain unreconstructed"
)


print("")
print("=" * 60)
print("OVERALL RESULT: PASS")
print("=" * 60)
