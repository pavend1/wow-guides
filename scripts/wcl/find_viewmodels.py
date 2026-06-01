import re
from pathlib import Path
html = Path(r'e:/wow_guides/wcl_full_page.html').read_text(encoding='utf-8', errors='replace')
for pat in [r'window\._pageViewModels\s*=\s*', r'_pageViewModels', r'pageViewModels', r'viewModel']:
    print(pat, len(re.findall(pat, html)))
idx = html.find('_pageViewModels')
print('idx', idx)
if idx>=0:
    print(html[idx:idx+500])
# search for highcharts series data
for pat in [r'series:\s*\[', r'"series":\s*\[', r'data:\s*\[\[' ]:
    print(pat, html.count(pat))
