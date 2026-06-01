import re, json
from pathlib import Path
html = Path(r'e:/wow_guides/wcl_player_damage_abilities.html').read_text(encoding='utf-8', errors='replace')
m = re.search(r'window\._pageViewModels\s*=\s*(\{.*?\});\s*\n', html, re.S)
if not m:
    m = re.search(r'window\._pageViewModels\s*=\s*(\{.*?\});', html, re.S)
print('match', bool(m), 'len', len(m.group(1)) if m else 0)
if m:
    raw = m.group(1)
    Path(r'e:/wow_guides/wcl_page_view_models_raw.js').write_text(raw[:2000000], encoding='utf-8')
    # try json after replacing js quirks - might not be valid json
    try:
        data = json.loads(raw)
        print('json ok keys', list(data.keys())[:20])
    except Exception as e:
        print('json fail', e)
        # extract damage table model key
        for key in ['damageTable','tableModel','reportTable','DamageDone','entries','rows']:
            print(key, raw.find(key))
