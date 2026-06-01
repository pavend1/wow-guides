import re
from pathlib import Path
html = Path(r'e:/wow_guides/wcl_player_damage_abilities.html').read_text(encoding='utf-8', errors='replace')
for m in re.finditer(r'window\.(\w+)\s*=\s*', html):
    print('window', m.group(1))
# table rows with numeric damage in report table
rows = re.findall(r'<tr[^>]*>.*?report-table.*?</tr>', html, re.S|re.I)
print('report-table tr', len(rows))
# simpler: parse tbody rows from main damage table
for cls in ['report-table', 'ability-table', 'tablesorter', 'data-table']:
    print(cls, html.count(cls))
# find all td with school-106 (devourer?)
links = re.findall(r'ability=(\d+)[^>]*>([^<]+)</a></td><td[^>]*>([\d.,]+[km]?)', html, re.I)
print('ability links with amounts', len(links))
if links:
    for x in links[:30]:
        print(x)
# pattern from wcl tables
pat = re.compile(r'class="[^"]*ability[^"]*"[^>]*>\s*<a[^>]*>([^<]+)</a>.*?<td[^>]*>\s*([\d.,]+%?).*?<td[^>]*>\s*([\d.,]+[km]?)', re.S|re.I)
ms = pat.findall(html)
print('pat matches', len(ms))
for x in ms[:25]:
    print(x)
