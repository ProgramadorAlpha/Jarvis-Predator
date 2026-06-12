$ErrorActionPreference = "Stop"

$projectDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$python = Join-Path $projectDir ".venv\Scripts\pythonw.exe"
$logDir = Join-Path $projectDir "logs"

if (-not (Test-Path $python)) {
    throw "Virtual environment not found. Run: py -3.12 -m venv .venv"
}

New-Item -ItemType Directory -Path $logDir -Force | Out-Null
$env:PYTHONUTF8 = "1"
$env:PYTHONUNBUFFERED = "1"

Start-Process `
    -FilePath $python `
    -ArgumentList "main.py" `
    -WorkingDirectory $projectDir `
    -RedirectStandardOutput (Join-Path $logDir "jarvis.log") `
    -RedirectStandardError (Join-Path $logDir "jarvis-error.log")
