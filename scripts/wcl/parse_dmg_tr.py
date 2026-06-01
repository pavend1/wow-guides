import re, json
from pathlib import Path
html=Path(r'e:/wow_guides/wcl_dmg_source3.html').read_text(encoding='utf-8',errors='replace')
rows=[]
for m in re.finditer(r'<tr[^>]*id="main-table-row-[^"]+"[\s\S]*?</tr>', html):
    tr=m.group(0)
    if 'report-amount-total' not in tr: continue
    # ability link text
    links=re.findall(r'class="[^"]*main-table-link[^"]*"[\s\S]*?<a[^>]*>\s*([^<\n]+?)\s*</a>', tr)
    name=links[0].strip() if links else None
    if not name or name in ('Teach Me!',''): 
        links2=re.findall(r'ability-menu-name[\s\S]*?<a[^>]*>\s*([^<\n]+?)\s*</a>', tr)
        name=links2[0].strip() if links2 else None
    pct_m=re.search(r'report-amount-percent">([\d.]+%)', tr)
    amt_m=re.search(r'report-amount-total">([\d.\w]+)', tr)
    casts_m=re.search(r'main-table-number[^>]*>\s*([\d,]+)\s*<', tr)
    dps_m=re.search(r'main-per-second-amount[^>]*>\s*([\d,.]+)', tr)
    if name and amt_m:
        rows.append({'name':name,'pct':pct_m.group(1) if pct_m else None,'amount':amt_m.group(1),'casts':casts_m.group(1) if casts_m else None,'dps':dps_m.group(1) if dps_m else None})
Path(r'e:/wow_guides/wcl_dmg_tr_rows.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
print(len(rows))
