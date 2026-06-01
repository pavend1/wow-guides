import json, re
from pathlib import Path
data = json.loads(Path(r'e:/wow_guides/wcl_table_extract.json').read_text(encoding='utf-8'))
url = [k for k in data if 'damage-done' in k][0]
rows = data[url]['rows']
# Heuristic: WCL ability rows often [rank?, name, pct, amount, casts?, hits?, avg?, dps?]
interesting_keys = ['consume','reap','void','metamorph','devour','cull','eradicate','melee','auto','soul','hunger','vortex','immolation','chaos','blade','fel','sigil','eye','hunt','total']
ability_rows = []
for r in rows:
    name = r[0].lower() if r else ''
    line = ' '.join(r).lower()
    if any(k in line for k in interesting_keys):
        ability_rows.append(r)
# top by damage amount - find rows with pattern containing m at end in a cell
parsed = []
for r in rows:
    for i,c in enumerate(r):
        if re.match(r'^\d+\.\d+m$', c.replace(',','')):
            # name likely previous cells
            name = r[0] if r else ''
            pct = next((x for x in r if x.endswith('%')), '')
            parsed.append({'row': r, 'name_guess': name, 'amount': c, 'pct': pct})
            break
parsed.sort(key=lambda x: float(x['amount'].replace('m','')), reverse=True)
out = {
    'row_count': len(rows),
    'first_rows': rows[:15],
    'interesting_rows': ability_rows[:80],
    'top_damage_guess': parsed[:30],
}
Path(r'e:/wow_guides/wcl_parsed_summary.json').write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding='utf-8')
print('written', len(ability_rows), 'interesting', len(parsed), 'parsed')
