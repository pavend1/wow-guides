import json
import urllib.request
from pathlib import Path

LOCALE = 7
OUT = Path(__file__).resolve().parents[2] / "data" / "wowhead" / "batch_ru.json"


def f(kind, iid):
    url = f"https://nether.wowhead.com/tooltip/{kind}/{iid}?locale={LOCALE}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.loads(r.read().decode()).get("name", "?")


ids = {
    "zones": [4131, 16395, 16573, 15808, 14032, 4813, 8910, 6988],
    "spells": [
        155835, 213771, 203964, 77761, 155578, 102693, 441678, 422118,
        393388, 393389, 53600, 375576,
    ],
    "items": [
        193701, 151332, 246278, 246295, 246296, 246297, 246298, 246299,
        246300, 246301, 246302, 246303, 246304, 193711, 249961, 249962,
        249963, 249964, 249965, 237567, 237568, 237569, 237570, 237571,
    ],
}
result = {}
for z in ids["zones"]:
    result[f"zone:{z}"] = f("zone", z)
for s in ids["spells"]:
    result[f"spell:{s}"] = f("spell", s)
for i in ids["items"]:
    result[f"item:{i}"] = f("item", i)
result["item-set:1980"] = f("item-set", 1980)

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
print("wrote", OUT)
