[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'

$python = Get-Command python -ErrorAction Stop

Write-Host 'Installing Graphify with optional Gemini support...'
& $python.Source -m pip install --upgrade 'graphifyy[gemini]'

Write-Host 'Installing Codex instructions and local Git hooks...'
& $python.Source -m graphify install --platform codex
& $python.Source -m graphify codex install
& $python.Source -m graphify hook install

if ([string]::IsNullOrWhiteSpace($env:GEMINI_API_KEY) -and [string]::IsNullOrWhiteSpace($env:GOOGLE_API_KEY)) {
    Write-Warning 'Gemini is not configured. Code graph updates still work; semantic document/image updates require GEMINI_API_KEY or GOOGLE_API_KEY.'
} else {
    Write-Host 'Gemini environment variable detected. Do not commit it to this repository.'
}

Write-Host 'Graphify bootstrap complete. Read docs/PROJECT_CONTEXT.md before working on architecture.'
