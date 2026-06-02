"""Fetch RU names for Subtlety Rogue guide."""
import json
import urllib.request
from pathlib import Path

LOCALE = 7
SPELLS = [
    53, 1766, 1856, 1966, 31224, 408, 2094, 1833, 5938, 114018, 36554,
    185313, 121471, 185438, 196819, 197835, 280719, 319175, 441776,
    385627, 328530, 57934, 1784, 2823, 381664, 381623, 207777, 381621,
    185311, 212283, 137619, 2094, 5277, 1966, 31224, 185311,
]
ITEMS = [
    250256, 250257, 246297, 246298,  # heart of wind, etc from other guides
]

def fetch(key: str, entry_id: int) -> str:
    kind, iid = key.split(":")
    url = f"https://nether.wowhead.com/tooltip/{kind}/{iid}?data={kind}&locale={LOCALE}"
    req = urllib.request.Request(url, headers={"User-Agent": "wow_guides"})
    data = json.loads(urllib.request.urlopen(req, timeout=15).read())
    return data.get("name", "?")

out = {"spells": {}, "items": {}}
for sid in SPELLS:
    try:
        out["spells"][str(sid)] = fetch(f"spell:{sid}", sid)
    except Exception as e:
        out["spells"][str(sid)] = f"ERR:{e}"

for iid in ITEMS:
    try:
        out["items"][str(iid)] = fetch(f"item:{iid}", iid)
    except Exception as e:
        out["items"][str(iid)] = f"ERR:{e}"

path = Path(__file__).resolve().parents[2] / "data" / "wowhead" / "subtlety_ru.json"
path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Wrote {path}")
