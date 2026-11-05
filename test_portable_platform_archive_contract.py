"""Synthetic, offline tests for the declarative archive contract."""

from dataclasses import FrozenInstanceError

import pytest

from portable_platform_manager.archive_contract import (
    ArchiveContractDecision,
    assess_archive_contract,
)


@pytest.mark.parametrize(
    "archive_format,filename_encryption",
    [
        ("zip", False),
        ("7z", False),
        ("7z", True),
    ],
)
def test_accepted_declarations(archive_format, filename_encryption):
    result = assess_archive_contract(
        archive_format,
        filename_encryption=filename_encryption,
    )
    assert result == ArchiveContractDecision(
        True,
        "DECLARATION_ONLY",
        archive_format,
        filename_encryption,
    )


@pytest.mark.parametrize(
    "archive_format",
    ["tar", "rar", "ZIP", "", None, 7, True, [], {}],
)
def test_unsupported_formats_fail_closed(archive_format):
    result = assess_archive_contract(archive_format)
    assert not result.accepted
    assert result.reason == "UNSUPPORTED_ARCHIVE_FORMAT"


@pytest.mark.parametrize(
    "encryption",
    ["ZIPCRYPTO", "AES128", "AES192", "aes256", "", None, 256, True],
)
def test_weak_or_invalid_encryption_rejected(encryption):
    result = assess_archive_contract("zip", encryption=encryption)
    assert not result.accepted
    assert result.reason == "ENCRYPTION_NOT_ACCEPTED"


@pytest.mark.parametrize(
    "filename_encryption",
    [True, 1, "true", None, [], {}],
)
def test_zip_filename_encryption_rejected(filename_encryption):
    result = assess_archive_contract(
        "zip",
        filename_encryption=filename_encryption,
    )
    assert not result.accepted
    assert result.reason in {
        "INVALID_FILENAME_ENCRYPTION",
        "ZIP_FILENAME_ENCRYPTION_UNSUPPORTED",
    }


@pytest.mark.parametrize(
    "password_delivery",
    [
        "COMMAND_LINE",
        "ENVIRONMENT_VARIABLE",
        "CONFIG_FILE",
        "INLINE_PASSWORD",
        "",
        None,
        True,
        [],
        {},
    ],
)
def test_unsafe_password_delivery_rejected(password_delivery):
    result = assess_archive_contract(
        "7z",
        password_delivery=password_delivery,
    )
    assert not result.accepted
    assert result.reason == "UNSAFE_PASSWORD_DELIVERY"


@pytest.mark.parametrize(
    "execution_requested",
    [True, 1, "true", None, [], {}],
)
def test_execution_not_authorized(execution_requested):
    result = assess_archive_contract(
        "7z",
        execution_requested=execution_requested,
    )
    assert not result.accepted
    assert result.reason in {
        "INVALID_EXECUTION_REQUEST",
        "EXECUTION_NOT_AUTHORIZED",
    }


def test_decision_is_immutable():
    result = assess_archive_contract("zip")
    with pytest.raises(FrozenInstanceError):
        result.accepted = False


def test_default_never_authorizes_execution():
    for archive_format in ("zip", "7z"):
        result = assess_archive_contract(archive_format)
        assert result.accepted
        assert result.reason == "DECLARATION_ONLY"
        assert result.archive_format == archive_format
