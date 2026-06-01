import re, json
from pathlib import Path

def read(p):
    return Path(p).read_text(encoding='utf-8', errors='replace')

PLAYER = '\u0410\u043d\u043f\u0430\u0432\u0430\u043b'
dmg = read(r'e:/wow_guides/wcl_full_page.txt')
casts = read(r'e:/wow_guides/wcl_player_casts.txt')

# Extract fight duration - patterns like 3:45 or 225s
dur = None
for pat in [r'Duration\s*(\d+:\d+)', r'(\d+:\d+)\s*Duration', r'Fight Time\s*(\d+:\d+)']:
    m = re.search(pat, dmg, re.I)
    if m: dur = m.group(1); break

# find segment around player in damage table - look for lines with DPS numbers
lines = dmg.splitlines()
idxs = [i for i,l in enumerate(lines) if PLAYER in l]
print('player line idxs', idxs[:10])
for i in idxs[:3]:
    print('context', lines[max(0,i-3):i+4])

# Regex on html for player row numbers
html = read(r'e:/wow_guides/wcl_full_page.html')
# WCL often encodes table in JSON in script tags
for pat in [r'\\"name\\":\\"' + PLAYER + r'\\"[^}]{0,400}', r'"name":"' + PLAYER + r'"[^}]{0,400}']:
    ms = re.findall(pat, html)
    print('json snippets', len(ms))
    if ms:
        print(ms[0][:400])

# Search abilities in casts page
abilities = {}
for ln in casts.splitlines():
    ln=ln.strip()
    if not ln: continue
    # ability lines often: name count or name damage
    if any(k in ln for k in ['Consume', 'Reap', 'Void', 'Metamorphosis', 'Ray', 'Devour', 'Cull', 'Eradicate', 'Soul', 'Поглощ', 'Жатва', 'Пустот', 'Метаморф', 'Луч']):
        print('cast line:', ln)

# dump portion of casts around player filter
print('--- casts head ---')
print('\n'.join(casts.splitlines()[:80]))
print('--- casts sample mid ---')
print('\n'.join(casts.splitlines()[80:200]))
