import re, cloudscraper
text = open(r"e:/wow_guides/wcl_report.html", encoding="utf-8", errors="replace").read()
scraper = cloudscraper.create_scraper()
for m in re.finditer(r'<script[^>]+src="([^"]+)"', text, re.I):
    src = m.group(1)
    if src.startswith('/'):
        src = 'https://www.warcraftlogs.com' + src
    if 'warcraftlogs' not in src:
        continue
    print('script', src[:120])
# inline search endpoints
for m in re.finditer(r'https://[^"\']+', text):
    u = m.group(0)
    if 'warcraftlogs' in u and ('api' in u or 'client' in u or 'table' in u):
        print('url', u)
# text snippets
for term in ['Last Pull', 'Mythic+ Season', 'damage done', 'player', 'actor']:
    i = text.lower().find(term.lower())
    if i>=0:
        print(term, 'context', text[max(0,i-80):i+120].replace('\n',' ')[:200])
# all data-* attributes with ids
for m in re.finditer(r'data-(?:fight|report|id)[^=]*="([^"]+)"', text, re.I):
    print('data attr', m.group(0)[:100])
