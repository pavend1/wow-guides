import json, urllib.request
out = {}
for sid in list(range(1242140, 1242220)) + list(range(1247300, 1247450)) + [458128, 390279, 390280, 390281, 390282, 390283, 390284, 390285, 390286, 390287, 390288, 390289, 390290, 458129, 458130, 458131, 458132, 458133, 458134, 458135, 458136, 458137, 458138, 458139, 458140]:
    try:
        url = f"https://nether.wowhead.com/tooltip/spell/{sid}?locale=7"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read().decode())
        name = data.get("name") or data.get("namePlain")
        if name and any(x in name.lower() for x in ["клад", "гнил", "сгнив", "коса", "запрет", "некрот", "нагно", "эпид", "болезн", "вспыш", "жнец", "войско", "темн"]):
            out[str(sid)] = name
    except Exception:
        pass
open(r"e:\wow_guides\data\wowhead\unholy_spells_filtered.json", "w", encoding="utf-8").write(json.dumps(out, ensure_ascii=False, indent=2))
print(json.dumps(out, ensure_ascii=False, indent=2))
