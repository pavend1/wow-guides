import re, json
from pathlib import Path
text = Path(r'e:/wow_guides/wcl_casts_only.txt').read_text(encoding='utf-8')
# pattern ability line then stats line
abilities=[]
for m in re.finditer(r'\n\t([^\n\t]+)\n\t\n([\d.]+%)\n([\d\t\-%.]+)\n', text):
    name=m.group(1).strip()
    pct=m.group(2)
    rest=m.group(3)
    parts=[p for p in rest.split('\t') if p]
    abilities.append({'name':name,'cast_pct':pct,'parts':parts})
# fallback: combined lines seen earlier
for m in re.finditer(r'\t([A-Za-z][^\n\t]+)\n\t\n([\d.]+%)\n([\d]+\t[^\n]+)', text):
    pass
Path(r'e:/wow_guides/wcl_cast_counts_full.json').write_text(json.dumps(abilities, ensure_ascii=False, indent=2), encoding='utf-8')
print(len(abilities))
for a in abilities:
    print(a)
