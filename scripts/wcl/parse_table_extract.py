import json, re
from pathlib import Path
data = json.loads(Path(r'e:/wow_guides/wcl_table_extract.json').read_text(encoding='utf-8'))
url = [k for k in data if 'damage-done' in k][0]
rows = data[url]['rows']
print('total rows', len(rows))
# find header-like row
for i,r in enumerate(rows[:30]):
    print(i, r)
# ability rows: look for rows with ability names and numbers
abilities = []
for r in rows:
    joined = ' | '.join(r)
    if any(x in joined for x in ['Consume','Reap','Void','Metamorphosis','Devour','Cull','Eradicate','Melee','Auto Attack','Soul']):
        abilities.append(r)
print('ability rows', len(abilities))
for r in abilities[:40]:
    print(r)
# top damage: rows with % and m/k amounts
candidates = []
for r in rows:
    if len(r) >= 3 and any('%' in c for c in r) and any(re.search(r'[km]$', c, re.I) or re.match(r'^\d+\.\d+m$', c) for c in r):
        candidates.append(r)
print('candidates', len(candidates))
for r in candidates[:25]:
    print(r)
Path(r'e:/wow_guides/wcl_player_ability_rows.json').write_text(json.dumps(candidates, ensure_ascii=False, indent=2), encoding='utf-8')
