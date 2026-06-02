"""Fetch RU names for Unholy DK guide."""
from __future__ import annotations

import json
import time
import urllib.request
from pathlib import Path

LOCALE = 7
OUT = Path(__file__).resolve().parents[2] / "data" / "wowhead" / "unholy_dk_ru.json"

SPELLS = [
    77575, 85948, 47541, 55090, 43265, 42650, 63560, 343294, 152280, 207317,
    48707, 49576, 47528, 48792, 48265, 61999, 46585, 327574, 207167, 108194,
    45524, 212552, 1247378, 1242153, 1242173, 1242171, 1247621, 1247380,
    1247381, 1247382, 1247383, 1247384, 1247385, 1247386, 1247387, 1247388,
    1247389, 1247390, 1247391, 1247392, 1247393, 1247394, 1247395, 1247396,
    1247397, 1247398, 1247399, 1247400, 1247401, 1247402, 1247403, 1247404,
    1247405, 1247406, 1247407, 1247408, 1247409, 1247410, 1247411, 1247412,
    1247413, 1247414, 1247415, 1247416, 1247417, 1247418, 1247419, 1247420,
    1247421, 1247422, 1247423, 1247424, 1247425, 1247426, 1247427, 1247428,
    1247429, 1247430, 1247431, 1247432, 1247433, 1247434, 1247435, 1247436,
    1247437, 1247438, 1247439, 1247440, 1247441, 1247442, 1247443, 1247444,
    1247445, 1247446, 1247447, 1247448, 1247449, 1247450,
]

ITEMS = [
    250256, 250257, 250258, 250259, 250255,
    250010, 250011, 250012, 250013, 250014, 250015,
    250030, 250031, 250032, 250033, 250034, 250035, 250036, 250037, 250038,
    250039, 250040, 250041, 250042, 250043, 250044,
]


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
            name = fetch("spell", sid)
            if name and "?" not in name:
                out["spells"][str(sid)] = name
                print("spell", sid, name)
        except Exception as e:
            print("spell", sid, "ERR", e)
        time.sleep(0.04)

    for iid in ITEMS:
        try:
            name = fetch("item", iid)
            if name and "?" not in name:
                out["items"][str(iid)] = name
                print("item", iid, name)
        except Exception as e:
            print("item", iid, "ERR", e)
        time.sleep(0.04)

    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print("Wrote", OUT)


if __name__ == "__main__":
    main()
