import re, json
from pathlib import Path
text = Path(r'e:/wow_guides/wcl_full_page.txt').read_text(encoding='utf-8')
# After player table, look for ability names with damage - search multiline windows
abilities = ['Consume','Reap','Void Ray','Void Metamorphosis','Devour','Cull','Eradicate','Melee','Soul','Hunger','Vortex']
found = {}
for ab in abilities:
    idx = text.find(ab)
    if idx >= 0:
        found[ab] = text[max(0,idx-120):idx+180]
# parse all lines that look like ability table rows: start with optional rank then name
rows=[]
lines=text.splitlines()
for i,l in enumerate(lines):
    s=l.strip()
    if s in abilities or s.startswith('Eradicate') or s.startswith('Void Ray'):
        ctx=lines[i:i+5]
        rows.append(ctx)
Path(r'e:/wow_guides/wcl_full_ability_context.json').write_text(json.dumps({'rows': rows, 'found_snips': found}, ensure_ascii=False, indent=2), encoding='utf-8')
print('rows', len(rows))
