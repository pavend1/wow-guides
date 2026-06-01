"""Fetch RU names for Shadow Priest guide."""
from __future__ import annotations

import json
import time
import urllib.request
from pathlib import Path

LOCALE = 7
OUT = Path(__file__).resolve().parents[2] / "data" / "wowhead" / "shadow_priest_ru.json"

SPELLS = [
    589, 34914, 8092, 15407, 32379, 10060, 15487, 47585, 586, 120644, 263165,
    194249, 232698, 21562, 8122, 108968, 391403, 73510, 450983, 450984, 450985,
    440725, 440726, 447444, 447445, 122121, 205385, 341374, 200174, 34433,
    451235, 451236, 428933, 428934, 373212, 373213,
]

ITEMS = [
    250256, 193701, 151332,  # trinkets from other guides - find SP trinkets
    246565, 246566, 246567, 246568, 246569, 246570,  # tier guess
    250010, 250011, 250012, 250013, 250014, 250015,
]

TIER_RANGE = list(range(250030, 250045))


def fetch(kind: str, iid: int) -> str | None:
    url = f"https://nether.wowhead.com/tooltip/{kind}/{iid}?locale={LOCALE}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=20) as r:
        data = json.loads(r.read().decode())
    return data.get("name") or data.get("namePlain")


def main() -> None:
    out: dict = {"spells": {}, "items": {}}
    for sid in SPELLS:
        try:
            out["spells"][str(sid)] = fetch("spell", sid)
            print("spell", sid, out["spells"][str(sid)])
        except Exception as e:
            print("spell", sid, "ERR", e)
        time.sleep(0.04)

    for iid in ITEMS + TIER_RANGE:
        try:
            name = fetch("item", iid)
            if name and "?" not in name:
                out["items"][str(iid)] = name
                if "клятв" in name.lower() or "слеп" in name.lower() or "жрец" in name.lower() or "tier" in name.lower():
                    print("item", iid, name)
        except Exception:
            pass
        time.sleep(0.04)

    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print("Wrote", OUT)


if __name__ == "__main__":
    main()
