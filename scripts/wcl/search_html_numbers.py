import re, json
from pathlib import Path
html = Path(r'e:/wow_guides/wcl_full_page.html').read_text(encoding='utf-8', errors='replace')
for term in ['90.21m','37586','37,586','473662','1225823','1214595']:
    print(term, html.find(term))
# find JSON fragments containing 37586
for m in re.finditer(r'.{0,40}37586.{0,80}', html):
    print(m.group(0)[:120])
    break
# search for tableData or entries in script tags larger than 10k
scripts = re.findall(r'<script[^>]*>(.*?)</script>', html, re.S|re.I)
big = [s for s in scripts if len(s)>50000]
print('big scripts', len(big), [len(s) for s in big[:5]])
for bi,s in enumerate(big[:3]):
    for ab in ['Consume','Reap','Void Ray','Devour','Cull']:
        if ab in s:
            print('script', bi, 'has', ab, 'count', s.count(ab))
    # write if has consume and 37586
    if 'Consume' in s and ('37586' in s or '9021' in s):
        Path(rf'e:/wow_guides/wcl_script_{bi}.js').write_text(s[:3000000], encoding='utf-8')
