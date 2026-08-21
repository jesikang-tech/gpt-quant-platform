from core.ai_decision_outcome_intelligence import AIDecisionOutcomeIntelligence

print("=" * 60)
print("PHASE 7-4-9 MASTER CONTROL STATUS OUTCOME CONTRACT")
print("=" * 60)

engine = AIDecisionOutcomeIntelligence()

base = {
    "decision": "ACCUMULATE",
    "action": "PROCEED",
    "execution_status": "EXECUTION_READY",
    "execution_authorization": "AUTHORIZED",
    "certification_status": "CERTIFIED",
    "feedback_status": "STABLE",
    "reassessment_required": False,
}

print()
print("=== CASE 1: MASTER READY ===")

ready_master_control = {
    "master_control_status": "MASTER_READY",
}

ready = engine.analyze(
    final_decision=base,
    final_execution_decision=base,
    final_decision_master_control=ready_master_control,
    final_decision_certification={
        "certification_status": "CERTIFIED",
    },
    final_decision_execution_feedback={
        "feedback_status": "STABLE",
    },
)

print("master_control_status:",
      ready.get("master_control_status"))
print("execution_status:",
      ready.get("execution_status"))
print("certification_status:",
      ready.get("certification_status"))
print("learning_status:",
      ready.get("learning_status"))
print("feedback_state:",
      ready.get("feedback_state"))

print()
print("=== CASE 2: MASTER BLOCKED ===")

blocked_master_control = {
    "master_control_status": "MASTER_BLOCKED",
}

blocked = engine.analyze(
    final_decision=base,
    final_execution_decision=base,
    final_decision_master_control=blocked_master_control,
    final_decision_certification={
        "certification_status": "CERTIFIED",
    },
    final_decision_execution_feedback={
        "feedback_status": "STABLE",
    },
)

print("master_control_status:",
      blocked.get("master_control_status"))
print("execution_status:",
      blocked.get("execution_status"))
print("certification_status:",
      blocked.get("certification_status"))
print("learning_status:",
      blocked.get("learning_status"))
print("feedback_state:",
      blocked.get("feedback_state"))

print()
print("=== SEMANTIC CHECK ===")

checks = {
    "ready status preserved":
        ready.get("master_control_status")
        == "MASTER_READY",

    "ready waits for outcome":
        ready.get("learning_status")
        == "WAITING_FOR_OUTCOME",

    "ready feedback collecting":
        ready.get("feedback_state")
        == "COLLECTING",

    "blocked status preserved":
        blocked.get("master_control_status")
        == "MASTER_BLOCKED",

    "blocked learning":
        blocked.get("learning_status")
        == "BLOCKED",

    "blocked feedback":
        blocked.get("feedback_state")
        == "BLOCKED",
}

all_pass = True

for name, result in checks.items():
    status = "PASS" if result else "FAIL"
    print(f"{name}: {status}")
    all_pass = all_pass and result

print()
print("OVERALL RESULT:", "PASS" if all_pass else "FAIL")
print("=" * 60)

if not all_pass:
    raise SystemExit(1)
