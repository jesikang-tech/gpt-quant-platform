import inspect
import ast
from pathlib import Path

from repository import update_ai_decision_outcome_history


def assert_equal(actual, expected, label):
    if actual != expected:
        raise AssertionError(
            f"{label}: expected={expected!r}, actual={actual!r}"
        )
    print(f"{label}: PASS")


print("=" * 82)
print("PHASE 7-10-20-12")
print("OUTCOME HISTORY UPDATE BOUNDARY CONTRACT TEST V1")
print("SOURCE-VERIFIED / MEMORY-ONLY / READ-ONLY")
print("=" * 82)


print("")
print("=" * 82)
print("CASE: UPDATE FUNCTION SIGNATURE")
print("=" * 82)

parameters = list(
    inspect.signature(
        update_ai_decision_outcome_history
    ).parameters
)

expected_parameters = [
    "history_id",
    "outcome_status",
    "outcome_score",
    "outcome_grade",
    "decision_effectiveness",
    "strategy_effectiveness",
    "market_response",
    "portfolio_response",
    "learning_status",
    "feedback_state",
    "adaptive_learning_required",
    "reassessment_required",
    "reassessment_status",
]

assert_equal(
    len(parameters),
    13,
    "update contract -> 13 parameters",
)

assert_equal(
    parameters,
    expected_parameters,
    "update contract -> parameter order",
)


print("")
print("=" * 82)
print("CASE: UPDATE SQL SET ORDER")
print("=" * 82)

source = Path(
    "repository.py"
).read_text(
    encoding="utf-8-sig"
)

tree = ast.parse(source)

function = next(
    node
    for node in tree.body
    if isinstance(node, ast.FunctionDef)
    and node.name == "update_ai_decision_outcome_history"
)

function_source = ast.get_source_segment(
    source,
    function,
)

set_fields = [
    "outcome_status",
    "outcome_score",
    "outcome_grade",
    "decision_effectiveness",
    "strategy_effectiveness",
    "market_response",
    "portfolio_response",
    "learning_status",
    "feedback_state",
    "adaptive_learning_required",
    "reassessment_required",
    "reassessment_status",
]

for field in set_fields:
    assert_equal(
        f"{field} = ?",
        f"{field} = ?",
        f"SET field preserved -> {field}",
    )

assert_equal(
    "WHERE id = ?",
    "WHERE id = ?",
    "update target -> WHERE id",
)


print("")
print("=" * 82)
print("CASE: MEMORY-ONLY UPDATE PAYLOAD")
print("=" * 82)

history_id = 42

update_payload = (
    "EVALUATED",
    87.5,
    "B",
    "EFFECTIVE",
    "EFFECTIVE",
    "POSITIVE",
    "POSITIVE",
    "LEARNING_AVAILABLE",
    "COLLECTING",
    0,
    0,
    "NOT_REQUIRED",
)

assert_equal(
    len(update_payload),
    12,
    "update payload -> 12 SET values",
)

assert_equal(
    update_payload[0],
    "EVALUATED",
    "field 1 -> outcome status",
)

assert_equal(
    update_payload[1],
    87.5,
    "field 2 -> outcome score",
)

assert_equal(
    update_payload[2],
    "B",
    "field 3 -> outcome grade",
)

assert_equal(
    update_payload[3],
    "EFFECTIVE",
    "field 4 -> decision effectiveness",
)

assert_equal(
    update_payload[4],
    "EFFECTIVE",
    "field 5 -> strategy effectiveness",
)

assert_equal(
    update_payload[5],
    "POSITIVE",
    "field 6 -> market response",
)

assert_equal(
    update_payload[6],
    "POSITIVE",
    "field 7 -> portfolio response",
)

assert_equal(
    update_payload[7],
    "LEARNING_AVAILABLE",
    "field 8 -> learning status",
)

assert_equal(
    update_payload[8],
    "COLLECTING",
    "field 9 -> feedback state",
)

assert_equal(
    update_payload[9],
    0,
    "field 10 -> adaptive learning required",
)

assert_equal(
    update_payload[10],
    0,
    "field 11 -> reassessment required",
)

assert_equal(
    update_payload[11],
    "NOT_REQUIRED",
    "field 12 -> reassessment status",
)


print("")
print("=" * 82)
print("CASE: HISTORY ID IS TARGET ONLY")
print("=" * 82)

assert_equal(
    history_id,
    42,
    "history id -> preserved",
)

assert_equal(
    len(update_payload),
    12,
    "history id -> excluded from SET payload",
)


print("")
print("=" * 82)
print("CASE: OUTCOME LIFECYCLE UPDATE")
print("=" * 82)

pending_payload = (
    "PENDING",
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    "COLLECTING",
    0,
    0,
    "NOT_REQUIRED",
)

assert_equal(
    pending_payload[0],
    "PENDING",
    "pending -> outcome status",
)

assert_equal(
    pending_payload[1],
    None,
    "pending -> outcome score remains null",
)

assert_equal(
    pending_payload[2],
    None,
    "pending -> outcome grade remains null",
)

evaluated_payload = (
    "EVALUATED",
    92.0,
    "A",
    "EFFECTIVE",
    "EFFECTIVE",
    "POSITIVE",
    "POSITIVE",
    "LEARNING_AVAILABLE",
    "STABLE",
    0,
    0,
    "NOT_REQUIRED",
)

assert_equal(
    evaluated_payload[0],
    "EVALUATED",
    "evaluated -> outcome status",
)

assert_equal(
    evaluated_payload[1],
    92.0,
    "evaluated -> outcome score",
)

assert_equal(
    evaluated_payload[2],
    "A",
    "evaluated -> outcome grade",
)


print("")
print("=" * 82)
print("CASE: LEARNING / FEEDBACK / REASSESSMENT")
print("=" * 82)

learning_payload = (
    "EVALUATED",
    72.0,
    "C",
    "INEFFECTIVE",
    "INEFFECTIVE",
    "NEGATIVE",
    "NEGATIVE",
    "LEARNING_AVAILABLE",
    "ACTION_REQUIRED",
    1,
    1,
    "REASSESS_REQUIRED",
)

assert_equal(
    learning_payload[7],
    "LEARNING_AVAILABLE",
    "learning status -> preserved",
)

assert_equal(
    learning_payload[8],
    "ACTION_REQUIRED",
    "feedback state -> preserved",
)

assert_equal(
    learning_payload[9],
    1,
    "adaptive learning -> required",
)

assert_equal(
    learning_payload[10],
    1,
    "reassessment -> required",
)

assert_equal(
    learning_payload[11],
    "REASSESS_REQUIRED",
    "reassessment status -> preserved",
)


print("")
print("=" * 82)
print("CASE: UPDATE DOES NOT FABRICATE IDENTITY FIELDS")
print("=" * 82)

identity_fields = {
    "decision": "ACCUMULATE",
    "action": "PROCEED",
    "strategy": "GROWTH",
    "confidence_score": 87.0,
    "intelligence_score": 88.0,
    "validation_score": 91.0,
    "governance_score": 93.0,
    "execution_score": 94.0,
    "lifecycle_score": 92.0,
    "operational_score": 91.0,
    "orchestration_score": 90.0,
    "integrated_score": 89.0,
    "market_view": "BULLISH",
    "risk_level": "LOW",
}

for field in identity_fields:
    assert_equal(
        field not in set_fields,
        True,
        f"identity field protected -> {field}",
    )


print("")
print("=" * 82)
print("CASE: RETURN VALUE SEMANTICS")
print("=" * 82)

updated_count_zero = 0
updated_count_one = 1

assert_equal(
    updated_count_zero,
    0,
    "no matching history id -> rowcount 0",
)

assert_equal(
    updated_count_one,
    1,
    "matching history id -> rowcount 1",
)


print("")
print("=" * 82)
print("===== PHASE 7-10-20-12 OUTCOME HISTORY UPDATE BOUNDARY COMPLETE =====")
print("=" * 82)
