$envPath = Join-Path (Split-Path $PSScriptRoot -Parent) ".env"
$token = $null
Get-Content $envPath | ForEach-Object {
    if ($_ -match '^TELEGRAM_BOT_TOKEN=(.+)$') { $token = $matches[1].Trim() }
}
if (-not $token) { Write-Host "no token"; exit 1 }

Invoke-RestMethod "https://api.telegram.org/bot$token/deleteWebhook" | Out-Null
$resp = Invoke-RestMethod "https://api.telegram.org/bot$token/getUpdates?limit=20"
Write-Host "update count:" $resp.result.Count
foreach ($u in $resp.result) {
    if ($u.message) {
        Write-Host "private/group:" $u.message.chat.id $u.message.chat.type $u.message.chat.title
    }
    if ($u.channel_post) {
        Write-Host "channel:" $u.channel_post.chat.id $u.channel_post.chat.title
    }
    if ($u.my_chat_member) {
        Write-Host "member event:" $u.my_chat_member.chat.id $u.my_chat_member.chat.type $u.my_chat_member.chat.title
    }
}
