from pathlib import Path
import json
text=Path(r'e:/wow_guides/wcl_dmg_source3.txt').read_text(encoding='utf-8')
res={}
for name in ['Void Ray','Collapsing Star','Soul Immolation','Eradicate','Void Metamorphosis','Devour','Consume','Reap','Cull','Catastrophe','Total']:
    idx=text.find(name)
    res[name]={'idx':idx,'ctx':text[idx:idx+300] if idx>=0 else None}
Path(r'e:/wow_guides/search_dmg.json').write_text(json.dumps(res,ensure_ascii=False,indent=2),encoding='utf-8')
