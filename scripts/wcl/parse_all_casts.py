import re, json
from pathlib import Path
text = Path(r'e:/wow_guides/wcl_casts_only.txt').read_text(encoding='utf-8')
lines = text.splitlines()
# parse blocks: line with tab Ability, next lines with pct and numbers
abilities = []
i=0
while i < len(lines):
    l=lines[i]
    if l.startswith('\t') and not l.startswith('\t\t'):
        name=l.strip()
        if i+2 < len(lines) and '%' in lines[i+2]:
            chunk=lines[i+2].strip()
            parts=[p for p in re.split(r'\t+', chunk) if p]
            abilities.append({'name': name, 'line': chunk, 'parts': parts})
            i+=3
            continue
    i+=1
# also grep Eradicate Meta
extra=[]
for i,l in enumerate(lines):
    if any(x in l for x in ['Eradicate','Metamorphosis','Collapsing','Void-Touched','Immolation','Hunger','Vortex','Disrupt','Blur']):
        if '\t' in l and '%' in l:
            extra.append((i,l))
Path(r'e:/wow_guides/wcl_cast_counts.json').write_text(json.dumps({'abilities': abilities, 'extra': extra[:40]}, ensure_ascii=False, indent=2), encoding='utf-8')
print(len(abilities))
