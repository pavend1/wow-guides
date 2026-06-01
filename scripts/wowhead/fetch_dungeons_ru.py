"""Fetch RU dungeon names from Wowhead tooltip API."""
import json
import urllib.request

LOCALE = 7
# zone IDs from Wowhead / WCL (Algeth'ar = 2526 per WCL)
ZONE_IDS = [
    2526, 2527, 2528, 2529, 2530,
    8910,  # Seat of the Triumvirate (wowhead search)
    1279, 952, 959,
]

def fetch_zone(zid: int) -> str | None:
    url = f"https://nether.wowhead.com/tooltip/zone/{zid}?locale={LOCALE}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            data = json.loads(r.read().decode("utf-8"))
        return data.get("name")
    except Exception as e:
        return f"ERR: {e}"

def main():
    out = {}
    for zid in ZONE_IDS:
        out[zid] = fetch_zone(zid)
    with open("dungeon_zones_ru.json", "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    for zid, name in out.items():
        print(f"{zid}: {name}")

if __name__ == "__main__":
    main()
