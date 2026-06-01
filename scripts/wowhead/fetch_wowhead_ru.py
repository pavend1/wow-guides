"""Fetch RU names from Wowhead tooltip API (locale=7 = ruRU)."""
import json
import urllib.request
from pathlib import Path

LOCALE = 7  # ruRU

ENTRIES = {
    # spells
    "spell:53600": "Shield of the Righteous",
    "spell:85673": "Word of Glory",
    "spell:26573": "Consecration",
    "spell:31935": "Avenger's Shield",
    "spell:31884": "Avenging Wrath",
    "spell:375576": "Divine Toll",
    "spell:427453": "Hammer of Light",
    "spell:204019": "Blessed Hammer",
    "spell:53595": "Hammer of the Righteous",
    "spell:24275": "Hammer of Wrath",
    "spell:275779": "Judgment",
    "spell:62124": "Hand of Reckoning",
    "spell:31850": "Ardent Defender",
    "spell:86659": "Guardian of Ancient Kings",
    "spell:642": "Divine Shield",
    "spell:633": "Lay on Hands",
    "spell:96231": "Rebuke",
    "spell:853": "Hammer of Justice",
    "spell:115750": "Blinding Light",
    "spell:213644": "Cleanse Toxins",
    "spell:1022": "Blessing of Protection",
    "spell:204018": "Blessing of Spellwarding",
    "spell:6940": "Blessing of Sacrifice",
    "spell:10326": "Turn Evil",
    "spell:391054": "Intercession",
    "spell:465": "Devotion Aura",
    "spell:432472": "Sacred Weapon",
    "spell:389539": "Sentinel",
    "spell:327193": "Shining Light proc",
    "spell:105805": "Vanguard",
    "spell:1044": "Blessing of Freedom",
    "spell:190784": "Divine Steed",
    "spell:28730": "Arcane Torrent",
    "spell:46968": "Final Stand",
    "spell:81256": "Consecrated Ground",
    # hero talents
    "spell:431377": "Templar",
    "spell:431414": "Lightsmith",
    # items - search by name on wowhead if needed
    "item:237568": "Luminant Verdict's Unwavering Gaze",
    "item:237570": "Luminant Verdict's Providence Watch",
    "item:237567": "Luminant Verdict's Divine Warplate",
    "item:237569": "Luminant Verdict's Greaves",
    "item:237571": "Luminant Verdict's Gauntlets",
    "item:246278": "Voidclaw Gauntlets",
    "item:246295": "Spellbane Cutlass",
    "item:246296": "Ward of the Spellbreaker",
    "item:246297": "Algeth'ar Puzzle Box",
    "item:246298": "Solarflare Prism",
    "item:246299": "Umbral Plume",
    "item:246300": "Loa Worshiper's Band",
    "item:246301": "Spellbreaker's Bracers",
    "item:246302": "Rotting Globule",
    "item:246303": "Heart of Wind",
    "item:246304": "Spellbreaker's Blade",
    "item:246305": "Spellbreaker's Rebuke",
    # enchants - item ids may vary, try search
    "item:240041": "Empowered Blessing of Speed",
    "item:240042": "Akil'zon's Swiftness",
    "item:240043": "Mark of the Worldsoul",
    "item:240044": "Blood Knight's Armor Kit",
    "item:240045": "Farstrider's Hunt",
    "item:240046": "Silvermoon's Tenacity ring",
    "item:240047": "Acuity of the Ren'dorei",
    "item:240048": "Thalassian Phoenix Oil",
    "item:240049": "Rite of Sanctification",
    "item:240050": "Indecipherable Eversong Diamond",
    "item:240051": "Flawless Masterful Peridot",
    "item:240052": "Stabilizing Gemstone Bandolier",
    "item:240053": "Flask of the Shattered Sun",
    "item:240054": "Light's Potential",
    "item:240055": "Silvermoon Health Potion",
    "item:240056": "Champion's Bento",
    "item:240057": "Void-Touched Augment Rune",
    "item:240058": "Radiant Jewelbinder",
}

def fetch(key):
    kind, iid = key.split(":")
    url = f"https://nether.wowhead.com/tooltip/{kind}/{iid}?locale={LOCALE}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=15) as r:
        data = json.loads(r.read().decode())
    name = data.get("name") or data.get("namePlain") or "?"
    return name

results = {}
errors = []
for key, en in ENTRIES.items():
    try:
        results[key] = {"en": en, "ru": fetch(key)}
        print(f"{key}: {results[key]['ru']}")
    except Exception as e:
        errors.append((key, en, str(e)))
        print(f"ERR {key} ({en}): {e}")

print("\n--- ERRORS ---")
for x in errors:
    print(x)

out = Path(__file__).resolve().parents[2] / "data" / "wowhead" / "wowhead_ru_names.json"
out.parent.mkdir(parents=True, exist_ok=True)
with open(out, "w", encoding="utf-8") as f:
    json.dump({"ok": results, "errors": errors}, f, ensure_ascii=False, indent=2)
