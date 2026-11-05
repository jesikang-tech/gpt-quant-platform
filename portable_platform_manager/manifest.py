"""Platform-independent portable deployment manifest validation."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import PurePosixPath
import re
from typing import Mapping


_PLATFORM_ID = re.compile(r"[a-z][a-z0-9_-]{2,63}\Z")
_VERSION = re.compile(r"[0-9]+\.[0-9]+\.[0-9]+\Z")

_REQUIRED_FIELDS = frozenset(
    {
        "platform_id",
        "platform_version",
        "package_format_version",
        "supported_operating_systems",
        "runtime_requirements",
        "install_directory_policy",
        "data_directory_policy",
        "log_directory_policy",
        "permitted_entrypoints",
        "execution_authority_policy",
        "backup_policy",
        "uninstall_policy",
    }
)


@dataclass(frozen=True)
class PlatformManifest:
    platform_id: str
    platform_version: str
    package_format_version: int
    permitted_entrypoints: tuple[str, ...]


_WINDOWS_RESERVED_NAMES = frozenset(
    {"CON", "PRN", "AUX", "NUL"}
    | {f"COM{i}" for i in range(1, 10)}
    | {f"LPT{i}" for i in range(1, 10)}
    | {"CONIN$", "CONOUT$"}
)

_WINDOWS_FORBIDDEN_CHARS = frozenset('<>:"|?*')


def _safe_relative_path(value: object) -> str:
    """Reject unsafe Windows archive and entrypoint paths."""

    if not isinstance(value, str) or not value:
        raise ValueError("invalid relative path")

    if "\\" in value or "\x00" in value:
        raise ValueError("unsafe relative path")

    path = PurePosixPath(value)

    if path.is_absolute():
        raise ValueError("absolute paths are denied")

    components = value.split("/")

    for component in components:
        if not component or component in (".", ".."):
            raise ValueError("unsafe path component")

        if component.endswith((".", " ")):
            raise ValueError("ambiguous Windows path")

        if any(char in _WINDOWS_FORBIDDEN_CHARS for char in component):
            raise ValueError("forbidden Windows path character")

        if any(ord(char) < 32 or ord(char) == 127 for char in component):
            raise ValueError("control characters are denied")

        base_name = component.split(".", 1)[0].upper()

        if base_name in _WINDOWS_RESERVED_NAMES:
            raise ValueError("reserved Windows device name")

    return value

def validate_manifest(data: Mapping[str, object]) -> PlatformManifest:
    """Validate a declarative manifest without filesystem access."""

    if not isinstance(data, dict):
        raise ValueError("manifest must be a dictionary")

    if set(data) != _REQUIRED_FIELDS:
        raise ValueError("manifest fields are missing or unknown")

    platform_id = data["platform_id"]
    version = data["platform_version"]
    format_version = data["package_format_version"]

    if not isinstance(platform_id, str) or not _PLATFORM_ID.fullmatch(
        platform_id
    ):
        raise ValueError("invalid platform id")

    if not isinstance(version, str) or not _VERSION.fullmatch(version):
        raise ValueError("invalid platform version")

    if type(format_version) is not int or format_version != 1:
        raise ValueError("unsupported package format")

    systems = data["supported_operating_systems"]

    if systems != ["windows"]:
        raise ValueError("unsupported operating system policy")

    requirements = data["runtime_requirements"]

    if not isinstance(requirements, dict) or requirements:
        raise ValueError("runtime requirements are not yet supported")

    for field in (
        "install_directory_policy",
        "data_directory_policy",
        "log_directory_policy",
        "execution_authority_policy",
        "backup_policy",
        "uninstall_policy",
    ):
        if data[field] != "DENIED":
            raise ValueError(f"unsupported policy: {field}")

    entrypoints = data["permitted_entrypoints"]

    if not isinstance(entrypoints, list):
        raise ValueError("entrypoints must be a list")

    if len(entrypoints) > 32:
        raise ValueError("too many entrypoints")

    paths = tuple(_safe_relative_path(item) for item in entrypoints)

    if len({path.casefold() for path in paths}) != len(paths):
        raise ValueError("duplicate entrypoints")

    return PlatformManifest(
        platform_id=platform_id,
        platform_version=version,
        package_format_version=format_version,
        permitted_entrypoints=paths,
    )
