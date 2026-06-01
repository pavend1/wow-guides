"""Fetch RU names for Brewmaster Monk guide."""
import json
import urllib.request
from pathlib import Path

LOCALE = 7
OUT = Path(__file__).resolve().parents[2] / "data" / "wowhead" / "brewmaster_ru.json"

SPELLS = [
    121253,  # Keg Smash
    100784,  # Blackout Kick
    107428,  # Rising Sun Kick
    322507,  # Spinning Crane Kick (or breath?)
    325153,  # Exploding Keg
    132578,  # Invoke Niuzao
    115203,  # Fortifying Brew
    115399,  # Black Ox Brew
    119582,  # Purifying Brew
    322960,  # Celestial Brew
    387184,  # Weapons of Order
    116705,  # Spear Hand Strike
    115078,  # Paralysis
    101545,  # Flying Serpent Kick
    109132,  # Roll
    115176,  # Zen Meditation
    122278,  # Dampen Harm
    122783,  # Diffuse Magic
    116844,  # Ring of Peace
    115315,  # Summon Black Ox Statue
    116670,  # Vivify
    322101,  # Expel Harm
    325197,  # Dance of Chi-Ji?
    388686,  # Shado-Pan?
    443028,  # Flurry Strikes hero?
    443087,  # Master of Harmony?
    325216,  # Bonedust Brew
    1249625, # blackout combo?
    132120,  # Breath of Fire
    205523,  # Blackout Combo buff?
    393400,  # counterstrike
    387231,  # Press the Advantage
    388809,  # Aspect of Harmony
]

ITEMS = [
    193701, 250256, 249343, 260235, 252421, 252420, 249807, 151336, 251162,
    243981, 244002, 240983, 240892,
]

ZONES = [4131, 16395, 16573, 15808, 14032, 4813, 8910, 6988]

ITEM_SETS = [1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990]


def fetch(kind: str, iid: int) -> str | None:
    url = f"https://nether.wowhead.com/tooltip/{kind}/{iid}?locale={LOCALE}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return json.loads(r.read().decode()).get("name")
    except Exception:
        return None


def main() -> None:
    out: dict = {"spells": {}, "items": {}, "zones": {}, "item_sets": {}}
    for s in SPELLS:
        n = fetch("spell", s)
        if n:
            out["spells"][str(s)] = n
            print(f"spell {s}: {n}")
    for i in ITEMS:
        n = fetch("item", i)
        if n:
            out["items"][str(i)] = n
    for z in ZONES:
        n = fetch("zone", z)
        if n:
            out["zones"][str(z)] = n
    for sid in ITEM_SETS:
        n = fetch("item-set", sid)
        if n:
            out["item_sets"][str(sid)] = n
            print(f"set {sid}: {n}")
    # monk tier pieces scan
    for i in range(250030, 250050):
        n = fetch("item", i)
        if n and ("монах" in n.lower() or "шелк" in n.lower() or "цветоч" in n.lower() or "silk" in n.lower() or "bloom" in n.lower() or "шёлк" in n.lower()):
            out["items"][str(i)] = n
            print(f"item {i}: {n}")
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
