import re, json
from pathlib import Path
html=Path(r'e:/wow_guides/wcl_dmg_source3.html').read_text(encoding='utf-8',errors='replace')
rows=[]
for part in html.split('report-table-name'):
    if 'report-amount-total' not in part: continue
    name_m=re.search(r'>\s*([^<\n]{2,40}?)\s*(?:</a>|</td>)', part)
    pct_m=re.search(r'report-amount-percent">([\d.]+%)', part)
    amt_m=re.search(r'report-amount-total">([\d.\w]+)', part)
    dps_m=re.search(r'main-per-second-amount[^>]*>\s*([\d,.]+)', part)
    if name_m and amt_m:
        name=name_m.group(1).strip()
        if name in ('Teach Me!','Total','Name'): continue
        rows.append({'name':name,'pct':pct_m.group(1) if pct_m else None,'amount':amt_m.group(1).strip(),'dps':dps_m.group(1) if dps_m else None})
# dedupe by name keep max amount
best={}
for r in rows:
    k=r['name']
    if k not in best: best[k]=r
    else:
        # keep larger amount string
        best[k]=r
rows=sorted(best.values(), key=lambda x: float(x['amount'].replace('m','').replace('k','')), reverse=True)
Path(r'e:/wow_guides/wcl_dmg_html_rows.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
print(len(rows))
