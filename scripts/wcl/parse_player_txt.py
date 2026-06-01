from pathlib import Path
text = Path(r'e:/wow_guides/wcl_player_damage_abilities.txt').read_text(encoding='utf-8')
lines = text.splitlines()
# find Parse % / Ability headers
for i,l in enumerate(lines):
    if l.strip() in ('Parse %','Ability','Name') and i+3 < len(lines):
        if any(x.strip()=='Amount' for x in lines[i:i+6]):
            print('header idx', i, lines[i:i+8])
# find Consume etc
for i,l in enumerate(lines):
    if l.strip() in ('Consume','Reap','Void Ray','Void Metamorphosis','Devour','Cull','Eradicate','Melee'):
        print('ability idx', i, lines[max(0,i-2):i+6])
# find Pit of Saron
for i,l in enumerate(lines):
    if 'Pit of Saron' in l or 'Last Run' in l:
        print('fight', i, l)
Path(r'e:/wow_guides/wcl_player_lines_slice.txt').write_text('\n'.join(f'{i}: {lines[i]}' for i in range(2200, min(2418,len(lines)))), encoding='utf-8')
print('total lines', len(lines))
