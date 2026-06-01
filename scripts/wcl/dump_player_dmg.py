from pathlib import Path
text = Path(r'e:/wow_guides/wcl_player_damage_abilities.txt').read_text(encoding='utf-8', errors='replace')
lines = [l.strip() for l in text.splitlines() if l.strip()]
for i,l in enumerate(lines):
    print(f'{i}: {l[:140]}')
