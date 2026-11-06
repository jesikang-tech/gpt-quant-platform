# Portable Platform Manager
# Minimal Windows menu. Actions are disabled until implemented.

$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "================================"
Write-Host " Portable Platform Manager"
Write-Host "================================"
Write-Host "1. ZIP compress (AES-256)"
Write-Host "2. ZIP extract"
Write-Host "3. ZIP delete"
Write-Host "4. Change administrator password"
Write-Host "5. Verify encrypted ZIP integrity"
Write-Host "0. Exit"
Write-Host ""

$choice = Read-Host "Select"

switch ($choice) {
    "1" {
        Add-Type -AssemblyName System.Windows.Forms

        $sevenZip = "C:\Program Files\7-Zip\7zFM.exe"

        if (-not (Test-Path -LiteralPath $sevenZip -PathType Leaf)) {
            throw "SEVEN_ZIP_NOT_INSTALLED"
        }

        $source = Read-Host "Enter full backup folder path (blank to cancel)"

        if ([string]::IsNullOrWhiteSpace($source)) {
            Write-Host "BACKUP_CANCELLED"
            break
        }

        $source = [Environment]::ExpandEnvironmentVariables($source.Trim().Trim('"'))

        if (-not [System.IO.Path]::IsPathRooted($source)) {
            throw "BACKUP_SOURCE_MUST_BE_ABSOLUTE"
        }

        if (-not (Test-Path -LiteralPath $source -PathType Container)) {
            throw "BACKUP_SOURCE_NOT_FOUND"
        }

        $source = (Resolve-Path -LiteralPath $source).ProviderPath

        Write-Host "BACKUP_SOURCE_SELECTED"
        Write-Host "In 7-Zip, select the required files or folder."
        Write-Host "Choose Add, ZIP format, AES-256 encryption, and enter a password."
        Write-Host "Verify the archive destination before confirming."
        Write-Host "No archive is created automatically by PPM."

        Start-Process -FilePath $sevenZip -ArgumentList "`"$source`""
    }
    "2" {
        Add-Type -AssemblyName System.Windows.Forms

        $sevenZip = "C:\Program Files\7-Zip\7z.exe"

        if (-not (Test-Path -LiteralPath $sevenZip -PathType Leaf)) {
            throw "SEVEN_ZIP_NOT_INSTALLED"
        }

        $dialog = New-Object System.Windows.Forms.OpenFileDialog
        $dialog.Title = "Select encrypted ZIP to restore"
        $dialog.Filter = "ZIP archives (*.zip)|*.zip"
        $dialog.CheckFileExists = $true
        $dialog.Multiselect = $false

        if ($dialog.ShowDialog() -ne [System.Windows.Forms.DialogResult]::OK) {
            Write-Host "RESTORE_CANCELLED"
            break
        }

        $archive = $dialog.FileName

        if ([System.IO.Path]::GetExtension($archive) -ine ".zip") {
            throw "ONLY_ZIP_RESTORE_ALLOWED"
        }

        $metadata = @(& $sevenZip l -slt -- $archive)

        if ($LASTEXITCODE -ne 0) {
            throw "ZIP_METADATA_READ_FAILED"
        }

        $separator = [Array]::FindIndex(
            $metadata,
            [Predicate[string]] {
                param($line)
                $line -match '^-{5,}$'
            }
        )

        if ($separator -lt 0) {
            throw "ZIP_ENTRY_SEPARATOR_MISSING"
        }

        $entries = @()
        $current = @{}

        foreach ($line in $metadata[($separator + 1)..($metadata.Count - 1)]) {
            if ([string]::IsNullOrWhiteSpace($line)) {
                if ($current.Count -gt 0) {
                    $entries += $current
                }
                $current = @{}
                continue
            }

            if ($line -match '^([^=]+?) = (.*)$') {
                $current[$matches[1].Trim()] = $matches[2]
            }
            else {
                throw "UNRECOGNIZED_ZIP_ENTRY_METADATA"
            }
        }

        if ($current.Count -gt 0) {
            $entries += $current
        }

        if ($entries.Count -eq 0) {
            throw "ZIP_HAS_NO_VERIFIABLE_ENTRIES"
        }

        foreach ($entry in $entries) {
            if (-not $entry.ContainsKey("Path")) {
                throw "ZIP_ENTRY_PATH_MISSING"
            }

            $entryPath = [string]$entry["Path"]
            $normalized = $entryPath.Replace("/", "\")

            if (
                [string]::IsNullOrWhiteSpace($entryPath) -or
                $normalized.StartsWith("\") -or
                $normalized -match '^[A-Za-z]:' -or
                $normalized -match '(^|\\)\.\.(\\|$)' -or
                $normalized.Contains(":")
            ) {
                throw "UNSAFE_ZIP_ENTRY_PATH"
            }

            if (-not $entry.ContainsKey("Attributes")) {
                throw "UNSAFE_ZIP_ENTRY_ATTRIBUTES"
            }

            $attributes = [string]$entry["Attributes"]

            if (
                $attributes -notmatch '^[A-Za-z.]+$' -or
                $attributes -match '[Ll]' -or
                $attributes -match '[^ADRHS.]'
            ) {
                throw "UNSAFE_ZIP_ENTRY_ATTRIBUTES"
            }
        }
        Write-Host "ZIP_ENTRY_GUARD: PASS"
        $restoreRoot = Join-Path $env:TEMP "PPM-Safe-Restore"

        if (-not (Test-Path -LiteralPath $restoreRoot)) {
            New-Item -ItemType Directory -Path $restoreRoot -ErrorAction Stop |
                Out-Null
        }

        $restoreName = "restore-" + [guid]::NewGuid().ToString("N")
        $destination = Join-Path $restoreRoot $restoreName

        if (Test-Path -LiteralPath $destination) {
            throw "RESTORE_DESTINATION_ALREADY_EXISTS"
        }

        New-Item -ItemType Directory -Path $destination -ErrorAction Stop |
            Out-Null

        Write-Host "RESTORE_DESTINATION: $destination"
        Write-Host "OVERWRITE_MODE: SKIP_EXISTING"
        Write-Host "Enter archive password only when prompted by 7-Zip."

        & $sevenZip x $archive "-o$destination" -aos

        if ($LASTEXITCODE -ne 0) {
            Write-Host "RESTORE_FAILED_OR_CANCELLED"
            break
        }

        Write-Host "RESTORE_COMMAND_COMPLETED"
        Write-Host "Verify restored files before using them."
    }
    "3" {
        Add-Type -AssemblyName System.Windows.Forms
        Add-Type -AssemblyName Microsoft.VisualBasic

        $dialog = New-Object System.Windows.Forms.OpenFileDialog
        $dialog.Title = "Select ZIP archive to delete"
        $dialog.Filter = "ZIP archives (*.zip)|*.zip"
        $dialog.Multiselect = $false
        $dialog.CheckFileExists = $true

        if ($dialog.ShowDialog() -eq [System.Windows.Forms.DialogResult]::OK) {
            $target = $dialog.FileName

            if ([System.IO.Path]::GetExtension($target) -ine ".zip") {
                throw "ONLY_ZIP_DELETION_ALLOWED"
            }

            $answer = [System.Windows.Forms.MessageBox]::Show(
                "Move this ZIP archive to Recycle Bin?`n`n$target",
                "Confirm ZIP deletion",
                [System.Windows.Forms.MessageBoxButtons]::YesNo,
                [System.Windows.Forms.MessageBoxIcon]::Warning
            )

            if ($answer -eq [System.Windows.Forms.DialogResult]::Yes) {
                [Microsoft.VisualBasic.FileIO.FileSystem]::DeleteFile(
                    $target,
                    [Microsoft.VisualBasic.FileIO.UIOption]::OnlyErrorDialogs,
                    [Microsoft.VisualBasic.FileIO.RecycleOption]::SendToRecycleBin
                )
                Write-Host "ZIP_MOVED_TO_RECYCLE_BIN"
            }
            else {
                Write-Host "ZIP_DELETE_CANCELLED"
            }
        }
        else {
            Write-Host "ZIP_DELETE_CANCELLED"
        }
    }
    "4" {
        . (Join-Path $PSScriptRoot "portable-platform-manager-credential.ps1")

        $existing = Read-PpmAdminCredential

        if ($null -ne $existing) {
            $oldSecure = Read-Host "Current administrator password" -AsSecureString
            $oldText = [System.Net.NetworkCredential]::new("", $oldSecure).Password
            $storedRecord = [System.Net.NetworkCredential]::new(
                "", $existing.Password
            ).Password

            if (-not (Test-PpmPassword -Password $oldText -Stored $storedRecord)) {
                Write-Host "ADMIN_PASSWORD_VERIFICATION_FAILED"
                break
            }
        }

        $newSecure = Read-Host "New administrator password" -AsSecureString
        $confirmSecure = Read-Host "Confirm new administrator password" -AsSecureString

        $newText = [System.Net.NetworkCredential]::new("", $newSecure).Password
        $confirmText = [System.Net.NetworkCredential]::new("", $confirmSecure).Password

        if ($newText.Length -lt 14 -or $newText.Length -gt 256 -or
            $newText -match '[\x00-\x1F\x7F]') {
            Write-Host "ADMIN_PASSWORD_FORMAT_INVALID"
            break
        }

        if ($newText -cne $confirmText) {
            Write-Host "ADMIN_PASSWORD_CONFIRMATION_FAILED"
            break
        }

        Save-PpmAdminCredential -Password $newText
        Write-Host "ADMIN_PASSWORD_UPDATED"
    }
    "5" {
        Add-Type -AssemblyName System.Windows.Forms

        $sevenZip = "C:\Program Files\7-Zip\7zFM.exe"

        if (-not (Test-Path -LiteralPath $sevenZip -PathType Leaf)) {
            throw "SEVEN_ZIP_NOT_INSTALLED"
        }

        $dialog = New-Object System.Windows.Forms.OpenFileDialog
        $dialog.Title = "Select encrypted ZIP to verify"
        $dialog.Filter = "ZIP archives (*.zip)|*.zip"
        $dialog.CheckFileExists = $true
        $dialog.Multiselect = $false

        if ($dialog.ShowDialog() -ne [System.Windows.Forms.DialogResult]::OK) {
            Write-Host "ZIP_VERIFICATION_CANCELLED"
            break
        }

        $archive = $dialog.FileName

        if ([System.IO.Path]::GetExtension($archive) -ine ".zip") {
            throw "ONLY_ZIP_VERIFICATION_ALLOWED"
        }

        Write-Host "Select Test in 7-Zip and enter the archive password."
        Write-Host "No files will be extracted by PPM."
        Write-Host "Verification result must be checked in the 7-Zip window."

        Start-Process -FilePath $sevenZip -ArgumentList "`"$archive`""
    }
    "0" { Write-Host "EXIT" }
    default { Write-Host "INVALID_SELECTION" }
}
