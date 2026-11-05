"""Isolated backup staging for synthetic or independently approved files.

Never authorizes operating-platform backup or archive execution.
The caller must provide a trusted, private, empty destination.
"""

from __future__ import annotations

import sys

import hashlib
import os
import stat
from dataclasses import dataclass
from pathlib import Path

from .backup_file_inspector import inspect_backup_file


def _open_windows_source_read_only(path: Path):
    """Open a Windows source using a non-following Win32 file handle.

    This helper is not yet authorized for operating-platform backup.
    """
    import ctypes
    import msvcrt
    from ctypes import wintypes

    GENERIC_READ = 0x80000000
    FILE_SHARE_READ = 0x00000001
    OPEN_EXISTING = 3
    FILE_FLAG_OPEN_REPARSE_POINT = 0x00200000
    FILE_ATTRIBUTE_REPARSE_POINT = 0x00000400
    FILE_ATTRIBUTE_DIRECTORY = 0x00000010

    class BY_HANDLE_FILE_INFORMATION(ctypes.Structure):
        _fields_ = [
            ("dwFileAttributes", wintypes.DWORD),
            ("ftCreationTime", wintypes.FILETIME),
            ("ftLastAccessTime", wintypes.FILETIME),
            ("ftLastWriteTime", wintypes.FILETIME),
            ("dwVolumeSerialNumber", wintypes.DWORD),
            ("nFileSizeHigh", wintypes.DWORD),
            ("nFileSizeLow", wintypes.DWORD),
            ("nNumberOfLinks", wintypes.DWORD),
            ("nFileIndexHigh", wintypes.DWORD),
            ("nFileIndexLow", wintypes.DWORD),
        ]

    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)

    create_file = kernel32.CreateFileW
    create_file.argtypes = [
        wintypes.LPCWSTR,
        wintypes.DWORD,
        wintypes.DWORD,
        ctypes.c_void_p,
        wintypes.DWORD,
        wintypes.DWORD,
        wintypes.HANDLE,
    ]
    create_file.restype = wintypes.HANDLE

    get_info = kernel32.GetFileInformationByHandle
    get_info.argtypes = [
        wintypes.HANDLE,
        ctypes.POINTER(BY_HANDLE_FILE_INFORMATION),
    ]
    get_info.restype = wintypes.BOOL

    close_handle = kernel32.CloseHandle
    close_handle.argtypes = [wintypes.HANDLE]
    close_handle.restype = wintypes.BOOL

    handle = create_file(
        str(path),
        GENERIC_READ,
        FILE_SHARE_READ,
        None,
        OPEN_EXISTING,
        FILE_FLAG_OPEN_REPARSE_POINT,
        None,
    )

    invalid_handle = ctypes.c_void_p(-1).value

    if handle in (None, 0, invalid_handle):
        raise OSError("WINDOWS_SOURCE_OPEN_FAILED")

    try:
        info = BY_HANDLE_FILE_INFORMATION()

        if not get_info(handle, ctypes.byref(info)):
            raise OSError("WINDOWS_SOURCE_HANDLE_INFO_FAILED")

        if info.dwFileAttributes & FILE_ATTRIBUTE_REPARSE_POINT:
            raise ValueError("WINDOWS_SOURCE_REPARSE_POINT_DENIED")

        if info.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY:
            raise ValueError("WINDOWS_SOURCE_DIRECTORY_DENIED")

        descriptor = msvcrt.open_osfhandle(
            handle,
            os.O_RDONLY | os.O_BINARY,
        )
        handle = None

        return os.fdopen(descriptor, "rb")

    finally:
        if handle is not None:
            close_handle(handle)

@dataclass(frozen=True)
class StagedBackupFile:
    relative_path: str
    sha256: str
    size: int


def stage_backup_file(
    source_root: Path,
    relative_path: str,
    staging_root: Path,
) -> StagedBackupFile:
    """Copy one inspected file to a separate staging tree.

    This function does not establish source-content safety or
    resistance to concurrent filesystem modifications.
    """

    if sys.platform == "win32":
        raise ValueError("WINDOWS_SAFE_SOURCE_READER_PENDING_VERIFICATION")

    inspection = inspect_backup_file(source_root, relative_path)

    if not inspection.accepted or inspection.relative_path is None:
        raise ValueError("BACKUP_FILE_INSPECTION_DENIED")

    if not isinstance(staging_root, Path) or not staging_root.is_absolute():
        raise ValueError("INVALID_STAGING_ROOT")

    source_root = Path(source_root)
    relative = inspection.relative_path

    source = source_root.joinpath(*relative.split("/"))
    destination = staging_root.joinpath(*relative.split("/"))

    if source_root == staging_root:
        raise ValueError("STAGING_ROOT_EQUALS_SOURCE")

    if os.path.commonpath(
        (str(source_root), str(staging_root))
    ) == str(source_root):
        raise ValueError("STAGING_INSIDE_SOURCE_DENIED")

    staging_stat = os.lstat(staging_root)

    if not stat.S_ISDIR(staging_stat.st_mode):
        raise ValueError("STAGING_ROOT_NOT_DIRECTORY")

    if stat.S_ISLNK(staging_stat.st_mode):
        raise ValueError("STAGING_ROOT_IS_LINK")

    if getattr(staging_stat, "st_file_attributes", 0) & 0x400:
        raise ValueError("STAGING_ROOT_REPARSE_POINT")

    if any(staging_root.iterdir()):
        raise ValueError("STAGING_ROOT_NOT_EMPTY")

    if len(relative.split("/")) != 1:
        raise ValueError("NESTED_STAGING_REQUIRES_SAFE_DIRECTORY_CREATION")

    if destination.exists() or destination.is_symlink():
        raise ValueError("STAGING_DESTINATION_ALREADY_EXISTS")

    digest = hashlib.sha256()
    size = 0

    destination_created = False

    try:
        before_stat = os.lstat(source)

        if not stat.S_ISREG(before_stat.st_mode):
            raise ValueError("SOURCE_CHANGED_BEFORE_OPEN")

        if getattr(before_stat, "st_file_attributes", 0) & 0x400:
            raise ValueError("SOURCE_REPARSE_POINT_DENIED")

        flags = os.O_RDONLY | getattr(os, "O_BINARY", 0)
        flags |= getattr(os, "O_NOFOLLOW", 0)

        if os.name == "nt":
            reader_context = _open_windows_source_read_only(source)
        else:
            descriptor = os.open(source, flags)
            reader_context = os.fdopen(descriptor, "rb")

        with reader_context as reader:
            opened_stat = os.fstat(reader.fileno())

            if not stat.S_ISREG(opened_stat.st_mode):
                raise ValueError("OPENED_SOURCE_NOT_REGULAR_FILE")

            if (
                opened_stat.st_dev != before_stat.st_dev
                or opened_stat.st_ino != before_stat.st_ino
                or opened_stat.st_size != before_stat.st_size
                or opened_stat.st_mtime_ns != before_stat.st_mtime_ns
            ):
                raise ValueError("SOURCE_CHANGED_DURING_OPEN")

            with destination.open("xb") as writer:
                destination_created = True

                while True:
                    block = reader.read(1024 * 1024)

                    if not block:
                        break

                    writer.write(block)
                    digest.update(block)
                    size += len(block)

        after_stat = os.lstat(source)

        if (
            after_stat.st_dev != before_stat.st_dev
            or after_stat.st_ino != before_stat.st_ino
            or after_stat.st_size != before_stat.st_size
            or after_stat.st_mtime_ns != before_stat.st_mtime_ns
        ):
            raise ValueError("SOURCE_CHANGED_DURING_COPY")

        destination_stat = os.lstat(destination)

        if not stat.S_ISREG(destination_stat.st_mode):
            raise ValueError("STAGING_OUTPUT_NOT_REGULAR_FILE")

        if destination_stat.st_size != size:
            raise ValueError("STAGING_OUTPUT_SIZE_MISMATCH")

        verification_digest = hashlib.sha256()

        with destination.open("rb") as verifier:
            while True:
                verification_block = verifier.read(1024 * 1024)

                if not verification_block:
                    break

                verification_digest.update(verification_block)

        if verification_digest.hexdigest() != digest.hexdigest():
            raise ValueError("STAGING_OUTPUT_HASH_MISMATCH")

    except BaseException:
        if destination_created:
            try:
                destination.unlink()
            except OSError:
                pass
        raise

    return StagedBackupFile(
        relative_path=relative,
        sha256=digest.hexdigest(),
        size=size,
    )