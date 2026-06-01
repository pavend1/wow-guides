$envPath = Join-Path (Split-Path $PSScriptRoot -Parent) ".env"
$token = $null
$chatId = $null
Get-Content $envPath | ForEach-Object {
    if ($_ -match '^TELEGRAM_BOT_TOKEN=(.+)$') { $token = $matches[1].Trim() }
    if ($_ -match '^TELEGRAM_CHAT_ID=(.+)$') { $chatId = $matches[1].Trim() }
}

if (-not $token -or -not $chatId) {
    Write-Host "ERROR: TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID missing in .env" -ForegroundColor Red
    exit 1
}

$text = if ($args.Count -gt 0) { $args -join ' ' } else {
    @"
Test from wow_guides bot.

Channel connection works.
Next: WoW Devourer DH guides can be posted here.
"@.Trim()
}

$body = @{
    chat_id = $chatId
    text    = $text
    parse_mode = "HTML"
}

try {
    $resp = Invoke-RestMethod -Uri "https://api.telegram.org/bot$token/sendMessage" -Method Post -Body $body
    if ($resp.ok) {
        Write-Host "OK: message sent (id $($resp.result.message_id))" -ForegroundColor Green
    } else {
        Write-Host "FAILED: $($resp | ConvertTo-Json -Compress)" -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Host "ERROR: $_" -ForegroundColor Red
    if ($_.ErrorDetails.Message) { Write-Host $_.ErrorDetails.Message -ForegroundColor Red }
    exit 1
}
