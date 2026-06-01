import re
from pathlib import Path
html = Path(r'e:/wow_guides/wcl_full_page.html').read_text(encoding='utf-8', errors='replace')
for term in ['Consume','Reap','Void Ray','Void Metamorphosis','Metamorphosis','Devour','Cull','Eradicate','Soul Immolation','Chaos Strike','Blade Dance','Fel Rush']:
    c = html.count(term)
    if c: print(term, c)
# find unicode escaped consume?
for m in re.finditer(r'.{0,30}Reap.{0,80}', html):
    if m.start() < 500000:
        s = m.group(0)
        if 'Reap' in s and ('damage' in s.lower() or 'total' in s.lower() or 'casts' in s.lower()):
            print('ctx', s[:120])
            break
# look for \u0410 (player) near abilities
player_idx = html.find('\u0410\u043d\u043f\u0430\u0432\u0430\u043b')
print('player idx', player_idx)
if player_idx > 0:
    chunk = html[player_idx:player_idx+5000]
    Path(r'e:/wow_guides/wcl_player_html_chunk.html').write_text(chunk, encoding='utf-8')
# search for "entries" json near damage table
for pat in [r'"entries"\s*:\s*\[', r'"total"\s*:\s*\d+', r'"abilities"\s*:\s*\[']:
    print(pat, len(re.findall(pat, html)))
