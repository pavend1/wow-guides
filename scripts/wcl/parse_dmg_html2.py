import re, json
from pathlib import Path
html=Path(r'e:/wow_guides/wcl_dmg_source3.html').read_text(encoding='utf-8',errors='replace')
# find all report-amount-total near ability names
names=[]
for m in re.finditer(r'>(Consume|Devour|Reap|Cull|Void Ray|Collapsing Star|Catastrophe|Eradicate|Voidfall Meteor|Melee|Soul Immolation)</a>[\s\S]{0,800}?report-amount-total">([\d.\w]+)</span>', html):
    names.append({'name': m.group(1), 'amount': m.group(2)})
# all amount totals count
amounts=re.findall(r'report-amount-total">([\d.\w]+)</span>', html)
print('matches', len(names), 'amounts', len(amounts))
Path(r'e:/wow_guides/wcl_dmg_html_names.json').write_text(json.dumps({'matches':names,'amount_count':len(amounts)},ensure_ascii=False,indent=2),encoding='utf-8')
