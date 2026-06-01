from pathlib import Path
text = Path(r'e:/wow_guides/wcl_player_damage_abilities.txt').read_text(encoding='utf-8', errors='replace')
lines = [l.strip() for l in text.splitlines() if l.strip()]
Path(r'e:/wow_guides/wcl_player_dmg_dump.txt').write_text('\n'.join(f'{i}: {l}' for i,l in enumerate(lines)), encoding='utf-8')
print('lines', len(lines))
# ability keywords
keys = ['Consume','Reap','Void','Metamorphosis','Ray','Devour','Cull','Eradicate','Soul','Immolation','Chaos','Blade','Fel','Погло','Жатва','Пуст','Мета','Луч','Пожир']
for i,l in enumerate(lines):
    if any(k.lower() in l.lower() for k in keys):
        pass
hits = [l for l in lines if any(k.lower() in l.lower() for k in keys)]
Path(r'e:/wow_guides/wcl_ability_hits.txt').write_text('\n'.join(hits), encoding='utf-8')
print('ability hits', len(hits))
