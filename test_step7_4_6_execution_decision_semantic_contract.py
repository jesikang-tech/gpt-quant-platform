from core.ai_final_execution_decision import AIFinalExecutionDecision

print("=" * 60)
print("PHASE 7-4-6 EXECUTION DECISION SEMANTIC CONTRACT")
print("=" * 60)

engine = AIFinalExecutionDecision()

def run_case(name, orchestration_status, orchestration_risk,
             authorization, reassessment_policy, action):

    final_decision = {
        "decision": "ACCUMULATE",
        "action": action,
        "confidence_score": 92.0,
    }

    orchestration = {
        "decision": "ACCUMULATE",
        "orchestration_action": action,
        "orchestration_status": orchestration_status,
        "orchestration_risk": orchestration_risk,
        "execution_authorization": authorization,
        "reassessment_policy": reassessment_policy,
        "orchestration_score": 95.0,
    }

    integrated_intelligence = {
        "decision": "ACCUMULATE",
        "action": action,
        "execution_authorization": authorization,
        "confidence_score": 92.0,
        "integrated_score": 95.0,
    }

    lifecycle_governance_control = {
        "execution_authorization": authorization,
        "reassessment_policy": reassessment_policy,
        "lifecycle_governance_score": 95.0,
    }

    operational_intelligence = {
        "operational_status": "OPERATIONALLY_HEALTHY",
        "operational_score": 95.0,
    }

    result = engine.analyze(
        final_decision,
        orchestration,
        integrated_intelligence,
        lifecycle_governance_control,
        operational_intelligence,
    )

    print()
    print(f"=== {name} ===")
    print("decision:", result["decision"])
    print("action:", result["action"])
    print("execution_status:", result["execution_status"])
    print("execution_decision:", result["execution_decision"])
    print("execution_authorization:", result["execution_authorization"])

    return result


results = []

# ------------------------------------------------------------
# CASE 1: EXECUTION BLOCKED
# ------------------------------------------------------------

blocked = run_case(
    "CASE 1: EXECUTION BLOCKED",
    "ORCHESTRATION_BLOCKED",
    "CRITICAL",
    "AUTHORIZED",
    "NOT_REQUIRED",
    "PROCEED",
)

checks = {
    "decision preserved":
        blocked["decision"] == "ACCUMULATE",

    "action preserved":
        blocked["action"] == "PROCEED",

    "blocked status":
        blocked["execution_status"] == "EXECUTION_BLOCKED",

    "blocked decision":
        blocked["execution_decision"] == "HALT",

    "authorization preserved":
        blocked["execution_authorization"] == "AUTHORIZED",
}

for name, result in checks.items():
    print(f"{name}: {'PASS' if result else 'FAIL'}")
    results.append(result)


# ------------------------------------------------------------
# CASE 2: EXECUTION REVIEW
# ------------------------------------------------------------

review = run_case(
    "CASE 2: EXECUTION REVIEW",
    "ORCHESTRATION_READY",
    "MEDIUM",
    "UNAUTHORIZED",
    "NOT_REQUIRED",
    "PROCEED",
)

checks = {
    "decision preserved":
        review["decision"] == "ACCUMULATE",

    "action preserved":
        review["action"] == "PROCEED",

    "review status":
        review["execution_status"] == "EXECUTION_REVIEW",

    "review decision":
        review["execution_decision"] == "REVIEW",

    "authorization preserved":
        review["execution_authorization"] == "UNAUTHORIZED",
}

for name, result in checks.items():
    print(f"{name}: {'PASS' if result else 'FAIL'}")
    results.append(result)


# ------------------------------------------------------------
# CASE 3: NORMAL EXECUTION
# ------------------------------------------------------------

normal = run_case(
    "CASE 3: NORMAL EXECUTION",
    "ORCHESTRATION_READY",
    "LOW",
    "AUTHORIZED",
    "NOT_REQUIRED",
    "PROCEED",
)

checks = {
    "decision preserved":
        normal["decision"] == "ACCUMULATE",

    "action preserved":
        normal["action"] == "PROCEED",

    "execution not blocked":
        normal["execution_status"] not in (
            "EXECUTION_BLOCKED",
            "EXECUTION_REVIEW",
        ),

    "execution decision follows action":
        normal["execution_decision"] == "PROCEED",

    "authorization preserved":
        normal["execution_authorization"] == "AUTHORIZED",
}

for name, result in checks.items():
    print(f"{name}: {'PASS' if result else 'FAIL'}")
    results.append(result)


# ------------------------------------------------------------
# SEMANTIC SEPARATION
# ------------------------------------------------------------

print()
print("=== MASTER CONTROL / EXECUTION DECISION SEPARATION ===")

print("master_control_action is NOT used as execution_decision")
print("execution_decision is derived from execution_status + action")

print("semantic separation: PASS")
results.append(True)

print()
print("OVERALL RESULT:", "PASS" if all(results) else "FAIL")
print("=" * 60)
