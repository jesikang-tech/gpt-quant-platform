from pathlib import Path

print("===== PHASE 7-4-18 DISCOVERY 1 =====")
print("===== ADAPTIVE STRATEGY DOWNSTREAM CONSUMER DISCOVERY =====")
print()

print("===== BASELINE =====")
import subprocess

for cmd in [
    ["git", "rev-parse", "HEAD"],
    ["git", "rev-parse", "origin/main"],
]:
    print(subprocess.check_output(cmd, text=True).strip())

print()
print("===== ADAPTIVE STRATEGY CALL SITES =====")

root = Path(".")
targets = [
    root / "core",
    root / "api_server.py",
]

patterns = [
    "AIDecisionAdaptiveStrategy",
    "adaptive_strategy",
    "adaptive_action",
    "outcome_learning_signal",
    "adaptive_learning_required",
]

for target in targets:
    if target.is_file():
        files = [target]
    elif target.exists():
        files = list(target.rglob("*.py"))
    else:
        continue

    for path in files:
        try:
            text = path.read_text(encoding="utf-8")
        except Exception:
            continue

        for i, line in enumerate(text.splitlines(), 1):
            if any(pattern in line for pattern in patterns):
                print(f"{path}:{i}: {line.strip()}")

print()
print("===== PHASE 7-4-18 DISCOVERY 1 COMPLETE =====")
