"""Fetch RU names for Guardian Druid guide."""
import json
import urllib.request

LOCALE = 7

SPELLS = {
    5487: "Bear Form",
    6807: "Maul",
    400254: "Raze",
    441605: "Ravage",
    77758: "Thrash",
    33917: "Mangle",
    192081: "Ironfur",
    22812: "Barkskin",
    61336: "Survival Instincts",
    102558: "Incarnation Guardian of Ursoc",
    22842: "Frenzied Regeneration",
    106839: "Skull Bash",
    99: "Incapacitating Roar",
    102793: "Ursol's Vortex",
    132469: "Typhoon",
    2782: "Remove Corruption",
    319454: "Heart of the Wild",
    164812: "Moonfire",
    213771: "Swipe Bear",
    204066: "Lunar Beam",
    1252871: "Red Moon",
    383197: "Bristling Fur",
    80313: "Pulverize",
    391888: "Fluid Form",
    433850: "Wild Guardian apex",
    391347: "Druid of the Claw",
    424113: "Elune's Chosen",
    319454: "HotW",
    48438: "Regrowth",
    20484: "Rebirth",
    77764: "Stampeding Roar",
    1126: "Mark of the Wild",
    2908: "Soothe",
    339: "Entangling Roots",
    421432: "After the Wildfire",
}

ITEMS = {
    193701: "Algethar Puzzle Box",
    249961: "tier helm placeholder",
}

ZONES = [14032, 8910, 16573, 16395, 15808, 4813, 6988, 4131]


def fetch(kind: str, iid: int):
    url = f"https://nether.wowhead.com/tooltip/{kind}/{iid}?locale={LOCALE}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.loads(r.read().decode("utf-8")).get("name")


def main():
    out = {"spells": {}, "zones": {}}
    for sid, en in SPELLS.items():
        try:
            out["spells"][sid] = {"en": en, "ru": fetch("spell", sid)}
        except Exception as e:
            out["spells"][sid] = {"en": en, "ru": str(e)}
    for zid in ZONES:
        try:
            out["zones"][zid] = fetch("zone", zid)
        except Exception as e:
            out["zones"][zid] = str(e)
    with open("guardian_ru_names.json", "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    for sid, v in out["spells"].items():
        print(f"{sid}: {v['ru']} ({v['en']})")


if __name__ == "__main__":
    main()
