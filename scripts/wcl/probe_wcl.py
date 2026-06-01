import re, cloudscraper, json
text = open(r"e:/wow_guides/wcl_report.html", encoding="utf-8", errors="replace").read()
scraper = cloudscraper.create_scraper()
# script srcs
srcs = []
for m in re.finditer(r'<script[^>]+src="([^"]+)"', text, re.I):
    src = m.group(1)
    if src.startswith('//'): src = 'https:' + src
    elif src.startswith('/'): src = 'https://www.warcraftlogs.com' + src
    srcs.append(src)
print('scripts', len(srcs))
for src in srcs:
    if any(x in src for x in ['app', 'report', 'chunk', 'main', 'vendor']):
        print(src)
# probe json endpoints
code='R47AwfNhdXpgD38c'
probes=[
 f'https://www.warcraftlogs.com/reports/{code}.json',
 f'https://www.warcraftlogs.com/reports/{code}?format=json',
 f'https://www.warcraftlogs.com/reports/{code}?json=1',
 f'https://www.warcraftlogs.com/reports/{code}/summary',
 f'https://www.warcraftlogs.com/reports/{code}/1/summary',
]
for u in probes:
    try:
        r=scraper.get(u, timeout=30)
        print(u, r.status_code, r.headers.get('content-type',''), len(r.text), r.text[:120].replace('\n',' '))
    except Exception as e:
        print(u, 'ERR', e)
# search inline for fight id numbers
nums = re.findall(r'fight[=:](\d+)', text, re.I)
print('fight nums in html', sorted(set(nums))[:20])
