# Upload built HTML guides (site/) to SFTP server.
# Usage:
#   .\scripts\deploy_site_sftp.ps1
#   .\scripts\deploy_site_sftp.ps1 -RemotePath /var/www/guides
param(
    [string]$SftpHost = "138.124.0.103",
    [int]$Port = 2121,
    [string]$User = "siteagent",
    [string]$Key = "$env:USERPROFILE\.ssh\id_rsa",
    [string]$RemotePath = "/html"
)

$ErrorActionPreference = "Stop"
$Root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location $Root

Write-Host "Building site..."
python scripts/build_guide_site.py
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

$siteDir = Join-Path $Root "site"
$batch = Join-Path $env:TEMP "wow_guides_sftp_upload.txt"
$remote = if ($RemotePath -eq ".") { "" } else { $RemotePath.TrimEnd("/") + "/" }

$lines = @(
    "cd $RemotePath",
    "put `"$siteDir\.nojekyll`" ${remote}.nojekyll",
    "put `"$siteDir\guides.css`" ${remote}guides.css",
    "put `"$siteDir\tooltips-fallback.js`" ${remote}tooltips-fallback.js",
    "put `"$siteDir\index.html`" ${remote}index.html",
    "put `"$siteDir\prot-paladin-mplus-ru.html`" ${remote}prot-paladin-mplus-ru.html",
    "put `"$siteDir\guardian-druid-mplus-ru.html`" ${remote}guardian-druid-mplus-ru.html",
    "put `"$siteDir\brewmaster-monk-mplus-ru.html`" ${remote}brewmaster-monk-mplus-ru.html",
    "put `"$siteDir\shadow-priest-mplus-ru.html`" ${remote}shadow-priest-mplus-ru.html",
    "put `"$siteDir\unholy-dk-mplus-ru.html`" ${remote}unholy-dk-mplus-ru.html",
    "put `"$siteDir\subtlety-rogue-mplus-ru.html`" ${remote}subtlety-rogue-mplus-ru.html",
    "put `"$siteDir\demonology-warlock-mplus-ru.html`" ${remote}demonology-warlock-mplus-ru.html",
    "put `"$siteDir\devourer-dh-rotation-ru.html`" ${remote}devourer-dh-rotation-ru.html",
    "bye"
)
$lines | Set-Content -Encoding ascii $batch

Write-Host "Uploading to ${User}@${SftpHost}:${Port} ($RemotePath)..."
sftp -P $Port -i $Key -o IdentitiesOnly=yes -b $batch "${User}@${SftpHost}"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host "Done."
