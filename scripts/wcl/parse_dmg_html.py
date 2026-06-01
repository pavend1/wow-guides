import re, json
from pathlib import Path
html = Path(r'e:/wow_guides/wcl_dmg_source3.html').read_text(encoding='utf-8', errors='replace')
rows=[]
for m in re.finditer(r'main-table-row-[^\"]+[\s\S]*?main-table-name report-table-name[\s\S]*?<a[^>]*>\s*([^<\n]+?)\s*</a>[\s\S]*?report-amount-percent">([\d.]+%)</div>[\s\S]*?report-amount-total">([\d.\w]+)</span>[\s\S]*?main-table-number[^>]*>\s*([\d,]+)[\s\S]*?main-per-second-amount[^>]*>\s*([\d,.]+)', html):
    rows.append({'name': m.group(1).strip(), 'pct': m.group(2), 'amount': m.group(3).strip(), 'casts': m.group(4).replace(',',''), 'dps': m.group(5)})
# simpler split by main-table-row
parts = html.split('main-table-row-')
parsed=[]
for part in parts[1:]:
    name_m=re.search(r'>\s*([^<\n]+?)\s*</a>\s*</td></tr></tbody></table>', part)
    pct_m=re.search(r'report-amount-percent">([\d.]+%)', part)
    amt_m=re.search(r'report-amount-total">([\d.\w]+)', part)
    dps_m=re.search(r'main-per-second-amount[^>]*>\s*([\d,.]+)', part)
    if name_m and pct_m and amt_m:
        parsed.append({'name': name_m.group(1).strip(), 'pct': pct_m.group(1), 'amount': amt_m.group(1).strip(), 'dps': dps_m.group(1) if dps_m else None})
Path(r'e:/wow_guides/wcl_dmg_all_abilities.json').write_text(json.dumps(parsed, ensure_ascii=False, indent=2), encoding='utf-8')
print('parsed', len(parsed))
