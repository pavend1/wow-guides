# Guides HTML server (Wowhead tooltips). Used by IntelliJ / manual run.
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot\..

python scripts\serve_guides.py --build --open --port 8080
