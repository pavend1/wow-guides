import json, re
from pathlib import Path
text = Path(r'e:/wow_guides/wcl_player_damage_abilities.txt').read_text(encoding='utf-8')
lines = text.splitlines()
headers = []
for i,l in enumerate(lines):
    if l.strip() in ('Parse %','Ability','Name','DPS','Total') and i+5 < len(lines):
        headers.append({'i': i, 'window': lines[i:i+8]})
abilities = []
for i,l in enumerate(lines):
    s=l.strip()
    if s in ('Consume','Reap','Void Ray','Void Metamorphosis','Devour','Cull','Eradicate','Melee','Auto Swings','Soul Immolation'):
        abilities.append({'i': i, 'ctx': lines[max(0,i-3):i+8]})
fight = [l for l in lines if 'Pit of Saron' in l or 'Last Run' in l][:5]
# parse damage table like full page - look for pattern rank name pct amount
rows = []
for i in range(len(lines)-5):
    if re.match(r'^\d+$', lines[i].strip()) and '%' in lines[i+2] and 'm' in lines[i+3]:
        rows.append(lines[i:i+6])
out = {'lines': len(lines), 'headers': headers[:10], 'abilities': abilities, 'fight': fight, 'rows': rows[:20]}
Path(r'e:/wow_guides/wcl_player_parse.json').write_text(json.dumps(out, ensure_ascii=True, indent=2), encoding='utf-8')
