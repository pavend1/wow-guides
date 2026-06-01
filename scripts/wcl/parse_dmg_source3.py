import re, json
from pathlib import Path
text = Path(r'e:/wow_guides/wcl_dmg_source3.txt').read_text(encoding='utf-8')
html = Path(r'e:/wow_guides/wcl_dmg_source3.html').read_text(encoding='utf-8', errors='replace')
print('err', 'Unable to fetch' in text, 'lines', len(text.splitlines()))
abilities=[]
for m in re.finditer(r'\n\t([^\n\t]+)\n\t\n([\d.]+%)\n([\d.]+\w?\t[^\n]+)', text):
    name=m.group(1).strip(); pct=m.group(2); rest=m.group(3)
    parts=[p for p in rest.split('\t') if p]
    abilities.append({'name':name,'pct':pct,'parts':parts})
# html table damage rows
dmg_rows=[]
for m in re.finditer(r'class="main-table-name report-table-name"[\s\S]*?<a[^>]*>\s*([^<\n]+?)\s*</a>[\s\S]*?report-amount-percent">([\d.]+%)</div>[\s\S]*?report-amount-total">([\d.]+\w*)</span>', html):
    dmg_rows.append({'name': m.group(1).strip(), 'pct': m.group(2), 'amount': m.group(3).strip()})
Path(r'e:/wow_guides/wcl_dmg_source3_parsed.json').write_text(json.dumps({'abilities': abilities, 'dmg_rows': dmg_rows[:40], 'err': 'Unable to fetch' in text}, ensure_ascii=False, indent=2), encoding='utf-8')
print('text abilities', len(abilities), 'dmg_rows', len(dmg_rows))
