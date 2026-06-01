import re, json
from pathlib import Path
text=Path(r'e:/wow_guides/wcl_dmg_source3.txt').read_text(encoding='utf-8')
start=text.find('Name\n\t\nAmount')
end=text.find('Total\t\n100%')
chunk=text[start:end]
lines=[l for l in chunk.splitlines() if l.strip()]
Path(r'e:/wow_guides/wcl_dmg_table_chunk.txt').write_text('\n'.join(lines), encoding='utf-8')
# parse alternating
rows=[]
i=0
while i < len(lines):
    l=lines[i]
    if l.startswith('\t') and l.count('\t')==1:
        name=l.strip()
        if i+2 < len(lines) and re.match(r'^[\d.]+%$', lines[i+2].strip()):
            pct=lines[i+2].strip(); data=lines[i+3].strip() if i+3 < len(lines) else ''
            rows.append({'name':name,'pct':pct,'data':data})
            i+=4; continue
    i+=1
Path(r'e:/wow_guides/wcl_dmg_rows.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
print(len(rows))
