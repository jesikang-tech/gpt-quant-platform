# PPM administrator credential store.
# PBKDF2-SHA256 hash only; no plaintext password persistence.

$ErrorActionPreference = "Stop"

function Get-PpmCredentialPath {
    Join-Path (Join-Path $env:LOCALAPPDATA "PortablePlatformManager") "admin-credential.xml"
}

function Get-PpmPasswordHash {
    param([string] $Password, [byte[]] $Salt)

    $kdf = New-Object System.Security.Cryptography.Rfc2898DeriveBytes(
        $Password,
        $Salt,
        210000,
        [System.Security.Cryptography.HashAlgorithmName]::SHA256
    )

    try {
        [Convert]::ToBase64String($kdf.GetBytes(32))
    }
    finally {
        $kdf.Dispose()
    }
}

function Test-PpmPassword {
    param([string] $Password, [string] $Stored)

    $parts = $Stored.Split(":")
    if ($parts.Count -ne 3 -or $parts[0] -cne "PBKDF2-SHA256") {
        return $false
    }

    try {
        $salt = [Convert]::FromBase64String($parts[1])
        $expected = [Convert]::FromBase64String($parts[2])
        if ($salt.Length -ne 16 -or $expected.Length -ne 32) {
            return $false
        }

        $actual = [Convert]::FromBase64String(
            (Get-PpmPasswordHash -Password $Password -Salt $salt)
        )

        $difference = 0
        for ($i = 0; $i -lt 32; $i++) {
            $difference = $difference -bor ($actual[$i] -bxor $expected[$i])
        }

        return ($difference -eq 0)
    }
    catch {
        return $false
    }
}

function Read-PpmAdminCredential {
    $path = Get-PpmCredentialPath
    if (-not (Test-Path -LiteralPath $path -PathType Leaf)) {
        return $null
    }

    $credential = Import-Clixml -LiteralPath $path
    if ($credential -isnot [System.Management.Automation.PSCredential]) {
        throw "INVALID_PPM_CREDENTIAL"
    }

    return $credential
}

function Save-PpmAdminCredential {
    param([string] $Password)

    $salt = New-Object byte[] 16
    $rng = [System.Security.Cryptography.RandomNumberGenerator]::Create()

    try {
        $rng.GetBytes($salt)
    }
    finally {
        $rng.Dispose()
    }

    $record = "PBKDF2-SHA256:{0}:{1}" -f (
        [Convert]::ToBase64String($salt)
    ), (Get-PpmPasswordHash -Password $Password -Salt $salt)

    $secureRecord = ConvertTo-SecureString $record -AsPlainText -Force
    $credential = New-Object System.Management.Automation.PSCredential(
        "PPM-Administrator",
        $secureRecord
    )

    $path = Get-PpmCredentialPath
    $folder = Split-Path -Parent $path

    if (-not (Test-Path -LiteralPath $folder)) {
        New-Item -ItemType Directory -Path $folder -Force | Out-Null
    }

    $temporary = Join-Path $folder ([System.IO.Path]::GetRandomFileName())

    try {
        $credential | Export-Clixml -LiteralPath $temporary

        if (Test-Path -LiteralPath $path -PathType Leaf) {
                        $backup = Join-Path $folder ([System.IO.Path]::GetRandomFileName())
            try {
                [System.IO.File]::Replace($temporary, $path, $backup)
            }
            finally {
                if (Test-Path -LiteralPath $backup) {
                    Remove-Item -LiteralPath $backup -Force
                }
            }
        }
        else {
            [System.IO.File]::Move($temporary, $path)
        }
    }
    finally {
        if (Test-Path -LiteralPath $temporary) {
            Remove-Item -LiteralPath $temporary -Force
        }
    }
}