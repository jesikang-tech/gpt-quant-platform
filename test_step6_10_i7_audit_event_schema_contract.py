AUDIT_REQUIRED_FIELDS = {
    "audit_event_id",
    "event_type",
    "event_time",
    "source",
    "status",
    "decision_history_id",
    "outcome_history_id",
    "correlation_key",
    "details",
}


AUDIT_EVENT_TYPES = {
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


FORBIDDEN_BUSINESS_STATE_DUPLICATES = {
    "outcome_status",
    "learning_status",
    "feedback_state",
    "reassessment_status",
}


def validate_audit_schema(event):
    required = set(event.keys())

    missing = AUDIT_REQUIRED_FIELDS - required

    forbidden = (
        FORBIDDEN_BUSINESS_STATE_DUPLICATES
        & required
    )

    assert not missing
    assert not forbidden

    assert (
        event["event_type"]
        in AUDIT_EVENT_TYPES
    )

    assert event["audit_event_id"]
    assert event["event_time"]
    assert event["source"]
    assert event["correlation_key"]

    assert isinstance(
        event["details"],
        dict,
    )


def run_case(
    name,
    event,
    expected_valid,
):
    valid = True

    try:
        validate_audit_schema(event)
    except AssertionError:
        valid = False

    assert valid is expected_valid

    print(
        f"{name}: PASS | "
        f"valid={valid} | "
        f"type={event.get('event_type')}"
    )


print("=" * 60)
print(
    "Step6-10-I-7 Audit Event Schema Contract Test"
)
print("=" * 60)


valid_event = {
    "audit_event_id":
        "OUTCOME_EVALUATED:outcome:201:1",

    "event_type":
        "OUTCOME_EVALUATED",

    "event_time":
        "2026-08-20T15:00:00+09:00",

    "source":
        "outcome_evaluation",

    "status":
        "EVALUATED",

    "decision_history_id":
        None,

    "outcome_history_id":
        201,

    "correlation_key":
        "outcome:201",

    "details": {
        "portfolio_return": 5.0,
    },
}


run_case(
    "CASE 1 VALID SCHEMA",
    valid_event,
    True,
)


missing_event_type = dict(valid_event)
del missing_event_type["event_type"]

run_case(
    "CASE 2 MISSING EVENT TYPE",
    missing_event_type,
    False,
)


missing_correlation = dict(valid_event)
del missing_correlation["correlation_key"]

run_case(
    "CASE 3 MISSING CORRELATION",
    missing_correlation,
    False,
)


duplicated_business_state = dict(valid_event)
duplicated_business_state["learning_status"] = (
    "WAITING_FOR_OUTCOME"
)

run_case(
    "CASE 4 BUSINESS STATE DUPLICATION",
    duplicated_business_state,
    False,
)


invalid_event_type = dict(valid_event)
invalid_event_type["event_type"] = (
    "UNKNOWN_EVENT"
)

run_case(
    "CASE 5 UNKNOWN EVENT TYPE",
    invalid_event_type,
    False,
)


empty_details = dict(valid_event)
empty_details["details"] = {}

run_case(
    "CASE 6 EMPTY DETAILS OBJECT",
    empty_details,
    True,
)


print("")
print("--- REQUIRED FIELD CONTRACT ---")

assert AUDIT_REQUIRED_FIELDS == {
    "audit_event_id",
    "event_type",
    "event_time",
    "source",
    "status",
    "decision_history_id",
    "outcome_history_id",
    "correlation_key",
    "details",
}

print(
    "REQUIRED_FIELDS: PASS | "
    f"count={len(AUDIT_REQUIRED_FIELDS)}"
)


print("")
print("--- EVENT TYPE CONTRACT ---")

assert len(AUDIT_EVENT_TYPES) == 9

print(
    "EVENT_TYPES: PASS | "
    f"count={len(AUDIT_EVENT_TYPES)}"
)


print("")
print("--- BUSINESS STATE SEPARATION CONTRACT ---")

for field in FORBIDDEN_BUSINESS_STATE_DUPLICATES:
    assert field not in AUDIT_REQUIRED_FIELDS

print("BUSINESS_STATE_SEPARATION: PASS")


print("")
print("=" * 60)
print("OVERALL RESULT: PASS")
print("=" * 60)
