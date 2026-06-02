import json, urllib.request
for sid in range(1242140, 1242220):
    try:
        url = f"https://nether.wowhead.com/tooltip/spell/{sid}?locale=7"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read().decode())
        name = data.get("name") or data.get("namePlain")
        if name and "?" not in name:
            print(sid, name)
    except Exception:
        pass
