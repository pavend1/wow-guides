import re, json
from pathlib import Path
html = Path(r'e:/wow_guides/wcl_full_page.html').read_text(encoding='utf-8', errors='replace')
start = html.find('window._pageViewModels = ')
if start < 0:
    raise SystemExit('not found')
i = start + len('window._pageViewModels = ')
# parse until semicolon at top level array end - starts with [
depth = 0
in_str = False
esc = False
quote = ''
end = i
for j in range(i, min(i+8000000, len(html))):
    ch = html[j]
    if in_str:
        if esc:
            esc = False
        elif ch == '\\':
            esc = True
        elif ch == quote:
            in_str = False
        continue
    if ch in ('"', "'"):
        in_str = True
        quote = ch
        continue
    if ch in '[{':
        depth += 1
    elif ch in ']}':
        depth -= 1
        if depth == 0:
            end = j+1
            break
raw = html[i:end]
Path(r'e:/wow_guides/wcl_page_view_models.json').write_text(raw, encoding='utf-8')
print('raw len', len(raw))
# it's JSON-like array
try:
    data = json.loads(raw)
    print('parsed type', type(data), 'len', len(data))
except Exception as e:
    print('json parse failed', e)
    # fix trailing issues - try demjson3?
# search raw text for player and abilities
player = '\u0410\u043d\u043f\u0430\u0432\u0430\u043b'
print('player in raw', raw.count(player))
for ab in ['Consume','Reap','Void Ray','Void Metamorphosis','Devour','Cull','Eradicate']:
    print(ab, raw.count(ab))
