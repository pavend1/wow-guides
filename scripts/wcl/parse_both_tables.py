import re, json
from pathlib import Path

def parse_table(path):
    text=Path(path).read_text(encoding='utf-8')
    out=[]
    i=0
    lines=text.splitlines()
    while i < len(lines)-3:
        if lines[i].startswith('\t') and lines[i].count('\t')==1:
            name=lines[i].strip()
            if i+2 < len(lines) and re.match(r'^[\d.]+%$', lines[i+2].strip()) and i+3 < len(lines):
                pct=lines[i+2].strip(); data=lines[i+3].strip()
                parts=[p for p in data.split('\t') if p]
                if parts and re.match(r'^[\d.]+m?$|^[\d.]+k$', parts[0].replace(',','')):
                    out.append({'name':name,'pct':pct,'parts':parts})
                    i+=4; continue
        i+=1
    return out

casts=parse_table(r'e:/wow_guides/wcl_casts_only.txt')
dmg=parse_table(r'e:/wow_guides/wcl_dmg_source3.txt')
# merge
Path(r'e:/wow_guides/wcl_anpaval_tables.json').write_text(json.dumps({'casts':casts,'damage':dmg},ensure_ascii=False,indent=2),encoding='utf-8')
print('casts',len(casts),'dmg',len(dmg))
