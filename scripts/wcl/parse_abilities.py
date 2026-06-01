from pathlib import Path
import re
text = Path(r'e:/wow_guides/wcl_player_damage_abilities.txt').read_text(encoding='utf-8')
lines = text.splitlines()
# find ability table header
start = None
for i,l in enumerate(lines):
    if 'Ability' in l and 'Amount' in lines[i:i+5]:
        start = i
        break
if start is None:
    for i,l in enumerate(lines):
        if l.strip() in ('Ability', 'Name') and i+1 < len(lines) and 'Amount' in lines[i+1]:
            start = i
            break
# simpler: find Parse % header block for abilities
for i,l in enumerate(lines):
    if l.strip() == 'Ability' or l.strip() == 'Name':
        if any('Amount' in x for x in lines[i:i+8]):
            start = i
            print('header at', i, lines[i:i+10])
            break
# extract rows after "Done By Ability" 
for i,l in enumerate(lines):
    if 'Done By Ability' in l:
        print('done by ability at', i)
        chunk = lines[i:i+120]
        Path(r'e:/wow_guides/wcl_ability_chunk.txt').write_text('\n'.join(f'{j}: {x}' for j,x in enumerate(chunk)), encoding='utf-8')
        break
# also search for percentage damage rows like "12.34%"
abilities = []
for i in range(len(lines)-2):
    if re.match(r'^\d+\.?\d*%$', lines[i].strip()) and re.match(r'^\d+\.?\d*m?$', lines[i+1].strip().replace(',','')):
        abilities.append((lines[i-1].strip(), lines[i].strip(), lines[i+1].strip()))
Path(r'e:/wow_guides/wcl_ability_guess.json').write_text(str(abilities[:30]), encoding='utf-8')
# dump lines 200-400
Path(r'e:/wow_guides/wcl_player_mid.txt').write_text('\n'.join(lines[180:450]), encoding='utf-8')
print('wrote chunks')
