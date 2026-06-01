import json, re
from pathlib import Path
lines = Path(r'e:/wow_guides/wcl_player_damage_abilities.txt').read_text(encoding='utf-8').splitlines()
# lines with both % and m
hits = []
for i,l in enumerate(lines):
    if '%' in l and ('m' in l.lower() or 'k' in l.lower()):
        hits.append((i,l))
# devourer spell ids from menu in html
Path(r'e:/wow_guides/wcl_pct_lines.json').write_text(json.dumps({'count': len(hits), 'sample': hits[:80], 'tail': [(i,lines[i]) for i in range(max(0,len(lines)-120), len(lines))]}, ensure_ascii=True, indent=2), encoding='utf-8')
print(len(hits))
