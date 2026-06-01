"""Fetch RU item/spell names; skip 404."""
import json
import urllib.request
from pathlib import Path

LOCALE = 7
OUT = Path(__file__).resolve().parents[2] / "data" / "wowhead" / "ru_names.json"

ENTRIES = [
    ("item", 251162),
    ("item", 249343),
    ("item", 246299),
    ("item", 246298),
    ("item", 246302),
    ("item", 246303),
    ("item", 246300),
    ("item", 246278),
    ("item", 246295),
    ("item", 246296),
    ("item", 193711),
    ("item", 193701),
    ("item", 151332),
    ("item", 249961),
    ("item", 249959),
    ("item", 249964),
    ("item", 249960),
    ("item", 249962),
    ("item", 243981),
    ("item", 243988),
    ("item", 240983),
    ("item", 240892),
    ("item", 223781),
    ("item", 243733),
    # druid tier pieces (Midnight S1)
    ("item", 249966),
    ("item", 249967),
    ("item", 249968),
    ("item", 249969),
    ("item", 249970),
    ("item", 249971),
    ("item", 249972),
    ("item", 249973),
    ("item", 249974),
    ("item", 249975),
    ("spell", 155835),
    ("spell", 155578),
    ("spell", 77761),
    ("spell", 203964),
    ("zone", 15808),
    ("item-set", 1980),
    ("item-set", 1985),
]


def fetch(kind: str, iid: int) -> str | None:
    url = f"https://nether.wowhead.com/tooltip/{kind}/{iid}?locale={LOCALE}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            data = json.loads(r.read().decode())
        return data.get("name")
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        raise


def main() -> None:
    out: dict = {}
    for kind, iid in ENTRIES:
        key = f"{kind}:{iid}"
        name = fetch(kind, iid)
        out[key] = name
        print(f"{key}: {name or '404'}")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
