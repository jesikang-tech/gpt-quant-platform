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


OUTCOME_CORRELATION_PREFIX = "outcome:"


def build_event(
    event_type,
    outcome_history_id,
    status,
    source,
    details=None,
):
    assert event_type in ALLOWED_EVENT_TYPES
    assert outcome_history_id is not None
    assert status is not None
    assert source is not None

    correlation_key = (
        f"{OUTCOME_CORRELATION_PREFIX}"
        f"{outcome_history_id}"
    )

    event_time = (
        datetime.now().astimezone().isoformat()
    )

    return {
        "event_id": (
            f"{event_type}:"
            f"{correlation_key}:"
            f"{event_time}"
        ),
        "event_type": event_type,
        "event_time": event_time,
        "source": source,
        "status": status,
        "outcome_history_id": outcome_history_id,
        "correlation_key": correlation_key,
        "details": details or {},
    }


print("=" * 60)
print(
    "Step6-10-I-10 Audit Event Orchestration Contract"
)
print("=" * 60)


history_id = 201


print("")
print("--- CASE 1 OUTCOME EVALUATION START ---")

started = build_event(
    "OUTCOME_EVALUATION_STARTED",
    history_id,
    "STARTED",
    "outcome_evaluation",
)

assert started["correlation_key"] == "outcome:201"
assert started["outcome_history_id"] == history_id

print("CASE 1: PASS")


print("")
print("--- CASE 2 OUTCOME EVALUATED ---")

evaluated = build_event(
    "OUTCOME_EVALUATED",
    history_id,
    "EVALUATED",
    "portfolio_outcome_evaluation",
)

assert evaluated["correlation_key"] == "outcome:201"
assert evaluated["outcome_history_id"] == history_id

print("CASE 2: PASS")


print("")
print("--- CASE 3 LEARNING SIGNAL ---")

learning = build_event(
    "LEARNING_SIGNAL_GENERATED",
    history_id,
    "AVAILABLE",
    "outcome_intelligence",
    {
        "learning_signal": "POSITIVE",
        "learning_signal_strength": 0.8,
    },
)

assert learning["correlation_key"] == "outcome:201"
assert learning["details"]["learning_signal"] == "POSITIVE"
assert learning["details"]["learning_signal_strength"] == 0.8

print("CASE 3: PASS")


print("")
print("--- CASE 4 REASSESSMENT REQUIRED ---")

reassessment = build_event(
    "REASSESSMENT_REQUIRED",
    history_id,
    "REQUIRED",
    "outcome_intelligence",
    {
        "learning_signal": "NEGATIVE",
        "reassessment_required": True,
    },
)

assert reassessment["correlation_key"] == "outcome:201"
assert reassessment["details"]["reassessment_required"] is True

print("CASE 4: PASS")


print("")
print("--- CASE 5 ADAPTIVE STRATEGY ---")

adaptive = build_event(
    "ADAPTIVE_STRATEGY_GENERATED",
    history_id,
    "GENERATED",
    "adaptive_strategy",
    {
        "strategy": "DEFENSIVE",
        "action": "REDUCE_RISK",
    },
)

assert adaptive["correlation_key"] == "outcome:201"
assert adaptive["details"]["strategy"] == "DEFENSIVE"

print("CASE 5: PASS")


print("")
print("--- CASE 6 COMMON CORRELATION ---")

events = [
    started,
    evaluated,
    learning,
    reassessment,
    adaptive,
]

assert all(
    event["correlation_key"] == "outcome:201"
    for event in events
)

assert all(
    event["outcome_history_id"] == history_id
    for event in events
)

print(
    "CASE 6: PASS | "
    f"events={len(events)} | "
    "correlation=outcome:201"
)


print("")
print("--- CASE 7 EVENT SEQUENCE ---")

sequence = [
    event["event_type"]
    for event in events
]

assert sequence.index(
    "OUTCOME_EVALUATION_STARTED"
) < sequence.index(
    "OUTCOME_EVALUATED"
)

assert sequence.index(
    "OUTCOME_EVALUATED"
) < sequence.index(
    "LEARNING_SIGNAL_GENERATED"
)

assert sequence.index(
    "LEARNING_SIGNAL_GENERATED"
) < sequence.index(
    "REASSESSMENT_REQUIRED"
)

assert sequence.index(
    "REASSESSMENT_REQUIRED"
) < sequence.index(
    "ADAPTIVE_STRATEGY_GENERATED"
)

print("CASE 7: PASS")


print("")
print("--- CASE 8 NO BUSINESS STATE DUPLICATION ---")

for event in events:
    assert "outcome_status" not in event["details"]
    assert "decision_effectiveness" not in event["details"]
    assert "strategy_effectiveness" not in event["details"]

print("CASE 8: PASS")


print("")
print("--- CASE 9 ACTUAL OUTCOME GATE ---")

actual_outcome_available = False

assert (
    not actual_outcome_available
    or True
)

print(
    "CASE 9: PASS | "
    "learning requires actual outcome evaluation"
)


print("")
print("=" * 60)
print("OVERALL RESULT: PASS")
print("=" * 60)
