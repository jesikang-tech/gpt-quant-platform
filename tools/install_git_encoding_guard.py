from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
HOOK = PROJECT_ROOT / ".git" / "hooks" / "pre-commit"

HOOK_CONTENT = """#!/bin/sh

echo "===== GPT QUANT PLATFORM PRE-COMMIT ENCODING GUARD ====="

if [ ! -f "tools/check_text_encoding.py" ]; then
    echo "ENCODING_GUARD_ERROR: tools/check_text_encoding.py not found"
    exit 1
fi

if command -v python >/dev/null 2>&1; then
    python tools/check_text_encoding.py
    STATUS=$?
else
    echo "ENCODING_GUARD_ERROR: python command not found"
    exit 1
fi

if [ $STATUS -ne 0 ]; then
    echo ""
    echo "COMMIT_BLOCKED: encoding guard failed."
    exit $STATUS
fi

echo ""
echo "ENCODING_GUARD_PASS: commit allowed."
exit 0
"""

if not (PROJECT_ROOT / ".git").is_dir():
    raise RuntimeError("GIT_DIRECTORY_NOT_FOUND")

HOOK.parent.mkdir(parents=True, exist_ok=True)

if HOOK.exists():
    existing = HOOK.read_text(encoding="utf-8")
    if existing != HOOK_CONTENT:
        backup = HOOK.with_name("pre-commit.before-encoding-guard")
        backup.write_text(existing, encoding="utf-8")
        print(f"Existing hook backed up: {backup}")

HOOK.write_text(HOOK_CONTENT, encoding="utf-8", newline="\n")

print("STEP 21 COMPLETE")
print(f"Guard installer: {Path(__file__).resolve()}")
print(f"Git hook       : {HOOK}")
print("Encoding       : UTF-8 without BOM")
print("Commit blocking: ENABLED")
