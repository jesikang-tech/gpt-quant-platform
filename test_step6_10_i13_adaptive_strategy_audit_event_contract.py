ALLOWED_EVENT_TYPES = {
    "ADAPTIVE_STRATEGY_GENERATED",
}


def build_adaptive_strategy_audit_event(
    strategy,
    action,
    outcome_learning_signal,
    outcome_learning_signal_strength,
    adaptive_learning_required,
    outcome_history_id,
    event_time,
):
    assert strategy is not None
    assert action is not None
    assert outcome_history_id is not None
    assert event_time is not None

    return {
        "event_type": "ADAPTIVE_STRATEGY_GENERATED",
        "event_time": event_time,
        "source": "adaptive_strategy",
        "status": "GENERATED",
        "outcome_history_id": outcome_history_id,
        "correlation_key": (
            f"outcome:{outcome_history_id}"
        ),
        "details": {
            "strategy": strategy,
            "action": action,
            "outcome_learning_signal":
                outcome_learning_signal,
            "outcome_learning_signal_strength":
                outcome_learning_signal_strength,
            "adaptive_learning_required":
                bool(adaptive_learning_required),
        },
    }


print("=" * 60)
print(
    "Step6-10-I-13 Adaptive Strategy Audit Event Contract"
)
print("=" * 60)


print("")
print("--- CASE 1 EVENT CONTRACT ---")

event = build_adaptive_strategy_audit_event(
    strategy="GROWTH",
    action="INCREASE_RISK",
    outcome_learning_signal="POSITIVE",
    outcome_learning_signal_strength=0.8,
    adaptive_learning_required=False,
    outcome_history_id=201,
    event_time="2026-08-30T15:00:00+09:00",
)

assert event["event_type"] == (
    "ADAPTIVE_STRATEGY_GENERATED"
)
assert event["source"] == "adaptive_strategy"
assert event["status"] == "GENERATED"

print("CASE 1: PASS")


print("")
print("--- CASE 2 OUTCOME CORRELATION ---")

assert event["outcome_history_id"] == 201
assert event["correlation_key"] == "outcome:201"

print(
    "CASE 2: PASS | "
    f"correlation={event['correlation_key']}"
)


print("")
print("--- CASE 3 LEARNING PAYLOAD ---")

assert event["details"]["strategy"] == "GROWTH"
assert event["details"]["action"] == "INCREASE_RISK"
assert event["details"]["outcome_learning_signal"] == "POSITIVE"
assert (
    event["details"]["outcome_learning_signal_strength"]
    == 0.8
)
assert (
    event["details"]["adaptive_learning_required"]
    is False
)

print("CASE 3: PASS")


print("")
print("--- CASE 4 NEGATIVE ADAPTIVE LEARNING ---")

negative_event = build_adaptive_strategy_audit_event(
    strategy="DEFENSIVE",
    action="REDUCE_RISK",
    outcome_learning_signal="NEGATIVE",
    outcome_learning_signal_strength=0.9,
    adaptive_learning_required=True,
    outcome_history_id=202,
    event_time="2026-08-30T15:01:00+09:00",
)

assert (
    negative_event["details"]["strategy"]
    == "DEFENSIVE"
)
assert (
    negative_event["details"]["action"]
    == "REDUCE_RISK"
)
assert (
    negative_event["details"]["outcome_learning_signal"]
    == "NEGATIVE"
)
assert (
    negative_event["details"]["adaptive_learning_required"]
    is True
)

print("CASE 4: PASS")


print("")
print("--- CASE 5 ACTUAL OUTCOME CORRELATION ---")

assert (
    negative_event["correlation_key"]
    == "outcome:202"
)
assert (
    negative_event["outcome_history_id"]
    == 202
)

print("CASE 5: PASS")


print("")
print("--- CASE 6 NO BUSINESS STATE DUPLICATION ---")

assert "outcome_status" not in event
assert "outcome_score" not in event
assert "learning_status" not in event

print("CASE 6: PASS")


print("")
print("--- CASE 7 EVENT TYPE CONTRACT ---")

assert ALLOWED_EVENT_TYPES == {
    "ADAPTIVE_STRATEGY_GENERATED"
}

print(
    "CASE 7: PASS | "
    f"event_type={event['event_type']}"
)


print("")
print("=" * 60)
print("OVERALL RESULT: PASS")
print("=" * 60)
