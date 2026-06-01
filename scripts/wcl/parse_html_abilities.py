import re, json
from pathlib import Path
html = Path(r'e:/wow_guides/wcl_player_damage_abilities.html').read_text(encoding='utf-8', errors='replace')
print('html len', len(html))
for term in ['Consume','Reap','Void Ray','Metamorphosis','Devour','Cull','Eradicate','461408','1226019']:
    print(term, html.count(term))
# find JSON arrays with ability names
patterns = [
    r'"ability"\s*:\s*\{[^}]*"name"\s*:\s*"([^"]+)"',
    r'"name"\s*:\s*"(Consume[^"]*)"',
    r'\\"name\\":\\"(Consume[^\\]*)\\"',
]
for p in patterns:
    m = re.findall(p, html)
    print('pat', p[:40], len(m))
    if m[:5]: print(' sample', m[:5])
# save all spell= ids
spells = set(re.findall(r'spell=(\d+)', html))
print('spell ids', len(spells), sorted(list(spells))[:20])
# search for source 3 specific data
idx = html.find('source=3')
print('source=3 count', html.count('source=3'))
# extract script with table data
for m in re.finditer(r'(\{"data":\{.*?"reportData".*?\})\s*,\s*"extensions"', html):
    print('found reportData chunk', len(m.group(1)))
    Path(r'e:/wow_guides/wcl_reportdata_snip.json').write_text(m.group(1)[:500000], encoding='utf-8')
    break
else:
    # try window.__APOLLO_STATE__
    for key in ['__APOLLO_STATE__', '__NUXT__', 'reportData', 'tableData', 'entries']:
        print(key, html.find(key))
