"""Fetch RU names from Wowhead tooltip API (locale=7 = ruRU)."""
from __future__ import annotations

import argparse
import json
import urllib.request
from pathlib import Path

LOCALE = 7
DATA_DIR = Path(__file__).resolve().parents[2] / "data" / "wowhead"


def fetch(kind: str, iid: int) -> str:
    url = f"https://nether.wowhead.com/tooltip/{kind}/{iid}?locale={LOCALE}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=20) as r:
        data = json.loads(r.read().decode("utf-8"))
    return data.get("name") or data.get("namePlain") or "?"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default=str(DATA_DIR / "batch.json"))
    parser.add_argument("keys", nargs="*", help="e.g. spell:53600 item:193701")
    args = parser.parse_args()

    if not args.keys:
        # default batch: load from registry
        registry = Path(__file__).with_name("registry.json")
        entries = json.loads(registry.read_text(encoding="utf-8"))
        keys = list(entries.keys())
    else:
        entries = {k: k for k in args.keys}

    results: dict = {}
    errors: list = []
    for key in keys:
        kind, iid = key.split(":")
        try:
            results[key] = {"en": entries.get(key, key), "ru": fetch(kind, int(iid))}
            print(f"{key}: {results[key]['ru']}")
        except Exception as e:
            errors.append({"key": key, "error": str(e)})
            print(f"ERR {key}: {e}")

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        json.dumps({"ok": results, "errors": errors}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
