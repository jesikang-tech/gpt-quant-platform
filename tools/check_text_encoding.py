from __future__ import annotations

from pathlib import Path
import subprocess
import sys


PROJECT_ROOT = Path(__file__).resolve().parent.parent

TEXT_EXTENSIONS = {
    ".py",
    ".js",
    ".css",
    ".html",
    ".json",
    ".md",
    ".txt",
    ".ps1",
}

EXCLUDED_DIRECTORIES = {
    ".git",
    ".venv",
    "__pycache__",
    ".pytest_cache",
    "build",
    "dist",
    "logs",
}


def should_check(path: Path) -> bool:
    if not path.is_file():
        return False

    if any(part in EXCLUDED_DIRECTORIES for part in path.parts):
        return False

    return path.suffix.lower() in TEXT_EXTENSIONS


def has_bom(data: bytes) -> bool:
    return data.startswith(b"\xef\xbb\xbf")


def validate_utf8(path: Path, data: bytes) -> list[str]:
    errors: list[str] = []

    if b"\x00" in data:
        errors.append("NUL byte detected")

    try:
        data.decode("utf-8")
    except UnicodeDecodeError as exc:
        errors.append(f"invalid UTF-8: {exc}")

    return errors


def get_head_bytes(relative_path: str) -> bytes | None:
    result = subprocess.run(
        ["git", "show", f"HEAD:{relative_path}"],
        cwd=PROJECT_ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        check=False,
    )

    if result.returncode != 0:
        return None

    return result.stdout


def get_tracked_files() -> set[str]:
    result = subprocess.run(
        [
            "git",
            "ls-files",
            "--",
            "*.py",
            "*.js",
            "*.css",
            "*.html",
            "*.json",
            "*.md",
            "*.txt",
            "*.ps1",
        ],
        cwd=PROJECT_ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True,
        encoding="utf-8",
        check=True,
    )

    return {
        line.strip()
        for line in result.stdout.splitlines()
        if line.strip()
    }


def main() -> int:
    failures: list[tuple[str, list[str]]] = []
    checked = 0
    legacy_bom = 0
    new_files = 0

    tracked_files = get_tracked_files()

    for path in PROJECT_ROOT.rglob("*"):
        if not should_check(path):
            continue

        relative = path.relative_to(PROJECT_ROOT).as_posix()
        data = path.read_bytes()

        checked += 1

        errors = validate_utf8(path, data)

        if relative in tracked_files:
            head_data = get_head_bytes(relative)

            if head_data is not None:
                head_has_bom = has_bom(head_data)
                work_has_bom = has_bom(data)

                if head_has_bom:
                    legacy_bom += 1

                # Existing BOM policy is preserved.
                # A new BOM introduced into a previously BOM-free
                # tracked file is considered an encoding regression.
                if not head_has_bom and work_has_bom:
                    errors.append("new UTF-8 BOM introduced relative to HEAD")

        else:
            new_files += 1

            # New text files must use UTF-8 without BOM.
            if has_bom(data):
                errors.append("new text file contains UTF-8 BOM")

        if errors:
            failures.append((relative, errors))

    print("===== GPT QUANT PLATFORM TEXT ENCODING CHECK =====")
    print(f"Project root       : {PROJECT_ROOT}")
    print(f"Files checked      : {checked}")
    print(f"Tracked text files : {len(tracked_files)}")
    print(f"Legacy BOM files   : {legacy_bom}")
    print(f"New text files     : {new_files}")

    if failures:
        print()
        print("ENCODING_CHECK_FAILED")

        for relative, errors in failures:
            print(f"\n{relative}")
            for error in errors:
                print(f"  - {error}")

        print()
        return 1

    print()
    print("ENCODING_CHECK_OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
