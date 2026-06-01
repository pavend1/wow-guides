param(
    [string]$ChannelUsername = ""
)

# Get TELEGRAM_CHAT_ID via Telegram Bot API
# Run: powershell -ExecutionPolicy Bypass -File .\scripts\get-telegram-chat-id.ps1
# Public channel: ... -ChannelUsername my_channel

$envPath = Join-Path (Split-Path $PSScriptRoot -Parent) ".env"
if (-not (Test-Path $envPath)) {
    Write-Host "ERROR: .env not found at $envPath" -ForegroundColor Red
    exit 1
}

$token = $null
Get-Content $envPath | ForEach-Object {
    if ($_ -match '^TELEGRAM_BOT_TOKEN=(.+)$') {
        $token = $matches[1].Trim()
    }
}

if (-not $token) {
    Write-Host "ERROR: TELEGRAM_BOT_TOKEN is empty in .env" -ForegroundColor Red
    exit 1
}

function Invoke-TgApi {
    param([string]$Method)
    $uri = "https://api.telegram.org/bot$token/$Method"
    return Invoke-RestMethod -Uri $uri -Method Get
}

if ($ChannelUsername) {
    $uname = $ChannelUsername.TrimStart('@')
    Write-Host "Looking up @$uname via getChat..." -ForegroundColor Cyan
    try {
        $chat = Invoke-TgApi -Method "getChat?chat_id=@$uname"
        if ($chat.ok) {
            Write-Host ""
            Write-Host "Copy into .env:" -ForegroundColor Green
            Write-Host "  TELEGRAM_CHAT_ID=$($chat.result.id)   [@$uname] $($chat.result.title)"
            Write-Host ""
        } else {
            Write-Host "getChat failed." -ForegroundColor Red
        }
    } catch {
        Write-Host "getChat error: $_" -ForegroundColor Red
    }
    exit 0
}

Write-Host ""
Write-Host "Step 0: clearing webhook (required for getUpdates)..." -ForegroundColor Cyan
try {
    $wh = Invoke-TgApi -Method "deleteWebhook"
    if ($wh.ok) {
        Write-Host "  Webhook cleared." -ForegroundColor DarkGray
    }
} catch {
    Write-Host "  Webhook step failed: $_" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Before Enter, do ONE of these:" -ForegroundColor Yellow
Write-Host "  A) Send /start to your bot in PRIVATE chat (easiest)"
Write-Host "  B) Post a NEW message IN THE CHANNEL (bot = channel admin)"
Write-Host "  C) Send a message in a GROUP where the bot is a member"
Write-Host ""
Write-Host "Note: chat under a channel post is a separate group, not the channel."
Write-Host "Press Enter after that..." -ForegroundColor Yellow
Read-Host | Out-Null

Write-Host ""
Write-Host "Fetching updates..." -ForegroundColor Cyan

try {
    $resp = Invoke-TgApi -Method "getUpdates?limit=100"
} catch {
    Write-Host "API error: $_" -ForegroundColor Red
    exit 1
}

if (-not $resp.ok) {
    Write-Host "Telegram API error." -ForegroundColor Red
    exit 1
}

$count = @($resp.result).Count
Write-Host "Updates received: $count" -ForegroundColor Cyan

if ($count -eq 0) {
    Write-Host ""
    Write-Host "Still empty. Try:" -ForegroundColor Red
    Write-Host "  1. Send /start to the bot in private chat"
    Write-Host "  2. Run this script again"
    Write-Host ""
    Write-Host "Public channel (@name):" -ForegroundColor Yellow
    Write-Host "  powershell -ExecutionPolicy Bypass -File .\scripts\get-telegram-chat-id.ps1 -ChannelUsername YOUR_CHANNEL"
    exit 1
}

$chats = @{}
$topics = @{}

foreach ($u in $resp.result) {
    foreach ($key in @('message', 'channel_post', 'edited_channel_post', 'my_chat_member', 'chat_member')) {
        $item = $u.$key
        if (-not $item) { continue }

        if ($item.chat) {
            $c = $item.chat
            $chats[$c.id] = @{
                Id    = $c.id
                Title = $c.title
                Type  = $c.type
                User  = $c.username
                From  = $key
            }
        }

        if ($item.message_thread_id) {
            $tid = $item.message_thread_id
            $cid = $item.chat.id
            $topics["$cid`:$tid"] = @{
                ChatId  = $cid
                TopicId = $tid
                Title   = $item.chat.title
            }
        }
    }
}

if ($chats.Count -eq 0) {
    $out = Join-Path $PSScriptRoot "last-updates.json"
    $resp | ConvertTo-Json -Depth 20 | Set-Content $out -Encoding UTF8
    Write-Host "No chat parsed. Saved raw JSON to $out" -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "Copy into .env:" -ForegroundColor Green
Write-Host ""

foreach ($c in ($chats.Values | Sort-Object { $_.Id })) {
    $name = if ($c.Title) { $c.Title } elseif ($c.User) { "@$($c.User)" } else { "?" }
    Write-Host "  TELEGRAM_CHAT_ID=$($c.Id)   [$($c.Type)] $name   (via $($c.From))"
}

if ($topics.Count -gt 0) {
    Write-Host ""
    Write-Host "Forum topics (optional):" -ForegroundColor Green
    foreach ($t in $topics.Values) {
        Write-Host "  TELEGRAM_TOPIC_ID=$($t.TopicId)   chat $($t.ChatId) $($t.Title)"
    }
}

Write-Host ""
