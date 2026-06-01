import re, json
from pathlib import Path
html = Path(r'e:/wow_guides/wcl_full_page.html').read_text(encoding='utf-8', errors='replace')
abilities = re.findall(r'setAbilityFilter\((-?\d+).*?>([^<]+)</a>', html)
# dedupe by id
seen=set(); out=[]
for aid,name in abilities:
    if aid not in seen:
        seen.add(aid); out.append({'id': aid, 'name': name})
# filter devourer relevant
keys=['consume','reap','void','meta','devour','cull','erad','soul','hunger','vortex','immolation','chaos','blade','fel','sigil','eye','hunt','melee','auto']
dev=[a for a in out if any(k in a['name'].lower() for k in keys)]
Path(r'e:/wow_guides/wcl_devourer_abilities.json').write_text(json.dumps({'all': len(out), 'devourer': dev}, ensure_ascii=False, indent=2), encoding='utf-8')
print('devourer', len(dev))
for a in dev[:40]:
    print(a['id'], a['name'])
