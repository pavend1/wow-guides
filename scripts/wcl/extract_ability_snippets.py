import re, json
from pathlib import Path
html = Path(r'e:/wow_guides/wcl_full_page.html').read_text(encoding='utf-8', errors='replace')
abilities = ['Consume','Reap','Void Ray','Void Metamorphosis','Devour','Cull','Eradicate','Soul Immolation','Chaos Strike','Blade Dance','Fel Rush','Sigil of Flame','Eye Beam','The Hunt','Immolation Aura']
found = {}
for ab in abilities:
    positions = [m.start() for m in re.finditer(re.escape(ab), html)]
    snippets = []
    for pos in positions[:8]:
        sn = html[max(0,pos-200):pos+200]
        snippets.append(sn)
    found[ab] = {"count": len(positions), "snippets": snippets[:3]}
Path(r'e:/wow_guides/wcl_ability_snippets.json').write_text(json.dumps(found, ensure_ascii=False, indent=2)[:200000], encoding='utf-8')
# also parse visible text from full page for ability table when filtered to player
text = Path(r'e:/wow_guides/wcl_full_page.txt').read_text(encoding='utf-8')
# After clicking player - search ability names in text
for ab in abilities:
    if ab in text:
        print('in text', ab, text.count(ab))
# extract lines containing abilities
abl_lines = [l for l in text.splitlines() if any(ab in l for ab in abilities)]
Path(r'e:/wow_guides/wcl_ability_lines.txt').write_text('\n'.join(abl_lines[:200]), encoding='utf-8')
print('ability lines', len(abl_lines))
