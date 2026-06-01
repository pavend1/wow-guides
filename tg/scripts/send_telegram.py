#!/usr/bin/env python3
"""Send a message to Telegram channel/group via Bot API or MTProto proxy."""
from __future__ import annotations

import asyncio
import sys

import requests

from telegram_env import get_api_credentials, load_env, parse_mtproxy, parse_socks5, require


def send_via_bot_api(token: str, chat_id: str, text: str, socks5: str | None) -> dict:
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    proxies = {"http": socks5, "https": socks5} if socks5 else None
    resp = requests.post(
        url,
        data={"chat_id": chat_id, "text": text},
        proxies=proxies,
        timeout=45,
    )
    resp.raise_for_status()
    return resp.json()


async def send_via_mtproxy(
    token: str,
    chat_id: str,
    text: str,
    api_id: int,
    api_hash: str,
    host: str,
    port: int,
    secret: str,
) -> None:
    from telethon import TelegramClient
    from telethon.network import (
        ConnectionTcpMTProxyIntermediate,
        ConnectionTcpMTProxyRandomizedIntermediate,
    )

    # ee... = TLS/fake domain -> randomized; dd... = classic intermediate
    if secret.lower().startswith("ee"):
        connection = ConnectionTcpMTProxyRandomizedIntermediate
    else:
        connection = ConnectionTcpMTProxyIntermediate

    client = TelegramClient(
        "wow_guides_bot_session",
        api_id,
        api_hash,
        connection=connection,
        proxy=(host, port, secret),
        device_model="Desktop",
        system_version="Windows 10",
        app_version="4.0.0",
    )
    async with client:
        await client.start(bot_token=token)
        entity = int(chat_id)
        msg = await client.send_message(entity, text)
        print(f"OK: message sent via MTProto (id {msg.id})")


def main() -> None:
    env = load_env()
    token = require(env, "TELEGRAM_BOT_TOKEN")
    chat_id = require(env, "TELEGRAM_CHAT_ID")
    text = " ".join(sys.argv[1:]).strip() or (
        "Test from wow_guides.\n\nBot + MTProto proxy: connection OK.\n"
        "Next: WoW guides will be posted here."
    )

    proxy_mode = env.get("TELEGRAM_PROXY_MODE", "").strip().lower()
    mtproxy = parse_mtproxy(env)
    socks5 = parse_socks5(env)

    if proxy_mode == "mtproto" or (mtproxy and proxy_mode != "socks5"):
        if not mtproxy:
            raise SystemExit("TELEGRAM_PROXY_MODE=mtproto but MTPROXY_* / MTPROXY_LINK not set in .env")
        api_id, api_hash, api_src = get_api_credentials(env)
        host, port, secret = mtproxy
        print(f"Sending via MTProto proxy {host}:{port} (API: {api_src}) ...")
        asyncio.run(
            send_via_mtproxy(token, chat_id, text, api_id, api_hash, host, port, secret)
        )
        return

    print("Sending via Bot API (HTTPS)" + (" + SOCKS5" if socks5 else "") + " ...")
    data = send_via_bot_api(token, chat_id, text, socks5)
    if not data.get("ok"):
        raise SystemExit(f"Telegram error: {data}")
    print(f"OK: message sent (id {data['result']['message_id']})")


if __name__ == "__main__":
    main()
