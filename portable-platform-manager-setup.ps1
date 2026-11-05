param(
    [Parameter(Mandatory)]
    [ValidateSet("Install", "Uninstall")]
    [string] $Action,

    [string] $TestInstallDirectory,
    [string] $TestShortcutPath,
    [switch] $ConfirmIsolatedTestRemoval
)

$ErrorActionPreference = "Stop"

$installDir = Join-Path $env:LOCALAPPDATA "Programs\PortablePlatformManager"
$shortcut = Join-Path ([Environment]::GetFolderPath("Desktop")) "Portable Platform Manager.lnk"

if ($TestInstallDirectory -or $TestShortcutPath) {
    if (-not $TestInstallDirectory -or -not $TestShortcutPath) {
        throw "BOTH_TEST_PATHS_REQUIRED"
    }

    $tempRoot = [System.IO.Path]::GetFullPath($env:TEMP)
    $installFull = [System.IO.Path]::GetFullPath($TestInstallDirectory)
    $shortcutFull = [System.IO.Path]::GetFullPath($TestShortcutPath)

    $prefix = $tempRoot.TrimEnd('\') + '\'

    if (-not $installFull.StartsWith(
        $prefix, [System.StringComparison]::OrdinalIgnoreCase
    ) -or -not $shortcutFull.StartsWith(
        $prefix, [System.StringComparison]::OrdinalIgnoreCase
    )) {
        throw "TEST_PATH_OUTSIDE_TEMP_DENIED"
    }

    $installDir = $installFull
    $shortcut = $shortcutFull
}
$files = @(
    "portable-platform-manager.ps1",
    "portable-platform-manager-credential.ps1"
)

if ($Action -eq "Install") {
    foreach ($name in $files) {
        if (-not (Test-Path -LiteralPath (Join-Path $PSScriptRoot $name) -PathType Leaf)) {
            throw "REQUIRED_PPM_FILE_MISSING: $name"
        }
    }

    New-Item -ItemType Directory -Path $installDir -Force | Out-Null

    foreach ($name in $files) {
        Copy-Item -LiteralPath (Join-Path $PSScriptRoot $name) `
            -Destination (Join-Path $installDir $name) -Force
    }

    $shell = New-Object -ComObject WScript.Shell
    $link = $shell.CreateShortcut($shortcut)
    $link.TargetPath = "powershell.exe"
    $link.Arguments = '-NoProfile -File "' +
        (Join-Path $installDir "portable-platform-manager.ps1") + '"'
    $link.WorkingDirectory = $installDir
    $link.Save()

    Write-Host "PPM_INSTALLED"
}
else {
    if ($ConfirmIsolatedTestRemoval) {
        if (-not $TestInstallDirectory -or -not $TestShortcutPath) {
            throw "ISOLATED_TEST_PATHS_REQUIRED"
        }
        $answer = "YES"
    }
    else {
        $answer = Read-Host "Remove PPM program files only? (YES to confirm)"
    }

    if ($answer -cne "YES") {
        Write-Host "PPM_UNINSTALL_CANCELLED"
        return
    }

    if (Test-Path -LiteralPath $shortcut) {
        Remove-Item -LiteralPath $shortcut -Force
    }

    foreach ($name in $files) {
        $path = Join-Path $installDir $name
        if (Test-Path -LiteralPath $path -PathType Leaf) {
            Remove-Item -LiteralPath $path -Force
        }
    }

    Write-Host "PPM_UNINSTALLED"
    Write-Host "ADMIN_CREDENTIALS_PRESERVED"
    Write-Host "PLATFORM_DATA_PRESERVED"
}