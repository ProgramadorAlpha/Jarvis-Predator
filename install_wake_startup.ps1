$ErrorActionPreference = "Stop"

$projectDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$pythonw = Join-Path $projectDir ".venv\Scripts\pythonw.exe"
$listener = Join-Path $projectDir "wake_listener.py"
$startup = [Environment]::GetFolderPath("Startup")
$shortcutPath = Join-Path $startup "Jarvis Wake Listener.lnk"

if (-not (Test-Path $pythonw)) {
    throw "Virtual environment not found: $pythonw"
}

$shell = New-Object -ComObject WScript.Shell
$shortcut = $shell.CreateShortcut($shortcutPath)
$shortcut.TargetPath = $pythonw
$shortcut.Arguments = "`"$listener`""
$shortcut.WorkingDirectory = $projectDir
$shortcut.Description = "Local clap and wake phrase listener for JARVIS"
$shortcut.WindowStyle = 7
$shortcut.Save()

Write-Output "Installed: $shortcutPath"
