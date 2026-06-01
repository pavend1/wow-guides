"""Load .env from project root (no external deps)."""
from __future__ import annotations

import os
from pathlib import Path
from urllib.parse import parse_qs, urlparse


def load_env() -> dict[str, str]:
    env_path = Path(__file__).resolve().parent.parent / ".env"
    values: dict[str, str] = {}
    if not env_path.exists():
        return values
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, val = line.partition("=")
        values[key.strip()] = val.strip()
    return values


def parse_mtproxy(values: dict[str, str]) -> tuple[str, int, str] | None:
    link = values.get("MTPROXY_LINK", "").strip()
    if link:
        if link.startswith(("tg://", "https://t.me/proxy", "http://t.me/proxy")):
            q = parse_qs(urlparse(link).query)
            host = q.get("server", [""])[0]
            port = int(q.get("port", ["443"])[0])
            secret = q.get("secret", [""])[0]
            if host and secret:
                return host, port, secret
        if link.count(":") >= 2 and not link.startswith("http"):
            host, port, secret = link.split(":", 2)
            return host, int(port), secret

    host = values.get("MTPROXY_HOST", "").strip()
    port = values.get("MTPROXY_PORT", "").strip()
    secret = values.get("MTPROXY_SECRET", "").strip()
    if host and port and secret:
        return host, int(port), secret
    return None


def parse_socks5(values: dict[str, str]) -> str | None:
    url = values.get("SOCKS5_PROXY", "").strip()
    if url:
        return url if "://" in url else f"socks5://{url}"
    host = values.get("SOCKS5_HOST", "").strip()
    port = values.get("SOCKS5_PORT", "").strip()
    if host and port:
        user = values.get("SOCKS5_USER", "").strip()
        pwd = values.get("SOCKS5_PASS", "").strip()
        if user and pwd:
            return f"socks5://{user}:{pwd}@{host}:{port}"
        return f"socks5://{host}:{port}"
    return None


def get_api_credentials(values: dict[str, str]) -> tuple[int, str, str]:
    """Return (api_id, api_hash, source_label)."""
    api_id = values.get("TELEGRAM_API_ID", "").strip()
    api_hash = values.get("TELEGRAM_API_HASH", "").strip()
    if api_id and api_hash:
        return int(api_id), api_hash, "my.telegram.org"

    use_desktop = values.get("TELEGRAM_USE_DESKTOP_API", "").strip().lower() in (
        "1",
        "true",
        "yes",
    )
    if use_desktop:
        # Public Telegram Desktop pair (official client). For bots only.
        # Prefer your own keys from https://my.telegram.org when registration works.
        return 2040, "b18441a1ff607e10a989891a5462e627", "Telegram Desktop (fallback)"

    raise SystemExit(
        "Missing TELEGRAM_API_ID / TELEGRAM_API_HASH in .env\n"
        "Either register at https://my.telegram.org/apps\n"
        "or set TELEGRAM_USE_DESKTOP_API=1 (see scripts/TELEGRAM-API-HELP.md)"
    )


def require(values: dict[str, str], key: str) -> str:
    val = values.get(key, "").strip()
    if not val:
        raise SystemExit(f"Missing {key} in .env")
    return val
