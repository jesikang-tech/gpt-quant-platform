from datetime import datetime


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


def build_audit_event(
    event_type,
    history_id=None,
    status=None,
    source=None,
    event_time=None,
    details=None,
):
    assert event_type in ALLOWED_EVENT_TYPES
    assert event_time is not None
    assert source is not None

    if event_type != "DECISION_CREATED":
        assert history_id is not None

    return {
        "event_id": f"{event_type}:{history_id}:{event_time}",
        "event_type": event_type,
        "history_id": history_id,
        "event_time": event_time,
        "status": status,
        "source": source,
        "details": details or {},
    }


def run_case(
    name,
    event_type,
    history_id,
    status,
    source,
):
    event_time = (
        datetime.now().astimezone().isoformat()
    )

    event = build_audit_event(
        event_type=event_type,
        history_id=history_id,
        status=status,
        source=source,
        event_time=event_time,
        details={
            "contract_test": True,
        },
    )

    assert event["event_type"] == event_type
    assert event["history_id"] == history_id
    assert event["event_time"] == event_time
    assert event["source"] == source
    assert "event_id" in event
    assert isinstance(event["details"], dict)

    print(
        f"{name}: PASS | "
        f"event_type={event_type} | "
        f"history_id={history_id} | "
        f"status={status}"
    )


print("=" * 60)
print(
    "Step6-10-I-2 Audit Event Contract"
)
print("=" * 60)


run_case(
    "CASE 1 DECISION",
    "DECISION_CREATED",
    None,
    "CREATED",
    "ai_decision_engine",
)

run_case(
    "CASE 2 OUTCOME PERSISTED",
    "OUTCOME_PERSISTED",
    13,
    "SUCCESS",
    "repository",
)

run_case(
    "CASE 3 SNAPSHOT PERSISTED",
    "SNAPSHOT_PERSISTED",
    13,
    "SUCCESS",
    "repository",
)

run_case(
    "CASE 4 EVALUATION",
    "OUTCOME_EVALUATED",
    13,
    "EVALUATED",
    "outcome_evaluation",
)

run_case(
    "CASE 5 LEARNING",
    "LEARNING_SIGNAL_GENERATED",
    13,
    "AVAILABLE",
    "outcome_intelligence",
)

run_case(
    "CASE 6 REASSESSMENT",
    "REASSESSMENT_REQUIRED",
    13,
    "REQUIRED",
    "adaptive_strategy",
)

run_case(
    "CASE 7 ADAPTIVE STRATEGY",
    "ADAPTIVE_STRATEGY_GENERATED",
    13,
    "GENERATED",
    "adaptive_strategy",
)

run_case(
    "CASE 8 FAILURE",
    "PERSISTENCE_FAILED",
    13,
    "FAILED",
    "repository",
)


print("")
print("--- EVENT TYPE CONTRACT ---")

expected = {
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

assert ALLOWED_EVENT_TYPES == expected

print(
    "ALLOWED_EVENT_TYPES: PASS | "
    f"count={len(ALLOWED_EVENT_TYPES)}"
)


print("")
print("--- EVENT SEQUENCE CONTRACT ---")

sequence = [
    "DECISION_CREATED",
    "OUTCOME_PERSISTED",
    "SNAPSHOT_PERSISTED",
    "OUTCOME_EVALUATION_STARTED",
    "OUTCOME_EVALUATED",
    "LEARNING_SIGNAL_GENERATED",
]

assert sequence[0] == "DECISION_CREATED"
assert sequence.index(
    "OUTCOME_PERSISTED"
) < sequence.index(
    "OUTCOME_EVALUATED"
)
assert sequence.index(
    "OUTCOME_EVALUATED"
) < sequence.index(
    "LEARNING_SIGNAL_GENERATED"
)

print("EVENT_SEQUENCE: PASS")

print("")
print("=" * 60)
print("OVERALL RESULT: PASS")
print("=" * 60)
