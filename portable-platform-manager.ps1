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
Write-Host "0. Exit"
Write-Host ""

$choice = Read-Host "Select"

switch ($choice) {
    "1" {
        Write-Host "Select files or folders in 7-Zip File Manager."
        Write-Host "Choose Add, ZIP format, AES-256, and enter a password."
        Start-Process -FilePath "C:\Program Files\7-Zip\7zFM.exe"
    }
    "2" {
        Write-Host "Select the encrypted ZIP in 7-Zip File Manager."
        Write-Host "Choose Extract and enter its password."
        Start-Process -FilePath "C:\Program Files\7-Zip\7zFM.exe"
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
    "0" { Write-Host "EXIT" }
    default { Write-Host "INVALID_SELECTION" }
}
