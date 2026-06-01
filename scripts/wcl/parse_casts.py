import re, json
from pathlib import Path
text = Path(r'e:/wow_guides/wcl_casts_only.txt').read_text(encoding='utf-8')
html = Path(r'e:/wow_guides/wcl_casts_only.html').read_text(encoding='utf-8', errors='replace')
print('lines', len(text.splitlines()), 'html', len(html))
# find ability rows in html table like main-table
rows = re.findall(r'main-table-name report-table-name.*?>([^<]+)</a>.*?main-table-number[^>]*>\s*([\d,]+)\s*', html, re.S)
# better: parse text lines around abilities
abilities=['Consume','Reap','Void Ray','Void Metamorphosis','Devour','Cull','Eradicate','Melee','Soul','Immolation','Vortex','Hunger','Sigil','Eye','Hunt','Fel','Blade','Chaos']
lines=text.splitlines()
parsed=[]
for i,l in enumerate(lines):
    s=l.strip()
    if s in abilities or any(s.startswith(x) for x in ['Void Ray','Eradicate','Soul ']):
        ctx=lines[max(0,i-2):i+6]
        parsed.append({'name': s, 'ctx': ctx})
# regex on html for cast counts in table rows
html_rows=[]
for m in re.finditer(r'id="main-table-row-[^"]+"[^>]*>.*?report-table-name.*?>\s*([^<\n]+).*?main-table-number[^>]*>\s*([\d,]+)', html, re.S):
    name=m.group(1).strip()
    cnt=m.group(2).replace(',','')
    if any(k.lower() in name.lower() for k in ['consume','reap','void','devour','cull','erad','melee','soul','vortex','immolation','hunger','sigil','eye','hunt','fel','blade','chaos']):
        html_rows.append({'name': name, 'casts': int(cnt)})
# all html rows first 40
all_rows=[]
for m in re.finditer(r'class="main-table-name report-table-name"[\s\S]*?<a[^>]*>\s*([^<\n]+?)\s*</a>[\s\S]*?class="main-table-number[^"]*"[^>]*>\s*([\d,]+)', html):
    all_rows.append({'name': m.group(1).strip(), 'casts': int(m.group(2).replace(',',''))})
out={'parsed_ctx': parsed[:50], 'html_rows': html_rows, 'all_rows': all_rows[:60], 'fight': [l for l in lines if 'Pit of Saron' in l or 'Last Run' in l][:3], 'title_snip': text[text.find('Casts'):text.find('Casts')+200] if 'Casts' in text else text[:300]}
Path(r'e:/wow_guides/wcl_casts_parsed.json').write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding='utf-8')
print('html_rows', len(html_rows), 'all_rows', len(all_rows))
